# Online Examination Portal — class diagram

This class diagram reflects the model contract in the current exam/attempt skeleton plus the Result model and scoring fields introduced in the results integration PR #24 (which is still open and must be merged before this schema is present on main). It is therefore an integration-target diagram, not a claim that PR #24 is already merged.

```mermaid
classDiagram
  class User {
    <<Django AUTH_USER_MODEL>>
    +id
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
    +DecimalField pass_percentage
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
    +PositiveIntegerField marks
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
  class Result {
    +BigAutoField id
    +OneToOneField attempt
    +ForeignKey student
    +ForeignKey exam
    +PositiveIntegerField score
    +PositiveIntegerField total_marks
    +DecimalField percentage
    +BooleanField passed
    +DateTimeField created_at
    +DateTimeField updated_at
  }
  User "1" --> "0..*" Exam : created_by
  User "1" --> "0..*" Attempt : student
  User "1" --> "0..*" Result : examination_results
  Exam "1" --> "0..*" Question : questions
  Exam "1" --> "0..*" Attempt : attempts
  Exam "1" --> "0..*" Result : examination_results
  Attempt "1" --> "0..*" AttemptAnswer : answers
  Question "1" --> "0..*" AttemptAnswer : selected for
  Attempt "1" --> "0..1" Result : result
```

## Relationships and constraints

- **User–Exam:** each Exam has one creator; a User may create many exams. Creator deletion is protected (PROTECT).
- **User–Attempt:** each Attempt belongs to one student; a User may have many attempts. Student deletion is protected.
- **Exam–Question:** each Question belongs to one Exam; deleting an Exam cascades to its questions.
- **Exam–Attempt:** each Attempt belongs to one Exam; Exam deletion is protected. A unique constraint permits one attempt per student/exam.
- **Attempt–AttemptAnswer:** an Attempt has zero or many saved answers; deleting an Attempt cascades to its answers. One answer per attempt/question is enforced by a unique constraint.
- **Question–AttemptAnswer:** each saved answer refers to one Question; deleting a referenced Question is protected. Selected option is A, B, C or D.
- **Attempt–Result:** each Result refers to exactly one Attempt through a OneToOneField; each Attempt has zero or one Result. Result deletion of its referenced Attempt is protected.
- **User–Result and Exam–Result:** each Result records the student and exam for the evaluated attempt; both references use PROTECT.
- **Exam scoring configuration:** pass_percentage is a DecimalField (default 50.00) constrained by model validation to 0–100.
- **Question scoring configuration:** marks is a PositiveIntegerField (default 1).
- **Result values:** score and total_marks are positive integers; percentage is Decimal(6,2); passed is boolean; created_at and updated_at are timestamps.

## Status and scope

The Attempt status is IN_PROGRESS, SUBMITTED or AUTO_SUBMITTED. Result is created/updated by the evaluation service after submission; the service compares saved answers with each question's correct option and calculates weighted marks and percentage.

**Integration dependency:** Result, Exam.pass_percentage and Question.marks are supplied by PR #24 (Bhumika's evaluation/results integration). The diagram records that proposed schema so the team can review the complete target model. If PR #24 changes before merge, update this diagram to the merged model before treating it as final.
