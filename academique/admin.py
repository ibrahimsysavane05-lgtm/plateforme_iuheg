from django.contrib import admin
from .models import Note, Deliberation

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'cours', 'note_cc', 'note_examen', 'note_finale', 'a_dette', 'date_saisie']
    list_filter = ['annee_academique']
    search_fields = ['etudiant__nom', 'etudiant__matricule', 'cours__nom']
    readonly_fields = ['note_finale', 'date_saisie']

@admin.register(Deliberation)
class DeliberationAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'annee_academique', 'moyenne_generale', 'decision', 'date_deliberation']
    list_filter = ['decision', 'annee_academique']
    search_fields = ['etudiant__nom', 'etudiant__matricule']
    readonly_fields = ['date_deliberation']
