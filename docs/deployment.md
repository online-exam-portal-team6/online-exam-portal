# Render deployment

The repository includes a Render Blueprint at `render.yaml`. It defines a
Python web service and a managed PostgreSQL database, and deploys from `main`.
The service uses the application directory as its root, collects static files,
runs migrations at startup, serves Django through Gunicorn, and exposes a
read-only `/health/` endpoint.

## Create the service

1. Push and merge the reviewed deployment branch and the application changes
   that should be included in the release.
2. Sign in to Render with an account that can access the GitHub repository.
3. Create a new Blueprint instance and select this repository's `render.yaml`.
4. Review the resources and region before confirming creation. The Blueprint
   uses Render's free web and database plans to avoid creating paid resources
   without explicit approval.
5. Wait for the service build, migration, health check, and GitHub Actions CI
   to complete. Render supplies the database URL and generated Django secret;
   do not copy secrets into the repository.
6. Create an administrator using a secure one-time management procedure
   supported by the selected Render plan. In the Render Shell, either run
   `python manage.py createsuperuser` and answer the prompts, or set
   `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and
   `DJANGO_SUPERUSER_PASSWORD` for a single command and run
   `python manage.py create_admin`. If the plan does not provide a shell, run
   the same command locally with `DATABASE_URL` set to the database's external
   connection string. Do not put administrator credentials in `render.yaml`,
   source control, or deployment logs.
7. Verify login, admin access, exam workflows, static assets, and the health
   endpoint against the live service.

## Configuration and security

Production settings require `DJANGO_SECRET_KEY`, `DATABASE_URL`, and a host
allowlist. The Blueprint obtains the database connection from Render and the
host from `RENDER_EXTERNAL_HOSTNAME`. Production mode disables debug, enables
HTTPS redirects and secure cookies, trusts the proxy's HTTPS header, and uses
WhiteNoise for collected static files. If a custom domain is added, set both
`DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` in the Render service
environment. Local development retains SQLite defaults when `DJANGO_DEBUG` is
enabled.

The free plan is suitable only for a temporary demonstration, not durable
production data: free web services sleep when idle and have ephemeral local
filesystems, while free Render Postgres expires after 30 days and does not
include backups. Before using real student data or relying on the service,
obtain approval for a suitable paid database/hosting plan, configure backups,
and verify restore procedures. Do not paste secrets into chat or commit them.
