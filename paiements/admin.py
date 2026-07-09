from django.contrib import admin
from .models import Paiement, Recu

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['reference', 'etudiant', 'tranche', 'montant_total', 'montant_paye', 'statut', 'date_paiement']
    list_filter = ['statut', 'tranche', 'moyen_paiement']
    search_fields = ['reference', 'etudiant__nom', 'etudiant__prenom', 'etudiant__matricule']
    readonly_fields = ['reference', 'date_paiement']

@admin.register(Recu)
class RecuAdmin(admin.ModelAdmin):
    list_display = ['numero_recu', 'paiement', 'envoye_email', 'date_generation']
    list_filter = ['envoye_email']
    search_fields = ['numero_recu', 'paiement__etudiant__nom']
    readonly_fields = ['numero_recu', 'date_generation']
