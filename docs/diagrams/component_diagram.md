# Online Examination Portal — component diagram

Logical component view of the modular Django monolith. The boxes are Django apps, not separately deployed services.

\`\`\`mermaid
flowchart TB
  Browser[Student / Admin Browser]
  subgraph Django[Django Web Application]
    UI[Templates and Static UI]
    Accounts[Accounts]
    Exams[Exams]
    Questions[Questions]
    Attempts[Attempts]
    Results[Results]
    Auth[(Django Auth and Sessions)]
    DB[(Relational Database)]
  end
  Browser -->|HTTPS, HTML forms, JSON| UI
  UI --> Accounts
  UI --> Exams
  UI --> Questions
  UI --> Attempts
  UI --> Results
  Accounts -->|requires| Auth
  Exams -->|requires| Auth
  Questions -->|requires| Auth
  Attempts -->|requires| Auth
  Results -->|requires| Auth
  Exams -->|Exam repository| DB
  Questions -->|Question repository| DB
  Attempts -->|Attempt and Answer repository| DB
  Results -->|Result repository| DB
  Attempts -->|evaluate submitted attempt| Results
  Attempts -->|read exam questions| Questions
\`\`\`

## Provided and required interfaces

| Component | Provides | Requires |
|---|---|---|
| Accounts | Registration, login/logout, role guards, student routes | Django auth and session services |
| Exams | Student/admin dashboards, exam list and create/edit routes | Authenticated user and Exam persistence |
| Questions | Question list/form/delete routes | Exam identity, admin guard, Question persistence |
| Attempts | Start, timed exam, save/change answer, submit | Exam availability, Question data, Attempt persistence, result evaluation |
| Results | Student result list/detail and admin result list | Submitted attempt, evaluation, result persistence, ownership checks |
| Templates/static | Server-rendered pages and browser interactions | View context and named URLs |

Browser-to-server requests use Django sessions, CSRF-protected POST forms and JSON for answer changes. The deployment is a single Django application sharing one configured database.
