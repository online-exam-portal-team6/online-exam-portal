# Changelog

All notable changes to the Online Exam Portal are recorded here. The project
follows [Semantic Versioning](https://semver.org/) and the format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-11-13

Initial release of the Online Exam Portal. Release notes are also available in
[`docs/releases/v1.0.md`](docs/releases/v1.0.md).

### Added

- Student registration, login, logout, and role-based access for students and
  administrators.
- Administrator dashboard, examination list, examination creation, and
  examination editing.
- Examination activation and deactivation so an examination can be withdrawn
  from students without deleting its data.
- Multiple-choice question management: add, edit, delete with confirmation,
  and per-question marks.
- Student dashboard listing examinations that are currently available, with
  resumption of an in-progress attempt.
- Timed examination attempts with a server-authoritative deadline and a
  remaining-time display.
- Answer selection and answer changes persisted per attempt and question.
- Manual examination submission and automatic submission when the deadline
  passes.
- Automatic evaluation with score, percentage, pass/fail outcome, and
  idempotent result storage.
- Student result list/detail pages with ownership checks, plus an administrator
  result list.
- Shared 403, 404, and 500 error pages.
- Demo-data seeding command for local and demonstration environments.
- Render Blueprint deployment with PostgreSQL, WhiteNoise static files, health
  endpoint, and production-safe settings.
- GitHub Actions CI running Flake8, Django system checks, migration checks, and
  the test suite on Python 3.11 and 3.12.
- Project documentation: requirements prioritisation, architecture and design,
  ER diagram and data dictionary, security architecture, backup and restore,
  release process, deployment runbook, SBOM, test execution log, and evidence.

### Security

- Passwords are stored using Django's password hashing and validated with the
  configured password validators.
- CSRF protection is enabled for state-changing requests.
- Role guards protect administrator pages, and ownership filters protect
  student attempts and results.
- Production mode enables HTTPS redirects, secure session and CSRF cookies,
  HSTS, and trusted proxy header handling.
- Secrets and database credentials are supplied through environment variables
  and are not stored in the repository.

### Known limitations

- One attempt is allowed per student and examination.
- Questions are limited to four-option multiple-choice questions.
- Password reset by email is not implemented.
- Student profile self-service updates are not implemented.
- The free Render plan is intended for demonstration only: services sleep when
  idle, the filesystem is ephemeral, and free PostgreSQL expires after 30 days.
