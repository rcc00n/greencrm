"""Simplified payment helpers.

All online payment processing has been removed. The helpers below keep the old
call sites working by creating manual payment records that can be managed
inside the admin only.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from django.db import transaction

from core.models import Appointment, Payment, PaymentMethod, PaymentStatus


@dataclass
class PaymentIntentBundle:
    payment: Payment
    intent: None = None  # preserved for backwards compatibility


def ensure_payment_method(name: str = "Manual") -> PaymentMethod:
    method, _ = PaymentMethod.objects.get_or_create(name=name)
    return method


def ensure_payment_status(name: str) -> PaymentStatus:
    status, _ = PaymentStatus.objects.get_or_create(name=name)
    return status


def create_or_update_payment_intent(
    appointment: Appointment,
    *,
    amount: Optional[Decimal] = None,
    currency: Optional[str] = None,
    **_: object,
) -> PaymentIntentBundle:
    """
    Legacy-compatible helper that now records a manual payment entry.

    When called repeatedly it updates the existing manual payment instead of
    creating Stripe intents like before.
    """
    total = Decimal(amount if amount is not None else appointment.final_price or 0)
    currency = (currency or "cad").lower()
    method = ensure_payment_method("Manual")
    status = ensure_payment_status("Paid" if total > Decimal("0.00") else "Not Required")

    with transaction.atomic():
        payment, created = Payment.objects.get_or_create(
            appointment=appointment,
            method=method,
            defaults={
                "amount": total,
                "currency": currency,
                "status": "succeeded",
                "amount_received": total,
                "metadata": {"note": "Manual payment entry"},
            },
        )
        if not created:
            payment.amount = total
            payment.currency = currency
            payment.amount_received = total
            payment.status = "succeeded"
            payment.metadata = {"note": "Manual payment entry (updated)"}
            payment.save(
                update_fields=["amount", "currency", "amount_received", "status", "metadata", "updated_at"]
            )

        appointment.payment_status = status
        appointment.save(update_fields=["payment_status"])

    return PaymentIntentBundle(payment=payment)


def sync_payment_from_intent(intent_id: str) -> Payment:
    """
    Kept for compatibility; raises to make misuse explicit.
    """
    raise NotImplementedError("Online payment intents are no longer supported.")


def handle_webhook_event(event: object) -> Payment:
    """
    Kept for compatibility; raises to make misuse explicit.
    """
    raise NotImplementedError("Stripe webhooks are no longer supported.")
