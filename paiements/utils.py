from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

def generer_recu_pdf(paiement):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)

    bleu_iuheg = colors.HexColor('#1a3a6b')
    orange_iuheg = colors.HexColor('#e07b00')

    style_titre = ParagraphStyle('titre', fontSize=14, textColor=bleu_iuheg,
        alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=4)
    style_sous_titre = ParagraphStyle('sous_titre', fontSize=10, textColor=bleu_iuheg,
        alignment=TA_CENTER, fontName='Helvetica', spaceAfter=3)
    style_center = ParagraphStyle('center', fontSize=10, alignment=TA_CENTER, fontName='Helvetica')

    elements = []

    # ENTÊTE
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph('INSTITUT UNIVERSITAIRE DES HAUTES ÉTUDES DE GUINÉE', style_titre))
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph('Soumambossia, Conakry, République de Guinée', style_sous_titre))
    elements.append(Paragraph('Tél: +224 625 35 35 10 | Email: ramatoulaye.diallo@iuheg.education', style_sous_titre))
    elements.append(Spacer(1, 0.3*cm))
    elements.append(HRFlowable(width="100%", thickness=2, color=bleu_iuheg))
    elements.append(Spacer(1, 0.4*cm))

    # TITRE REÇU
    elements.append(Paragraph('REÇU DE PAIEMENT', ParagraphStyle('recu',
        fontSize=18, textColor=orange_iuheg, alignment=TA_CENTER,
        fontName='Helvetica-Bold', spaceAfter=6)))
    elements.append(Spacer(1, 0.2*cm))

    # NUMÉRO ET DATE
    recu = paiement.recu
    elements.append(Paragraph(f'N° {recu.numero_recu}', ParagraphStyle('num',
        fontSize=12, textColor=bleu_iuheg, alignment=TA_CENTER,
        fontName='Helvetica-Bold', spaceAfter=4)))
    elements.append(Paragraph(
        f'Date : {recu.date_generation.strftime("%d/%m/%Y à %H:%M")}', style_center))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.4*cm))

    # INFOS ÉTUDIANT
    elements.append(Paragraph("INFORMATIONS DE L'ÉTUDIANT", ParagraphStyle('section',
        fontSize=12, textColor=bleu_iuheg, fontName='Helvetica-Bold', spaceAfter=6)))

    etudiant = paiement.etudiant
    data_etudiant = [
        ['Matricule :', etudiant.matricule, 'Filière :', etudiant.filiere],
        ['Nom complet :', f'{etudiant.nom} {etudiant.prenom}', 'Niveau :', etudiant.niveau],
        ['Téléphone :', etudiant.telephone, 'Année :', etudiant.annee_academique],
    ]
    table_etudiant = Table(data_etudiant, colWidths=[3.5*cm, 6*cm, 3*cm, 5*cm])
    table_etudiant.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), bleu_iuheg),
        ('TEXTCOLOR', (2, 0), (2, -1), bleu_iuheg),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.whitesmoke, colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table_etudiant)
    elements.append(Spacer(1, 0.5*cm))

    # DÉTAILS PAIEMENT
    elements.append(Paragraph('DÉTAILS DU PAIEMENT', ParagraphStyle('section2',
        fontSize=12, textColor=bleu_iuheg, fontName='Helvetica-Bold', spaceAfter=6)))

    data_paiement = [
        ['DÉSIGNATION', 'MONTANT'],
        [f'Frais de scolarité - {paiement.get_tranche_display()}',
         f'{paiement.montant_total:,.0f} GNF'],
        ['Montant payé', f'{paiement.montant_paye:,.0f} GNF'],
        ['Reste à payer', f'{paiement.reste_a_payer:,.0f} GNF'],
        ['Moyen de paiement', paiement.get_moyen_paiement_display()],
        ['Statut', paiement.get_statut_display()],
    ]
    table_paiement = Table(data_paiement, colWidths=[12*cm, 5.5*cm])
    table_paiement.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bleu_iuheg),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.green),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 3), (-1, 3), colors.red),
    ]))
    elements.append(table_paiement)
    elements.append(Spacer(1, 1*cm))

    # SIGNATURE
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.4*cm))
    data_signature = [
        ['Signature du Caissier', '', "Cachet de l'établissement"],
        ['\n\n\n_________________', '', '_________________'],
    ]
    table_sign = Table(data_signature, colWidths=[6*cm, 5.5*cm, 6*cm])
    table_sign.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, 0), bleu_iuheg),
    ]))
    elements.append(table_sign)
    elements.append(Spacer(1, 0.5*cm))

    # PIED DE PAGE
    elements.append(HRFlowable(width="100%", thickness=2, color=bleu_iuheg))
    elements.append(Spacer(1, 0.2*cm))
    elements.append(Paragraph(
        "Ce reçu est un document officiel de l'IUHEG. Conservez-le précieusement.",
        ParagraphStyle('footer', fontSize=8, alignment=TA_CENTER,
                      textColor=colors.grey, fontName='Helvetica-Oblique')))

    doc.build(elements)
    buffer.seek(0)
    return buffer
