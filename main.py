from datetime import datetime, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def iso_minutes_from_now(minutes: int) -> datetime:
    return datetime.now() + timedelta(minutes=minutes)


def main():
    owner = Owner(owner_id="o1", name="Alex")

    dog = Pet(pet_id="p1", name="Rex", species="dog", age=4)
    cat = Pet(pet_id="p2", name="Mittens", species="cat", age=2)

    # Tasks with different durations and priorities
    t1 = Task(task_id="t1", title="Morning Walk", duration_minutes=30, priority=5, due_time=None)
    t2 = Task(task_id="t2", title="Feed Breakfast", duration_minutes=10, priority=8, due_time=None)
    t3 = Task(task_id="t3", title="Give Medication", duration_minutes=5, priority=10, due_time=iso_minutes_from_now(60))

    dog.add_task(t1)
    dog.add_task(t3)
    cat.add_task(t2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler()
    today = date.today()
    plan = scheduler.generate_daily_plan(owner, today, available_minutes=180)

    # Print readable schedule
    print("Today's Schedule:\n")
    if not plan:
        print("(no tasks scheduled)")
        return

    for item in plan:
        start = item["start"].strftime("%H:%M")
        end = item["end"].strftime("%H:%M") if item["end"] != item["start"] else start
        task = item["task"]
        print(f"{start} - {end}: {item['pet_name']} — {task.title} ({task.duration_minutes}m) [priority={task.priority}]")


if __name__ == "__main__":
    main()
