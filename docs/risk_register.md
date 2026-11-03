# Project Risk Register

**Review cadence:** Daily during active development and before each release.  
**Register owner:** Project team. Individual risk owners are listed below.  
**Last reviewed:** 3 November 2026.

## Scoring approach

Likelihood and impact are rated from 1 (Low) to 3 (High). The overall rating is the product of the two scores: 1–2 Low, 3–4 Medium, 6–9 High. Ratings are qualitative planning assessments, not measured incident probabilities. Owners should update the status, rating, mitigation and review date during the daily review.

## Risks

| ID | Risk | Likelihood | Impact | Rating | Mitigation / response | Owner | Status |
|---|---|---:|---:|---|---|---|---|
| R-01 | Merge conflicts or integration regressions delay delivery. | 3 | 2 | High (6) | Integrate feature branches frequently, keep pull requests focused, resolve conflicts against the latest `main`, and rerun CI after conflict resolution. | Technical lead / PR author | Monitor |
| R-02 | Defects in answer evaluation produce incorrect examination results. | 2 | 3 | High (6) | Test correct, incorrect and unanswered options; verify marks, percentage and pass threshold; review evaluation logic and regression-test TC-RES-01. | Backend lead | Monitor |
| R-03 | Duplicate or inconsistent results occur when submission/evaluation is retried. | 2 | 3 | High (6) | Enforce one result per attempt at database level, use transactional idempotent persistence, and test repeated evaluation (TC-RES-03, TC-SEC-05). | Backend lead | Mitigated; verify in CI |
| R-04 | Students access another student's attempt or restricted administrative functions. | 2 | 3 | High (6) | Enforce authentication, role and object-ownership checks on the server; test forbidden and not-found cases; do not rely on hidden UI controls. | Security / backend owner | Monitor |
| R-05 | Exam deadlines are not enforced consistently, allowing late answers or missed auto-submission. | 2 | 3 | High (6) | Enforce deadlines using server-side timestamps in answer-save and submit services; test boundary conditions and automatic submission. | Backend lead | Monitor |
| R-06 | Production secrets, database settings or allowed hosts are misconfigured. | 2 | 3 | High (6) | Store secrets in environment variables, keep `DEBUG=False` in production, configure allowed hosts and production database, and verify deployment configuration before release. | Deployment owner | Monitor |
| R-07 | Database failure or accidental data loss affects exams and results. | 2 | 3 | High (6) | Establish automated backups, document restore procedures, restrict production database access, and test restoration before release. | Database / deployment owner | Monitor |
| R-08 | CI or lint failures are discovered late and block release. | 2 | 2 | Medium (4) | Run Django checks, migration checks, the full test suite and Flake8 locally and in CI for each pull request; fix failures before merge. | PR author / CI owner | Monitor |
| R-09 | Error pages expose internal exception details or fail to render during an outage. | 2 | 2 | Medium (4) | Use generic 403/404/500 templates, keep them independent of database-backed context, log diagnostics server-side, and verify production behaviour with `DEBUG=False`. | Backend owner | Monitor |
| R-10 | Required reviews or Product Owner acceptance are delayed or not recorded. | 2 | 2 | Medium (4) | Track reviewer and Product Owner approval as explicit Definition of Done items; do not close tickets based only on local test results. | Project manager | Monitor |

## Daily review procedure

At the daily project check-in, the project manager or delegated register owner should:

1. Review every open High-rated risk and any risk whose trigger has occurred.
2. Ask each named owner for changes in likelihood, impact, mitigation progress and blockers.
3. Record newly identified risks, decisions, action owners and target dates.
4. Escalate High risks that have no effective mitigation or threaten a release milestone.
5. Update this file in a reviewed pull request so the history of changes is traceable.

## Escalation triggers

- Any failed CI check on a release candidate.
- Any confirmed cross-student data exposure or privilege bypass.
- Any incorrect persisted result or duplicate result in production.
- Any missed deadline enforcement or inability to submit an active exam.
- Any failed backup restoration test or missing production backup.
- Any unresolved High risk at the planned release decision.

## Review log

| Date | Reviewer | Summary / actions |
|---|---|---|
| 2026-11-03 | Project team — initial register | Initial qualitative risks and mitigations recorded. Daily review ownership and updates remain a team activity. |

> **Important:** The review date above records creation of this register, not evidence that a daily review meeting has already occurred. Update the review log only when the review is actually performed.
