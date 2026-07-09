from django.db import models
from inscriptions.models import Etudiant

class Paiement(models.Model):
    STATUT_CHOICES = [
        ('a_jour', 'À jour'),
        ('retard', 'En retard'),
        ('solde', 'Soldé'),
    ]
    TRANCHE_CHOICES = [
        ('tranche1', 'Tranche 1'),
        ('tranche2', 'Tranche 2'),
        ('tranche3', 'Tranche 3'),
        ('totalite', 'Totalité'),
    ]
    MOYEN_CHOICES = [
        ('especes', 'Espèces'),
        ('orange_money', 'Orange Money'),
        ('virement', 'Virement bancaire'),
    ]

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='paiements')
    tranche = models.CharField(max_length=20, choices=TRANCHE_CHOICES)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=12, decimal_places=2)
    moyen_paiement = models.CharField(max_length=20, choices=MOYEN_CHOICES, default='especes')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_jour')
    date_paiement = models.DateTimeField(auto_now_add=True)
    date_echeance = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            super().save(*args, **kwargs)
            self.reference = f'PAY-{self.date_paiement.year}-{self.id:05d}'
            kwargs['force_insert'] = False
        super().save(*args, **kwargs)

    @property
    def reste_a_payer(self):
        if self.montant_total is None or self.montant_paye is None:
            return 0
        return self.montant_total - self.montant_paye

    def __str__(self):
        return f'{self.reference} - {self.etudiant} - {self.montant_paye} GNF'

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-date_paiement']


class Recu(models.Model):
    paiement = models.OneToOneField(Paiement, on_delete=models.CASCADE, related_name='recu')
    numero_recu = models.CharField(max_length=50, unique=True, blank=True)
    fichier_pdf = models.FileField(upload_to='recus/', blank=True, null=True)
    envoye_email = models.BooleanField(default=False)
    date_generation = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.numero_recu:
            super().save(*args, **kwargs)
            self.numero_recu = f'RECU-{self.date_generation.year}-{self.id:05d}'
            kwargs['force_insert'] = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero_recu} - {self.paiement.etudiant}'

    class Meta:
        verbose_name = 'Reçu'
        verbose_name_plural = 'Reçus'
        ordering = ['-date_generation']
