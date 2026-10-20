# Starter skeleton (Contract v1.0)

Pushed by Bhumika on Day 1. What is already done:

- Django project `oep` with apps `accounts`, `exams`, `questions`, `attempts`, `results`.
- Every URL name and path from the team contract (B7) is wired to a stub view that returns "TODO (owner): ...".
  Owners replace the stub BODY only. Do not rename URL names or move paths.
- Access control is already applied to each stub (`student_required` / `admin_required` from `accounts/decorators.py`).
- Service function stubs exist (`exams/services.py`, `attempts/services.py`, `results/services.py`) with the contract signatures.
- `models.py` files are empty on purpose: Thejas adds all models and migrations on Day 1 evening.
- `templates/` and `static/` are empty on purpose: Akash adds `base.html` and the placeholder pages on Day 1.
- `accounts/tests/test_skeleton_urls.py` keeps the contract URLs and role access honest. Keep it passing.

Run it:

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py test
    python manage.py runserver
