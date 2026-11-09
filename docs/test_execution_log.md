# Regression test execution log (OEP-88)

Regression re-run of every test case in `test_cases.xlsx` (OEP-83) against the
release candidate.

| Item | Value |
| --- | --- |
| Release candidate | `main` at `4db3a21ad55408afd2a18b0de28872a225a96fd4` (Merge PR #46, error-handling-pages) |
| Release tag | None yet; `v1.0` is to be created from this commit per `docs/release_process.md` |
| Execution date | 2026-11-09 |
| Tester | Vijay (executed with Claude Code assistance) |
| Environment | Windows 11, Python 3.11.9, Django 5.2.19; clean detached worktree of `origin/main` (no local changes) |
| Test data | Django's throwaway in-memory test database; synthetic users only, passwords generated at runtime |
| Overall outcome | **Pass**: 23 Pass, 0 Fail, 1 Not executed (stretch feature not implemented) |

## 1. CI quality gates

The same commands as `.github/workflows/ci.yml`, run from
`online-exam-portal-skeleton/online-exam-portal`.

| Gate | Command | Result |
| --- | --- | --- |
| Flake8 | `flake8 . --max-line-length=100 --extend-ignore=E501 --exclude=migrations,venv,.venv,.git,__pycache__` | Pass (no findings) |
| Django system check | `python manage.py check` | Pass ("System check identified no issues (0 silenced).") |
| Migration check | `python manage.py makemigrations --check --dry-run` | Pass ("No changes detected") |
| Django test suite | `python manage.py test -v 2` | Pass: **112 tests, OK** (243 s) |

## 2. Supplementary checks

Some test cases are not fully covered by a committed test. For those, the
Django test-client checks used during the OEP-83 execution were re-run against
the release candidate. They are kept outside the repository as scratch modules
(`tc_checks.py`, `tc_stu02.py`). The OEP-84 end-to-end test
(`tests/test_e2e_flow.py`, not yet merged into `main`) was run against the
release-candidate code in the same way.

| Run | Command | Result |
| --- | --- | --- |
| Test-case checks + E2E flow | `PYTHONPATH=<scratch> python manage.py test tc_checks rc_e2e_flow -v 2` | Pass: **16 tests, OK** |
| TC-STU-02 profile probe | `PYTHONPATH=<scratch> python manage.py test tc_stu02 -v 2` | Probe ran OK; feature absent (see TC-STU-02) |

E2E results on the release candidate:
`test_full_exam_flow_from_creation_to_result` passed, and
`test_timeout_path_auto_submits_expired_attempt` passed.

## 3. Test case results

| TC ID | Jira | Title | Evidence (tests executed) | Status |
| --- | --- | --- | --- | --- |
| TC-AUTH-01 | OEP-16 | Valid login redirects to role dashboard | `tc_checks`: `test_TC_AUTH_01_student_valid_login_lands_on_student_dashboard`, `test_TC_AUTH_01_staff_valid_login_lands_on_admin_dashboard`; E2E flow | Pass |
| TC-AUTH-02 | OEP-17 | Invalid login is rejected | `tc_checks`: `test_TC_AUTH_02_wrong_password_is_rejected_without_session` | Pass |
| TC-AUTH-03 | OEP-18 | Role-based access protects admin area | `accounts/tests/test_skeleton_urls.py`: `test_student_cannot_open_admin_pages`, `test_admin_cannot_open_student_pages`, `test_correct_role_reaches_stub` | Pass |
| TC-STU-01 | OEP-20 | Valid student registration | `tc_checks`: `test_TC_STU_01_valid_registration_creates_student_account`; E2E flow | Pass |
| TC-STU-02 | OEP-24 | Student updates profile (stretch) | `tc_stu02` probe: `/student/` 200 with no profile link; `/profile/`, `/accounts/profile/`, `/student/profile/`, `/accounts/profile/edit/` all 404; no URL route contains "profile" | Not executed |
| TC-STU-03 | OEP-22 | Admin manages student accounts | `tc_checks`: `test_TC_STU_03_staff_sees_student_list_with_profile_data`, `test_TC_STU_03_staff_can_disable_and_enable_student`, `test_TC_STU_03_non_staff_access_is_denied` | Pass |
| TC-EXAM-01 | OEP-25 | Admin creates a valid exam | `exams/tests/test_exam_create.py`: `test_TC_EXAM_01_valid_details_create_exam`; E2E flow | Pass |
| TC-EXAM-02 | OEP-26 | Admin updates a future exam | `tc_checks`: `test_TC_EXAM_02_staff_updates_future_exam_and_changes_persist` | Pass |
| TC-EXAM-03 | OEP-31 | Admin deactivates an exam (stretch) | `exams/tests/test_exam_toggle.py`: `test_admin_can_deactivate_exam_and_hide_it_from_students` | Pass |
| TC-EXAM-04 | OEP-27 | Dashboard lists only available exams | `exams/tests/test_available_exams.py`: `test_TC_EXAM_04_*` | Pass |
| TC-EXAM-05 | OEP-36 | Student starts an exam only once | `attempts/tests/test_start_attempt.py`: `test_TC_ATT_01_student_can_start_available_exam`, `test_TC_ATT_01_repeated_start_returns_same_in_progress_attempt`; E2E flow (retake blocked) | Pass |
| TC-EXAM-06 | OEP-37 | Question page renders questions and options | `tc_checks`: `test_TC_EXAM_06_question_options_timer_and_controls_render` | Pass |
| TC-EXAM-07 | OEP-38 | Timer reflects server remaining time | `attempts/tests/test_exam_take.py`: `test_TC_ATT_02_student_sees_exam_questions_and_remaining_time`, `test_TC_ATT_03_expired_attempt_has_zero_remaining_time`; E2E timeout path | Pass |
| TC-EXAM-08 | OEP-39 | Student changes a saved answer | `attempts/tests/test_answer_submission.py`: `test_TC_EXAM_08_student_can_change_saved_option`; E2E flow | Pass |
| TC-EXAM-09 | OEP-40 | Student manually submits | `attempts/tests/test_answer_submission.py`: `test_TC_EXAM_09_manual_submission_records_attempt_and_evaluates`; E2E flow | Pass |
| TC-EXAM-10 | OEP-41 | Expired attempt is auto-submitted | `attempts/tests/test_auto_submit.py`: `test_expired_attempt_is_auto_submitted_through_endpoint`; E2E timeout path (late answer rejected with 403, single result) | Pass |
| TC-QUES-01 | OEP-32 | Admin adds a four-option MCQ | `questions/tests/test_question_create.py`: `test_TC_QUES_01_admin_can_create_four_option_mcq`; E2E flow | Pass |
| TC-QUES-02 | OEP-33 | Admin edits a question | `questions/tests/test_question_edit.py`: `test_TC_QUES_02_admin_can_update_question` | Pass |
| TC-QUES-03 | OEP-34 | Admin deletes a question | `questions/tests/test_question_delete.py`: `test_TC_QUES_03_post_confirmation_deletes_question` | Pass |
| TC-RES-01 | OEP-46 | Evaluation compares with correct options | `results/tests/test_evaluation.py`: `test_TC_RES_01_answers_are_compared_with_stored_correct_options` | Pass |
| TC-RES-02 | OEP-47 | Score, percentage and pass threshold | `results/tests/test_evaluation.py`: `test_TC_RES_02_score_percentage_and_pass_are_calculated_by_marks`, `test_TC_RES_02_student_passes_at_configured_threshold` | Pass |
| TC-RES-03 | OEP-48 | Result stored idempotently | `results/tests/test_evaluation.py`: `test_TC_RES_03_evaluated_result_is_persisted`, `test_TC_RES_03_re_evaluation_updates_instead_of_duplicating`; E2E timeout path (repeat submit, one result) | Pass |
| TC-RES-04 | OEP-49 | Result display and ownership | `tc_checks`: `test_TC_RES_04_stored_result_matches_expected`, `..._owner_sees_correct_result`, `..._other_student_is_denied`, `..._staff_can_view_result`, `..._anonymous_is_redirected_to_login` | Pass |
| TC-RES-05 | OEP-50 | Admin result list | `results/tests/test_admin_results_integration.py`: `test_TC_RES_05_admin_sees_completed_result_data`, `test_TC_RES_05_student_is_forbidden_from_admin_results`; E2E flow (result register) | Pass |

## 4. Comparison with previous execution

Compared with the OEP-83 execution on 2026-11-09, there are no regressions.
Every case keeps its previous status. The committed suite grew from 112 tests
to 114 once OEP-84 merges. That merge was not needed here, because its E2E
test was run separately against the release candidate.

## 5. Defects and observations

- **No new defects raised.**
- **TC-STU-02** stays *Not executed*. The student profile feature (OEP-F-005,
  stretch/backlog) is not implemented, so this is out of v1.0 scope and not a
  failure.
- **Coverage gap:** TC-AUTH-01, TC-AUTH-02, TC-STU-01, TC-STU-03, TC-EXAM-02,
  TC-EXAM-06 and TC-RES-04 rely partly or fully on scratch checks that are not
  committed. Several are now also covered by the OEP-84 E2E test once it is
  merged. Committing the remaining checks under `tests/` would let CI enforce
  them.
- **Not covered by automation:** the JavaScript countdown display in a real
  browser (TC-EXAM-06/07). Only the server-rendered HTML and the server-side
  deadline were verified.
- A harmless `UserWarning: No directory at: .../staticfiles/` appears during
  test runs because `collectstatic` was not run locally.

## 6. Sign-off

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Tester | Vijay | Regression passed; release candidate recommended for `v1.0` | 2026-11-09 |
| Product Owner | Vijay | _Pending acceptance on PR review_ | |
