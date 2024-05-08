from django.db import models

from medspa.models import Medspa


class Service(models.Model):
    medspa = models.ForeignKey(Medspa, related_name="services", db_index=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    duration = models.DurationField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.pk}>"

    def __str__(self):
        return f"Service {self.name} by {self.medspa}"
