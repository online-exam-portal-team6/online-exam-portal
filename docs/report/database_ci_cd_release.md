# Database, CI/CD and release management

## Database design and operation

The portal uses a relational model implemented with Django ORM. The primary
application entities are `Exam`, `Question`, `Attempt`, and `AttemptAnswer`;
examination creators and students reference Django's configured user model.
An exam owns its questions and attempts. Each attempt belongs to one student
and one exam, while each answer records one selected option for a question in
an attempt. Database uniqueness constraints prevent duplicate student/exam
attempts and duplicate answers for an attempt/question pair. Foreign-key delete
rules protect historical attempts and answers where needed.

The checked-in development configuration uses SQLite. The database file is
local and ignored by Git; it is not a source-controlled production database.
The project currently has no production database connection configured.
Schema changes are represented by Django migrations. The ER diagram and field
definitions are documented separately in `docs/er_diagram.md` and
`docs/data_dictionary.md`.

For operational resilience, database backups must be stored outside the
repository, access-controlled, encrypted, and periodically restore-tested.
SQLite backup and restore guidance is in `docs/backup_and_restore.md`; a
production database provider and its backup schedule must be confirmed during
deployment planning.

## Continuous integration

GitHub Actions runs the workflow in `.github/workflows/ci.yml` for pull
requests to `main`, pushes to `main`, and version tags. The workflow tests
Python 3.11 and 3.12, installs the project requirements and Flake8, and runs:

1. Flake8 over the Django project (excluding generated migrations and
   environment directories).
2. `python manage.py check` for Django system checks.
3. `python manage.py makemigrations --check --dry-run` to detect model changes
   without committed migrations.
4. `python manage.py test` for the application test suite.

The committed CycloneDX inventory at `docs/sbom.json` records the resolved
Python runtime dependencies used for the SBOM generation. Regenerate it when
the declared application dependencies change and review the resulting diff.

## Release management

Releases should be created only from an approved, tested commit on `main`.
Release preparation includes review of open defects, passing CI, migration
consistency, dependency inventory, and release notes. The release process and
versioned notes are maintained in `docs/release_process.md` and
`docs/releases/`.

Version tags trigger CI. A tag should not be treated as a production
deployment: the production hosting, environment configuration, secrets,
database, and rollback procedure must be set up and verified separately. The
live deployment remains an outstanding project task; therefore this section
does not claim that a production release has been deployed.
