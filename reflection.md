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


- No changes yet. This draft is the initial skeleton mapped directly from the UML.

- Next step: ask Copilot to review the skeleton in `#file:pawpal_system.py` and suggest missing relationships or potential bottlenecks (for example: task dependencies, owner-level concurrency constraints, or a need for a `Schedule`/`ScheduledTask` value object).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
