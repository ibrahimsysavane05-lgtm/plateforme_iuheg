from django.urls import path
from . import views


urlpatterns = [

    path(
        '<int:paiement_id>/recu/',
        views.generer_recu,
        name='generer_recu'
    ),

]
