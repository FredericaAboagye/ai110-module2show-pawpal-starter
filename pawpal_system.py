from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, date, time, timedelta
import json
import os


@dataclass
class Task:
    task_id: str
    title: str
    description: Optional[str] = ""
    duration_minutes: int = 0
    priority: int = 0  # higher number = higher priority
    recurrence: Optional[str] = None  # e.g. "daily", "weekly"
    due_time: Optional[datetime] = None
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task complete."""
        self.completed = True
        # If this task is recurring, return a new Task instance for the next occurrence.
        if self.recurrence in ("daily", "weekly"):
            delta = timedelta(days=1) if self.recurrence == "daily" else timedelta(weeks=1)
            new_due = None
            if self.due_time:
                new_due = self.due_time + delta
            # Create a shallow copy with a new id (caller should add it to the pet)
            new_task = Task(
                task_id=f"{self.task_id}_next",
                title=self.title,
                description=self.description,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                recurrence=self.recurrence,
                due_time=new_due,
                completed=False,
            )
            return new_task
        return None

    def reschedule(self, new_time: datetime) -> None:
        """Reschedule the task to a new datetime by updating `due_time`."""
        self.due_time = new_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "recurrence": self.recurrence,
            "due_time": self.due_time.isoformat() if self.due_time else None,
            "completed": self.completed,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Task":
        due = None
        if d.get("due_time"):
            due = datetime.fromisoformat(d["due_time"])
        return Task(
            task_id=d["task_id"],
            title=d.get("title", ""),
            description=d.get("description", ""),
            duration_minutes=d.get("duration_minutes", 0),
            priority=d.get("priority", 0),
            recurrence=d.get("recurrence"),
            due_time=due,
            completed=d.get("completed", False),
        )


@dataclass
class Pet:
    pet_id: str
    name: str
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)
    medical_info: Optional[dict] = field(default_factory=dict)

    def add_task(self, task: Task) -> None:
        """Add a `Task` to this pet's task list."""
        self.tasks.append(task)

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """Mark a task complete by id; if it is recurring, return the generated next Task so caller can add it.

        Returns:
            Optional[Task]: the newly created recurring task, or None.
        """
        for t in self.tasks:
            if t.task_id == task_id:
                new_task = t.mark_complete()
                return new_task
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pet_id": self.pet_id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "medical_info": self.medical_info,
            "tasks": [t.to_dict() for t in self.tasks],
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Pet":
        p = Pet(
            pet_id=d.get("pet_id", ""),
            name=d.get("name", ""),
            species=d.get("species"),
            breed=d.get("breed"),
            age=d.get("age"),
            medical_info=d.get("medical_info", {}),
        )
        for td in d.get("tasks", []):
            p.tasks.append(Task.from_dict(td))
        return p

    def remove_task(self, task_id: str) -> None:
        """Remove a Task by `task_id`. No-op if not found."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def upcoming_tasks(self, until: Optional[datetime] = None) -> List[Task]:
        """Return tasks that are not completed and optionally due by `until`."""
        candidates = [t for t in self.tasks if not t.completed]
        if until is None:
            return candidates
        return [t for t in candidates if t.due_time is None or t.due_time <= until]


class Owner:
    def __init__(self, owner_id: str, name: str, contact_info: Optional[dict] = None, preferences: Optional[dict] = None):
        self.owner_id = owner_id
        self.name = name
        self.contact_info = contact_info or {}
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a `Pet` to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet by id. No-op if not found."""
        self.pets = [p for p in self.pets if p.pet_id != pet_id]

    def get_all_tasks(self) -> List[Tuple[Pet, Task]]:
        """Return a list of (pet, task) tuples for all tasks across pets."""
        out: List[Tuple[Pet, Task]] = []
        for pet in self.pets:
            for t in pet.tasks:
                out.append((pet, t))
        return out

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Tuple[Pet, Task]]:
        """Filter tasks by completion status and/or pet name.

        Args:
            completed: if set, filters tasks by their completed value.
            pet_name: if set, only returns tasks for the matching pet name.
        """
        out: List[Tuple[Pet, Task]] = []
        for pet, task in self.get_all_tasks():
            if completed is not None and task.completed != completed:
                continue
            if pet_name is not None and pet.name != pet_name:
                continue
            out.append((pet, task))
        return out

    def to_dict(self) -> Dict[str, Any]:
        return {
            "owner_id": self.owner_id,
            "name": self.name,
            "contact_info": self.contact_info,
            "preferences": self.preferences,
            "pets": [p.to_dict() for p in self.pets],
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Owner":
        o = Owner(owner_id=d.get("owner_id", ""), name=d.get("name", ""), contact_info=d.get("contact_info", {}), preferences=d.get("preferences", {}))
        for pd in d.get("pets", []):
            o.pets.append(Pet.from_dict(pd))
        return o

    def save_to_json(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @staticmethod
    def load_from_json(filepath: str) -> Optional["Owner"]:
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Owner.from_dict(data)

    def get_pets(self) -> List[Pet]:
        return self.pets


class Scheduler:
    """Generates plans/schedules for an Owner's pets based on tasks and constraints."""

    def __init__(self):
        # future: configuration, scoring weights, etc.
        # Scheduler is stateless for now; configuration can be added later.
        self.default_start_time = time(hour=9, minute=0)

    def generate_daily_plan(self, owner: Owner, day: date, available_minutes: int = 480) -> List[dict]:
        """Return a list of scheduled items (dicts with start/end/task).

        This is a skeleton stub; scheduling logic will be implemented in later phases.
        """
        # Collect all incomplete tasks
        items: List[Tuple[Pet, Task]] = [pt for pt in owner.get_all_tasks() if not pt[1].completed]

        # Simple scoring: higher priority first, then earlier due_time
        def sort_key(pt: Tuple[Pet, Task]):
            pet, task = pt
            due_ts = task.due_time.timestamp() if task.due_time else float('inf')
            return (-task.priority, due_ts)

        items.sort(key=sort_key)

        # Schedule sequentially starting at default_start_time
        current_dt = datetime.combine(day, self.default_start_time)
        remaining = available_minutes
        schedule: List[dict] = []

        for pet, task in items:
            if task.duration_minutes <= 0:
                # treat zero-duration tasks as instantaneous; schedule if there's any time left
                start = current_dt
                end = current_dt
            else:
                if task.duration_minutes > remaining:
                    # skip tasks that can't fit; could be improved later
                    continue
                start = current_dt
                end = start + timedelta(minutes=task.duration_minutes)
                current_dt = end
                remaining -= task.duration_minutes

            schedule.append({
                "start": start,
                "end": end,
                "pet_id": pet.pet_id,
                "pet_name": pet.name,
                "task": task,
            })

        return schedule

    def sort_by_time(self, plan: List[dict]) -> List[dict]:
        """Return a copy of `plan` sorted by the `start` datetime."""
        return sorted(plan, key=lambda i: i["start"])

    def detect_conflicts(self, plan: List[dict]) -> List[str]:
        """Detect overlapping scheduled items and return warning messages.

        This performs a lightweight check: if two items overlap in time, a warning string is generated.
        """
        warnings: List[str] = []
        # sort by start time to simplify overlap checking
        ordered = self.sort_by_time(plan)
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                a = ordered[i]
                b = ordered[j]
                # overlap if a.start < b.end and b.start < a.end
                if a["start"] < b["end"] and b["start"] < a["end"]:
                    warnings.append(
                        f"Conflict: '{a['task'].title}' (pet {a['pet_name']}) overlaps with '{b['task'].title}' (pet {b['pet_name']})"
                    )
        return warnings

    def detect_due_time_conflicts(self, owner: Owner) -> List[str]:
        """Detect tasks across an owner that have identical explicit `due_time` values.

        This is a lightweight check to warn when two tasks are expected at the exact same time.
        """
        seen = {}
        warnings: List[str] = []
        for pet, task in owner.get_all_tasks():
            if task.due_time is None:
                continue
            key = task.due_time
            if key in seen:
                other_pet, other_task = seen[key]
                warnings.append(
                    f"Due-time conflict: '{task.title}' (pet {pet.name}) has same due_time as '{other_task.title}' (pet {other_pet.name})"
                )
            else:
                seen[key] = (pet, task)
        return warnings

    def explain_plan(self, plan: List[dict]) -> str:
        """Produce a human-readable explanation of why tasks were scheduled."""
        lines: List[str] = []
        for item in plan:
            task: Task = item["task"]
            lines.append(f"Scheduled '{task.title}' for {item['pet_name']} (priority={task.priority})")
        return "\n".join(lines)

    def score_task(self, task: Task, constraints: dict) -> float:
        """Return a numerical score for task priority under given constraints."""
        score = float(task.priority)
        # penalize long tasks if max_duration constraint exists
        max_dur = constraints.get("max_task_duration") if constraints else None
        if max_dur and task.duration_minutes > max_dur:
            score -= 1.0
        return score


@dataclass
class ScheduledTask:
    start: datetime
    end: datetime
    task: Task
    pet_id: str
    pet_name: str


__all__ = ["Task", "Pet", "Owner", "Scheduler", "ScheduledTask"]


__all__ = ["Task", "Pet", "Owner", "Scheduler"]
