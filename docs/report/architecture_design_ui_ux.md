# Architecture, Design and UI/UX

## System architecture
The Online Examination Portal is a modular Django monolith. Application boundaries separate accounts, exam configuration, question management, timed attempts and result presentation. Django authentication and session middleware provide identity. The browser uses server-rendered HTML and forms, plus a JSON endpoint for saving or changing an MCQ answer. The server remains authoritative for ownership, availability, deadlines and submission state.

## Design decisions
- Django MTV separates persistence, request handling and presentation.
- Service functions centralise attempt start, answer-save and submit rules.
- ORM constraints enforce one attempt per student/exam and one answer per attempt/question.
- Role guards and object-level ownership filters protect private workflows.
- Server-side deadline is authoritative; browser countdown is only a display aid.
- Modular monolith keeps deployment simple while preserving app boundaries.

## Data design
Current exam-taking entities are Exam, Question, Attempt and AttemptAnswer. Exam owns questions and attempts; Attempt belongs to one student and one exam; AttemptAnswer joins a question to an attempt and stores the selected option. Unique constraints prevent duplicate attempts and answer rows. Result schema/evaluation remains a separate integration responsibility and this report must be updated when the approved Result model is merged.

## UI and UX
The UI uses a shared dark visual system, side navigation, cards, tables, status labels and responsive layouts. Student journeys prioritise available exams, start instructions, remaining time, answer-save feedback and submit action. Administrator journeys prioritise exam, question and student management. Result pages put score, percentage and pass/fail status first; status text accompanies colour.

## Security and usability
Django sessions and password hashing protect authentication. CSRF middleware protects state-changing requests. Role guards and ownership filters protect student data. Answer and submit operations validate the server deadline. The shared 403 handler now has a designed access-denied template in the pending OEP-42/51/71 change set. The detailed controls, production configuration warnings and remaining hardening actions are documented in [Security Architecture](../security_architecture.md).

The UI applies a shared dark visual system, responsive navigation and card layouts. The usability review records observations from the supplied rendered captures and source inspection in [Usability Review](../usability_review.md). The eight screenshot binaries are not yet repository-hosted, so this report does not claim that evidence is attached.

## Design patterns
The implementation uses Django Model–Template–View, a service layer for attempt lifecycle operations, role decorators, ORM constraints and transactions, Post/Redirect/Get, and idempotent start/save/submit operations. See [Design Patterns](../design_patterns.md) for the pattern-to-code mapping.

## Verification and limitations
GitHub Actions runs the repository's Django checks, tests and lint workflow on pull requests. Feature tests use SRS test IDs. The main remaining integration dependency is final confirmation of the result evaluation/persistence schema and its end-to-end behaviour. The report should be refreshed after the result-owner integration and Product Owner acceptance.
