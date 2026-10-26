# Requirements Prioritisation (MoSCoW) and Sprint Scope

| Field | Value |
|---|---|
| Project | Online Exam Portal (Jira key: OEP) |
| Owner | Vijay Suriya P (Product Owner / Business Analyst) |
| Source of truth | Team SRS, requirements OEP-F-001 to OEP-F-023 |

## 1. Purpose

This document ranks the SRS requirements using MoSCoW and confirms what is in scope for the one-week sprint.
The scope is fixed by the team contract (Part B1): **21 of 23 requirements are in scope**. OEP-F-005 and
OEP-F-009 are stretch/backlog.

## 2. MoSCoW definitions used

| Category | Meaning in this sprint |
|---|---|
| Must have | The product is unusable or the demo fails without it. Must be done and accepted before the Day 5 feature freeze. |
| Should have | Important and in scope, but a workaround exists. Done if capacity allows; first to slip to a bugfix branch after freeze. |
| Could have | Nice to have. Only attempted if everything else is Done. Moved to the backlog otherwise. |
| Won't have (this sprint) | Explicitly out of scope. Recorded so nobody builds it by accident. |

## 3. Prioritisation by feature area

Requirement IDs for areas other than F-005, F-009 and F-020 to F-023 are taken from the SRS. The "SRS IDs" column
must be filled in from the SRS before this file is merged (see section 7), because the contract only fixes the IDs
named in B1 and Part A.

| # | Feature area | SRS IDs | Owner | Priority | Reason |
|---|---|---|---|---|---|
| 1 | Student registration (creates StudentProfile) | TBC from SRS | Bhumika | Must | No students without it. |
| 2 | Login, logout, invalid-login handling | TBC from SRS | Bhumika | Must | Entry point for all roles. |
| 3 | Role-based access (admin vs student, 403) | TBC from SRS | Bhumika | Must | Security requirement; admin pages must not be open to students. |
| 4 | Admin: create and edit exams | TBC from SRS | Thejas | Must | Without exams there is nothing to take. |
| 5 | Admin: exam list and dashboard | TBC from SRS | Thejas | Should | Admin can work through the exam list; the dashboard summary is convenience. |
| 6 | Admin: add, edit, delete questions | TBC from SRS | Thejas | Must | Exams need questions with a correct option. |
| 7 | Admin: view student list | TBC from SRS | Thejas | Should | Useful for oversight; does not block the exam flow. |
| 8 | Student: view available exams (dashboard) | TBC from SRS | Thejas | Must | Students must find the exam to start it. |
| 9 | Student: start exam only when available | TBC from SRS | Bhumika | Must | Core rule; protects time-window integrity. |
| 10 | Timed exam, server-side timer, remaining time | TBC from SRS | Bhumika | Must | Core feature of a timed exam. |
| 11 | Select and change answers (saved) | TBC from SRS | Bhumika | Must | Core exam taking. |
| 12 | Manual submit | TBC from SRS | Bhumika | Must | Core flow. |
| 13 | Auto-submit when time ends | TBC from SRS | Bhumika | Must | Fairness rule; server is the authority. |
| 14 | Evaluate answers (compare with correct option) | OEP-F-020 | Vijay | Must | Automatic evaluation is the product's main value. |
| 15 | Calculate score, percentage, pass/fail | OEP-F-021 | Vijay | Must | Needed for a meaningful result. |
| 16 | Store result (idempotent) | OEP-F-022 | Vijay | Must | Result must persist and not duplicate. |
| 17 | Display result (student own result, 403 for others) | OEP-F-023 | Vijay | Must | Student must see the outcome; privacy rule. |
| 18 | Admin result list | Covered under F-023 (admin view) | Vijay | Should | Admin visibility of all results; not needed for the student journey. |
| 19 | Student profile update | OEP-F-005 | Bhumika | Could | Stretch/backlog per contract. |
| 20 | Delete or deactivate exam | OEP-F-009 | Thejas | Could | Stretch/backlog per contract. Exams can be hidden by editing the time window meanwhile. |

Rows 1 to 18 are the in-scope work (21 SRS requirements across these areas). Rows 19 and 20 are the two
stretch requirements.

## 4. Scope summary

| MoSCoW | SRS requirements | Count |
|---|---|---|
| Must have | Rows 1-4, 6, 8-17 | to be totalled once IDs are filled in |
| Should have | Rows 5, 7, 18 | to be totalled once IDs are filled in |
| In scope (Must + Should) | | **21** |
| Could have | OEP-F-005, OEP-F-009 | **2** |
| **Total SRS requirements** | | **23** |

Rule: if a Must item is at risk on Day 4, the Product Owner and Scrum Master first drop a Should item to the
backlog, then re-plan. Could items are never started before every Must item is accepted.

## 5. Won't have this sprint (out of SRS scope)

| Item | Why not now | Where recorded |
|---|---|---|
| Negative marking per exam | Contract B6 fixes "no negative marking". Handled as change request. | CR-001 in `docs/change_requests.md` (decision: backlog for Sprint 2) |
| Multiple attempts per exam | Data model enforces one attempt per (student, exam). | Backlog |
| Question types other than four-option MCQ | Contract B5 fixes exactly four options. | Backlog |
| Password reset by email | Not in SRS; no email service in the stack. | Backlog |
| Custom user model, REST API, mobile app | Not in SRS; contract fixes built-in auth and Django templates. | Not planned |

## 6. Scope confirmation

- In scope this sprint: **21 of 23 requirements** (all Must and Should items above).
- Stretch/backlog: **OEP-F-005** (student profile update) and **OEP-F-009** (delete/deactivate exam).
- Scope changes after today go through the change process: raise at stand-up, log in `docs/change_requests.md`
  with impact analysis, Bhumika records it in `docs/contract_changes.md` if the contract is affected.
- After the Day 5 evening feature freeze, only bugfix branches linked to a Jira Bug key are allowed.

## 7. Open items before this file is final

1. Fill the "SRS IDs" column from the SRS and total the Must/Should counts so they add up to 21.
2. Confirm sprint start and end dates (contract B1 leaves them blank).
3. Review the priorities with Bhumika (Scrum Master) at the Day 1 stand-up and note any disagreement here.
4. Link each requirement to its Jira key in `RTM.xlsx` ("Start RTM" story).

## 8. Definition of Done (applies to every story and to this document's follow-up work)

A story or task is **Done** only when all of these hold:

- [ ] Code merged through a pull request that has been **reviewed and approved** by the review partner
      (merge commit, not squash).
- [ ] Tests written and **passing in CI**; test method names contain the SRS test case ID.
- [ ] **flake8 clean** (max line length 120).
- [ ] Documentation updated if affected (RTM, test cases, README).
- [ ] Story **accepted by the Product Owner (Vijay Suriya P)** against its acceptance criteria in Jira.

Jira flow: To Do -> In Progress -> In Review -> Done. A ticket cannot move to Done until the Product Owner accepts it.
