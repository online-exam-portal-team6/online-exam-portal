# Project Management and Backend Implementation

## 1. Project management

### Delivery approach
The Online Examination Portal is developed incrementally, with work organised into feature tickets and pull requests. Each ticket describes expected behaviour and acceptance criteria; implementation is integrated into `main` through review and automated checks. This keeps changes traceable and allows features to be verified independently before integration.

### Planning and tracking
Project work is tracked through the team's issue/ticket and pull-request workflow. Feature-sized tasks are assigned to contributors, implemented on dedicated branches, and submitted as pull requests targeting `main`. Pull requests provide the change summary, discussion and review record. Where a change affects shared code, conflicts are resolved against the current base branch and the resulting checks are rerun.

### Quality gates
The repository's CI workflow is documented in the database/CI/CD report. It installs the supported Python versions and dependencies, then runs Flake8, Django system checks, migration consistency checks and the Django test suite. A change should be considered ready for integration only after the relevant checks pass and required human review is complete.

### Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Conflicting changes to shared files | Integrate frequently with `main`, resolve conflicts deliberately, and rerun checks. |
| Regressions in exam and result workflows | Keep automated tests for attempt lifecycle, answer saving, submission and result evaluation. |
| Incorrect or duplicate results | Enforce database uniqueness and use transactional, idempotent result persistence. |
| Production configuration differs from local development | Require secrets, allowed hosts and a database URL through environment configuration; validate deployment settings separately. |
| Incomplete release readiness | Treat passing CI, review, migration checks, backup/restore planning and deployment verification as release gates. |

### Project status and reporting discipline
This section describes the repository workflow and implementation visible in the project; it does not claim that every ticket is closed, every pull request is merged, or that production deployment has occurred. Current ticket ownership, approvals and release status should be taken from the team's issue tracker, GitHub pull requests and deployment environment.

## 2. Backend implementation

### Technology and structure
The backend is a Django modular monolith. Django apps separate account management, examinations, questions, attempts and results. Django ORM models provide relational persistence, migrations manage schema changes, and server-rendered templates present the user interface. The backend is authoritative for permissions, exam availability, deadlines, answer persistence and submission state.

### Core domain model
- **User:** Django authentication identity used for students and staff.
- **Exam:** stores exam configuration, availability window, duration and pass threshold.
- **Question:** belongs to an exam and stores the MCQ options, correct option and marks.
- **Attempt:** associates a student with an exam and tracks start time, deadline, submission time and status.
- **AttemptAnswer:** associates an attempt with a question and stores the selected option.
- **Result:** stores the evaluated score, total marks, percentage and pass outcome for an attempt.

Database relationships and uniqueness constraints protect key invariants, including one attempt per student/exam, one answer per attempt/question, and one result per attempt.

### Attempt lifecycle and answer handling
The `attempts.services` module centralises the main attempt operations:
1. `start_attempt` validates the exam availability window and returns an existing in-progress attempt rather than creating a second one.
2. `save_answer` validates the selected option, confirms the question belongs to the attempt's exam, checks that the attempt is still active and before its deadline, then uses `update_or_create` to persist the answer.
3. `submit_attempt` locks the attempt, finalises it once as manually or automatically submitted, and invokes result evaluation.

The service layer uses database transactions and row-level locking where appropriate to reduce race conditions around starting, saving and submitting attempts. The browser countdown is not trusted as the source of deadline enforcement; server-side timestamps determine whether an operation is allowed.

### Result evaluation and persistence
The `results.services` module compares each saved selected option with the question's stored correct option. It calculates awarded marks, total possible marks, percentage and pass/fail outcome using the exam's pass threshold. The result is persisted with `update_or_create` keyed by attempt, making evaluation repeatable without creating duplicate result rows. Evaluation is restricted to submitted or automatically submitted attempts and rejects exams with no questions.

### Security and validation
Django authentication, password hashing, CSRF middleware and role/ownership checks protect application workflows. The backend validates that requested questions belong to the relevant exam and that a student can only operate on their own attempt. Expected validation failures are handled as user-facing errors; unexpected failures should be logged server-side without exposing internal exception details to users. Production settings require environment-provided secret key, allowed hosts and database URL, and enable secure cookie/HTTPS-related settings when debug mode is disabled.

### Configuration and deployment considerations
Development defaults use SQLite. A production database is supplied through `DATABASE_URL`; secret key and allowed-host configuration are also environment-driven. Static assets are collected under `STATIC_ROOT` and WhiteNoise is configured for production static-file serving. These settings support deployment configuration but do not by themselves prove that a live production deployment has been completed.

### Verification
The documented CI workflow runs:
- Flake8 linting.
- `python manage.py check`.
- `python manage.py makemigrations --check --dry-run`.
- `python manage.py test`.

Feature-level tests should cover attempt ownership, deadline enforcement, manual and automatic submission, correct/incorrect/unanswered MCQ evaluation, and idempotent result persistence. The latest CI result for a particular commit must be checked in GitHub rather than inferred from the existence of tests.

## 3. References
- `docs/report/architecture_design_ui_ux.md` — system architecture and design decisions.
- `docs/report/database_ci_cd_release.md` — database, CI/CD and release management.
- `docs/error_handling.md` — error-handling approach.
- `docs/data_dictionary.md` and `docs/er_diagram.md` — data definitions and relationships.
- `attempts/services.py` — attempt lifecycle and answer persistence.
- `results/services.py` — answer comparison, scoring and result persistence.
