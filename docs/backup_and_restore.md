# Database backup and restore

## Current configuration

The checked-in development settings use SQLite at
`online-exam-portal-skeleton/online-exam-portal/db.sqlite3`. The database file
is ignored by Git and must not be committed. Production database settings are
environment-specific; do not assume the development SQLite file contains
production data.

## SQLite backup

Stop application processes that write to the database, create a private backup
directory, and use SQLite's online backup API rather than copying a live
database file:

```powershell
Set-Location online-exam-portal-skeleton/online-exam-portal
New-Item -ItemType Directory -Force backups | Out-Null
python -c "import sqlite3; src=sqlite3.connect('db.sqlite3'); dst=sqlite3.connect('backups/oep.sqlite3'); src.backup(dst); dst.close(); src.close()"
```

Store backups outside the repository, restrict access, encrypt them at rest and
in transit, and apply the retention schedule approved by the team. The example
filename is illustrative; use a dated, unique filename for each backup.

## SQLite restore

Restore only after confirming the target environment and obtaining approval.
Stop the application first, preserve a copy of the current database, then
restore the selected backup:

```powershell
Set-Location online-exam-portal-skeleton/online-exam-portal
Copy-Item db.sqlite3 db.before-restore.sqlite3
python -c "import sqlite3; src=sqlite3.connect('backups/oep.sqlite3'); dst=sqlite3.connect('db.sqlite3'); src.backup(dst); dst.close(); src.close()"
python -c "import sqlite3; db=sqlite3.connect('db.sqlite3'); print(db.execute('PRAGMA integrity_check').fetchone()[0]); db.close()"
```

The integrity check must report `ok`. Run Django migrations and the test suite,
then verify login, exam availability, attempts, submissions, and results before
reopening the application. Keep the pre-restore copy until the restored data is
accepted.

## PostgreSQL (when configured)

Use the database provider's approved backup mechanism or PostgreSQL custom
format tools. Keep credentials in protected environment variables, never in
the command history, repository, or backup filename. These examples require a
separately configured connection string and PostgreSQL client tools:

```powershell
pg_dump --format=custom --no-owner --file=oep.dump $env:DATABASE_URL
pg_restore --no-owner --dbname=$env:RESTORE_DATABASE_URL oep.dump
```

Restore to a separate, isolated database first. Validate schema migrations,
row counts, representative records, and application behavior before any
production restore. Never point a restore command at production until the
target has been independently verified and the restore has explicit approval.

## Operational checks

- Record the backup time, source environment, application commit, and operator
  without recording secrets or personal data in the log.
- Periodically perform a restore drill and record the result and elapsed time.
- Include uploaded media in backups if the deployment later introduces
  user-uploaded files; no media storage location is currently configured.
