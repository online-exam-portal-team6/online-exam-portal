# Code review audit

An audit of whether every pull request (PR) to the Online Exam Portal
repository was reviewed by someone other than its author before it was merged.

| Item | Value |
| --- | --- |
| Repository | `online-exam-portal-team6/online-exam-portal` |
| PRs audited | #1–#58 (57 PRs; #27 does not exist). #59 is excluded because it was open and in review when the data was collected |
| Data collected | 2026-11-09, from the GitHub REST API (`/pulls?state=all` and `/pulls/{n}/reviews`) |
| Auditor | Vijay (with Claude Code assistance) |
| Review rule | A PR counts as **reviewed** when someone other than its author submitted an `APPROVED` review before the merge. Comments alone, bot reviews and authors' own reviews do not count. |

## 1. Summary

| Measure | Result |
| --- | ---: |
| PRs audited | 57 |
| Merged | 53 (49 into `main`, 4 into feature branches) |
| Closed without merging / still open | 3 / 1 |
| **Merged with an independent approval** | **45 of 53 (84.9%)** |
| Merged into `main` with an approval | 44 of 49 (89.8%) |
| Merged without any approval | 8: #1, #2, #3, #4, #5 (into `main`); #14, #15, #19 (stacked feature branches) |
| Merged into `main` without approval since 2026-10-29 | **0** (every PR from #6 onwards was approved) |
| Reviews requesting changes | 0 |

**Conclusion.** Not every PR had a reviewer. The five unreviewed merges into
`main` (#1–#5) are all from the project's first four days (26–29 October),
before peer review became the team's working practice. From PR #6 onwards,
every PR merged into `main` carried an approval from a teammate other than its
author. The three stacked PRs (#14, #15, #19) were merged into feature
branches. Their changes reached `main` only through PRs that were approved:
#16 (approved by Bhumika487) and #28 (approved by akashsb2005).

## 2. Unreviewed merges

| PR | Title | Author | Merged into | Notes |
| ---: | --- | --- | --- | --- |
| #1 | OEP-14: add MoSCoW prioritisation and sprint scope | VijaySuriyaP | `main` | ThejasBG was requested but did not review. A Copilot bot review failed ("insufficient remaining quota"). Documentation only. |
| #2 | OEP-79: add SRS v1.1 revision note | VijaySuriyaP | `main` | No reviewer requested. Documentation only. |
| #3 | OEP-95: document defect management process | VijaySuriyaP | `main` | No reviewer requested. Documentation only. |
| #4 | OEP-25: Create examination (OEP-F-007) | ThejasBG | `main` | Bhumika487 was requested but no review was submitted. **Application code.** |
| #5 | ci: add GitHub Actions workflow for Django tests | VijaySuriyaP | `main` | No reviewer requested. CI configuration. |
| #14 | OEP-35/64/65/...: UI and project documentation | akashsb2005 | `feature/oep-exam-attempt-flow` | Stacked. Reached `main` via #16, which was reviewed. |
| #15 | OEP-F-017: Save and update exam answers | Bhumika487 | `feature/oep-exam-attempt-flow` | Stacked. Reached `main` via #16, which was reviewed. |
| #19 | OEP-F-019: Automatically submit expired exam attempts | Bhumika487 | `feature/oep-f-018-submit-exam` | Stacked: #19 → #18 (reviewed) → `feature/oep-f-017-save-answers` → `main` via #28 (reviewed). |

#4 is the only unreviewed merge that put application code straight onto
`main`. The exam-creation code it added has since been exercised by the
automated suite (`exams/tests/test_exam_create.py`) and by later reviewed PRs
that build on it.

## 3. Review practice observations

**Who reviewed.** Every developer both authored and reviewed PRs, and no one
approved their own work.

| Reviewer | Approvals given | PRs authored |
| --- | ---: | ---: |
| ThejasBG | 24 | 19 |
| Bhumika487 | 9 | 13 |
| VijaySuriyaP | 8 | 11 |
| akashsb2005 | 4 | 15 |

ThejasBG gave more than half of all approvals (24 of 45), which concentrates
review knowledge and workload on one person.

**Review depth.**

- 46 approvals in total. None requested changes, and only 4 included a written
  summary (all by akashsb2005, using the same template text). The remaining
  approvals carry no comment. Discussion may have happened outside GitHub, but
  the review record on the PRs is thin.
- The PR was merged **less than 1 minute after approval in 29 of 45** reviewed
  merges (median 0.3 minutes). Approving and merging in one sitting is not wrong
  in itself, but it leaves little room for a second look or for a CI run on the
  final commit.
- **Limitation:** inline review comments, PR conversation comments and the
  identity of the person who pressed "merge" were not collected, because the
  unauthenticated GitHub API limit (60 requests per hour) was used up. This
  audit therefore measures formal approvals only.

**Closed without merging.** #9 (replaced by #10), #43 (duplicate of #20) and
#52 (a revert of #51 that was not needed) were closed correctly instead of
being merged.

## 4. Recommendations

1. **Enable branch protection on `main`**: require one approving review from
   someone other than the author and a passing `Lint and test` CI check before
   merging. This turns the practice the team has followed since #6 into a rule.
2. **Ask reviewers for a short written comment** on what they checked (scope,
   tests, CI result), even when approving. The written summaries on #21, #28,
   #31 and #33 are a good model.
3. **Spread reviews more evenly** across the team, so that no single reviewer
   approves most PRs.
4. **Avoid deep stacks of PRs.** Chains such as #19 → #18 → #15 → #16/#28 make
   it harder to see what was reviewed. Where stacking is needed, rebase onto
   `main` and review each PR against `main`.
5. **Retrospective review of #4** is optional. Its code is covered by the
   automated tests and has been modified by later reviewed PRs.

## 5. Full PR register

"Approval → merge" is the time from the last independent approval to the merge.

| PR | Title | Author | Base | Outcome | Approved by | Approval → merge | Audit result |
| ---: | --- | --- | --- | --- | --- | ---: | --- |
| #1 | OEP-14: add MoSCoW prioritisation and sprint scope | VijaySuriyaP | `main` | Merged 2026-10-26 | — | — | **No approval** |
| #2 | OEP-79: add SRS v1.1 revision note | VijaySuriyaP | `main` | Merged 2026-10-26 | — | — | **No approval** |
| #3 | OEP-95: document defect management process | VijaySuriyaP | `main` | Merged 2026-10-26 | — | — | **No approval** |
| #4 | OEP-25: Create examination (OEP-F-007) | ThejasBG | `main` | Merged 2026-10-27 | — | — | **No approval** |
| #5 | ci: add GitHub Actions workflow for Django tests | VijaySuriyaP | `main` | Merged 2026-10-29 | — | — | **No approval** |
| #6 | Feature/oep 23 admin student list | akashsb2005 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #7 | OEP-66: Add login and exam sequence diagrams | akashsb2005 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #8 | oep53 flake8 and tests | ThejasBG | `main` | Merged 2026-10-30 | VijaySuriyaP | < 1 min | Reviewed |
| #9 | OEP : implement dashboards login page student management exam manag... | ThejasBG | `main` | Closed, not merged | — | — | N/A (not merged) |
| #10 | Feature/oep 26 update exam | ThejasBG | `main` | Merged 2026-10-30 | VijaySuriyaP | < 1 min | Reviewed |
| #11 | Implement exam attempt start and timed exam page | Bhumika487 | `main` | Merged 2026-10-30 | VijaySuriyaP | < 1 min | Reviewed |
| #12 | OEP-51: Build student and admin result pages | akashsb2005 | `main` | Merged 2026-10-31 | ThejasBG | < 1 min | Reviewed |
| #13 | OEP-39/40: Save answers and submit timed exams | akashsb2005 | `main` | Merged 2026-10-31 | ThejasBG | < 1 min | Reviewed |
| #14 | OEP-35/64/65/68/69/71/75/99/102: UI and project documentation | akashsb2005 | `feature/oep-exam-attempt-flow` | Merged 2026-10-31 | — | — | **No approval** (stacked; reached `main` via reviewed PR) |
| #15 | OEP-F-017: Save and update exam answers | Bhumika487 | `feature/oep-exam-attempt-flow` | Merged 2026-10-31 | — | — | **No approval** (stacked; reached `main` via reviewed PR) |
| #16 | Feature/oep exam attempt flow | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 23 min | Reviewed |
| #17 | OEP-32: Add MCQ questions to exams | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 2.2 h | Reviewed |
| #18 | OEP-F-018: Submit exam and calculate score | Bhumika487 | `feature/oep-f-017-save-answers` | Merged 2026-11-01 | ThejasBG | < 1 min | Reviewed |
| #19 | OEP-F-019: Automatically submit expired exam attempts | Bhumika487 | `feature/oep-f-018-submit-exam` | Merged 2026-11-01 | — | — | **No approval** (stacked; reached `main` via reviewed PR) |
| #20 | Feature/oep 33 edit mcq | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 2.3 h | Reviewed |
| #21 | Feature/oep 34 delete mcq | ThejasBG | `main` | Merged 2026-11-02 | akashsb2005 | 104 min | Reviewed |
| #22 | OEP-35/64/65/68/69/71/75/99/102: Integrate UI and architecture docu... | akashsb2005 | `main` | Merged 2026-11-01 | ThejasBG | < 1 min | Reviewed |
| #23 | OEP-66: Add login and exam-taking sequence diagrams | akashsb2005 | `main` | Merged 2026-11-01 | ThejasBG | < 1 min | Reviewed |
| #24 | OEP-F-020/021/022: Compare answers, calculate scores, and persist r... | Bhumika487 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #25 | OEP-F-024: Administrator views completed examination results | Bhumika487 | `main` | Merged 2026-11-02 | ThejasBG | 28.8 h | Reviewed |
| #26 | OEP-F-010: Filter exams available to each student | Bhumika487 | `main` | Merged 2026-11-01 | ThejasBG | < 1 min | Reviewed |
| #28 | Feature/oep f 017 save answers | ThejasBG | `main` | Merged 2026-11-02 | akashsb2005 | 27 min | Reviewed |
| #29 | OEP-31: deactivate and reactivate exams | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 26 min | Reviewed |
| #30 | OEP-59: add CycloneDX SBOM | ThejasBG | `main` | Merged 2026-11-01 | Bhumika487 | 3 min | Reviewed |
| #31 | OEP-60: add release process and v1.0 notes | ThejasBG | `main` | Merged 2026-11-02 | akashsb2005 | 25 min | Reviewed |
| #32 | OEP-55: document ER diagram and data dictionary | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 18 min | Reviewed |
| #33 | OEP-62: document database backup and restore | ThejasBG | `main` | Merged 2026-11-02 | akashsb2005 | 28 min | Reviewed |
| #34 | OEP-100: add database CI release report section | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 8 min | Reviewed |
| #35 | OEP-103: draft AI-use reflection | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 7 min | Reviewed |
| #36 | OEP-58: prepare Render deployment | ThejasBG | `main` | Merged 2026-11-02 | Bhumika487 | 3 min | Reviewed |
| #37 | OEP-71: Add rendered screenshot usability findings | akashsb2005 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #38 | OEP-102: Add concrete AI-assisted review experience | akashsb2005 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #39 | OEP-75: Fix use-case diagram Mermaid source | akashsb2005 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #40 | OEP-64/65: Fix Mermaid rendering in architecture diagrams | akashsb2005 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #41 | OEP-42/51/71: Polish exam instructions, result states and access-de... | akashsb2005 | `main` | Merged 2026-11-02 | ThejasBG | < 1 min | Reviewed |
| #42 | OEP-99: Complete architecture and UI/UX report | akashsb2005 | `main` | Merged 2026-11-02 | VijaySuriyaP | 103 min | Reviewed |
| #43 | Feature/oep 33 edit mcq | ThejasBG | `main` | Closed, not merged | — | — | N/A (not merged) |
| #44 | Live deployment | ThejasBG | `main` | Merged 2026-11-03 | VijaySuriyaP | < 1 min | Reviewed |
| #45 | Add development seed_demo management command | Bhumika487 | `main` | Merged 2026-11-03 | ThejasBG | < 1 min | Reviewed |
| #46 | Add custom error handling pages and tests | Bhumika487 | `main` | Merged 2026-11-07 | VijaySuriyaP | 71.7 h | Reviewed |
| #47 | Add Bhumika AI-use reflection | Bhumika487 | `main` | Merged 2026-11-03 | ThejasBG | < 1 min | Reviewed |
| #48 | Add project management and backend implementation report | Bhumika487 | `main` | Merged 2026-11-03 | ThejasBG | < 1 min | Reviewed |
| #49 | Add project risk register | Bhumika487 | `main` | Merged 2026-11-03 | ThejasBG | < 1 min | Reviewed |
| #50 | Docs: sync architecture and usability evidence with merged integrat... | akashsb2005 | `main` | Merged 2026-11-04 | VijaySuriyaP | < 1 min | Reviewed |
| #51 | Docs: add diagram source exports and evidence bundle manifest | akashsb2005 | `main` | Merged 2026-11-05 | VijaySuriyaP | < 1 min | Reviewed |
| #52 | Revert "Docs: add diagram source exports and evidence bundle manifest" | VijaySuriyaP | `main` | Closed, not merged | — | — | N/A (not merged) |
| #53 | OEP-73: add template render tests | VijaySuriyaP | `main` | Merged 2026-11-09 | ThejasBG | < 1 min | Reviewed |
| #54 | OEP-80: add ethics and licensing note | VijaySuriyaP | `main` | Merged 2026-11-09 | ThejasBG | < 1 min | Reviewed |
| #55 | OEP-83: add detailed test cases | VijaySuriyaP | `main` | Merged 2026-11-09 | ThejasBG | < 1 min | Reviewed |
| #56 | Implement student profile view and edit (OEP-F-005) | Bhumika487 | `main` | Open | — | — | N/A (not merged) |
| #57 | test: add end-to-end exam flow test including timeout path (OEP-84) | VijaySuriyaP | `main` | Merged 2026-11-09 | ThejasBG | < 1 min | Reviewed |
| #58 | docs: add regression test execution log for release candidate (OEP-88) | VijaySuriyaP | `main` | Merged 2026-11-09 | ThejasBG | < 1 min | Reviewed |

## 6. How to reproduce

The repository is public, so the data can be fetched without credentials:

```bash
curl -s "https://api.github.com/repos/online-exam-portal-team6/online-exam-portal/pulls?state=all&per_page=100" > pulls.json
# for each PR number N:
curl -s "https://api.github.com/repos/online-exam-portal-team6/online-exam-portal/pulls/N/reviews?per_page=100" > rev_N.json
```

A PR is counted as reviewed when `rev_N.json` contains a review with
`"state": "APPROVED"` whose `user.login` differs from the PR author's.
