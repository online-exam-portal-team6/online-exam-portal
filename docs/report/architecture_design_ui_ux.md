# Architecture, Design and UI/UX

## System architecture

The Online Examination Portal is a modular Django monolith. Application boundaries separate accounts, exam configuration, question management, timed attempts and result presentation. Django authentication and session middleware provide identity. The browser uses server-rendered HTML and forms, plus a JSON endpoint for saving or changing an MCQ answer. The server remains authoritative for ownership, availability, deadlines and submission state.

## Design decisions

- Django MTV separates persistence, request handling and presentation.
- Service functions centralise attempt start, answer-save, submit and result-evaluation rules.
- ORM constraints enforce one attempt per student/exam, one answer per attempt/question and one persisted result per attempt.
- Role guards and object-level ownership filters protect private workflows.
- Server-side deadline is authoritative; browser countdown is only a display aid.
- Modular monolith keeps deployment simple while preserving app boundaries.

## Data design

The core entities are Exam, Question, Attempt, AttemptAnswer and Result. Exam owns questions and attempts; Attempt belongs to one student and one exam; AttemptAnswer joins a question to an attempt and stores the selected option; Result stores the evaluated score, total marks, percentage and pass outcome for one submitted attempt. The Result has a one-to-one relationship with Attempt. The evaluation service compares saved answers with correct options and applies per-question marks and the exam pass-percentage threshold. Unique constraints and protected/cascading foreign keys preserve the intended lifecycle and data integrity.

## UI and UX

The UI uses a shared dark visual system, side navigation, cards, tables, status labels and responsive layouts. Student journeys prioritise available exams, start instructions, remaining time, answer-save feedback and submit action. Administrator journeys prioritise exam, question and student management. Result pages put score, percentage and pass/fail status first; status text accompanies colour. Pending evaluation must be distinguished from a persisted evaluated result.

## Security and usability

Django sessions and password hashing protect authentication. CSRF middleware protects state-changing requests. Role guards and ownership filters protect student data. Answer and submit operations validate the server deadline. The shared 403 handler and designed access-denied template are included in the merged UI changes. The detailed controls, production configuration warnings and remaining hardening actions are documented in [Security Architecture](../security_architecture.md).

The UI applies a shared dark visual system, responsive navigation and card layouts. The usability review records observations from the supplied rendered captures and source inspection in [Usability Review](../usability_review.md). Eight screenshot captures were inspected, but their PNG binaries still need to be committed under docs/images/usability/ before the repository contains the visual evidence.

## Design patterns

The implementation uses Django Model–Template–View, a service layer for attempt lifecycle and result evaluation, role decorators, ORM constraints and transactions, Post/Redirect/Get, and idempotent start/save/submit/evaluate operations. See [Design Patterns](../design_patterns.md) for the pattern-to-code mapping.

## Verification and limitations

The result model, evaluation service and administrator result register have been integrated on main (PRs #24 and #25). Question create/edit/delete implementation PRs #17, #20 and #21 are also merged. Their CI runs and the merged code are evidence of automated integration, but they do not replace browser-level end-to-end verification against representative student and administrator accounts.

The outstanding evidence/acceptance items are the repository-hosted screenshot binaries, exported diagram PNGs, final integrated browser checks, and Product Owner review. The report intentionally does not claim those items are complete.
