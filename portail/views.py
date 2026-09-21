from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inscriptions.models import Etudiant
from professeurs.models import Professeur
from cours.models import Cours

def portail_login(request):
    if request.method == "POST":
        matricule = request.POST.get("matricule")
        password = request.POST.get("password")
        try:
            professeur = Professeur.objects.get(matricule=matricule)
            user = authenticate(username=professeur.email, password=password)
            if user:
                login(request, user)
                return redirect("professeur_accueil")
            else:
                messages.error(request, "Mot de passe incorrect.")
                return render(request, "portail/login.html")
        except Professeur.DoesNotExist:
            pass
        try:
            etudiant = Etudiant.objects.get(matricule=matricule)
            user = authenticate(username=etudiant.email, password=password)
            if user:
                login(request, user)
                return redirect("portail_accueil")
            else:
                messages.error(request, "Mot de passe incorrect.")
                return render(request, "portail/login.html")
        except Etudiant.DoesNotExist:
            pass
        messages.error(request, "Matricule ou mot de passe incorrect.")
    return render(request, "portail/login.html")

@login_required(login_url='/portail/login/')
def portail_accueil(request):
    try:
        etudiant = Etudiant.objects.get(email=request.user.email)
        return render(request, "portail/accueil.html", {"etudiant": etudiant})
    except Etudiant.DoesNotExist:
        messages.error(request, "Profil étudiant introuvable.")
        return redirect("portail_login")

@login_required(login_url='/portail/login/')
def professeur_accueil(request):
    try:
        professeur = Professeur.objects.get(user=request.user)
    except Professeur.DoesNotExist:
        messages.error(request, "Aucun profil professeur associé. Contactez l'administration.")
        return redirect("portail_login")
    cours = Cours.objects.filter(professeur=professeur)
    return render(request, "portail/professeur.html", {
        "professeur": professeur,
        "cours": cours
    })

@login_required(login_url='/portail/login/')
def mes_cours(request):
    try:
        professeur = Professeur.objects.get(user=request.user)
    except Professeur.DoesNotExist:
        return redirect("portail_login")
    cours = Cours.objects.filter(professeur=professeur)
    return render(request, "portail/mes_cours.html", {
        "professeur": professeur,
        "cours": cours
    })

@login_required(login_url='/portail/login/')
def liste_etudiants_cours(request, id):
    try:
        professeur = Professeur.objects.get(user=request.user)
    except Professeur.DoesNotExist:
        return redirect("portail_login")
    try:
        cours = Cours.objects.get(id=id, professeur=professeur)
    except Cours.DoesNotExist:
        messages.error(request, "Cours introuvable.")
        return redirect("professeur_accueil")
    etudiants = cours.etudiants.all()
    return render(request, "portail/liste_etudiants.html", {
        "cours": cours,
        "etudiants": etudiants
    })

def portail_logout(request):
    logout(request)
    return redirect("portail_login")

@login_required(login_url='/portail/login/')
def jury_accueil(request):
    from inscriptions.models import Etudiant
    from academique.models import Note, Deliberation
    etudiants = Etudiant.objects.filter(statut='actif').order_by('nom')
    deliberations = Deliberation.objects.all().select_related('etudiant')
    return render(request, 'portail/jury.html', {
        'etudiants': etudiants,
        'deliberations': deliberations,
    })

@login_required(login_url='/portail/login/')
def valider_deliberation(request, id):
    from inscriptions.models import Etudiant
    from academique.models import Deliberation
    etudiant = Etudiant.objects.get(id=id)
    if request.method == 'POST':
        decision = request.POST.get('decision')
        observations = request.POST.get('observations', '')
        annee = request.POST.get('annee_academique', '2025-2026')
        Deliberation.objects.update_or_create(
            etudiant=etudiant,
            annee_academique=annee,
            defaults={
                'decision': decision,
                'observations': observations,
            }
        )
        messages.success(request, f'Délibération enregistrée pour {etudiant.nom} {etudiant.prenom} !')
        return redirect('jury_accueil')
    return render(request, 'portail/valider_deliberation.html', {'etudiant': etudiant})

@login_required(login_url='/portail/login/')
def saisir_note(request, cours_id, etudiant_id):
    from academique.models import Note, Cours
    from inscriptions.models import Etudiant
    cours = Cours.objects.get(id=cours_id)
    etudiant = Etudiant.objects.get(id=etudiant_id)
    if request.method == 'POST':
        note_cc = request.POST.get('note_cc')
        note_examen = request.POST.get('note_examen')
        note, _ = Note.objects.get_or_create(
            etudiant=etudiant,
            cours=cours,
            defaults={'annee_academique': cours.annee_academique}
        )
        if note_cc:
            note.note_cc = float(note_cc)
        if note_examen:
            note.note_examen = float(note_examen)
        note.save()
        messages.success(request, 'Note enregistrée !')
        return redirect('professeur_accueil')
    note = Note.objects.filter(etudiant=etudiant, cours=cours).first()
    return render(request, 'portail/saisir_note.html', {
        'cours': cours,
        'etudiant': etudiant,
        'note': note
    })
