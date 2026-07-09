from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Professeur


def inscription_professeur(request):

    if request.method == 'POST':

        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        date_naissance = request.POST.get('date_naissance')
        lieu_naissance = request.POST.get('lieu_naissance')
        nationalite = request.POST.get('nationalite', 'Guinéenne')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        specialite = request.POST.get('specialite')
        grade = request.POST.get('grade')
        departement = request.POST.get('departement')
        date_recrutement = request.POST.get('date_recrutement')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')


        # Vérifier les mots de passe
        if password != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'professeurs/inscription.html')


        # Vérifier email existant
        if Professeur.objects.filter(email=email).exists():
            messages.error(request, 'Cet email est déjà utilisé.')
            return render(request, 'professeurs/inscription.html')


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte existe déjà avec cet email.')
            return render(request, 'professeurs/inscription.html')


        # Création du compte utilisateur
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=prenom,
            last_name=nom
        )


        # Création du profil professeur
        professeur = Professeur.objects.create(
            user=user,
            nom=nom,
            prenom=prenom,
            sexe=sexe,
            date_naissance=date_naissance,
            lieu_naissance=lieu_naissance,
            nationalite=nationalite,
            telephone=telephone,
            email=email,
            adresse=adresse,
            specialite=specialite,
            grade=grade,
            departement=departement,
            date_recrutement=date_recrutement
        )


        messages.success(
            request,
            f'Inscription réussie ! Votre matricule est : {professeur.matricule}'
        )

        return redirect('confirmation_professeur')


    return render(request, 'professeurs/inscription.html')


def confirmation_professeur(request):
    return render(request, 'professeurs/confirmation.html')
