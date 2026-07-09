from django.db import models
from professeurs.models import Professeur
from inscriptions.models import Etudiant

class Cours(models.Model):

    professeur = models.ForeignKey(
        Professeur,
        on_delete=models.CASCADE,
        related_name='cours'
    )

    nom = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    semestre = models.CharField(
        max_length=20
    )
    
    etudiants = models.ManyToManyField(
    Etudiant,
    blank=True,
    related_name='cours'
)

    def __str__(self):
        return f"{self.code} - {self.nom}"


    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
