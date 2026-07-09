from django.urls import path
from . import views

urlpatterns = [
    path('preinscription/', views.preinscription, name='preinscription'),
    path('confirmation/', views.confirmation_preinscription, name='confirmation_preinscription'),
]
