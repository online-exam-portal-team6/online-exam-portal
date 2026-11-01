# Online Examination Portal — class diagram

This diagram is derived from the current Django model definitions in contract B5's application skeleton. It documents only fields that exist in the inspected models. results/models.py is currently a placeholder, so no Result class or invented result fields are shown.

\`\`\`mermaid
classDiagram
  class User {
    <<Django AUTH_USER_MODEL>>
    +primary_key id
    +username
    +email
    +is_staff
  }
  class Exam {
    +BigAutoField id
    +CharField title
    +TextField description
    +PositiveIntegerField duration_minutes
    +DateTimeField start_time
    +DateTimeField end_time
    +BooleanField is_active
    +ForeignKey created_by
    +DateTimeField created_at
    +clean()
  }
  class Question {
    +BigAutoField id
    +ForeignKey exam
    +TextField text
    +CharField option_a
    +CharField option_b
    +CharField option_c
    +CharField option_d
    +CharField correct_option
    +DateTimeField created_at
    +options
  }
  class Attempt {
    +BigAutoField id
    +ForeignKey student
    +ForeignKey exam
    +DateTimeField started_at
    +DateTimeField deadline_at
    +DateTimeField submitted_at
    +CharField status
  }
  class AttemptAnswer {
    +BigAutoField id
    +ForeignKey attempt
    +ForeignKey question
    +CharField selected_option
    +DateTimeField updated_at
  }
  User "1" --> "0..*" Exam : created_by
  User "1" --> "0..*" Attempt : student
  Exam "1" --> "0..*" Question : questions
  Exam "1" --> "0..*" Attempt : attempts
  Attempt "1" --> "0..*" AttemptAnswer : answers
  Question "1" --> "0..*" AttemptAnswer : selected for
\`\`\`

## Model constraints and behaviour

- **Exam:** title must not be blank; duration is 1–600 minutes; end time must be after start time; the availability window must be at least the exam duration. Deleting the creator is protected (PROTECT).
- **Question:** belongs to one Exam (CASCADE on exam deletion); answer key is restricted to A, B, C or D. The options property exposes the four option labels and text; it is not a database column.
- **Attempt:** belongs to one student and one Exam; deleting either referenced record is protected. A database unique constraint enforces one attempt per student/exam. Status is IN_PROGRESS, SUBMITTED or AUTO_SUBMITTED.
- **AttemptAnswer:** belongs to one Attempt and one Question; deleting an Attempt cascades, while deleting a Question is protected. A database unique constraint enforces one answer row per attempt/question. The selected option is restricted to A–D.
- **User:** uses Django's configured AUTH_USER_MODEL; the diagram does not assume a custom StudentProfile or roll-number field.

## Deliberate scope boundary

The current results/models.py contains no model and the evaluation service is not yet implemented in the inspected base branch. The Result class, score/percentage fields, pass/fail attribute and relationship cardinality must be added only after the result-owner's approved model contract is merged. This avoids presenting a speculative schema as implemented fact.
