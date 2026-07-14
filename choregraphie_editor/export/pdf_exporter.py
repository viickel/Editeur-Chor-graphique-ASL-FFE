# -*- coding: utf-8 -*-
"""
Générateur de PDF pour les projets chorégraphiques — Version 2.1

Améliorations ergonomiques v2.1 :
  - Chaque combattant a une couleur pastel unique cohérente avec le tableau UI
  - Page de garde : tableau des combattants avec badge couleur par combattant
  - Légende des couleurs en haut de chaque page de phrase
  - Colonnes "Cible MD / Cible MG" affichent le nom du combattant ciblé
    avec fond coloré correspondant à la couleur de la cible
  - En-tête de groupe par combattant coloré dans la couleur soutenue
  - Compatible avec les formats A4/A3 Portrait/Paysage

Structure du PDF généré :
  1. Page de garde : titre, club, intrigue, durée, catégorie, participants
  2. Une page (ou plus) par phrase d'armes avec tableau des actions coloré
"""

from reportlab.lib.pagesizes import A4, A3, landscape, portrait
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.platypus.flowables import Flowable

from models.projet_choregraphique import ProjetChoregraphique
from models.phrase_darmes import PhraseDArmes
from models.action import Action
from models.combattant import Combattant


# ---------------------------------------------------------------------------
# Palette de couleurs globale de l'application (identique à combattant_colors.py)
# Utilisée aussi bien pour l'interface Qt que pour le PDF ReportLab.
# ---------------------------------------------------------------------------
PALETTE = [
    {"name": "Bleu",   "bg": "#D6EAF8", "header": "#2E86C1", "text": "#1A5276"},
    {"name": "Vert",   "bg": "#D5F5E3", "header": "#1E8449", "text": "#145A32"},
    {"name": "Rouge",  "bg": "#FDEDEC", "header": "#CB4335", "text": "#7B241C"},
    {"name": "Jaune",  "bg": "#FEF9E7", "header": "#B7950B", "text": "#7D6608"},
    {"name": "Violet", "bg": "#F4ECF7", "header": "#7D3C98", "text": "#4A235A"},
    {"name": "Orange", "bg": "#FDEBD0", "header": "#CA6F1E", "text": "#784212"},
    {"name": "Cyan",   "bg": "#E8F8F5", "header": "#117A65", "text": "#0E6655"},
    {"name": "Gris",   "bg": "#F2F3F4", "header": "#616A6B", "text": "#2C3E50"},
]

# Couleurs générales du document (non liées aux combattants)
C_TITRE      = colors.HexColor("#1a1a1a")
C_SOUS_TITRE = colors.HexColor("#5a6a7a")
C_BLEU_DOC   = colors.HexColor("#4a90d9")
C_BORD_DOC   = colors.HexColor("#cccccc")
C_PAIR       = colors.HexColor("#f8f9fa")

# Nombre max d'actions par segment de tableau avant saut de page
SEUIL_ACTIONS = 8


def _pal(index: int) -> dict:
    """Retourne la palette du combattant à l'index donné (boucle si > 8)."""
    return PALETTE[index % len(PALETTE)]


def _rc(hex_color: str) -> colors.HexColor:
    """Convertit une couleur hex string en objet ReportLab."""
    return colors.HexColor(hex_color)


class PdfExporter:
    """
    Génère un fichier PDF à partir d'un ProjetChoregraphique.

    La palette de couleurs par combattant est calculée une seule fois
    dans generate() et transmise à toutes les méthodes de construction.

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
        page_size = cls._resolve_page_size(page_size_str)

        # Construire le mapping ID combattant → index palette
        # Trié par ID pour garantir la cohérence avec l'interface Qt
        sorted_ids = sorted(c.id for c in projet.liste_combattants)
        color_map: dict[int, int] = {cid: i for i, cid in enumerate(sorted_ids)}

        doc = SimpleDocTemplate(
            output_path,
            pagesize=page_size,
            leftMargin=1.2 * cm,
            rightMargin=1.2 * cm,
            topMargin=1.8 * cm,
            bottomMargin=1.8 * cm,
            title=projet.titre or "Chorégraphie",
            author="Éditeur Chorégraphique ASL-FFE v2",
        )

        styles = cls._build_styles()
        story = []
        story += cls._build_cover_page(projet, styles, page_size, color_map)

        for phrase in sorted(projet.choregraphie_sections, key=lambda p: p.numero):
            story.append(PageBreak())
            story += cls._build_phrase_section(phrase, projet, styles, page_size, color_map)

        doc.build(
            story,
            onFirstPage=cls._make_page_decorator(projet),
            onLaterPages=cls._make_page_decorator(projet),
        )

    # =========================================================================
    # PAGE DE GARDE
    # =========================================================================

    @classmethod
    def _build_cover_page(
        cls, projet, styles, page_size, color_map: dict
    ) -> list:
        """
        Construit la page de garde.

        La liste des combattants affiche désormais un bandeau coloré
        par combattant pour établir la légende visuelle dès la première page.
        """
        story = []

        # Titre
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(
            projet.titre or "Chorégraphie sans titre",
            styles["titre_principal"]
        ))
        story.append(Spacer(1, 0.2 * cm))
        if projet.nom_du_club:
            story.append(Paragraph(projet.nom_du_club, styles["sous_titre"]))

        story.append(HRFlowable(
            width="100%", thickness=2, color=C_BLEU_DOC,
            spaceAfter=8, spaceBefore=6
        ))

        # Informations générales
        info_data = [
            ["Catégorie",            projet.categorie or "—"],
            ["Durée totale",         projet.duree or "—"],
            ["Durée d'opposition",   projet.duree_opposition or "—"],
            ["Nombre de phrases",    str(len(projet.choregraphie_sections))],
            ["Total actions",        str(
                sum(len(p.liste_actions) for p in projet.choregraphie_sections)
            )],
        ]
        info_table = Table(info_data, colWidths=[5 * cm, 8 * cm])
        info_table.setStyle(TableStyle([
            ("FONTNAME",       (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE",       (0, 0), (-1, -1), 10),
            ("FONTNAME",       (0, 0), (0, -1),  "Helvetica-Bold"),
            ("TEXTCOLOR",      (0, 0), (0, -1),  C_BLEU_DOC),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [C_PAIR, colors.white]),
            ("GRID",           (0, 0), (-1, -1), 0.5, C_BORD_DOC),
            ("TOPPADDING",     (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
            ("LEFTPADDING",    (0, 0), (-1, -1), 8),
        ]))
        story.append(info_table)

        # Intrigue
        if projet.intrigue:
            story.append(Spacer(1, 0.5 * cm))
            story.append(Paragraph("Information : Intrigue, musiques, etc.", styles["section_header"]))
            story.append(Paragraph(
                projet.intrigue.replace("\n", "<br/>"),
                styles["corps"]
            ))

        # Combattants — avec bandeau couleur
        if projet.liste_combattants:
            story.append(Spacer(1, 0.5 * cm))
            story.append(Paragraph("Combattants", styles["section_header"]))
            story.append(cls._build_combattants_table(
                projet.liste_combattants, color_map, page_size
            ))

        # Assistants
        if projet.liste_assistants:
            story.append(Spacer(1, 0.5 * cm))
            story.append(Paragraph("Assistants/Figurants", styles["section_header"]))
            assist_data = [["Nom", "Prénom", "Licence", "Rôle"]]
            for a in projet.liste_assistants:
                assist_data.append([
                    a.nom, a.prenom,
                    a.numero_licence or "—",
                    a.role or "—",
                ])
            assist_table = Table(
                assist_data,
                colWidths=[4 * cm, 4 * cm, 4 * cm, 5 * cm]
            )
            assist_table.setStyle(cls._base_table_style())
            story.append(assist_table)

        return story

    @classmethod
    def _build_combattants_table(
        cls,
        combattants: list,
        color_map: dict,
        page_size,
    ) -> Table:
        """
        Construit le tableau des combattants avec une ligne colorée par combattant.

        Chaque ligne a le fond pastel de la couleur attribuée au combattant,
        établissant ainsi la légende visuelle pour le reste du document.
        """
        # En-tête
        header = ["", "Prénom", "Nom", "Licence", "Capitaine"]
        data = [header]
        row_colors = []   # (row_index, bg_hex, text_hex, header_hex)

        for c in combattants:
            ci = color_map.get(c.id, 0)
            p = _pal(ci)
            data.append([
                f"● {p['name']}",     # Colonne couleur (pastille + nom couleur)
                c.prenom,
                c.nom,
                c.numero_licence or "—",
                "⭐ Oui" if c.capitaine else "Non",
            ])
            row_colors.append((len(data) - 1, p["bg"], p["text"], p["header"]))

        # Largeurs : pastille couleur | prénom | nom | licence | capitaine
        usable = page_size[0] - 2.4 * cm
        col_widths = [2.5 * cm, 4 * cm, 4 * cm, 4 * cm, 2.5 * cm]

        table = Table(data, colWidths=col_widths)

        style_cmds = [
            # En-tête général
            ("BACKGROUND",   (0, 0), (-1, 0), C_BLEU_DOC),
            ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, -1), 9),
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("GRID",         (0, 0), (-1, -1), 0.5, C_BORD_DOC),
            ("BOX",          (0, 0), (-1, -1), 1,   C_BLEU_DOC),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
            ("LEFTPADDING",  (0, 0), (-1, -1), 6),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN",        (0, 0), (0, -1),  "CENTER"),
        ]

        # Coloriser chaque ligne de données selon la palette du combattant
        for row_idx, bg_hex, text_hex, header_hex in row_colors:
            style_cmds += [
                ("BACKGROUND", (0, row_idx), (-1, row_idx),  _rc(bg_hex)),
                ("TEXTCOLOR",  (1, row_idx), (-1, row_idx),  _rc(text_hex)),
                # Colonne pastille : fond plus soutenu + texte blanc
                ("BACKGROUND", (0, row_idx), (0, row_idx),   _rc(header_hex)),
                ("TEXTCOLOR",  (0, row_idx), (0, row_idx),   colors.white),
                ("FONTNAME",   (0, row_idx), (0, row_idx),   "Helvetica-Bold"),
            ]

        table.setStyle(TableStyle(style_cmds))
        return table

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
        color_map: dict,
    ) -> list:
        """
        Construit la section PDF d'une phrase d'armes.

        Structure du tableau (orientation "actions en colonnes") :
          - Colonne 0       : libellé du champ (Main D, Zone MD…)
          - Colonnes 1..N   : valeur pour chaque action
          - Groupe de lignes par combattant avec en-tête coloré
        """
        story = []

        # Titre de la phrase
        story.append(Paragraph(
            f"Phrase {phrase.numero} — {phrase.description_section}",
            styles["titre_phrase"]
        ))
        story.append(Spacer(1, 0.2 * cm))

        # Légende des couleurs (une pastille par combattant)
        if len(projet.liste_combattants) > 1:
            story.append(cls._build_legend_row(projet.liste_combattants, color_map, page_size))
            story.append(Spacer(1, 0.3 * cm))

        if not phrase.liste_actions:
            story.append(Paragraph("Aucune action définie pour cette phrase.", styles["corps"]))
            return story

        ordered_actions = sorted(phrase.liste_actions, key=lambda a: a.numero_action)
        show_cible = len(projet.liste_combattants) > 2

        # Découper en segments de SEUIL_ACTIONS actions pour éviter les tableaux trop larges
        for seg_start in range(0, len(ordered_actions), SEUIL_ACTIONS):
            segment = ordered_actions[seg_start: seg_start + SEUIL_ACTIONS]

            tbl, tbl_style = cls._build_actions_table(
                segment, projet.liste_combattants, color_map, page_size, show_cible
            )
            story.append(tbl)
            story.append(Spacer(1, 0.4 * cm))

            # Saut de page entre segments (pas après le dernier)
            if seg_start + SEUIL_ACTIONS < len(ordered_actions):
                story.append(PageBreak())
                story.append(Paragraph(
                    f"Phrase {phrase.numero} — {phrase.description_section} (suite)",
                    styles["titre_phrase"]
                ))
                story.append(cls._build_legend_row(
                    projet.liste_combattants, color_map, page_size
                ))
                story.append(Spacer(1, 0.3 * cm))

        return story

    @classmethod
    def _build_legend_row(
        cls, combattants: list, color_map: dict, page_size
    ) -> Table:
        """
        Construit une ligne de légende horizontale avec une pastille colorée
        par combattant, affichant son prénom et son ID.

        Placée en haut de chaque page de phrase pour que le lecteur puisse
        retrouver rapidement à quelle couleur correspond chaque escrimeur.
        """
        cells = []
        for c in combattants:
            ci = color_map.get(c.id, 0)
            p = _pal(ci)
            label = f"ID {c.id} — {c.prenom} {c.nom}"
            cells.append(Paragraph(
                f"<b>{label}</b>",
                ParagraphStyle(
                    f"legend_{c.id}",
                    fontName="Helvetica-Bold",
                    fontSize=8,
                    textColor=_rc(p["text"]),
                    alignment=TA_CENTER,
                )
            ))

        nb = len(cells)
        usable = page_size[0] - 2.4 * cm
        col_w = usable / nb if nb > 0 else usable

        table = Table([cells], colWidths=[col_w] * nb)
        style_cmds = [
            ("GRID",         (0, 0), (-1, -1), 1, C_BORD_DOC),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]
        for i, c in enumerate(combattants):
            ci = color_map.get(c.id, 0)
            p = _pal(ci)
            style_cmds += [
                ("BACKGROUND", (i, 0), (i, 0), _rc(p["bg"])),
                ("BOX",        (i, 0), (i, 0), 2, _rc(p["header"])),
            ]
        table.setStyle(TableStyle(style_cmds))
        return table

    @classmethod
    def _build_actions_table(
        cls,
        segment: list,
        combattants: list,
        color_map: dict,
        page_size,
        show_cible: bool,
    ):
        """
        Construit le tableau des actions pour un segment donné.

        Orientation : actions en colonnes, champs de mouvements en lignes.
        Chaque groupe de lignes correspond à un combattant et reçoit
        un en-tête de groupe coloré avec la couleur soutenue du combattant.

        Retourne (Table, TableStyle).
        """
        # ── Ligne d'en-tête : "Champ" + numéros d'action ─────────────────────
        header_row = [""] + [f"Action {a.numero_action}" for a in segment]
        data = [header_row]
        style_cmds = [
            # En-tête des numéros d'action
            ("BACKGROUND",    (0, 0), (-1, 0),  C_BLEU_DOC),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8),
            ("GRID",          (0, 0), (-1, -1), 0.5, C_BORD_DOC),
            ("BOX",           (0, 0), (-1, -1), 1.5, C_BLEU_DOC),
            ("TOPPADDING",    (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("LEFTPADDING",   (0, 0), (-1, -1), 4),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 4),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
            ("ALIGN",         (0, 1), (0, -1),  "LEFT"),
        ]

        # ── Propriétés à afficher par combattant ──────────────────────────────
        mvt_props = [
            ("Main Droite",    "main_droite"),
            ("Zone MD",        "zone_main_droite"),
            ("Main Gauche",    "main_gauche"),
            ("Zone MG",        "zone_main_gauche"),
            ("Déplacement",    "deplacement"),
            ("Commentaire",    "commentaire"),
        ]
        # Colonnes Cible uniquement en Bataille / Ensemble
        if show_cible:
            mvt_props.insert(2, ("Cible MD", "cible_main_droite_id"))
            mvt_props.insert(5, ("Cible MG", "cible_main_gauche_id"))

        # Mapping ID → combattant pour résolution des cibles
        id_to_combattant = {c.id: c for c in combattants}

        # ── Lignes par combattant ─────────────────────────────────────────────
        for c in combattants:
            ci = color_map.get(c.id, 0)
            p = _pal(ci)

            # Ligne d'en-tête du combattant (fond coloré soutenu, texte blanc)
            group_header = [f"{c.prenom} {c.nom}  (ID {c.id})"] + [""] * len(segment)
            data.append(group_header)
            grp_row = len(data) - 1
            style_cmds += [
                ("SPAN",       (0, grp_row), (-1, grp_row)),
                ("BACKGROUND", (0, grp_row), (-1, grp_row), _rc(p["header"])),
                ("TEXTCOLOR",  (0, grp_row), (-1, grp_row), colors.white),
                ("FONTNAME",   (0, grp_row), (-1, grp_row), "Helvetica-Bold"),
                ("FONTSIZE",   (0, grp_row), (-1, grp_row), 8),
                ("TOPPADDING", (0, grp_row), (-1, grp_row), 4),
                ("BOTTOMPADDING",(0, grp_row),(-1, grp_row), 4),
            ]

            # Lignes de données du combattant
            for label, attr in mvt_props:
                row_data = [label]
                has_data = False

                for action in segment:
                    mvt = action.get_mouvement_pour_combattant(c.id)
                    raw = getattr(mvt, attr, "") if mvt else ""

                    # Résolution de l'ID cible → nom du combattant ciblé
                    if attr in ("cible_main_droite_id", "cible_main_gauche_id"):
                        cible_id = int(raw) if raw and str(raw) not in ("0", "") else 0
                        if cible_id and cible_id in id_to_combattant:
                            cible = id_to_combattant[cible_id]
                            cible_ci = color_map.get(cible_id, 0)
                            cible_p = _pal(cible_ci)
                            # Cellule avec fond coloré de la cible
                            cell = Paragraph(
                                f"<b>{cible.prenom} {cible.nom}</b>",
                                ParagraphStyle(
                                    f"cible_{c.id}_{cible_id}",
                                    fontName="Helvetica-Bold",
                                    fontSize=7,
                                    textColor=_rc(cible_p["text"]),
                                    backColor=_rc(cible_p["bg"]),
                                    alignment=TA_CENTER,
                                    borderPad=2,
                                )
                            )
                            row_data.append(cell)
                            has_data = True
                        else:
                            row_data.append("")
                    else:
                        val = str(raw) if raw and str(raw) not in ("0", "None") else ""
                        # Pour le commentaire : utiliser un Paragraph pour le retour à la ligne
                        if attr == "commentaire" and val.strip():
                            cell = Paragraph(
                                val.replace("\n", "<br/>"),
                                ParagraphStyle(
                                    "commentaire_cell",
                                    fontName="Helvetica",
                                    fontSize=7,
                                    leading=9,
                                    wordWrap="CJK",
                                )
                            )
                            row_data.append(cell)
                            has_data = True
                        else:
                            row_data.append(val)
                            if val.strip():
                                has_data = True

                # N'ajouter la ligne que si elle contient au moins une donnée
                if has_data:
                    data.append(row_data)
                    data_row = len(data) - 1
                    # Fond pastel de la couleur du combattant pour les lignes de données
                    style_cmds += [
                        ("BACKGROUND", (0, data_row), (0, data_row),  _rc(p["bg"])),
                        ("FONTNAME",   (0, data_row), (0, data_row),  "Helvetica-Bold"),
                        ("TEXTCOLOR",  (0, data_row), (0, data_row),  _rc(p["text"])),
                        ("BACKGROUND", (1, data_row), (-1, data_row), colors.white),
                    ]

        # ── Calcul des largeurs de colonnes ──────────────────────────────────
        usable = page_size[0] - 2.4 * cm
        col_label_w = 2.8 * cm
        nb_actions = len(segment)
        col_action_w = (usable - col_label_w) / nb_actions if nb_actions else usable

        col_widths = [col_label_w] + [col_action_w] * nb_actions

        # Hauteur de ligne minimale (commentaires longs → wrapping automatique)
        table = Table(data, colWidths=col_widths, repeatRows=1)
        # WORDWRAP activé : la hauteur s'adapte automatiquement au contenu Paragraph
        style_cmds.append(("WORDWRAP", (0, 0), (-1, -1), True))
        table.setStyle(TableStyle(style_cmds))
        return table, style_cmds

    # =========================================================================
    # STYLES DE PARAGRAPHES
    # =========================================================================

    @classmethod
    def _build_styles(cls) -> dict:
        """Construit le dictionnaire de styles de paragraphes ReportLab."""
        styles = {}

        styles["titre_principal"] = ParagraphStyle(
            "titre_principal",
            fontName="Helvetica-Bold", fontSize=22,
            textColor=C_TITRE, alignment=TA_CENTER, spaceAfter=6,
        )
        styles["sous_titre"] = ParagraphStyle(
            "sous_titre",
            fontName="Helvetica", fontSize=14,
            textColor=C_SOUS_TITRE, alignment=TA_CENTER, spaceAfter=8,
        )
        styles["titre_phrase"] = ParagraphStyle(
            "titre_phrase",
            fontName="Helvetica-Bold", fontSize=13,
            textColor=C_TITRE, spaceAfter=4, spaceBefore=4,
        )
        styles["section_header"] = ParagraphStyle(
            "section_header",
            fontName="Helvetica-Bold", fontSize=11,
            textColor=C_BLEU_DOC, spaceBefore=6, spaceAfter=4,
        )
        styles["corps"] = ParagraphStyle(
            "corps",
            fontName="Helvetica", fontSize=9,
            textColor=colors.black, spaceAfter=4, leading=13,
        )

        return styles

    @classmethod
    def _base_table_style(cls) -> TableStyle:
        """Style de tableau générique pour la page de garde."""
        return TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0),  C_BLEU_DOC),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 9),
            ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, C_PAIR]),
            ("GRID",          (0, 0), (-1, -1), 0.5, C_BORD_DOC),
            ("BOX",           (0, 0), (-1, -1), 1,   C_BLEU_DOC),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING",   (0, 0), (-1, -1), 6),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ])

    # =========================================================================
    # FORMAT DE PAGE ET DÉCORATION
    # =========================================================================

    @classmethod
    def _resolve_page_size(cls, page_size_str: str):
        """Traduit la chaîne de format de page en tuple ReportLab."""
        return {
            "A4 Paysage":  landscape(A4),
            "A4 Portrait": portrait(A4),
            "A3 Paysage":  landscape(A3),
            "A3 Portrait": portrait(A3),
        }.get(page_size_str, landscape(A4))

    @classmethod
    def _make_page_decorator(cls, projet: ProjetChoregraphique):
        """Retourne la fonction de décoration (pied de page + numérotation)."""
        def decorate_page(canvas, doc):
            canvas.saveState()
            pw, ph = doc.pagesize
            margin = 1.2 * cm
            canvas.setFont("Helvetica", 7)
            canvas.setFillColor(C_SOUS_TITRE)
            canvas.drawString(margin, 0.8 * cm, projet.titre or "Chorégraphie")
            canvas.drawRightString(pw - margin, 0.8 * cm, f"Page {doc.page}")
            canvas.setStrokeColor(C_BORD_DOC)
            canvas.setLineWidth(0.5)
            canvas.line(margin, 1.1 * cm, pw - margin, 1.1 * cm)
            canvas.restoreState()
        return decorate_page
