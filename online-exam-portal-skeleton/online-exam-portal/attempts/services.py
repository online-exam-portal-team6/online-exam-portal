"""Exam attempt services (contract B6). Owner: Bhumika."""


def start_attempt(student, exam):
    raise NotImplementedError("TODO (Bhumika, OEP-F-014)")


def save_answer(attempt, question_id, option):
    raise NotImplementedError("TODO (Bhumika, OEP-F-017)")


def submit_attempt(attempt, auto=False):
    """Idempotent. Sets SUBMITTED / AUTO_SUBMITTED, then calls results.services.evaluate_attempt(attempt)."""
    raise NotImplementedError("TODO (Bhumika, OEP-F-018/019)")
