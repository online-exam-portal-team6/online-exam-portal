# Online Exam Portal — ER diagram

This diagram reflects the Django models currently implemented in the portal.
The user entity is Django's configured `AUTH_USER_MODEL` (the default project
configuration uses `auth.User`).

```mermaid
erDiagram
    AUTH_USER ||--o{ EXAM : creates
    AUTH_USER ||--o{ ATTEMPT : takes
    EXAM ||--o{ QUESTION : contains
    EXAM ||--o{ ATTEMPT : receives
    ATTEMPT ||--o{ ATTEMPT_ANSWER : records
    QUESTION ||--o{ ATTEMPT_ANSWER : is_answered_in

    AUTH_USER {
        bigint id PK
        string username
    }
    EXAM {
        bigint id PK
        string title
        text description
        positive_integer duration_minutes
        datetime start_time
        datetime end_time
        boolean is_active
        bigint created_by_id FK
        datetime created_at
    }
    QUESTION {
        bigint id PK
        bigint exam_id FK
        text text
        string option_a
        string option_b
        string option_c
        string option_d
        string correct_option
        datetime created_at
    }
    ATTEMPT {
        bigint id PK
        bigint student_id FK
        bigint exam_id FK
        datetime started_at
        datetime deadline_at
        datetime submitted_at
        string status
    }
    ATTEMPT_ANSWER {
        bigint id PK
        bigint attempt_id FK
        bigint question_id FK
        string selected_option
        datetime updated_at
    }
```

## Relationship and integrity notes

- A user may create many examinations; every examination has one creator.
- An examination may contain many questions and have many student attempts.
- A student may have at most one attempt per examination, enforced by the
  `unique_student_exam_attempt` constraint.
- An attempt may store one latest answer per question, enforced by the
  `unique_answer_per_attempt_question` constraint.
- Deleting an examination cascades to its questions. Attempts protect their
  examination and student rows; attempt answers cascade with their attempt and
  protect referenced questions.
- Correct answers are stored on questions; student selections are stored on
  attempt answers. Results are calculated from these records; there is no
  separate results table in the current schema.
