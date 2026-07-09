from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Etudiant
from django.contrib.auth.models import User

def preinscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        lieu_naissance = request.POST.get('lieu_naissance')
        sexe = request.POST.get('sexe')
        nationalite = request.POST.get('nationalite', 'Guinéenne')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        filiere = request.POST.get('filiere')
        niveau = request.POST.get('niveau')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Vérifier mots de passe
        if password != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'inscriptions/preinscription.html')

        # Vérifier email existant
        if Etudiant.objects.filter(email=email).exists():
            messages.error(request, 'Cet email est déjà utilisé.')
            return render(request, 'inscriptions/preinscription.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte existe déjà avec cet email.')
            return render(request, 'inscriptions/preinscription.html')

        # Créer le compte utilisateur Django
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=prenom,
            last_name=nom
        )

        # Créer l'étudiant
        etudiant = Etudiant.objects.create(
            nom=nom,
            prenom=prenom,
            date_naissance=date_naissance,
            lieu_naissance=lieu_naissance,
            sexe=sexe,
            nationalite=nationalite,
            telephone=telephone,
            email=email,
            adresse=adresse,
            filiere=filiere,
            niveau=niveau,
            annee_academique='2025-2026',
            statut='preinscrit'
        )

        messages.success(request, f'Préinscription réussie ! Votre matricule est : {etudiant.matricule}')
        return redirect('confirmation_preinscription')

    return render(request, 'inscriptions/preinscription.html')

def confirmation_preinscription(request):
    return render(request, 'inscriptions/confirmation.html')
