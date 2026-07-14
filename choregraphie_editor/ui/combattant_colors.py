# -*- coding: utf-8 -*-
"""
Palette de couleurs des combattants — partagée entre dialog_actions.py et pdf_exporter.py.

Chaque combattant se voit attribuer une couleur unique et cohérente
dans toute l'application : tableau d'édition, légende, et export PDF.

Deux variantes de chaque couleur sont définies :
  - "light"  : tons pastels clairs pour le thème clair
  - "dark"   : tons sombres saturés pour le thème sombre
                (texte toujours blanc sur ces fonds)

Le module détecte automatiquement le thème actif via l'application Qt.
"""

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt


# ---------------------------------------------------------------------------
# Palette principale — 8 teintes distinctes
#
# light_bg     : fond pastel léger (thème clair)
# light_header : couleur soutenue pour en-tête et badge (thème clair)
# light_text   : texte foncé sur fond pastel (thème clair)
# dark_bg      : fond sombre saturé (thème sombre)
# dark_header  : couleur vive pour en-tête et badge (thème sombre)
# dark_text    : toujours blanc sur fond sombre
# pdf_bg       : fond pour le PDF (toujours clair, le PDF est imprimé)
# pdf_header   : en-tête groupe dans le PDF
# ---------------------------------------------------------------------------
PALETTE = [
    {
        "name":         "Bleu",
        "light_bg":     "#D6EAF8",  # pastel bleu clair
        "light_header": "#2E86C1",  # bleu soutenu
        "light_text":   "#1A5276",  # bleu très foncé
        "dark_bg":      "#0d2137",  # bleu nuit profond
        "dark_header":  "#4a90d9",  # bleu laser
        "dark_text":    "#ffffff",
        "pdf_bg":       "#D6EAF8",
        "pdf_header":   "#2E86C1",
        "pdf_text":     "#1A5276",
    },
    {
        "name":         "Vert",
        "light_bg":     "#D5F5E3",
        "light_header": "#1E8449",
        "light_text":   "#145A32",
        "dark_bg":      "#0d2e1a",
        "dark_header":  "#27ae60",
        "dark_text":    "#ffffff",
        "pdf_bg":       "#D5F5E3",
        "pdf_header":   "#1E8449",
        "pdf_text":     "#145A32",
    },
    {
        "name":         "Rouge",
        "light_bg":     "#FDEDEC",
        "light_header": "#CB4335",
        "light_text":   "#7B241C",
        "dark_bg":      "#2e0d0d",
        "dark_header":  "#e74c3c",
        "dark_text":    "#ffffff",
        "pdf_bg":       "#FDEDEC",
        "pdf_header":   "#CB4335",
        "pdf_text":     "#7B241C",
    },
    {
        "name":         "Jaune",
        "light_bg":     "#FEF9E7",
        "light_header": "#B7950B",
        "light_text":   "#7D6608",
        "dark_bg":      "#2e2600",
        "dark_header":  "#d4ac0d",
        "dark_text":    "#ffffff",
        "pdf_bg":       "#FEF9E7",
        "pdf_header":   "#B7950B",
        "pdf_text":     "#7D6608",
    },
    {
        "name":         "Violet",
        "light_bg":     "#F4ECF7",
        "light_header": "#7D3C98",
        "light_text":   "#4A235A",
        "dark_bg":      "#1e0d2e",
        "dark_header":  "#9b59b6",
        "dark_text":    "#ffffff",
        "pdf_bg":       "#F4ECF7",
        "pdf_header":   "#7D3C98",
        "pdf_text":     "#4A235A",
    },
    {
        "name":         "Orange",
        "light_bg":     "#FDEBD0",
        "light_header": "#CA6F1E",
        "light_text":   "#784212",
        "dark_bg":      "#2e1800",
        "dark_header":  "#e67e22",
        "dark_text":    "#ffffff",
        "pdf_bg":       "#FDEBD0",
        "pdf_header":   "#CA6F1E",
        "pdf_text":     "#784212",
    },
    {
        "name":         "Cyan",
        "light_bg":     "#E8F8F5",
        "light_header": "#117A65",
        "light_text":   "#0E6655",
        "dark_bg":      "#00201a",
        "dark_header":  "#1abc9c",
        "dark_text":    "#ffffff",
        "pdf_bg":       "#E8F8F5",
        "pdf_header":   "#117A65",
        "pdf_text":     "#0E6655",
    },
    {
        "name":         "Gris",
        "light_bg":     "#F2F3F4",
        "light_header": "#616A6B",
        "light_text":   "#2C3E50",
        "dark_bg":      "#1a1f20",
        "dark_header":  "#95a5a6",
        "dark_text":    "#ffffff",
        "pdf_bg":       "#F2F3F4",
        "pdf_header":   "#616A6B",
        "pdf_text":     "#2C3E50",
    },
]


def _is_dark_theme() -> bool:
    """
    Détecte si l'application utilise actuellement le thème sombre.
    Compatible avec le système de thèmes de main.py.
    """
    app = QApplication.instance()
    if app is None:
        return False
    return app.styleHints().colorScheme() == Qt.ColorScheme.Dark


def get_palette(index: int) -> dict:
    """
    Retourne toute la palette de couleurs pour le combattant à l'index donné.
    Tourne en boucle si plus de 8 combattants.
    """
    return PALETTE[index % len(PALETTE)]


def get_bg(index: int) -> str:
    """
    Retourne la couleur de fond hex adaptée au thème actif.
    Thème clair → pastel,  thème sombre → sombre saturé.
    """
    p = get_palette(index)
    return p["dark_bg"] if _is_dark_theme() else p["light_bg"]


def get_header(index: int) -> str:
    """Retourne la couleur d'en-tête hex adaptée au thème actif."""
    p = get_palette(index)
    return p["dark_header"] if _is_dark_theme() else p["light_header"]


def get_text(index: int) -> str:
    """
    Retourne la couleur de texte hex adaptée au thème actif.
    En thème sombre, toujours blanc sur fond sombre.
    """
    p = get_palette(index)
    return p["dark_text"] if _is_dark_theme() else p["light_text"]


def qt_bg(index: int) -> QColor:
    """Retourne la couleur de fond (QColor) adaptée au thème actif."""
    return QColor(get_bg(index))


def qt_header(index: int) -> QColor:
    """Retourne la couleur d'en-tête (QColor) adaptée au thème actif."""
    return QColor(get_header(index))


def qt_text(index: int) -> QColor:
    """Retourne la couleur de texte (QColor) adaptée au thème actif."""
    return QColor(get_text(index))


def badge_style(index: int) -> str:
    """
    Retourne un stylesheet Qt pour un badge coloré (étiquette ID combattant).
    Toujours fond coloré + texte blanc pour garantir la lisibilité
    en thème clair ET sombre.
    """
    header = get_header(index)
    return (
        f"background-color: {header}; "
        f"color: white; "
        f"border-radius: 8px; "
        f"padding: 2px 8px; "
        f"font-weight: bold; "
        f"font-size: 11px;"
    )
