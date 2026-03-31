from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, date


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
        pass

    def reschedule(self, new_time: datetime) -> None:
        """Reschedule the task to a new datetime."""
        pass


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
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def upcoming_tasks(self, until: Optional[datetime] = None) -> List[Task]:
        pass


class Owner:
    def __init__(self, owner_id: str, name: str, contact_info: Optional[dict] = None, preferences: Optional[dict] = None):
        self.owner_id = owner_id
        self.name = name
        self.contact_info = contact_info or {}
        self.preferences = preferences or {}
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        return self.pets


class Scheduler:
    """Generates plans/schedules for an Owner's pets based on tasks and constraints."""

    def __init__(self):
        # future: configuration, scoring weights, etc.
        pass

    def generate_daily_plan(self, owner: Owner, day: date, available_minutes: int = 480) -> List[dict]:
        """Return a list of scheduled items (dicts with start/end/task).

        This is a skeleton stub; scheduling logic will be implemented in later phases.
        """
        pass

    def explain_plan(self, plan: List[dict]) -> str:
        """Produce a human-readable explanation of why tasks were scheduled."""
        pass

    def score_task(self, task: Task, constraints: dict) -> float:
        """Return a numerical score for task priority under given constraints."""
        pass


__all__ = ["Task", "Pet", "Owner", "Scheduler"]
