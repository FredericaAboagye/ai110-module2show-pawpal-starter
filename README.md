# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

This project includes several algorithmic improvements beyond the initial skeleton:

- Sorting: tasks are ordered by priority and due time before scheduling.
- Filtering: API to filter tasks by completion status or pet name.
- Recurring tasks: marking a `daily` or `weekly` task complete will create the next occurrence automatically.
- Conflict detection: lightweight checks detect overlapping scheduled items and identical due-times across pets and emit warnings.

These features are intentionally simple to keep the system testable and deterministic. Future work can add more sophisticated planners and constraint-solving.

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

Tests included:
- Sorting correctness: verifies scheduled items are ordered by start time.
- Recurrence logic: verifies marking a `daily` task complete creates the next occurrence.
- Conflict detection: verifies the scheduler flags identical due-time tasks across pets.

Confidence Level: ★★★☆☆ (3/5) — basic behaviors are covered; more edge cases and conflict resolution need tests.

## 📸 Demo

To include an app screenshot, export a screenshot of the running Streamlit app and save it under `/course_images/ai110/your_screenshot_name.png` then embed it like this:

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

If you want the final UML image included, render `class_diagram.mmd` with the Mermaid Live Editor and save it as `uml_final.png` in the project root.
