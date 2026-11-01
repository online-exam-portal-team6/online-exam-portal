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
Django sessions and password hashing protect authentication. CSRF middleware protects state-changing requests. Role guards and ownership filters protect student data. Answer and submit operations validate the server deadline. The usability review applies Nielsen heuristics; source CSS contains responsive breakpoints, but rendered screenshots and live browser verification must still be attached.

## Verification and limitations
GitHub Actions checks Flake8, Django system checks, migration consistency and Django tests. Feature tests use SRS test IDs. Remaining integration dependencies include the approved result persistence/evaluation service and live desktop/mobile screenshot evidence.
