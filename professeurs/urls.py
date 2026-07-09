from django.urls import path
from . import views


urlpatterns = [

    path(
        'inscription/',
        views.inscription_professeur,
        name='inscription_professeur'
    ),

    path(
        'confirmation/',
        views.confirmation_professeur,
        name='confirmation_professeur'
    ),

]