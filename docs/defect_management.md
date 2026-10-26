# Defect Management Process

| Field | Value |
|---|---|
| Project | Online Exam Portal (Jira key: OEP) |
| Owner | Vijay Suriya P (QA/Testing, Product Owner) |
| Applies to | All four team members, all bugs found in code, templates, tests or deployment |

## 1. Purpose

This document defines how a bug is reported, rated, fixed, verified and closed, and how bugs are handled before and
after the Day 5 feature freeze. It follows the team contract (Part B4, B8): Jira Bug issue type with severity
High/Medium/Low, bugfix branches, reviewed pull requests, and a Done status that only the Product Owner grants.

## 2. Bug workflow

Bugs use the same Jira flow as stories: **To Do, In Progress, In Review, Done**.

| Step | Status | Who | What happens |
|---|---|---|---|
| 1. Report | To Do | Anyone who finds the bug | Create a Jira issue of type **Bug** using the template in section 3. Link it to the failing test case and requirement. |
| 2. Triage | To Do | Vijay (Product Owner) | Confirm the bug is reproducible, confirm or change the severity, and set the owner (see section 6). Triage on the same day the bug is raised. |
| 3. Fix | In Progress | Module owner | Work on a branch `bugfix/OEP-31-short-slug` (OEP-31 is the Bug key). Commit as `OEP-31: summary`. Add a test whose name contains the TC ID, which fails before the fix and passes after. |
| 4. Review | In Review | Review partner | Pull request title starts with the Bug key. CI green, flake8 clean, one approval, merge with a merge commit (no squash). |
| 5. Verify | In Review | Vijay | Re-run the failing test case, then the related regression cases. Record the result in `test_execution_log.md`. |
| 6. Accept | Done | Vijay | Move to Done only if verification passes. If it fails, move back to In Progress with a comment saying what still fails. |

A bug is never moved to Done by the person who fixed it.

**Not fixing a bug:** a Low or Medium bug can be moved to the backlog only by the Product Owner, with the reason
written in a Jira comment (for example "cosmetic, deferred to Sprint 2"). High bugs cannot be deferred.

## 3. Bug report template

| Field | What to write |
|---|---|
| Summary | One line: what is wrong and where (for example "Student can open another student's result") |
| Severity | High, Medium or Low (see section 4) |
| Requirement / Test case | SRS requirement ID and TC ID, for example OEP-F-023 / TC-RES-04 |
| Module and owner | accounts, exams, questions, attempts, results, templates, CI or deployment |
| Environment | Local or deployed site, browser, branch or release tag, commit hash |
| Steps to reproduce | Numbered steps, with the test data used |
| Expected result | What the SRS or acceptance criteria say should happen |
| Actual result | What happened, including the error text or HTTP status |
| Evidence | Screenshot, log or traceback attached to the issue |
| Found by / date | Name and date |

Never put passwords, secret keys or api keys or real student data in a bug report.

## 4. Severity rules

| Severity | Definition | Examples in this project | Target |
|---|---|---|---|
| **High** | A core flow is blocked, a result is wrong, data is lost, or there is a security or access-control failure. No workaround. | Login fails for valid users; student cannot submit; auto-submit does not happen; score or pass/fail is wrong; student can open another student's result or `/manage/`; a 500 error on login, answer or submit; submitted answers are lost | Fix and verify before the next integration checkpoint. Blocks the release tag. |
| **Medium** | A feature works only partly, or there is a workaround, and no data or security impact. | Wrong or missing validation message; admin result list shows wrong columns; timer display drifts but the server still submits on time; a 500 error on a rarely used page | Fix and verify before the release candidate (Day 6). |
| **Low** | Cosmetic or wording issue with no effect on behaviour. | Typo, alignment, colour, button label | Fix if time allows, otherwise backlog with a reason. |

Rules for rating:
- If in doubt between two levels, rate the higher one and let triage lower it.
- Any 500 error found by the fuzz test (`tests/fuzz_inputs.py`) is at least Medium.
- Any failure in the security validation checks (access control, another student's result, CSRF, SQL-injection style
  input, re-submitting a finished exam) is High.

## 5. Rules by sprint phase

| When | Rule |
|---|---|
| Day 1 to Day 4 | Bugs found while building are fixed on the feature branch of the same story if it is not yet merged. Once merged, raise a Bug. |
| Day 4 to Day 5 | Manual test execution starts; every failure becomes a Bug with severity. |
| After the Day 5 evening feature freeze | Only `bugfix/OEP-nn-...` branches with a Jira Bug key. No new features. |
| Day 6 (regression, release candidate) | Re-run all test cases. **No High bug may remain open.** Open Medium bugs need a Product Owner decision recorded in Jira. This supports SRS exit criteria OEP-EXIT-002 and OEP-EXIT-003. |
| Day 7 (patch) | If a bug is found after the v1.0 tag, fix it through a bugfix branch and release patch v1.0.1 (Thejas tags it). Vijay verifies the patch. |

## 6. Who owns bugs

The bug goes to the owner of the file where the cause is (contract B3). If the cause is unclear, Bhumika (Scrum
Master) assigns it at stand-up.

| Area | Owner |
|---|---|
| accounts, attempts, settings, urls | Bhumika |
| templates, static (HTML, CSS, JS) | Akash |
| models, migrations, exams, questions, CI, deployment | Thejas |
| results, cross-cutting tests, docs | Vijay |

## 7. Traceability and reporting

- Every Bug links to a test case ID and a requirement ID. The Bug key is written in the failing row of
  `test_execution_log.md`.
- When a bug is closed, the RTM status of the affected requirement is updated.
- `test_execution_log.md` and the final report include a defect summary: bugs raised, by severity, and how many are
  open, fixed and deferred.

## 8. Definition of Done

- [ ] Reviewed pull request merged (merge commit, not squash)
- [ ] Tests passing in CI
- [ ] flake8 clean
- [ ] Accepted by the Product Owner (Vijay Suriya P) in Jira
