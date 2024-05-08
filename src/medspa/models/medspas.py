from django.db import models


class Medspa(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField(default="", blank=True)
    phone_number = models.CharField(blank=True, null=True, max_length=32)
    email_address = models.EmailField(blank=True, null=True, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.pk}>"

    def __str__(self):
        return f"Medspa {self.name}"
