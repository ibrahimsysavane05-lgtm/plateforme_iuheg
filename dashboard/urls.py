from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_admin, name='login_admin'),
    path('', views.dashboard_view, name='dashboard'),
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/<int:etudiant_id>/', views.detail_etudiant, name='detail_etudiant'),
    path('etudiants/export/', views.export_etudiants_excel, name='export_etudiants'),
    path('notes/', views.saisie_notes, name='saisie_notes'),
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    path('paiements/ajouter/', views.ajouter_paiement, name='ajouter_paiement'),
    path('paiements/historique/', views.historique_paiements, name='historique_paiements'),
    path('deliberations/', views.gestion_deliberations, name='gestion_deliberations'),
    path('deliberations/ajouter/', views.ajouter_deliberation, name='ajouter_deliberation'),
    path('cours/', views.gestion_cours, name='gestion_cours'),
    path('cours/ajouter/', views.ajouter_cours, name='ajouter_cours'),
    path('utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('utilisateurs/ajouter/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('reinscription/', views.reinscription, name='reinscription'),
    path('historique/<str:email>/', views.historique_etudiant, name='historique_etudiant'),
    path('documents/', views.gestion_documents, name='gestion_documents'),
    path('documents/<int:doc_id>/valider/', views.valider_document, name='valider_document'),
]
