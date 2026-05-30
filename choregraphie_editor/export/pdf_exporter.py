# -*- coding: utf-8 -*-
"""
Générateur de PDF pour les projets chorégraphiques.

Équivalent de la logique de génération PDF de Form1.vb (btnGeneratePdf_Click)
qui utilisait iTextSharp dans le projet VB.NET original.

Ici on utilise ReportLab, bibliothèque Python multiplateforme.

Formats supportés :
  - A4 Portrait / A4 Paysage
  - A3 Portrait / A3 Paysage

Structure du PDF généré :
  1. Page de garde : titre, club, intrigue, durée, catégorie, participants
  2. Une page (ou plus) par phrase d'armes avec le tableau des actions
"""

from reportlab.lib.pagesizes import A4, A3, landscape, portrait
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.flowables import Flowable

from models.projet_choregraphique import ProjetChoregraphique
from models.phrase_darmes import PhraseDArmes
from models.action import Action
from models.combattant import Combattant


# ---------------------------------------------------------------------------
# Palette de couleurs 
# ---------------------------------------------------------------------------
COULEUR_TITRE       = colors.HexColor("#1a1a1a")   # Presque noir pour le texte
COULEUR_EN_TETE     = colors.HexColor("#4a90d9")   # Bleu Laser
COULEUR_EN_TETE_TXT = colors.white
COULEUR_LIGNE_PAIRE = colors.HexColor("#f8f9fa")   # Très léger gris
COULEUR_LIGNE_IMPR  = colors.white
COULEUR_BORD        = colors.HexColor("#4a90d9")   # Bordures bleues type "lame"
COULEUR_SOUS_TITRE  = colors.HexColor("#5a6a7a")
COULEUR_SEPARATEUR  = colors.HexColor("#4a90d9")


class PdfExporter:
    """
    Génère un fichier PDF à partir d'un ProjetChoregraphique.

    Méthode principale : PdfExporter.generate(projet, chemin_pdf, format_page)
    """

    @classmethod
    def generate(
        cls,
        projet: ProjetChoregraphique,
        output_path: str,
        page_size_str: str = "A4 Paysage",
    ) -> None:
        """
        Génère le PDF complet du projet chorégraphique.

        Paramètres
        ----------
        projet : ProjetChoregraphique
            Le projet à exporter.
        output_path : str
            Chemin complet du fichier PDF de destination.
        page_size_str : str
            Format de page : "A4 Paysage", "A4 Portrait", "A3 Paysage", "A3 Portrait".
        """
        # Déterminer le format de page
        page_size = cls._resolve_page_size(page_size_str)

        # Marges du document
        margin_h = 1.2 * cm
        margin_v = 1.8 * cm

        # Créer le document ReportLab
        doc = SimpleDocTemplate(
            output_path,
            pagesize=page_size,
            leftMargin=margin_h,
            rightMargin=margin_h,
            topMargin=margin_v,
            bottomMargin=margin_v,
            title=projet.titre or "Chorégraphie",
            author="Éditeur Chorégraphique ASL-FFE v2",
        )

        # Définir les styles de paragraphes
        styles = cls._build_styles()

        # Construire le contenu (flowables ReportLab)
        story = []
        story += cls._build_cover_page(projet, styles, page_size)

        # Une section par phrase d'armes
        for phrase in sorted(projet.choregraphie_sections, key=lambda p: p.numero):
            story.append(PageBreak())
            story += cls._build_phrase_section(phrase, projet, styles, page_size)

        # Générer le PDF
        doc.build(
            story,
            onFirstPage=cls._make_page_decorator(projet),
            onLaterPages=cls._make_page_decorator(projet),
        )

    # =========================================================================
    # PAGE DE GARDE
    # =========================================================================

    @classmethod
    def _build_cover_page(cls, projet, styles, page_size) -> list:
        """Construit la page de garde du PDF."""
        story = []
        page_width = page_size[0]

        # Titre principal
        story.append(Spacer(1, 0.2 * cm))
        story.append(Paragraph(
            projet.titre or "Chorégraphie sans titre",
            styles["titre_principal"]
        ))

        # Ajouter un petit espace entre le titre et le sous-titre
        story.append(Spacer(1, 0.3 * cm))


        # Sous-titre : Club
        if projet.nom_du_club:
            story.append(Paragraph(projet.nom_du_club, styles["sous_titre"]))

        story.append(HRFlowable(
            width="100%", thickness=2, color=COULEUR_SEPARATEUR,
            spaceAfter=6, spaceBefore=6
        ))

        # Informations générales (tableau 2 colonnes)
        info_data = [
            ["Catégorie", projet.categorie or "—"],
            ["Durée totale", projet.duree or "—"],
            ["Durée d'opposition", projet.duree_opposition or "—"],
            ["Nombre de phrases", str(len(projet.choregraphie_sections))],
            ["Nombre d'actions total", str(
                sum(len(p.liste_actions) for p in projet.choregraphie_sections)
            )],
        ]

        info_table = Table(info_data, colWidths=[5 * cm, 8 * cm])
        info_table.setStyle(TableStyle([
            ("FONTNAME",    (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE",    (0, 0), (-1, -1), 10),
            ("FONTNAME",    (0, 0), (0, -1),  "Helvetica-Bold"),
            ("TEXTCOLOR",   (0, 0), (0, -1),  COULEUR_TITRE),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [COULEUR_LIGNE_PAIRE, COULEUR_LIGNE_IMPR]),
            ("GRID",        (0, 0), (-1, -1), 0.5, COULEUR_BORD),
            ("TOPPADDING",  (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(Spacer(1, 0.4 * cm))
        story.append(info_table)

        # Intrigue
        if projet.intrigue:
            story.append(Spacer(1, 0.6 * cm))
            story.append(Paragraph("Intrigue", styles["section_header"]))
            story.append(Paragraph(
                projet.intrigue.replace("\n", "<br/>"),
                styles["corps"]
            ))

        # Combattants
        if projet.liste_combattants:
            story.append(Spacer(1, 0.6 * cm))
            story.append(Paragraph("Combattants", styles["section_header"]))

            comb_data = [["ID", "Nom", "Prénom", "Licence", "Capitaine"]]
            for c in projet.liste_combattants:
                comb_data.append([
                    str(c.id),
                    c.nom,
                    c.prenom,
                    c.numero_licence or "—",
                    "Oui" if c.capitaine else "Non",
                ])

            comb_table = Table(
                comb_data,
                colWidths=[1.2 * cm, 4 * cm, 4 * cm, 4 * cm, 2.5 * cm]
            )
            comb_table.setStyle(cls._table_style_base())
            story.append(comb_table)

        # Assistants
        if projet.liste_assistants:
            story.append(Spacer(1, 0.6 * cm))
            story.append(Paragraph("Assistants Plateau", styles["section_header"]))

            assist_data = [["Nom", "Prénom", "Licence", "Rôle"]]
            for a in projet.liste_assistants:
                assist_data.append([
                    a.nom,
                    a.prenom,
                    a.numero_licence or "—",
                    a.role or "—",
                ])

            assist_table = Table(
                assist_data,
                colWidths=[4 * cm, 4 * cm, 4 * cm, 5 * cm]
            )
            assist_table.setStyle(cls._table_style_base())
            story.append(assist_table)

        return story

    @classmethod
    def _build_phrase_section(
        cls,
        phrase: PhraseDArmes,
        projet: ProjetChoregraphique,
        styles,
        page_size,
    ) -> list:
        story = []
        
        story.append(Paragraph(f"Phrase {phrase.numero} : {phrase.description_section}", styles["titre_phrase"]))
        story.append(Spacer(1, 0.3 * cm))

        if not phrase.liste_actions:
            story.append(Paragraph("Aucune action définie pour cette phrase.", styles["corps"]))
            return story

        ordered_actions = sorted(phrase.liste_actions, key=lambda a: a.numero_action)
        SEUIL_ACTIONS = 8
        
        for i in range(0, len(ordered_actions), SEUIL_ACTIONS):
            segment = ordered_actions[i : i + SEUIL_ACTIONS]
            
            header_row = ["N° Action"] + [str(a.numero_action) for a in segment]
            table_data = [header_row]
            
            # Initialisation du style avec les règles de base
            table_styles = [
                ("BACKGROUND", (0, 0), (-1, 0), COULEUR_EN_TETE),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, COULEUR_BORD),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]

            mvt_props = [
                ("Main D", "main_droite"), ("Zone MD", "zone_main_droite"), ("Cible MD", "cible_main_droite_id"),
                ("Main G", "main_gauche"), ("Zone MG", "zone_main_gauche"), ("Cible MG", "cible_main_gauche_id"),
                ("Dépl.", "deplacement"), ("Com.", "commentaire")
            ]

            for combatant in sorted(projet.liste_combattants, key=lambda c: c.id):
                # 1. Ajout ligne combattant (fusionnée)
                combatant_row = [f"{combatant.nom} {combatant.prenom} (ID: {combatant.id})"] + [""] * len(segment)
                table_data.append(combatant_row)
                row_idx = len(table_data) - 1
                
                # Appliquer la fusion et le style bleu
                table_styles.append(("SPAN", (0, row_idx), (-1, row_idx)))
                table_styles.append(("BACKGROUND", (0, row_idx), (-1, row_idx), COULEUR_EN_TETE))
                table_styles.append(("TEXTCOLOR", (0, row_idx), (-1, row_idx), colors.white))
                table_styles.append(("FONTNAME", (0, row_idx), (-1, row_idx), "Helvetica-Bold"))
                # Supprimer les lignes verticales parasites sur cette ligne fusionnée
                table_styles.append(("LINEBEFORE", (0, row_idx), (-1, row_idx), 0, colors.white))
                table_styles.append(("LINEAFTER", (0, row_idx), (-1, row_idx), 0, colors.white))

                # 2. Lignes de données
                for label, attr in mvt_props:
                    row = [label]
                    has_data = False
                    for action in segment:
                        mvt = action.get_mouvement_pour_combattant(combatant.id)
                        val = str(getattr(mvt, attr, "")) if mvt else ""
                        if val in ["0", "None"]: val = ""
                        row.append(Paragraph(val, styles["corps"]))
                        if val.strip(): has_data = True
                    
                    if has_data:
                        table_data.append(row)

            available_width = page_size[0] - 3 * cm
            col_widths = [2.5 * cm] + [(available_width - 2.5 * cm) / len(segment)] * len(segment)

            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle(table_styles))
            
            story.append(table)
            story.append(Spacer(1, 0.5 * cm))
            
            if i + SEUIL_ACTIONS < len(ordered_actions):
                story.append(PageBreak())

        return story
    

    # =========================================================================
    # STYLES COMMUNS
    # =========================================================================

    @classmethod
    def _build_styles(cls) -> dict:
        """Construit et retourne le dictionnaire de styles de paragraphes."""
        base = getSampleStyleSheet()

        styles = {}

        styles["titre_principal"] = ParagraphStyle(
            "titre_principal",
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=COULEUR_TITRE,
            alignment=TA_CENTER,
            spaceAfter=6,
        )

        styles["sous_titre"] = ParagraphStyle(
            "sous_titre",
            fontName="Helvetica",
            fontSize=14,
            textColor=COULEUR_SOUS_TITRE,
            alignment=TA_CENTER,
            spaceAfter=10,
        )

        styles["titre_phrase"] = ParagraphStyle(
            "titre_phrase",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=COULEUR_TITRE,
            spaceAfter=4,
            spaceBefore=4,
        )

        styles["description_phrase"] = ParagraphStyle(
            "description_phrase",
            fontName="Helvetica-Oblique",
            fontSize=10,
            textColor=COULEUR_SOUS_TITRE,
            spaceAfter=6,
            leftIndent=12,
        )

        styles["section_header"] = ParagraphStyle(
            "section_header",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=COULEUR_EN_TETE,
            spaceBefore=6,
            spaceAfter=4,
        )

        styles["corps"] = ParagraphStyle(
            "corps",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.black,
            spaceAfter=6,
            leading=14,
        )

        return styles

    @classmethod
    def _table_style_base(cls) -> TableStyle:
        """Retourne le style de tableau de base réutilisable."""
        return TableStyle([
            # En-tête
            ("BACKGROUND",   (0, 0), (-1, 0), COULEUR_EN_TETE),
            ("TEXTCOLOR",    (0, 0), (-1, 0), COULEUR_EN_TETE_TXT),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 8),
            ("ALIGN",        (0, 0), (-1, 0), "CENTER"),
            # Données
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COULEUR_LIGNE_IMPR, COULEUR_LIGNE_PAIRE]),
            # Bordures
            ("GRID",         (0, 0), (-1, -1), 0.5, COULEUR_BORD),
            ("BOX",          (0, 0), (-1, -1), 1,   COULEUR_EN_TETE),
            # Padding
            ("TOPPADDING",   (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 3),
            ("LEFTPADDING",  (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ])

    # =========================================================================
    # FORMAT DE PAGE
    # =========================================================================

    @classmethod
    def _resolve_page_size(cls, page_size_str: str):
        """
        Traduit la chaîne de format de page en tuple ReportLab.

        Paramètres
        ----------
        page_size_str : str
            "A4 Paysage", "A4 Portrait", "A3 Paysage" ou "A3 Portrait".
        """
        mapping = {
            "A4 Paysage":  landscape(A4),
            "A4 Portrait": portrait(A4),
            "A3 Paysage":  landscape(A3),
            "A3 Portrait": portrait(A3),
        }
        return mapping.get(page_size_str, landscape(A4))

    # =========================================================================
    # DÉCORATION DES PAGES (numérotation + pied de page)
    # =========================================================================

    @classmethod
    def _make_page_decorator(cls, projet: ProjetChoregraphique):
        """
        Retourne une fonction de décoration de page (en-tête et pied de page).
        Compatible avec les callbacks onFirstPage/onLaterPages de ReportLab.
        """
        def decorate_page(canvas, doc):
            """Dessine l'en-tête et le pied de page sur chaque page."""
            canvas.saveState()

            page_width, page_height = doc.pagesize
            margin = 1.5 * cm

            # --- Pied de page ---
            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(COULEUR_SOUS_TITRE)

            # Titre à gauche
            titre = projet.titre or "Chorégraphie"
            canvas.drawString(margin, 0.8 * cm, titre)

            # Numéro de page à droite
            page_info = f"Page {doc.page}"
            canvas.drawRightString(page_width - margin, 0.8 * cm, page_info)

            # Ligne de séparation du pied de page
            canvas.setStrokeColor(COULEUR_BORD)
            canvas.setLineWidth(0.5)
            canvas.line(margin, 1.1 * cm, page_width - margin, 1.1 * cm)

            canvas.restoreState()

        return decorate_page
