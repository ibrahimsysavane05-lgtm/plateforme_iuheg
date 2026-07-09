from django.contrib import admin
from .models import Etudiant

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'nom', 'prenom', 'filiere', 'niveau', 'statut', 'date_inscription']
    list_filter = ['statut', 'filiere', 'niveau', 'annee_academique']
    search_fields = ['matricule', 'nom', 'prenom', 'email']
    readonly_fields = ['matricule', 'date_inscription', 'date_modification']
