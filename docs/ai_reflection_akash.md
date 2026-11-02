# AI-use reflection — Akash

## How I used AI assistance
I used an AI assistant as a development support tool while working on the Online Examination Portal. It helped me inspect repository structure, interpret Jira acceptance criteria, plan implementation steps, draft parts of Django views and templates, brainstorm test cases, and organise technical documentation.

For result pages, assistance helped structure the student result history, individual result detail and administrator result list. For the exam workflow, it helped reason about JSON answer saving, changing selections, server-side deadlines, manual submission, automatic submission and idempotency.

## Example experience from this project
During the usability and integration review, I used AI assistance to organise a checklist for comparing the student dashboard, result-history screen and the expected attempt lifecycle. The review surfaced a mismatch in the supplied UI evidence: the student dashboard showed zero completed examinations, while the results page displayed one submitted examination. It also highlighted a result card labelled “Evaluated” even though its score and percentage were blank.

Rather than accepting a generated explanation as fact, I treated these as review findings and checked them against the actual screenshots and project implementation context. I recorded them as issues requiring verification by the relevant backend and frontend owners. This helped me distinguish a visual inconsistency from a confirmed root cause and avoid changing shared result logic without understanding its ownership and data contract.

A useful lesson from this experience was that AI is most valuable when it helps frame questions and organise evidence; the developer must still verify the evidence, trace the implementation and obtain peer review before treating a finding as resolved.

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
