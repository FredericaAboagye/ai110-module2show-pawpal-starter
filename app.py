import streamlit as st
from datetime import date

# import domain classes from the logic layer
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Pets & Tasks")
st.caption("Create pets and add tasks to them. These objects persist in `st.session_state`.")

# Create or retrieve Owner in session_state
if "owner" not in st.session_state:
    if st.button("Create owner"):
        st.session_state.owner = Owner(owner_id="o1", name=owner_name)
        st.success(f"Created owner: {owner_name}")
else:
    owner: Owner = st.session_state.owner

    st.write(f"**Owner:** {owner.name} (pets: {len(owner.pets)})")

    colp1, colp2 = st.columns([2, 1])
    with colp1:
        new_pet_name = st.text_input("New pet name", value=pet_name, key="new_pet_name")
    with colp2:
        new_species = st.selectbox("Species (new pet)", ["dog", "cat", "other"], key="new_pet_species")

    if st.button("Add pet", key="add_pet"):
        pet_id = f"pet{len(owner.pets) + 1}"
        pet = Pet(pet_id=pet_id, name=new_pet_name, species=new_species)
        owner.add_pet(pet)
        st.success(f"Added pet {new_pet_name}")

    # Show existing pets and allow adding tasks to a selected pet
    if owner.pets:
        pet_options = [f"{p.name} ({p.pet_id})" for p in owner.pets]
        sel = st.selectbox("Select pet", pet_options, key="sel_pet")
        sel_index = pet_options.index(sel)
        selected_pet = owner.pets[sel_index]

        st.markdown(f"**Selected pet:** {selected_pet.name}")

        tcol1, tcol2, tcol3 = st.columns(3)
        with tcol1:
            task_title = st.text_input("Task title", value="Morning walk", key="task_title")
        with tcol2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
        with tcol3:
            priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority")

        priority_map = {"low": 1, "medium": 5, "high": 10}

        if st.button("Add task to pet", key="add_task"):
            task_id = f"task{sum(len(p.tasks) for p in owner.pets) + 1}"
            t = Task(task_id=task_id, title=task_title, duration_minutes=int(duration), priority=priority_map[priority_label])
            selected_pet.add_task(t)
            st.success(f"Added task '{task_title}' to {selected_pet.name}")

        # Display pets and their tasks
        for p in owner.pets:
            st.markdown(f"- **{p.name}** ({p.species}) — {len(p.tasks)} tasks")
            if p.tasks:
                for tt in p.tasks:
                    status = "✓" if tt.completed else " "
                    st.write(f"    - {tt.title} ({tt.duration_minutes}m) [priority={tt.priority}] {status}")
    else:
        st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule for today using your Scheduler implementation.")

if st.button("Generate schedule"):
    if "owner" not in st.session_state:
        st.error("Create an owner first.")
    else:
        owner = st.session_state.owner
        scheduler = Scheduler()
        plan = scheduler.generate_daily_plan(owner, date.today(), available_minutes=8 * 60)
        if not plan:
            st.info("No scheduled tasks (none fit or no tasks).")
        else:
            st.markdown("### Today's Schedule")
            for item in plan:
                start = item["start"].strftime("%H:%M")
                end = item["end"].strftime("%H:%M") if item["end"] != item["start"] else start
                task = item["task"]
                st.write(f"{start} - {end}: {item['pet_name']} — {task.title} ({task.duration_minutes}m) [priority={task.priority}]")
