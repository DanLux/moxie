from django.urls import re_path

from medspa.views import AppointmentsView
from medspa.views import ServicesView

urlpatterns = [
    re_path(r"^v1/medspas/(?P<medspa_pk>[0-9]+)/services$", ServicesView.as_view(), name="api.v1.services"),
    re_path(
        r"^v1/medspas/(?P<medspa_pk>[0-9]+)/services/(?P<pk>[0-9]+)$", ServicesView.as_view(), name="api.v1.services"
    ),
    re_path(r"^v1/medspas/(?P<medspa_pk>[0-9]+)/appointments$", AppointmentsView.as_view(), name="api.v1.appointments"),
    re_path(
        r"^v1/medspas/(?P<medspa_pk>[0-9]+)/appointments/(?P<pk>[0-9]+)$",
        AppointmentsView.as_view(),
        name="api.v1.appointments",
    ),
]
