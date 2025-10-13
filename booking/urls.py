"""URL configuration focused on the Django admin."""
from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from core.autocomplete import ServiceAutocomplete
from core.views import service_promocodes_api


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "admin/autocomplete/service/",
        admin.site.admin_view(ServiceAutocomplete.as_view()),
        name="service-autocomplete",
    ),
    path(
        "admin/api/services/<uuid:service_id>/promocodes/",
        service_promocodes_api,
        name="admin-service-promocodes",
    ),
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]

if settings.MEDIA_URL.startswith("/") and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
