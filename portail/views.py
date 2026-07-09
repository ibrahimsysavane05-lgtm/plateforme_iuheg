from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from inscriptions.models import Etudiant
from professeurs.models import Professeur
from cours.models import Cours
from jury.models import Jury
from academique.models import Deliberation
from academique.models import Note
from academique.forms import NoteForm


@login_required(login_url='/portail/login/')
def jury_accueil(request):

    jury = Jury.objects.get(
        user=request.user
    )

    deliberations = Deliberation.objects.all()

    context = {
        "jury": jury,
        "deliberations": deliberations
    }

    return render(
        request,
        "portail/jury.html",
        context
    )



def portail_login(request):

    if request.method == "POST":

        matricule = request.POST.get("matricule")
        password = request.POST.get("password")


        # ==========================
        # CONNEXION JURY
        # ==========================

        try:

            jury = Jury.objects.get(
                user__username=matricule
            )

            user = authenticate(
                username=matricule,
                password=password
            )

            if user:

                login(request, user)

                return redirect(
                    "jury_accueil"
                )


        except Jury.DoesNotExist:
            pass



        # ==========================
        # CONNEXION PROFESSEUR
        # ==========================

        try:

            professeur = Professeur.objects.get(
                matricule=matricule
            )

            user = authenticate(
                username=professeur.email,
                password=password
            )

            if user:

                login(request, user)

                return redirect(
                    "professeur_accueil"
                )


        except Professeur.DoesNotExist:
            pass



        # ==========================
        # CONNEXION ETUDIANT
        # ==========================

        try:

            etudiant = Etudiant.objects.get(
                matricule=matricule
            )

            user = authenticate(
                username=etudiant.email,
                password=password
            )

            if user:

                login(request, user)

                return redirect(
                    "portail_accueil"
                )


        except Etudiant.DoesNotExist:
            pass



        messages.error(
            request,
            "Identifiant ou mot de passe incorrect"
        )


    return render(
        request,
        "portail/login.html"
    )


@login_required
def portail_accueil(request):

    etudiant = Etudiant.objects.get(
        email=request.user.email
    )

    notes = etudiant.notes.all()

    deliberations = etudiant.deliberations.filter(
        validee=True
    )

    return render(
        request,
        "portail/accueil.html",
        {
            "etudiant": etudiant,
            "notes": notes,
            "deliberations": deliberations
        }
    )


@login_required
def professeur_accueil(request):

    professeur = Professeur.objects.get(
        user=request.user
    )

    cours = Cours.objects.filter(
        professeur=professeur
    )

    return render(
        request,
        "portail/professeur.html",
        {
            "professeur": professeur,
            "cours": cours
        }
    )



@login_required
def mes_cours(request):

    professeur = Professeur.objects.get(
        user=request.user
    )

    cours = Cours.objects.filter(
        professeur=professeur
    )

    return render(
        request,
        "portail/mes_cours.html",
        {
            "professeur": professeur,
            "cours": cours
        }
    )



def portail_logout(request):

    logout(request)

    return redirect(
        "portail_login"
    )



@login_required(login_url='/portail/login/')
def liste_etudiants_cours(request, id):

    professeur = Professeur.objects.get(
        user=request.user
    )

    cours = Cours.objects.get(
        id=id,
        professeur=professeur
    )

    etudiants = cours.etudiants.all()

    context = {
        "cours": cours,
        "etudiants": etudiants
    }

    return render(
        request,
        "portail/liste_etudiants.html",
        context
    )
@login_required(login_url='/portail/login/')
def valider_deliberation(request, id):

    deliberation = Deliberation.objects.get(
        id=id
    )

    jury = Jury.objects.get(
        user=request.user
    )

    from django.utils import timezone

    deliberation.validee = True
    deliberation.jury_validateur = jury
    deliberation.date_validation = timezone.now()

    deliberation.save()

    return redirect(
        "jury_accueil"
    )
@login_required(login_url='/portail/login/')
def saisir_note(request, cours_id, etudiant_id):

    professeur = Professeur.objects.get(
        user=request.user
    )


    cours = Cours.objects.get(
        id=cours_id,
        professeur=professeur
    )


    etudiant = Etudiant.objects.get(
        id=etudiant_id
    )


    note, created = Note.objects.get_or_create(
        cours=cours,
        etudiant=etudiant,
        annee_academique="2025-2026"
    )


    if request.method == "POST":

        form = NoteForm(
            request.POST,
            instance=note
        )

        if form.is_valid():

            form.save()

            return redirect(
                "liste_etudiants_cours",
                id=cours.id
            )

    else:

        form = NoteForm(
            instance=note
        )


    return render(
        request,
        "portail/saisir_note.html",
        {
            "cours":cours,
            "etudiant":etudiant,
            "form":form
        }
    )