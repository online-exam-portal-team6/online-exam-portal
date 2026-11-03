# AI-use reflection — Bhumika

## How I used AI

I used ChatGPT as a support tool while developing and documenting the Online Exam Portal. I asked it to explain Django concepts and sprint tasks, help inspect existing project code, suggest implementation approaches, draft documentation, and identify tests and verification steps.

Examples of this support included:
- Understanding the existing Django models, views, services, and URL configuration before making changes.
- Discussing implementation and test coverage for question management, exam evaluation, result persistence, and development seed data.
- Preparing project documentation, including coding standards, error handling, and this reflection.
- Troubleshooting Git commands, pull-request conflicts, and interpreting test or CI feedback.

## What I learned

AI was useful for breaking unfamiliar tasks into smaller steps and giving me a starting point for code, tests, and documentation. It also helped me understand why particular Django patterns are used, such as database transactions, one-to-one relationships, and idempotent updates.

I learned that an AI-generated answer is a suggestion, not proof that a feature works. It can miss project-specific details, make assumptions about files or configuration, or suggest code that has not actually been run in the project.

## How I checked the work

I reviewed suggestions against the repository's existing code and requirements, and used the project checks and tests where possible. I also used GitHub pull requests to review changes and resolve integration issues. When a test, CI result, lint result, or Product Owner approval had not been verified, I treated it as outstanding rather than claiming it had passed.

For future changes, I will continue to:
- Understand the requirement and inspect existing code before accepting a proposed solution.
- Review generated code for correctness, security, maintainability, and consistency with the project.
- Run relevant automated tests and the full test suite when appropriate.
- Run Flake8 and check CI results before considering a change complete.
- Ask for human review and Product Owner acceptance where required.

## Responsible use

I remain responsible for the code and documentation submitted under my work. I do not treat AI output as a replacement for understanding, testing, code review, or team decisions. I avoid sharing passwords, private credentials, or other sensitive information in prompts, and I verify important technical claims against the project and its authoritative documentation.

## Overall reflection

AI helped me work more efficiently, especially when exploring unfamiliar code and turning broad sprint tasks into actionable steps. The most valuable part was using it interactively to ask questions, compare options, and improve my understanding. The experience also reinforced that reliable software comes from combining assistance with independent review, testing, and accountability.
