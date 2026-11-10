# Test coverage report (OEP-85)

Statement and **branch** coverage of the Online Exam Portal Django application,
measured with Coverage.py against the release candidate.

| Item | Value |
| --- | --- |
| Commit measured | `main` at `4db3a21ad55408afd2a18b0de28872a225a96fd4` |
| Date | 2026-11-09 |
| Tool | Coverage.py 7.17.0 (C extension), branch measurement on |
| Environment | Windows 11, Python 3.11.9, Django 5.2.19 |
| Test suite | `python manage.py test`: 112 tests, all passing |
| Target | 70% or more |
| **Result** | **80.48% combined statement + branch coverage: target met** |

## 1. Summary

| Measure | Covered / total | Coverage | Target 70% |
| --- | ---: | ---: | --- |
| **Combined (statements + branches)**, the figure Coverage.py reports | 841 / 1045 | **80.48%** | Met |
| Statements (line coverage) | 700 / 833 | 84.03% | Met |
| Branches only | 141 / 212 (39 partial) | 66.51% | Not met on `main` alone |

With `branch = True`, Coverage.py's headline percentage counts every executed
statement and every taken branch together:
(covered lines + covered branches) / (statements + branches). That combined
figure is the one checked against the 70% target and enforced by
`fail_under = 70`. Branch-only coverage is reported separately, so the weaker
decision paths stay visible.

### Projection once OEP-84 is merged

The OEP-84 end-to-end test (`tests/test_e2e_flow.py`, PR pending) exercises the
real registration, login and logout forms. Measured against the same commit
with that test added (114 tests, all passing):

| Measure | `main` | `main` + OEP-84 E2E |
| --- | ---: | ---: |
| Combined | 80.48% | **86.22%** |
| Statements | 84.03% | 89.56% |
| Branches only | 66.51% | **73.11%** |

After OEP-84 merges, both the combined and the branch-only figures exceed 70%.

## 2. Scope

Configuration lives in `online-exam-portal-skeleton/online-exam-portal/.coveragerc`.

- **Measured:** all application code under the project: the `accounts`,
  `attempts`, `exams`, `questions` and `results` apps (models, forms, views,
  services, decorators, URL configs, management commands) and `oep/` (settings,
  URLs, health check).
- **Excluded:** `*/migrations/*` (generated), test code (`*/tests/*`,
  `tests/*`, `*/test_*.py`), `manage.py` and `oep/wsgi.py` (entry-point
  boilerplate that the test runner does not exercise).

## 3. Coverage by file

Files with no statements, and fully covered `apps.py` / `urls.py` files, are
omitted. "With OEP-84" is the combined figure after adding the E2E test.

| File | Stmts | Miss | Branches | Br. covered | Partial | Line % | Branch % | Combined % | With OEP-84 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `accounts/decorators.py` | 16 | 0 | 4 | 4 | 0 | 100.00 | 100.00 | 100.00 | 100.00 |
| `accounts/forms.py` | 36 | 22 | 8 | 0 | 0 | 38.89 | 0.00 | 31.82 | 84.09 |
| `accounts/views.py` | 54 | 26 | 14 | 4 | 0 | 51.85 | 28.57 | 47.06 | 82.35 |
| `accounts/views_admin.py` | 25 | 13 | 4 | 0 | 0 | 48.00 | 0.00 | 41.38 | 41.38 |
| `attempts/models.py` | 33 | 2 | 0 | 0 | 0 | 93.94 | n/a | 93.94 | 93.94 |
| `attempts/services.py` | 56 | 7 | 20 | 16 | 2 | 87.50 | 80.00 | 85.53 | 88.16 |
| `attempts/views.py` | 80 | 9 | 22 | 16 | 6 | 88.75 | 72.73 | 85.29 | 90.20 |
| `exams/forms.py` | 24 | 2 | 6 | 4 | 2 | 91.67 | 66.67 | 86.67 | 86.67 |
| `exams/management/commands/seed_demo.py` | 46 | 2 | 18 | 16 | 2 | 95.65 | 88.89 | 93.75 | 93.75 |
| `exams/models.py` | 33 | 2 | 14 | 13 | 1 | 93.94 | 92.86 | 93.62 | 93.62 |
| `exams/services.py` | 14 | 0 | 2 | 2 | 0 | 100.00 | 100.00 | 100.00 | 100.00 |
| `exams/views.py` | 56 | 11 | 8 | 4 | 0 | 80.36 | 50.00 | 76.56 | 76.56 |
| `oep/health.py` | 5 | 0 | 0 | 0 | 0 | 100.00 | n/a | 100.00 | 100.00 |
| `oep/settings.py` | 54 | 14 | 20 | 9 | 9 | 74.07 | 45.00 | 66.22 | 66.22 |
| `questions/forms.py` | 23 | 2 | 8 | 6 | 2 | 91.30 | 75.00 | 87.10 | 87.10 |
| `questions/models.py` | 34 | 2 | 8 | 7 | 1 | 94.12 | 87.50 | 92.86 | 92.86 |
| `questions/views.py` | 45 | 3 | 10 | 10 | 0 | 93.33 | 100.00 | 94.55 | 94.55 |
| `results/models.py` | 16 | 1 | 0 | 0 | 0 | 93.75 | n/a | 93.75 | 93.75 |
| `results/services.py` | 27 | 1 | 4 | 3 | 1 | 96.30 | 75.00 | 93.55 | 93.55 |
| `results/views.py` | 108 | 14 | 42 | 27 | 13 | 87.04 | 64.29 | 80.67 | 84.67 |
| **Total** | **833** | **133** | **212** | **141** | **39** | **84.03** | **66.51** | **80.48** | **86.22** |

## 4. Gaps and analysis

The core exam pipeline is well covered. Exam scheduling, question management,
attempt handling, evaluation and results are all at 80–100% combined. The gaps
are concentrated in three areas.

1. **Account forms and views** (`accounts/forms.py` 31.82%,
   `accounts/views.py` 47.06%). The committed tests sign in with
   `force_login`, so the registration form's validation (lines 28–59) and the
   login, registration and logout views (lines 43–65, 76–92, 102–104) are not
   run. The OEP-84 E2E test drives these real forms and lifts the two files to
   84.09% and 82.35%.
2. **Admin student management** (`accounts/views_admin.py` 41.38%). The
   student list and enable/disable toggle (lines 20–54, 62–83) have no
   committed test. They were verified for TC-STU-03 only by uncommitted
   scratch checks (see `docs/test_execution_log.md`).
3. **Environment-dependent settings** (`oep/settings.py` 66.22%). The missed
   branches are production-only paths: `DATABASE_URL`, `ALLOWED_HOSTS` and
   security settings that apply when `DEBUG` is off. A single test run cannot
   take both sides of these, so this is expected.

Smaller gaps: `exams/views.py` lines 83–101 (the exam edit view, verified for
TC-EXAM-02 only by a scratch check) and partial branches in `results/views.py`
(filter and ordering options on the admin result list).

## 5. Recommendations

1. Merge OEP-84, which raises branch-only coverage to 73.11%.
2. Commit tests for `accounts/views_admin.py` (student list and toggle) and the
   exam edit view. Committing the remaining TC scratch checks under `tests/`
   measured **89.38% combined / 76.89% branch** (128 tests, all passing).
3. Optionally add a coverage step to CI
   (`coverage run manage.py test` then `coverage report`); `fail_under = 70`
   fails the build if coverage drops below target. CI was not changed in this
   task.

## 6. How to reproduce

From `online-exam-portal-skeleton/online-exam-portal`:

```powershell
pip install coverage
python -m coverage erase
python -m coverage run manage.py test
python -m coverage report          # terminal table with missing lines
python -m coverage html            # optional: browsable report in htmlcov/
```

`.coveragerc` turns on branch coverage, applies the exclusions above and sets
`fail_under = 70`, so `coverage report` exits non-zero if combined coverage
falls below the target. The generated files (`.coverage`, `htmlcov/`) are
git-ignored.
