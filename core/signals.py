"""Minimal signal hooks required for the admin-only deployment."""
from __future__ import annotations

from django.apps import apps
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save


DEFAULT_PAYMENT_STATUSES = ("Not Paid", "Pending", "Paid", "Failed")
DEFAULT_PAYMENT_METHODS = ("Manual", "Cash")


def ensure_payment_statuses(sender, **kwargs):
    """Populate essential payment metadata records when migrations run."""
    PaymentStatus = apps.get_model("core", "PaymentStatus")
    PaymentMethod = apps.get_model("core", "PaymentMethod")

    with transaction.atomic():
        for name in DEFAULT_PAYMENT_STATUSES:
            PaymentStatus.objects.get_or_create(name=name)

    with transaction.atomic():
        for name in DEFAULT_PAYMENT_METHODS:
            PaymentMethod.objects.get_or_create(name=name)


def ensure_user_profile(sender, instance, created, **kwargs):
    """Automatically create a matching UserProfile for every auth user."""
    if not created:
        return

    UserProfile = apps.get_model("core", "UserProfile")
    UserProfile.objects.get_or_create(user=instance)


post_save.connect(ensure_user_profile, sender=get_user_model())
