# Design patterns used in the Online Examination Portal

## Model–Template–View (Django MTV)
Models represent Exam, Question, Attempt and AttemptAnswer. Views validate requests, apply authorization and call services. Templates render HTML from explicit context; JavaScript enhances autosave and countdown without becoming the source of truth.

## Service layer
- start_attempt(student, exam) validates availability and creates or reuses the one allowed attempt.
- save_answer(attempt, question_id, option) validates the question and persists the selected option.
- submit_attempt(attempt, auto=False) records manual or automatic submission and invokes result evaluation.

Views translate service validation failures into HTTP responses or user messages. This keeps exam rules out of duplicated view logic.

## Decorator / role guard
student_required and admin_required centralise authentication and role checks. Anonymous users are redirected to login; authenticated users with the wrong role receive HTTP 403. Object-level ownership filters are still required because a role check does not prove that a student owns an attempt or result.

## ORM, transactions and constraints
Django ORM querysets express relationships and ownership. transaction.atomic(), row locks and unique constraints protect concurrent state changes and prevent duplicate attempts or answers.

## Post/Redirect/Get and JSON
HTML start/submit forms use POST then redirect to avoid refresh resubmission. The answer endpoint returns JSON so the page can show immediate save feedback.

## Idempotency
Starting returns an existing in-progress attempt, answer updates replace the same question's saved answer, and repeated submission returns the persisted state without evaluating twice.

| Pattern | Where used |
|---|---|
| MTV | models.py, views.py and app templates |
| Service layer | attempts/services.py, exams/services.py, results/services.py |
| Decorator | accounts/decorators.py |
| ORM / transaction | model relations, constraints and atomic service operations |
| Post/Redirect/Get | start and submit views |
| Idempotency | start, answer update and submit services |

The application remains a modular monolith: simpler to deploy for this project while retaining clear app boundaries.
