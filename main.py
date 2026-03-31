from datetime import datetime, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


def iso_minutes_from_now(minutes: int) -> datetime:
    return datetime.now() + timedelta(minutes=minutes)


def main():
    owner = Owner(owner_id="o1", name="Alex")

    dog = Pet(pet_id="p1", name="Rex", species="dog", age=4)
    cat = Pet(pet_id="p2", name="Mittens", species="cat", age=2)

    # Tasks with different durations and priorities
    # Add tasks out of chronological order to test sorting
    t1 = Task(task_id="t1", title="Morning Walk", duration_minutes=30, priority=5, due_time=None)
    t2 = Task(task_id="t2", title="Feed Breakfast", duration_minutes=10, priority=8, due_time=None)
    # recurring daily medication
    t3 = Task(task_id="t3", title="Give Medication", duration_minutes=5, priority=10, due_time=iso_minutes_from_now(60), recurrence="daily")
    # two simultaneous tasks to test conflict detection
    t4 = Task(task_id="t4", title="Grooming", duration_minutes=30, priority=3, due_time=None)
    t5 = Task(task_id="t5", title="Training", duration_minutes=30, priority=4, due_time=None)

    # Add tasks in an intentionally mixed order
    dog.add_task(t3)
    cat.add_task(t2)
    dog.add_task(t1)

    # schedule two same-time items (we'll force same start by giving them same priority and zero due_time)
    dog.add_task(t4)
    cat.add_task(t5)

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler()
    today = date.today()
    plan = scheduler.generate_daily_plan(owner, today, available_minutes=180)

    # Demonstrate sorting and filtering
    print("\nAll scheduled items (unsorted):")
    for item in plan:
        print(item["task"].title, item["start"].strftime("%H:%M"))

    sorted_plan = scheduler.sort_by_time(plan)
    print("\nSorted schedule by start time:")
    for item in sorted_plan:
        print(item["start"].strftime("%H:%M"), "-", item["task"].title)

    # Detect conflicts
    warnings = scheduler.detect_conflicts(plan)
    if warnings:
        print("\nConflicts detected:")
        for w in warnings:
            print("-", w)

    # Also run a lightweight due_time conflict detector across owner's tasks
    due_warnings = scheduler.detect_due_time_conflicts(owner)
    if due_warnings:
        print("\nDue-time conflicts detected:")
        for w in due_warnings:
            print("-", w)

    # Demonstrate recurring task auto-creation: mark medication complete and add its next occurrence
    print("\nMarking medication complete (recurring)...")
    new_t = dog.mark_task_complete("t3")
    if new_t:
        dog.add_task(new_t)
        print(f"Created recurring task: {new_t.task_id} with due {new_t.due_time}")

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
