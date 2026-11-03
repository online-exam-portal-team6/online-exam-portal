# Error handling approach

## Goals
- Give users a clear, friendly response when a request cannot be completed.
- Preserve correct HTTP status codes.
- Never expose tracebacks, secrets, SQL, filesystem paths, or other internal details in production responses.
- Keep enough diagnostic information in server logs for maintainers to investigate failures.

## HTTP status codes
| Status | Meaning | Application behaviour |
| --- | --- | --- |
| 400 | Bad request | Reject malformed or invalid input; show form validation feedback where applicable. |
| 403 | Forbidden | The user is authenticated or the request is understood, but access is not permitted. Render `templates/403.html`. |
| 404 | Not found | The requested URL or resource does not exist. Render `templates/404.html`. |
| 500 | Internal server error | An unexpected server-side exception occurred. Render `templates/500.html` without exception details. |

## Application rules
1. Validate user input with Django forms and model validation. Return field-level errors for expected validation failures rather than raising an unhandled exception.
2. Use authentication and role/permission checks on protected views. A denied request must return 403; do not rely only on hiding navigation links.
3. Use 404 for missing resources. Avoid revealing whether a protected resource exists when that would disclose information.
4. Let unexpected exceptions reach Django's exception handling so they are logged and converted to a 500 response. Do not return exception text to the browser.
5. Use Django's normal logging configuration and deployment platform logs for diagnosis. Do not log passwords, session identifiers, tokens, or other credentials.
6. Keep `DEBUG=False` in production and configure `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and `DATABASE_URL` as documented in the deployment guide. Django's custom 404/500 templates are used when `DEBUG=False`.

## Templates and handlers
- `templates/403.html`: access-denied message and a safe link home. The existing `handler403` points to `accounts.views.error_403`.
- `templates/404.html`: not-found message and a safe link home. Django discovers this template automatically in production.
- `templates/500.html`: generic server-error message and a safe link home. Django discovers this template automatically in production.
- Keep these pages independent of application data so they can render even when a view or database operation fails.

## Verification
Run from `online-exam-portal-skeleton/online-exam-portal`:
```cmd
python manage.py check
python manage.py test
flake8 .
```
For custom 404 and 500 pages, verify with `DEBUG=False` in a production-like test configuration. A 500 response must contain only the generic message, never the exception or traceback.

## Definition of Done
- [ ] Documentation and custom 403/404/500 templates reviewed.
- [ ] Tests pass locally and in CI.
- [ ] Flake8 reports no violations.
- [ ] Pull request reviewed and merged.
- [ ] Product Owner (Vijay) accepts the work.
