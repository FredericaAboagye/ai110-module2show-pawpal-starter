from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime, date, time, timedelta


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

    def reschedule(self, new_time: datetime) -> None:
        """Reschedule the task to a new datetime by updating `due_time`."""
        self.due_time = new_time


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
