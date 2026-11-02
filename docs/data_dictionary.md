# Online Exam Portal — data dictionary

This dictionary describes the current Django persistence models. Primary keys
are Django-generated `BigAutoField` values unless noted otherwise. The user
foreign keys target `settings.AUTH_USER_MODEL` (currently Django's default
`auth.User`).

## `exams_exam` — `Exam`

| Field | Type | Required / default | Meaning and constraints |
|---|---|---|---|
| `id` | BigAutoField | Generated | Primary key. |
| `title` | CharField(200) | Required | Exam title; model validation rejects whitespace-only titles. |
| `description` | TextField | Required | Exam description. |
| `duration_minutes` | PositiveIntegerField | Required | Duration from 1 through 600 minutes. |
| `start_time` | DateTimeField | Required | Earliest time an exam can be started. |
| `end_time` | DateTimeField | Required | Latest time an exam can be started; must be after `start_time`, with an availability window at least as long as the duration. |
| `is_active` | BooleanField | `true` | Whether the exam is enabled for student availability. |
| `created_by_id` | ForeignKey to configured user model | Required | Creator; `PROTECT` prevents deleting a creator that owns exams. Reverse name: `created_exams`. |
| `created_at` | DateTimeField | Set on insert | Creation timestamp. |

Default ordering is by descending `start_time`.

## `questions_question` — `Question`

| Field | Type | Required / default | Meaning and constraints |
|---|---|---|---|
| `id` | BigAutoField | Generated | Primary key. |
| `exam_id` | ForeignKey to `Exam` | Required | Parent exam; `CASCADE` deletes questions with their exam. Reverse name: `questions`. |
| `text` | TextField | Required | Question prompt. |
| `option_a` … `option_d` | CharField(500) each | Required | Four answer choices. |
| `correct_option` | CharField(1) | Required | One of `A`, `B`, `C`, or `D`. |
| `created_at` | DateTimeField | Set on insert | Creation timestamp. |

Default ordering is by ascending `id`.

## `attempts_attempt` — `Attempt`

| Field | Type | Required / default | Meaning and constraints |
|---|---|---|---|
| `id` | BigAutoField | Generated | Primary key. |
| `student_id` | ForeignKey to configured user model | Required | Student taking the exam; `PROTECT` prevents deleting a student with attempts. Reverse name: `exam_attempts`. |
| `exam_id` | ForeignKey to `Exam` | Required | Exam being attempted; `PROTECT` prevents deleting an exam with attempts. Reverse name: `attempts`. |
| `started_at` | DateTimeField | Required | Attempt start timestamp. |
| `deadline_at` | DateTimeField | Required | Deadline for submission. |
| `submitted_at` | DateTimeField | Nullable, blank allowed | Submission timestamp, absent until submitted. |
| `status` | CharField(20) | `IN_PROGRESS` | `IN_PROGRESS`, `SUBMITTED`, or `AUTO_SUBMITTED`. |

The pair (`student_id`, `exam_id`) is unique (`unique_student_exam_attempt`).
Default ordering is by descending `started_at`.

## `attempts_attemptanswer` — `AttemptAnswer`

| Field | Type | Required / default | Meaning and constraints |
|---|---|---|---|
| `id` | BigAutoField | Generated | Primary key. |
| `attempt_id` | ForeignKey to `Attempt` | Required | Parent attempt; `CASCADE` deletes answers with the attempt. Reverse name: `answers`. |
| `question_id` | ForeignKey to `Question` | Required | Answered question; `PROTECT` prevents deleting a question with recorded answers. Reverse name: `attempt_answers`. |
| `selected_option` | CharField(1) | Required | Selected choice: `A`, `B`, `C`, or `D`. |
| `updated_at` | DateTimeField | Updated on save | Timestamp of the latest saved selection. |

The pair (`attempt_id`, `question_id`) is unique
(`unique_answer_per_attempt_question`); this stores the latest answer for each
question in an attempt. Default ordering is by `question_id`.

## Scope notes

- Authentication and staff/student role fields come from Django's configured
  user model; the portal does not currently define a custom profile model.
- The `results` app does not define a separate results database model. Result
  data is derived from attempts, answers, and question correct choices.
