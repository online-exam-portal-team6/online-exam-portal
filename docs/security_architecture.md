# Security architecture

## Objectives
Protect account credentials, exam content, student answers and results. Only authenticated users access protected workflows; students access only their own attempts and results; administrators manage exams and questions; state-changing requests are CSRF-protected; server-side deadlines remain authoritative.

## Authentication and sessions
The project uses Django's built-in authentication and session framework. Passwords are stored through Django's password hashing API (set_password), not as plain text. Login uses AuthenticationForm; logout is POST-only. Production must supply DJANGO_SECRET_KEY, set DEBUG=0, configure exact DJANGO_ALLOWED_HOSTS and enforce HTTPS with secure cookies.

**Configuration warning:** development settings contain an insecure fallback secret key and DEBUG defaults to enabled. These defaults must never be used in production.

## Authorization
- student_required allows authenticated non-staff users.
- admin_required allows staff users.
- Attempt querysets scope by both attempt ID and student=request.user.
- Result detail must enforce the same owner check.
- Answer saving verifies that the question belongs to the exam attached to the attempt.
- Role checks and object ownership checks are separate controls; both are required.

## CSRF and validation
CsrfViewMiddleware is enabled. HTML POST forms include csrf_token. JSON answer requests send X-CSRFToken. JSON bodies, question IDs, option values, attempt state and deadlines are validated server-side. State-changing endpoints accept POST only. Django templates escape variables by default.

## Data integrity and exam integrity
Unique constraints protect (student, exam) attempts and (attempt, question) answers. Foreign keys preserve relationships. Transactions and row locks protect state transitions. The server stores deadline_at; browser countdown is informational. Submission is idempotent.

## Operational hardening

| Control | Current evidence | Production action |
|---|---|---|
| Password hashing | Django auth | Keep hashers and validators enabled |
| CSRF | Middleware and tokens | Do not exempt exam endpoints |
| Sessions | Django session middleware | Secure, HttpOnly and suitable SameSite cookies |
| HTTPS | Deployment-dependent | Enforce TLS |
| Secret key | Environment variable supported; dev fallback exists | Set strong secret and remove fallback |
| DEBUG | Development default enabled | Set DJANGO_DEBUG=0 |
| Allowed hosts | Environment configurable | Set exact hostnames |
| Rate limiting | Not evidenced | Add login throttling before public deployment |
| Audit events | Not evidenced for all sensitive actions | Add admin/submission audit logging |
| Backup and retention | Deployment-dependent | Define backup and recovery policy |

Security tests should cover anonymous access, wrong roles, cross-student access, CSRF, malformed JSON, invalid options, foreign-exam question IDs, expired attempts and repeated submission.
