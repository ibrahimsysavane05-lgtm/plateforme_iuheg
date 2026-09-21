from django.db import models
from professeurs.models import Professeur
from inscriptions.models import Etudiant

class Cours(models.Model):
    professeur = models.ForeignKey(
        Professeur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cours'
    )
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    semestre = models.CharField(max_length=20)
    filiere = models.CharField(max_length=100, blank=True, default='')
    niveau = models.CharField(max_length=20, blank=True, default='')
    credits = models.IntegerField(default=3)
    coefficient = models.FloatField(default=1)
    annee_academique = models.CharField(max_length=9, default='2025-2026')
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
