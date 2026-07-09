from django.contrib import admin
from .models import Cours


class CoursAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'nom',
        'professeur',
        'semestre'
    )

    list_filter = (
        'semestre',
        'professeur'
    )

    search_fields = (
        'code',
        'nom'
    )

    filter_horizontal = (
        'etudiants',
    )
