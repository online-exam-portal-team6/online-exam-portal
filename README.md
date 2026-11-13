# Online Exam Portal

A role-based web application for creating, conducting, and automatically evaluating multiple-choice examinations. Administrators manage examinations and questions; students attend scheduled, timed exams and review their results.

## Features

### Administrator
- Secure staff login and administrator dashboard.
- Create, update, activate, and deactivate examinations.
- Create, edit, and delete four-option multiple-choice questions.
- Manage student accounts and view examination results.

### Student
- Register and sign in to a student account.
- View examinations available during their configured availability window.
- Start a timed attempt, save and change answers, and submit manually.
- Have an expired attempt automatically submitted by the server.
- View evaluated results.
- Student profile editing is proposed separately in open PR #56 and is not part of the current `main` branch.

### Reliability and security
- Role-based access controls for administrator and student routes.
- Server-side exam deadlines and answer-submission validation.
- Django CSRF protection and password hashing.
- Idempotent result evaluation and database constraints for attempts and answers.
- Custom 403, 404, and 500 error pages.
- Automated lint, Django system, migration, and test checks in GitHub Actions.

## Technology stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript, Django templates |
| Backend | Python, Django |
| Development database | SQLite |
| Production database | PostgreSQL via `DATABASE_URL` |
| Application server | Gunicorn |
| Static files | WhiteNoise |
| CI | GitHub Actions, Flake8, Django test runner |

Supported Python versions: **3.11 and 3.12**.

## Repository layout

```text
.
├── .github/workflows/ci.yml
├── docs/                                  # SRS, design, diagrams, testing, release docs
├── online-exam-portal-skeleton/
│   └── online-exam-portal/
│       ├── accounts/
│       ├── attempts/
│       ├── exams/
│       ├── questions/
│       ├── results/
│       ├── oep/
│       ├── templates/
│       ├── static/
│       ├── manage.py
│       └── requirements.txt
├── render.yaml
└── README.md
```

## Local setup (Windows PowerShell)

Run the commands from the repository root:

```powershell
cd online-exam-portal-skeleton/online-exam-portal

# Create and activate a virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install flake8

# Create database tables
python manage.py migrate

# Create your own administrator account
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. The development configuration uses SQLite and enables Django debug mode by default. Do not use development settings or demo credentials for real student data.

### Optional demo data

For a disposable local demonstration, the project provides an idempotent `seed_demo` management command. It is development-only and refuses to run when `DEBUG=False`.

Set a unique local demo password before running it:

```powershell
$env:DEMO_USER_PASSWORD = "Choose-A-Unique-Local-Password"
python manage.py seed_demo
```

The command creates a demo administrator, three demo students, two sample exams, and twenty sample MCQs when they do not already exist. Existing accounts are not reset. Never reuse the demo password in a shared or production environment.

## Quality checks

Run from `online-exam-portal-skeleton/online-exam-portal`:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
flake8 . --max-line-length=100 --extend-ignore=E501 --exclude=migrations,venv,.venv,.git,__pycache__
```

The GitHub Actions workflow runs these quality gates for Python 3.11 and 3.12 on pull requests targeting `main`, pushes to `main`, and version tags.

## Documentation

- [Software Requirements Specification](docs/SRS/Online_Exam_Portal_SRS_v1.0.docx)
- [Software Architecture and Design](Team_6_Online_Exam_Portal_Software_Architecture_and_Design.pdf)
- [Architecture, design, and UI/UX report](docs/report/architecture_design_ui_ux.md)
- [Project management and implementation report](docs/report/project_management_implementation.md)
- [ER diagram](docs/er_diagram.md) and [data dictionary](docs/data_dictionary.md)
- [Use-case diagram](docs/diagrams/use_case_diagram.md)
- [Class diagram](docs/diagrams/class_diagram.md)
- [Component diagram](docs/diagrams/component_diagram.md)
- [Security architecture](docs/security_architecture.md)
- [Usability review](docs/usability_review.md)
- [Test cases and execution evidence](docs/test_execution_log.md)
- [Coverage report](docs/coverage_report.md)
- [Deployment guide](docs/deployment.md)
- [Release process](docs/release_process.md) and [v1.0 release notes](docs/releases/v1.0.md)
- [Evidence bundle status](docs/evidence/README.md)

## Deployment

A Render Blueprint is provided in `render.yaml`. Read [docs/deployment.md](docs/deployment.md) before deploying. Production requires a strong `DJANGO_SECRET_KEY`, `DATABASE_URL`, and an appropriate allowed-host configuration. Keep all secrets in the hosting provider's environment settings, never in source control.

The free hosting configuration is intended for a temporary demonstration only; it is not a durable production environment for real student records. Review database retention, backups, restore procedures, and hosting costs before production use.

## Team members and roles

| Name | USN | Role | Responsibilities |
|---|---|---|---|
| Bhumika Praveen Patil | PES1UG24AM352 | Backend Developer | Django backend, project coordination, GitHub management |
| Akash Shivanand Bagoji | PES1UG24AM339 | Frontend Developer + UI/UX | HTML, CSS, JavaScript, user interface |
| Thejas B G | PES1UG24AM306 | Database Developer | Database design, Django models, data management |
| Vijay Suriya P | PER1UG24AM320 | QA / Testing + Documentation | Testing, test cases, defect tracking, documentation |

## Project status

The repository's `main` branch has a passing GitHub Actions CI run on the commit recorded in [the release-readiness audit](docs/release_readiness_audit.md). A passing CI run is not a substitute for integrated browser testing, Product Owner acceptance, or live deployment verification. Consult the audit and release checklist before creating a release.
