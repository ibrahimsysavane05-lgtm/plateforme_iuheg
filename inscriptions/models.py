from django.db import models

class Etudiant(models.Model):
    STATUT_CHOICES = [
        ('preinscrit', 'Préinscrit'),
        ('inscrit', 'Inscrit'),
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
    ]
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    # Infos personnelles
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    nationalite = models.CharField(max_length=50, default='Guinéenne')
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    adresse = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    # Infos académiques
    matricule = models.CharField(max_length=20, unique=True, blank=True)
    filiere = models.CharField(max_length=100)
    niveau = models.CharField(max_length=20)
    annee_academique = models.CharField(max_length=9)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='preinscrit')

    # Dates
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Génération automatique du matricule
        if not self.matricule:
            super().save(*args, **kwargs)
            # Extraire l'année depuis annee_academique (ex: "2025-2026" -> "2025")
            # ou utiliser l'année courante si annee_academique est mal renseigné
            from datetime import datetime
            if self.annee_academique and len(self.annee_academique) >= 4 and self.annee_academique[:4].isdigit():
                annee = self.annee_academique[:4]
            else:
                annee = str(datetime.now().year)
            self.matricule = f'IUHEG-{annee}-{self.id:04d}'
            kwargs['force_insert'] = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.matricule} - {self.nom} {self.prenom}'

    class Meta:
        verbose_name = 'Étudiant'
        verbose_name_plural = 'Étudiants'
        ordering = ['-date_inscription']
