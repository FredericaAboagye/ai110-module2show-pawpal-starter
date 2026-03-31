import pytest
from pawpal_system import Task, Pet
from pawpal_system import Owner, Scheduler
from datetime import datetime, timedelta


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


def test_sorting_correctness():
    owner = Owner(owner_id="o_test", name="TestOwner")
    pet = Pet(pet_id="p_test", name="Spot")
    # create tasks with different priorities so scheduler orders them
    t_high = Task(task_id="th", title="High", duration_minutes=5, priority=10)
    t_med = Task(task_id="tm", title="Medium", duration_minutes=10, priority=5)
    t_low = Task(task_id="tl", title="Low", duration_minutes=15, priority=1)
    pet.add_task(t_low)
    pet.add_task(t_high)
    pet.add_task(t_med)
    owner.add_pet(pet)

    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner, datetime.today().date(), available_minutes=180)
    sorted_plan = scheduler.sort_by_time(plan)

    # assert non-decreasing start times
    starts = [item["start"] for item in sorted_plan]
    assert all(starts[i] <= starts[i + 1] for i in range(len(starts) - 1))


def test_recurrence_logic():
    pet = Pet(pet_id="p_r", name="Repeat")
    due = datetime.now()
    t = Task(task_id="tr", title="DailyMed", duration_minutes=5, priority=5, due_time=due, recurrence="daily")
    pet.add_task(t)

    new_task = pet.mark_task_complete("tr")
    assert new_task is not None
    assert new_task.recurrence == "daily"
    assert new_task.due_time == due + timedelta(days=1)


def test_due_time_conflict_detection():
    owner = Owner(owner_id="o_conf", name="ConfOwner")
    pet1 = Pet(pet_id="p1", name="A")
    pet2 = Pet(pet_id="p2", name="B")
    due = datetime.now() + timedelta(hours=2)
    t1 = Task(task_id="c1", title="T1", duration_minutes=10, due_time=due)
    t2 = Task(task_id="c2", title="T2", duration_minutes=15, due_time=due)
    pet1.add_task(t1)
    pet2.add_task(t2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler()
    warnings = scheduler.detect_due_time_conflicts(owner)
    assert any("Due-time conflict" in w for w in warnings)
