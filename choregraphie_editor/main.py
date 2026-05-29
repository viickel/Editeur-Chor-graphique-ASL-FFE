#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Éditeur Chorégraphique ASL-FFE - Version 2
Point d'entrée de l'application.

Auteur : Migration VB.NET → Python/PyQt6
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


def main():
    """Point d'entrée principal de l'application."""
    # Activer le support DPI haute résolution
    app = QApplication(sys.argv)
    app.setApplicationName("Éditeur Chorégraphique ASL-FFE")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("ASL-FFE")

    # Appliquer un style propre et moderne
    app.setStyle("Fusion")

    # Feuille de style globale pour améliorer l'apparence
    app.setStyleSheet("""
        /* Fond global très sombre (gris sidéral) */
        QMainWindow, QDialog {
            background-color: #121212;
            color: #e0e0e0;
        }

        /* Groupes stylés avec bordure fine et discrète */
        QGroupBox {
            font-weight: bold;
            border: 1px solid #333333;
            border-radius: 6px;
            margin-top: 14px;
            padding-top: 10px;
            color: #ffffff;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #4a90d9;
        }

        /* Boutons avec une touche de profondeur */
        QPushButton {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 1px solid #4a90d9;
            border-radius: 4px;
            padding: 6px 14px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #2a2a2a;
            border-color: #6fb3ff;
            color: #ffffff;
        }
        
        /* Boutons spéciaux type "Laser" */
        QPushButton[success="true"] { background-color: #004d40; border-color: #00e676; color: white; }
        QPushButton[danger="true"] { background-color: #4a1414; border-color: #ff5252; color: white; }
        QPushButton[secondary="true"] { background-color: #263238; border-color: #78909c; color: white; }

        /* Saisie de texte */
        QLineEdit, QTextEdit, QComboBox {
            background-color: #0a0a0a;
            border: 1px solid #333333;
            color: #ffffff;
            padding: 4px;
            border-radius: 3px;
        }

        /* Tableaux et Listes */
        QTableWidget, QListWidget {
            background-color: #121212;
            alternate-background-color: #1a1a1a;
            border: 1px solid #333333;
            gridline-color: #333333;
        }
        QTableWidget::item:selected, QListWidget::item:selected {
            background-color: #005f87;
            color: white;
        }
        QHeaderView::section {
            background-color: #1e1e1e;
            color: #aaaaaa;
            padding: 4px;
            border: 1px solid #333333;
        }

        /* Tabs */
        QTabBar::tab {
            background-color: #1e1e1e;
            color: #888888;
            padding: 6px 14px;
            border: 1px solid #333333;
        }
        QTabBar::tab:selected {
            background-color: #121212;
            color: #4a90d9;
            border-bottom: none;
        }
    """)

    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
