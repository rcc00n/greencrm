"""Legacy task stubs kept for backwards compatibility.

The original project relied on Celery to deliver email and SMS reminders.
Those integrations have been removed, but a few call sites still import the
task functions.  The no-op implementations below keep the imports working
without performing any external side effects.
"""
from __future__ import annotations

from typing import Any, Dict


def _noop_response(label: str) -> Dict[str, Any]:
    return {"status": "disabled", "task": label}


def send_appointment_reminders(*args, **kwargs) -> Dict[str, Any]:
    return _noop_response("send_appointment_reminders")


def post_appointment_status_and_reviews(*args, **kwargs) -> Dict[str, Any]:
    return _noop_response("post_appointment_status_and_reviews")


def run_all_schedulers(*args, **kwargs) -> Dict[str, Any]:
    return _noop_response("run_all_schedulers")


def send_cancellation_email(*args, **kwargs) -> bool:
    return False
