from django.db import models
from django.contrib.auth.models import User


class Jury(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    nom = models.CharField(
        max_length=100
    )

    president = models.BooleanField(
        default=False
    )


    def __str__(self):
        return self.nom
