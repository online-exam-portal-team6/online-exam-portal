# OEP-66: Take Exam Sequence Diagram

**Status:** Intended end-to-end flow based on the SRS and service contracts. Result evaluation remains a separately owned integration dependency.

```mermaid
sequenceDiagram
    actor Student
    participant Browser
    participant StartView as Exam Start View
    participant AttemptService as Attempt Service
    participant ExamView as Exam Take View
    participant AnswerService as Answer Service
    participant SubmitView as Exam Submit View
    participant Evaluation as Evaluation Service
    participant DB as Database
    participant ResultView as Result Detail View

    Student->>Browser: Open available exam
    Browser->>StartView: GET exam start page
    StartView-->>Browser: Display exam rules
    Browser-->>Student: Show rules and start option

    Student->>Browser: Confirm start
    Browser->>StartView: POST start request
    StartView->>AttemptService: start_attempt(student, exam)
    AttemptService->>DB: Create or retrieve unique attempt
    DB-->>AttemptService: Attempt record
    AttemptService-->>StartView: Return attempt
    StartView-->>Browser: Redirect to exam-taking page

    Browser->>ExamView: GET attempt page
    ExamView->>DB: Load exam, questions, answers and deadline
    DB-->>ExamView: Return exam data
    ExamView-->>Browser: Render questions and timer
    Browser-->>Student: Display exam

    loop For each answer
        Student->>Browser: Select or change an option
        Browser->>AnswerService: POST question_id and option
        AnswerService->>DB: Validate ownership, exam and deadline; save answer
        DB-->>AnswerService: Save outcome
        AnswerService-->>Browser: Return save status
    end

    alt Student submits before deadline
        Student->>Browser: Confirm submission
        Browser->>SubmitView: POST manual submit
    else Timer reaches zero
        Browser->>SubmitView: POST automatic submit
    end

    SubmitView->>AttemptService: submit_attempt(attempt, auto)
    AttemptService->>DB: Persist submitted state and timestamp
    DB-->>AttemptService: Submission state
    AttemptService->>Evaluation: evaluate_attempt(attempt)
    Evaluation->>DB: Read answers and correct options
    DB-->>Evaluation: Return answer data
    Evaluation->>DB: Persist score and pass/fail result
    DB-->>Evaluation: Evaluation saved
    Evaluation-->>AttemptService: Return evaluation outcome
    AttemptService-->>SubmitView: Submission complete
    SubmitView-->>Browser: Redirect to result detail

    Browser->>ResultView: GET result detail
    ResultView-->>Browser: Return result details
    Browser-->>Student: Display examination result
```

**Integration note:** The current results evaluator is still a placeholder in the inspected main branch. The evaluation lifeline documents the intended contract and is not proof that score persistence is implemented.
