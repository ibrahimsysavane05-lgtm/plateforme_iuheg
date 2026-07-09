from django.db import models
from django.contrib.auth.models import User


class Professeur(models.Model):

    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    # Liaison avec le compte utilisateur Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Informations personnelles
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=50, default='Guinéenne')
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    adresse = models.TextField()
    photo = models.ImageField(upload_to='professeurs/', blank=True, null=True)

    # Informations professionnelles
    matricule = models.CharField(max_length=20, unique=True, blank=True)
    specialite = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    departement = models.CharField(max_length=100)

    date_recrutement = models.DateField()

    def save(self, *args, **kwargs):
        # Génération automatique du matricule professeur
        if not self.matricule:
            super().save(*args, **kwargs)

            self.matricule = f'PROF-IUHEG-{self.id:04d}'

            kwargs['force_insert'] = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.matricule} - {self.nom} {self.prenom}'

    class Meta:
        verbose_name = 'Professeur'
        verbose_name_plural = 'Professeurs'
        ordering = ['nom']