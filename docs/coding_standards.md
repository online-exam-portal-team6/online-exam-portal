# Coding Standards

This document defines the coding and review standards for the Online Exam Portal (Django).

## 1. General principles

- Prefer clear, simple, readable code over clever or overly compact code.
- Follow the conventions already used in the project unless there is a good reason to change them.
- Keep changes focused; do not mix unrelated refactoring with feature work.
- Do not commit secrets, credentials, database files, generated files, or environment-specific configuration.
- Validate all input on the server. Never rely on browser-side validation or permissions alone for security.

## 2. Python and PEP 8

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Use four spaces per indentation level; do not use tabs.
- Keep lines to a reasonable length (the project Flake8 configuration is authoritative; otherwise use the PEP 8 default of 79 characters for code).
- Put imports at the top of the file, grouped in this order: standard library, third-party packages, then local application imports. Separate groups with a blank line.
- Avoid unused imports, wildcard imports, unexplained constants, and unnecessary commented-out code.
- Add docstrings to non-obvious modules, classes, and public functions. Use comments to explain why, not to repeat what the code does.
- Handle expected errors explicitly. Do not silently swallow exceptions.

## 3. Naming conventions

- Modules and packages: `lowercase_with_underscores`.
- Functions and variables: `snake_case`; use descriptive names such as `exam_deadline`, not `x` or `data1`.
- Classes and Django models: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Django model fields and URL names: descriptive `snake_case`.
- Boolean variables should read like a yes/no question, for example `is_active`, `has_submitted`, or `can_attempt`.
- Avoid ambiguous abbreviations unless they are widely understood in the project.

## 4. Django and application structure

- Keep views focused on HTTP handling and orchestration. Move reusable or complex business logic into an appropriate helper/service.
- Use Django forms or serializers and server-side validation for user input.
- Use the ORM rather than constructing SQL with string interpolation. Parameterize any unavoidable raw SQL.
- Enforce authentication and role/ownership checks on every protected server endpoint, not only by hiding links in templates.
- Use POST (with CSRF protection) for state-changing actions. Do not perform deletes, submissions, or updates through GET requests.
- Use `get_object_or_404` where a missing object should produce a 404 response.
- Avoid N+1 queries; use `select_related` or `prefetch_related` when appropriate.
- Store passwords using Django's password APIs. Never log or display passwords, session tokens, or other secrets.
- Keep settings and secrets out of source control. Production settings must use secure secret management and appropriate HTTPS, cookie, and debug settings.

## 5. Django template rules

- Put HTML templates in the app's `templates/` directory, following the existing app/template naming structure.
- Use Django template inheritance: shared page structure belongs in a base template, and pages should extend it with named blocks.
- Use `{% url %}` for named routes instead of hard-coded internal paths.
- Use `{% csrf_token %}` in every POST form.
- Escape untrusted values by default. Do not use `safe` or disable auto-escaping for user-provided content.
- Keep business logic out of templates; use views and context data to prepare what the page needs.
- Use clear, consistent indentation and semantic HTML. Labels must be associated with their form controls.
- Do not put secrets or authorization decisions in client-side code.

## 6. Tests and quality checks

- Add or update tests for every behavior change, including permission checks and invalid input.
- Test success paths, failure paths, boundary conditions, and relevant user roles.
- Tests must be repeatable and must not depend on external services or real user data.
- Before requesting review, run the project's test suite and Flake8 locally.
- CI must pass before a PR can be merged. Fix lint and test failures rather than suppressing them without justification.

Suggested checks (run from the directory containing `manage.py`):

```bash
python manage.py check
python manage.py test
flake8 .
```

If the repository defines a narrower Flake8 target or configuration, follow that configuration.

## 7. Code examples

### Example 1 — Naming and readability

Bad:
```python
def f(x):
    y = x * 60
    return y
```

Good:
```python
def minutes_to_seconds(minutes):
    seconds = minutes * 60
    return seconds
```

### Example 2 — Safe database access

Bad:
```python
# Never build SQL by interpolating user input.
query = f"SELECT * FROM questions WHERE id = {question_id}"
```

Good:
```python
question = get_object_or_404(Question, pk=question_id)
```

### Example 3 — Secure state-changing template form

Bad:
```html
<a href="/exams/submit/42/">Submit exam</a>
```

Good:
```html
<form method="post" action="{% url 'exam_submit' exam.id %}">
    {% csrf_token %}
    <button type="submit">Submit exam</button>
</form>
```

## 8. Pull request review and Definition of Done

A change is complete only when all of the following are true:

1. The implementation and documentation follow these standards.
2. Relevant tests are added or updated, and the full required test suite passes.
3. Flake8 reports no violations for the changed code (and the required CI lint job is green).
4. The PR has been reviewed and approved; requested changes are addressed.
5. CI checks pass.
6. The PR is merged into the target branch.
7. The Product Owner, Vijay, accepts the completed work.

Do not mark a ticket Done while any Definition of Done item remains outstanding.
