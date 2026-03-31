import pytest
from pawpal_system import Task, Pet


def test_mark_complete():
    t = Task(task_id="tx", title="Test", duration_minutes=5)
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_add_task_to_pet():
    p = Pet(pet_id="px", name="Buddy")
    assert len(p.tasks) == 0
    t = Task(task_id="tadd", title="Feed", duration_minutes=10)
    p.add_task(t)
    assert len(p.tasks) == 1
    assert p.tasks[0].task_id == "tadd"
