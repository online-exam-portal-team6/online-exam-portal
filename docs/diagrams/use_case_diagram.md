# Online Examination Portal — use-case diagram

Source: SRS section 7.1, functional requirements OEP-F-001 to OEP-F-024 and the SRS v1.1 revision note.

\`\`\`mermaid
flowchart LR
  Student([Student])
  Admin([Administrator])
  PO([Product Owner])
  subgraph OEP[Online Examination Portal]
    Register([Register])
    Login([Log in / log out])
    Browse([View available exams])
    Start([Read rules and start exam])
    Take([Answer MCQs and view timer])
    Save([Save or change answer])
    Submit([Submit examination])
    Result([View own result])
    ManageExam([Create and edit exams])
    ManageQ([Manage questions])
    Students([View student list])
    AdminResults([View all results])
    Accept([Review and accept release])
  end
  Student --> Register
  Student --> Login
  Student --> Browse
  Student --> Start
  Student --> Take
  Student --> Save
  Student --> Submit
  Student --> Result
  Admin --> Login
  Admin --> ManageExam
  Admin --> ManageQ
  Admin --> Students
  Admin --> AdminResults
  PO --> Accept
  Start --> Take
  Take --> Save
  Take --> Submit
  Submit --> Result
\`\`\`

## Actors and scope

| Actor | Responsibilities |
|---|---|
| Student | Register, authenticate, browse available exams, start an allowed attempt, answer and change MCQ selections, submit, view own result |
| Administrator | Authenticate, create/edit exams, manage questions, view students and inspect results |
| Product Owner | Review delivered work and accept against Jira criteria |

The in-scope question type is four-option MCQ. One attempt per student/exam is enforced. The server deadline is authoritative. Student result privacy is OEP-F-023 / TC-RES-04; administrator result visibility is OEP-F-024 / TC-RES-05.

## Export status

This editable Mermaid source is committed for review and rendering. Jira asks for a PNG export as well; the connected GitHub file operation supports text assets, not binary PNG upload. The PNG export is therefore still outstanding and is not claimed as completed.
