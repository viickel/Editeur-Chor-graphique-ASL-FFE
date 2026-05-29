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
# Palette de couleurs (cohérente avec l'interface graphique)
# ---------------------------------------------------------------------------
COULEUR_TITRE       = colors.HexColor("#2c3e50")   # Bleu-gris foncé
COULEUR_EN_TETE     = colors.HexColor("#4a90d9")   # Bleu principal
COULEUR_EN_TETE_TXT = colors.white
COULEUR_LIGNE_PAIRE = colors.HexColor("#f0f6ff")   # Bleu très clair
COULEUR_LIGNE_IMPR  = colors.white
COULEUR_BORD        = colors.HexColor("#b0c4de")   # Gris-bleu clair
COULEUR_SOUS_TITRE  = colors.HexColor("#5a6a7a")   # Gris-bleu
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
        margin_h = 1.5 * cm
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
        story.append(Spacer(1, 1.5 * cm))
        story.append(Paragraph(
            projet.titre or "Chorégraphie sans titre",
            styles["titre_principal"]
        ))

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

    # =========================================================================
    # SECTION PHRASE D'ARMES
    # =========================================================================

    @classmethod
    def _build_phrase_section(
        cls,
        phrase: PhraseDArmes,
        projet: ProjetChoregraphique,
        styles,
        page_size,
    ) -> list:
        """Construit la section PDF d'une phrase d'armes (tableau des actions)."""
        story = []
        combattants = projet.liste_combattants
        show_cible = len(combattants) > 2

        # En-tête de la phrase
        story.append(Paragraph(
            f"Phrase {phrase.numero}",
            styles["titre_phrase"]
        ))
        if phrase.description_section:
            story.append(Paragraph(
                phrase.description_section.replace("\n", "<br/>"),
                styles["description_phrase"]
            ))
        story.append(Spacer(1, 0.3 * cm))

        if not phrase.liste_actions:
            story.append(Paragraph("(Aucune action dans cette phrase)", styles["corps"]))
            return story

        # Construire les en-têtes du tableau des actions
        # Ligne 1 : "Action" + nom de chaque combattant sur plusieurs colonnes
        # Ligne 2 : numéros + champs détaillés
        header_row1 = [""]  # Colonne "N°"
        header_row2 = ["N°"]

        # Calculer le nombre de colonnes par combattant
        cols_par_combattant = 7 if show_cible else 5  # avec ou sans cibles

        for c in combattants:
            header_row1 += [f"{c.prenom} {c.nom}"] + [""] * (cols_par_combattant - 1)
            if show_cible:
                header_row2 += [
                    "Main D", "Zone MD", "Cible MD",
                    "Main G", "Zone MG", "Cible MG",
                    "Déplacement",
                ]
            else:
                header_row2 += [
                    "Main D", "Zone MD",
                    "Main G", "Zone MG",
                    "Déplacement",
                ]

        # Colonnes commentaires (une par combattant)
        for _ in combattants:
            header_row1.append("Commentaire")
            header_row2.append("")

        # Construire les lignes de données
        data_rows = []
        for action in sorted(phrase.liste_actions, key=lambda a: a.numero_action):
            row = [str(action.numero_action)]

            for c in combattants:
                m = action.get_mouvement_pour_combattant(c.id)
                if m:
                    if show_cible:
                        row += [
                            m.main_droite,
                            m.zone_main_droite,
                            str(m.cible_main_droite_id) if m.cible_main_droite_id else "—",
                            m.main_gauche,
                            m.zone_main_gauche,
                            str(m.cible_main_gauche_id) if m.cible_main_gauche_id else "—",
                            m.deplacement,
                        ]
                    else:
                        row += [
                            m.main_droite,
                            m.zone_main_droite,
                            m.main_gauche,
                            m.zone_main_gauche,
                            m.deplacement,
                        ]
                else:
                    row += [""] * cols_par_combattant

            # Commentaires
            for c in combattants:
                m = action.get_mouvement_pour_combattant(c.id)
                row.append(m.commentaire if m else "")

            data_rows.append(row)

        # Assembler toutes les lignes
        all_data = [header_row1, header_row2] + data_rows

        # Calculer les largeurs de colonnes dynamiquement
        page_width = page_size[0]
        usable_width = page_width - 3 * cm  # marges gauche + droite
        nb_combattants = len(combattants)
        total_cols = 1 + nb_combattants * (cols_par_combattant + 1)  # +1 pour commentaire

        # Colonne N° : fixe, petite
        col_num_w = 0.9 * cm
        # Colonnes commentaire : légèrement plus larges
        col_comment_w = 3.0 * cm
        # Colonnes mouvements : répartition du reste
        remaining = usable_width - col_num_w - (nb_combattants * col_comment_w)
        col_mvt_w = max(remaining / (nb_combattants * cols_par_combattant), 1.5 * cm)

        col_widths = [col_num_w]
        for _ in combattants:
            col_widths += [col_mvt_w] * cols_par_combattant
        for _ in combattants:
            col_widths.append(col_comment_w)

        # Créer le tableau ReportLab
        table = Table(all_data, colWidths=col_widths, repeatRows=2)

        # Style de base
        style = cls._table_style_base()

        # Span de la ligne 1 pour regrouper les colonnes par combattant
        col_start = 1
        for ci in range(nb_combattants):
            end = col_start + cols_par_combattant - 1
            style.add("SPAN", (col_start, 0), (end, 0))
            style.add("ALIGN", (col_start, 0), (end, 0), "CENTER")
            style.add("BACKGROUND", (col_start, 0), (end, 0), COULEUR_EN_TETE)
            style.add("TEXTCOLOR", (col_start, 0), (end, 0), COULEUR_EN_TETE_TXT)
            col_start += cols_par_combattant

        # Commentaires : colonnes regroupées ligne 1
        for ci in range(nb_combattants):
            style.add("BACKGROUND", (col_start + ci, 0), (col_start + ci, 0), COULEUR_SOUS_TITRE)
            style.add("TEXTCOLOR", (col_start + ci, 0), (col_start + ci, 0), colors.white)

        # Colonne N°
        style.add("SPAN", (0, 0), (0, 1))
        style.add("VALIGN", (0, 0), (0, 1), "MIDDLE")
        style.add("BACKGROUND", (0, 0), (0, 1), COULEUR_SOUS_TITRE)
        style.add("TEXTCOLOR", (0, 0), (0, 1), colors.white)

        # Ligne d'en-tête 2
        style.add("BACKGROUND", (1, 1), (-1, 1), COULEUR_SOUS_TITRE)
        style.add("TEXTCOLOR", (1, 1), (-1, 1), colors.white)
        style.add("FONTSIZE", (0, 0), (-1, 1), 7)
        style.add("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold")

        table.setStyle(style)
        story.append(table)

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
