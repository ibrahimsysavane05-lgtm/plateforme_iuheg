from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Paiement, Recu
from .utils import generer_recu_pdf
import os
from django.conf import settings

@staff_member_required
def generer_recu(request, paiement_id):
    paiement = get_object_or_404(Paiement, id=paiement_id)

    # Créer ou récupérer le reçu
    recu, created = Recu.objects.get_or_create(paiement=paiement)

    # Générer le PDF
    buffer = generer_recu_pdf(paiement)

    # Sauvegarder le fichier
    nom_fichier = f'recu_{recu.numero_recu}.pdf'
    chemin = os.path.join(settings.MEDIA_ROOT, 'recus', nom_fichier)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)

    with open(chemin, 'wb') as f:
        f.write(buffer.getvalue())

    recu.fichier_pdf = f'recus/{nom_fichier}'
    recu.save()

    # Retourner le PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nom_fichier}"'
    return response
