from django.db import models
from cours.models import Cours
from inscriptions.models import Etudiant
from decimal import Decimal

class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='notes')
    note_cc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note_examen = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    note_finale = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    annee_academique = models.CharField(max_length=9)
    date_saisie = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

     if self.note_cc is not None and self.note_examen is not None:

        self.note_finale = (
            (self.note_cc * Decimal("0.40")) +
            (self.note_examen * Decimal("0.60"))
        )

     super().save(*args, **kwargs)
    def a_dette(self):
        return self.note_finale is not None and self.note_finale < 10

    def __str__(self):
        return f'{self.etudiant} - {self.cours} - {self.note_finale}'

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        unique_together = ['etudiant', 'cours', 'annee_academique']

class Deliberation(models.Model):
    DECISION_CHOICES = [
        ('admis', 'Admis'),
        ('ajourne', 'Ajourné'),
        ('autorise_dettes', 'Autorisé avec dettes'),
        ('redoublement', 'Redoublement'),
    ]

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='deliberations')
    annee_academique = models.CharField(max_length=9)
    moyenne_generale = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    observations = models.TextField(blank=True)
    date_deliberation = models.DateTimeField(auto_now_add=True)

    validee = models.BooleanField(default=False)

    date_validation = models.DateTimeField(
        null=True,
        blank=True
)
    jury_validateur = models.ForeignKey(
        'jury.Jury',
         null=True,
         blank=True,
         on_delete=models.SET_NULL
)



def __str__(self):
        return f'{self.etudiant} - {self.annee_academique} - {self.decision}'

class Meta:
        verbose_name = 'Délibération'
        verbose_name_plural = 'Délibérations'
        unique_together = ['etudiant', 'annee_academique']

class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20)
    specialite = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    departement = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
