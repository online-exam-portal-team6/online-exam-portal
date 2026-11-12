# Release-readiness audit

**Audit date:** 2026-11-12  
**Repository:** `online-exam-portal-team6/online-exam-portal`  
**Audited branch:** `main`  
**Audited commit:** `f5b0c7c61d451dbaaff839c93a841d1938a9cd6e`

This document records the repository and GitHub state observed during the release-readiness review. It distinguishes automated checks from activities that still require human or live-environment verification.

## 1. Repository and CI state

- The default branch is `main`; branch protection is enabled.
- The audited `main` commit is `f5b0c7c` (merge of PR #60, code-review audit).
- GitHub Actions run [42763011234](https://github.com/online-exam-portal-team6/online-exam-portal/actions/runs/42763011234) completed successfully.
- Both matrix jobs passed: Python 3.11 and Python 3.12.
- In both jobs, dependency installation, Flake8, Django system checks, migration checks, and the Django test command completed successfully.

A green workflow confirms the configured automated checks passed for that commit. It does not establish browser-level usability, live deployment health, or Product Owner acceptance.

## 2. Pull request state

At the time of this audit, one pull request was open:

| PR | Scope | Head commit | CI | Review state |
|---|---|---|---|---|
| [#56 — Student profile view and edit (OEP-F-005)](https://github.com/online-exam-portal-team6/online-exam-portal/pull/56) | Student profile view/edit, validation, access-control tests | `dbbba175f042e826a71d94d876bafaab1a80a323` | Python 3.11 and 3.12 passed | No submitted reviews; PR remains open |

PR #56 is authored by a teammate and is intentionally left open for team review. The earlier regression log classifies student profile editing as a stretch/backlog feature outside the stated v1.0 scope. Do not merge it solely to close the PR; confirm scope and obtain an independent review/approval first.

PR [#57 — OEP-84 end-to-end exam flow](https://github.com/online-exam-portal-team6/online-exam-portal/pull/57) was merged into `main` on 2026-11-09. Its exam-flow and timeout tests are present in the audited main tree.

## 3. Documentation and evidence observations

- The repository contains the SRS, architecture/design report, ER diagram, data dictionary, editable class/component diagrams, use-case diagram, security notes, risk register, test cases, test execution log, coverage report, release notes, and deployment instructions.
- The regression log and coverage report contain measurements against the earlier release-candidate commit `4db3a21`. They are historical measurements, not a fresh coverage run against `f5b0c7c`.
- The earlier coverage report's OEP-84 section was a projection measured with the E2E tests added to its then-current baseline. OEP-84 is now merged; do not present that projection as a newly measured coverage result for the audited `main` commit.
- The companion evidence archive was inspected in the ChatGPT Library. It contains eight usability PNG captures, class/component diagram PNG and SVG exports, and DOT sources. The binary screenshots and exports are not currently present in the repository tree; `docs/evidence/README.md` records this distinction.

## 4. Remaining release gates

| Gate | Current evidence | Required next action |
|---|---|---|
| Automated CI | Passing on audited `main` commit for Python 3.11 and 3.12 | Recheck after any new merge |
| Open PR review | PR #56 has passing CI but no review | Confirm whether OEP-F-005 is in scope; request independent review if retained |
| Browser-level verification | Automated Django tests exist; CI does not run a real browser | Verify admin/student flows, responsive layouts, timer display, and result states in a browser |
| Evidence binaries | Companion archive exists outside the Git repository | Decide with the team whether to commit the required image exports/screenshots |
| Coverage freshness | Historical report only | Re-run Coverage.py against the final release candidate before quoting current coverage |
| Deployment | Render configuration and deployment guide exist | Verify the actual live service, health endpoint, authentication, static files, and full exam lifecycle |
| Product Owner acceptance | Not established by CI | Obtain explicit acceptance from the Product Owner |
| Release tag | No release tag was observed during this audit | Create `v1.0` only after scope, review, CI, deployment, and sign-off gates are satisfied |

## 5. Release decision

**Status: not yet approved for final release.**

The current `main` branch is green under the configured CI workflow, and the core examination lifecycle has extensive automated coverage. The remaining blockers are release governance and evidence: the open profile PR needs a scope decision and independent review, browser/deployment checks need recorded evidence, coverage should be refreshed if a current percentage is required, and Product Owner acceptance must be obtained.

No teammate branch or pull request was merged, closed, or rewritten as part of this audit.
