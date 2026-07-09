from django.db import models
from inscriptions.models import Etudiant

class Document(models.Model):
    TYPE_CHOICES = [
        ('identite', "Pièce d'identité"),
        ('diplome', 'Diplôme'),
        ('photo', 'Photo'),
        ('certificat', 'Certificat'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='documents')
    type_document = models.CharField(max_length=20, choices=TYPE_CHOICES)
    nom_fichier = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='documents/')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    observations = models.TextField(blank=True)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.etudiant} - {self.type_document} - {self.statut}'

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-date_upload']
