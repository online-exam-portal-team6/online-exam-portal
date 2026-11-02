# AI-use reflection — Thejas

> Draft based on the AI-assisted work recorded for this project. Personalise
> this reflection and confirm it matches your own experience before submitting.

## How I used AI assistance

I used an AI coding assistant to inspect the repository and Jira acceptance
criteria, plan feature work, draft Django implementation and tests, and prepare
technical documentation. Examples include MCQ creation, editing and confirmed
deletion; examination activation controls; a CycloneDX software bill of
materials; and database, release, backup, and reporting documentation.

The assistant also helped run and interpret automated checks. The feature
branches were tested with Django's test suite, and relevant Python files were
checked with Flake8. The SBOM was generated from a clean environment containing
the application's resolved dependencies and validated as CycloneDX JSON.

## My responsibility

AI-generated work is a proposal, not proof of correctness. I remain responsible
for understanding each change, checking it against the real models and Jira
criteria, reviewing the diff, ensuring tests are meaningful, and getting peer
and Product Owner review before considering a task complete. I must not include
credentials, tokens, or real student records in prompts or commits.

## Benefits

- Faster navigation of a multi-app Django repository and its assigned issues.
- More systematic tests for role access, invalid input, object ownership, and
  state-changing requests.
- Faster first drafts of data and operational documentation.
- Dependency inventory produced in a standard CycloneDX format.

## Limitations and risks

AI may trust stale Jira statuses or assume a feature is absent without checking
the integrated branch. For example, an issue initially appeared outstanding in
Jira even though its implementation had already merged into `main`; checking
Git history prevented duplicate work. Generated documentation can also
overstate functionality, so it must be compared with the code and current
configuration. Automated tests do not replace manual review, CI, security
review, or product acceptance.

## What I learned

AI is most useful for repository exploration, drafting, and test
brainstorming—not for taking over engineering decisions. I should verify
claims against the source, preserve reviewable one-issue branches, and be
prepared to explain every committed change.

## Personal review before submission

Add a concrete example of an AI suggestion you personally changed or rejected,
and revise any wording above that does not reflect your own experience. Do not
submit this draft unchanged unless you have verified that it is accurate.
