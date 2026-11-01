# Online Examination Portal — class diagram

This diagram reflects the models present in the exam-attempt integration branch. It deliberately does not invent a Result schema: results/models.py is still a placeholder in the inspected source.

\`\`\`mermaid
classDiagram
  class User {
    <<Django auth user>>
    +id
    +username
    +email
    +is_staff
  }
  class Exam {
    +id
    +title
    +description
    +duration_minutes
    +start_time
    +end_time
    +is_active
    +created_at
    +clean()
  }
  class Question {
    +id
    +text
    +option_a
    +option_b
    +option_c
    +option_d
    +correct_option
    +created_at
    +options
  }
  class Attempt {
    +id
    +started_at
    +deadline_at
    +submitted_at
    +status
  }
  class AttemptAnswer {
    +id
    +selected_option
    +updated_at
  }
  User "1" --> "0..*" Exam : created_by
  User "1" --> "0..*" Attempt : student
  Exam "1" --> "0..*" Question : questions
  Exam "1" --> "0..*" Attempt : attempts
  Attempt "1" --> "0..*" AttemptAnswer : answers
  Question "1" --> "0..*" AttemptAnswer : selected for
\`\`\`

## Constraints

- Unique student/exam pair for Attempt.
- Unique attempt/question pair for AttemptAnswer; changing an option updates the existing row.
- Answer service verifies the question belongs to the attempt's exam.
- Attempt moves from IN_PROGRESS to SUBMITTED or AUTO_SUBMITTED.
- Options are restricted to A, B, C and D.

The final class diagram must be extended with the approved Result fields and relationships after the results owner supplies that schema.
