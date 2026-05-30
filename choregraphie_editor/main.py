#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Éditeur Chorégraphique ASL-FFE - Version 2
Migration VB.NET → Python/PyQt6.

Auteur : Vincent Thivolle
Compatibilité : Windows, macOS, Linux
"""

import sys
import os


# Assure que le dossier du script est dans le path Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from ui.main_window import MainWindow

def apply_theme(app):
    """Détecte le thème système et charge le fichier QSS."""
    # On force la détection via le styleHint
    is_dark = app.styleHints().colorScheme() == Qt.ColorScheme.Dark
    
    # On ajoute un print pour déboguer (tu verras ça dans ton terminal)
    theme_file = "dark.qss" if is_dark else "light.qss"
    print(f"Tentative de chargement du thème : {theme_file}")
    
    # Chemin absolu pour être sûr que Python trouve le fichier
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, theme_file)
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            print("Thème chargé avec succès !")
    else:
        print(f"ERREUR : Fichier {file_path} introuvable.")
        # Fallback forcé
        app.setStyle("Fusion")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Éditeur Chorégraphique ASL-FFE")
    
    # Appliquer le thème adaptatif
    apply_theme(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()