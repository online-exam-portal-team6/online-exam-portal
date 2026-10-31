# AI-use reflection — Akash

## How I used AI assistance
I used an AI assistant as a development support tool while working on the Online Examination Portal. It helped me inspect repository structure, interpret Jira acceptance criteria, plan implementation steps, draft parts of Django views and templates, brainstorm test cases, and organise technical documentation.

For result pages, assistance helped structure the student result history, individual result detail and administrator result list. For the exam workflow, it helped reason about JSON answer saving, changing selections, server-side deadlines, manual submission, automatic submission and idempotency.

## My responsibility
AI-generated suggestions are not proof that a feature works. I remain responsible for understanding the code, checking it against the approved team contract, reviewing changes, ensuring tests represent acceptance criteria, verifying behaviour and coordinating with owners of shared models and evaluation services.

## Benefits
- Faster initial understanding of modules and acceptance criteria.
- More systematic test-case brainstorming for invalid input, ownership and expired attempts.
- Clearer documentation structure and consistent terminology.
- Earlier identification of integration dependencies.

## Limitations and risks
AI can assume fields, routes or service behaviour that do not exist. Generated code may miss concurrency, authorization, accessibility or deployment concerns. I must verify model fields, run Django tests and Flake8, inspect CI and request peer review. Credentials, tokens and real student records must never be entered into AI tools.

## What I learned
The best use of AI is exploration, drafting and review while retaining engineering ownership of decisions. The final implementation must be explainable, tested, reviewed by teammates and accepted by the Product Owner.

## Personal review before submission
This is a draft based on the AI-assisted workflow used during the project. Before submitting it as my personal reflection, I should confirm that each example accurately describes my own work and add one concrete example of a suggestion I changed or rejected after checking the repository.
