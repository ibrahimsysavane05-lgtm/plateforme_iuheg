from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [

    path(
        '',
        TemplateView.as_view(template_name='accueil.html'),
        name='accueil'
    ),

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'gestion/',
        include('dashboard.urls')
    ),

    path(
        'portail/',
        include('portail.urls')
    ),

    path(
        'inscriptions/',
        include('inscriptions.urls')
    ),

    path(
        'professeurs/',
        include('professeurs.urls')
    ),

    path(
        'paiements/',
        include('paiements.urls')
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accueil.html',
            next_page='/gestion/'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/'
        ),
        name='logout'
    ),

    path(
    'documents/',
    include('documents.urls')
    ),

]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
