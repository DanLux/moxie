from django.db import models
from django.db.models import Sum

from medspa.models import Medspa
from medspa.models import Service


class AppointmentManager(models.Manager):
    def get_or_create(self, *args, **kwargs):
        services = kwargs.pop("services", None)
        total_duration = services and services.aggregate(Sum("duration"))["duration__sum"]
        total_price = services and services.aggregate(Sum("price"))["price__sum"]
        appointment, created = super(AppointmentManager, self).create(
            *args,
            **kwargs,
            total_duration=total_duration,
            total_price=total_price,
        )
        if created:
            ServiceAppointment.objects.bulk_create(
                ServiceAppointment(appointment=appointment, service_id=service.pk) for service in services
            )
        return appointment, created

    def create(self, *args, **kwargs):
        services = kwargs.pop("services", None)

        total_duration = services and services.aggregate(Sum("duration"))["duration__sum"]
        total_price = services and services.aggregate(Sum("price"))["price__sum"]

        appointment = super(AppointmentManager, self).create(
            *args,
            **kwargs,
            total_duration=total_duration,
            total_price=total_price,
        )
        ServiceAppointment.objects.bulk_create(
            ServiceAppointment(appointment=appointment, service_id=service.pk) for service in services
        )
        return appointment


class Appointment(models.Model):
    objects = AppointmentManager()

    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"

    STATUS = (
        (SCHEDULED, "Scheduled"),
        (COMPLETED, "Completed"),
        (CANCELED, "Canceled"),
    )

    medspa = models.ForeignKey(Medspa, related_name="appointments", db_index=True, on_delete=models.CASCADE)

    start_time = models.DateTimeField()
    total_price = models.DecimalField(decimal_places=2, max_digits=8)
    total_duration = models.DurationField()
    status = models.CharField(choices=STATUS, default=SCHEDULED, max_length=32, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.pk}>"

    def __str__(self):
        return f"Appointment {self.pk} at {self.start_time}"


class ServiceAppointment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.pk}>"

    def __str__(self):
        return f"{self.service} - {self.appointment}"
