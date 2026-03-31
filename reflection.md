# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- I designed four primary classes to model the system and keep the responsibilities focused:
	- `Owner`: holds owner metadata, contact info, preferences, and a collection of `Pet` objects. Responsible for managing pets and exposing owner-level preferences used by the scheduler.
	- `Pet` (dataclass): represents a single animal with identifying info, simple medical info, and a list of `Task` instances. Responsible for managing its tasks (add/remove/upcoming queries).
	- `Task` (dataclass): represents an individual care item (walk, feed, med, grooming). Contains `task_id`, `title`, `duration_minutes`, `priority`, optional `recurrence`/`due_time`, and a `completed` flag. Responsible for small task operations like `mark_complete()` and `reschedule()`.
	- `Scheduler`: contains scheduling logic to generate a daily plan for an `Owner` (examining their pets' `Task`s and owner preferences). Responsible for `generate_daily_plan()`, `score_task()` and `explain_plan()`.

	The responsibilities follow a separation-of-concerns approach: data containers (`Pet`, `Task`) are lightweight dataclasses, `Owner` is the aggregate root for user data, and `Scheduler` is the pure logic layer that reads domain objects and produces schedules.

**b. Design changes**

- No major design changes yet — this is the initial implementation derived from the UML.

- Practical additions made during implementation:

-  - Introduced a `ScheduledTask` dataclass returned by the scheduler (implemented as dicts in this phase) so scheduled items are structured and include start/end, `task`, and pet metadata. This keeps the scheduler's output explicit and easier to format or persist.
-  - Added `Owner.get_all_tasks()` to provide the `Scheduler` an easy, single API to retrieve `(pet, task)` tuples across all pets. This reduced coupling and clarified how the `Scheduler` accesses domain data.
-  - Implemented a simple, deterministic `Scheduler.generate_daily_plan()` that sorts tasks by priority and due time and schedules them sequentially starting at 09:00. Tasks that don't fit are skipped. This is intentionally simple to keep the first working iteration easy to test.

- Potential next refinements I may make based on AI feedback:

-  - Replace the temporary dict-based schedule with `ScheduledTask` objects everywhere and expose clearer constraints (time windows, owner availability slots).
-  - Add non-overlap checks for single-owner constraints across multiple pets, and support splitting long tasks or partial scheduling.
-  - Add a `Schedule` or `PlannerConfig` object to tune weights and allow deterministic unit testing of scheduling heuristics.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**


- Tradeoff chosen: lightweight conflict detection vs. full interval scheduling.

- I implemented simple conflict checks: (1) an overlap check on the generated schedule and (2) a due-time equality check across tasks. I deliberately did not implement a full interval-graph-based conflict resolver or preemptive task splitting. That would be more flexible but also more complex and harder to test.

- Why reasonable: for a first iteration the owner benefits more from predictable, deterministic scheduling and clear warnings about exact time clashes. Full overlap resolution and task-splitting are future improvements once basic behavior is stable and covered by tests.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- I used Copilot (Inline Chat and Agent modes) throughout the project to brainstorm UML designs, generate class skeletons, suggest scheduling heuristics, and draft tests. The most helpful prompts asked for concrete code patterns ("create a dataclass for Task with X fields") or for short algorithm sketches ("simple conflict detection strategy for scheduled tasks").


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- Example rejected suggestion: Copilot proposed automatically splitting long tasks to fit the schedule. I rejected this for the initial implementation because it would complicate scheduling semantics and increase testing surface; instead I preferred clear warnings and deterministic behavior. I evaluated this by writing unit tests and choosing the simpler path that is easier to reason about.

**c. Copilot features and workflow**

- Inline Chat: used to iterate quickly on small code changes and ask targeted questions about the local file (e.g., how to sort a plan by start time).
- Agent Mode / Multi-file edits: used for larger refactors or when creating multiple files like `main.py`, `tests`, and `pawpal_system.py` skeletons.
- Suggestion review: I kept suggestions that were clear and testable, and modified or rejected suggestions that risked adding hidden state or unnecessary complexity.

Using separate chat sessions per phase helped keep prompts focused (design → implementation → testing → polish). That separation made it easier to reproduce the reasoning for each phase and roll back if a change didn't work.

**d. Lead architect takeaways**

- Being the lead architect means making tradeoffs: prefer deterministic, testable features first (sorting, warnings, recurrence) before adding complex automation (task splitting, constraint solvers). AI accelerates drafting and brainstorming, but human judgment guided what to accept.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
