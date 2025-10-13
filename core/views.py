"""Minimal view helpers that remain after removing the client-facing stack."""
from __future__ import annotations

from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, JsonResponse
from django.utils import timezone

from core.models import PromoCode


@staff_member_required
def service_promocodes_api(request, service_id: str):
    """
    Return currently active promocodes for a given service.

    Used by the custom admin appointment form to pre-fill select options.
    """
    if request.method != "GET":
        raise Http404()

    today = timezone.localdate()
    qs = (
        PromoCode.objects.filter(
            applicable_services__id=service_id,
            active=True,
            start_date__lte=today,
            end_date__gte=today,
        )
        .distinct()
        .order_by("code")
    )

    payload = [
        {
            "id": str(code.pk),
            "code": code.code,
            "discount_percent": code.discount_percent,
        }
        for code in qs
    ]
    return JsonResponse(payload, safe=False)
