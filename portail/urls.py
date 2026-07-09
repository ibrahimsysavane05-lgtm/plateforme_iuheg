from django.urls import path
from . import views


urlpatterns = [

    path(
        'login/',
        views.portail_login,
        name='portail_login'
    ),

    path(
        'accueil/',
        views.portail_accueil,
        name='portail_accueil'
    ),

    path(
        'professeur/',
        views.professeur_accueil,
        name='professeur_accueil'
    ),

    path(
        'professeur/cours/',
        views.mes_cours,
        name='mes_cours'
    ),

    path(
        'logout/',
        views.portail_logout,
        name='portail_logout'
    ),

    path(
    'professeur/cours/<int:id>/etudiants/',
    views.liste_etudiants_cours,
    name='liste_etudiants_cours'
    ),
    path(
    'jury/',
    views.jury_accueil,
    name='jury_accueil'
    ),
    path(
    'jury/valider/<int:id>/',
    views.valider_deliberation,
    name='valider_deliberation'
    ),
    path(
    'saisir-note/<int:cours_id>/<int:etudiant_id>/',
    views.saisir_note,
    name='saisir_note'
    ),

]
