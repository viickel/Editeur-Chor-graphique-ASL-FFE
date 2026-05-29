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
        QMainWindow {
            background-color: #f5f5f5;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        QPushButton {
            background-color: #4a90d9;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 6px 14px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #357abd;
        }
        QPushButton:pressed {
            background-color: #2a6099;
        }
        QPushButton:disabled {
            background-color: #aaaaaa;
            color: #dddddd;
        }
        QPushButton[danger="true"] {
            background-color: #d9534f;
        }
        QPushButton[danger="true"]:hover {
            background-color: #c9302c;
        }
        QPushButton[secondary="true"] {
            background-color: #6c757d;
        }
        QPushButton[secondary="true"]:hover {
            background-color: #545b62;
        }
        QPushButton[success="true"] {
            background-color: #5cb85c;
        }
        QPushButton[success="true"]:hover {
            background-color: #449d44;
        }
        QTableWidget {
            gridline-color: #dddddd;
            alternate-background-color: #f9f9f9;
        }
        QTableWidget::item:selected {
            background-color: #4a90d9;
            color: white;
        }
        QHeaderView::section {
            background-color: #e8e8e8;
            padding: 4px;
            border: 1px solid #dddddd;
            font-weight: bold;
        }
        QListWidget::item:selected {
            background-color: #4a90d9;
            color: white;
        }
        QTabWidget::pane {
            border: 1px solid #cccccc;
        }
        QTabBar::tab {
            background-color: #e8e8e8;
            padding: 6px 14px;
            border: 1px solid #cccccc;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background-color: white;
            font-weight: bold;
        }
    """)

    # Créer et afficher la fenêtre principale
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
