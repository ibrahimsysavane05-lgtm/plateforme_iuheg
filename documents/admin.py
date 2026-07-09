from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'type_document', 'nom_fichier', 'statut', 'date_upload']
    list_filter = ['type_document', 'statut']
    search_fields = ['etudiant__nom', 'etudiant__matricule', 'nom_fichier']
    readonly_fields = ['date_upload']
