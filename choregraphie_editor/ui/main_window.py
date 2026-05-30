# -*- coding: utf-8 -*-
"""
Fenêtre principale de l'éditeur chorégraphique.

Équivalent de Form1.vb dans le projet VB.NET original.
Gère l'affichage du projet, la sauvegarde/chargement XML,
et l'ouverture des dialogues d'édition.
"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget,
    QCheckBox, QComboBox, QGroupBox, QSplitter, QMessageBox,
    QFileDialog, QStatusBar, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QCloseEvent, QAction

from models.projet_choregraphique import ProjetChoregraphique
from serialization.xml_serializer import XmlSerializer
from export.pdf_exporter import PdfExporter
from ui.dialog_combattants import DialogCombattants
from ui.dialog_assistants import DialogAssistants
from ui.dialog_phrases import DialogPhrases


class MainWindow(QMainWindow):
    """
    Fenêtre principale de l'application.

    Contient le formulaire principal du projet (titre, intrigue, durée, club),
    les listes des combattants et assistants, ainsi que les boutons d'action.
    """

    def __init__(self):
        super().__init__()

        # --- État de l'application ---
        # Projet actuellement ouvert
        self._current_projet: ProjetChoregraphique = ProjetChoregraphique()
        # Chemin du fichier en cours (vide si nouveau projet)
        self._current_file_path: str = ""
        # Indicateur de modifications non sauvegardées
        self._is_dirty: bool = False

        # Construire l'interface
        self._build_ui()
        self._build_menu()
        self._connect_signals()

        # Charger un projet vide au démarrage
        self._new_project(confirm=False)

        self.setMinimumSize(800, 600)
        self.resize(900, 680)

    # =========================================================================
    # CONSTRUCTION DE L'INTERFACE
    # =========================================================================

    def _build_ui(self) -> None:
        """Construit tous les widgets de la fenêtre principale."""
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # --- Barre d'outils de fichier ---
        main_layout.addWidget(self._build_file_toolbar())

        # --- Informations générales du projet ---
        main_layout.addWidget(self._build_project_info_group())

        # --- Zone d'intrigue + image ---
        main_layout.addWidget(self._build_content_area(), stretch=2)

        # --- Combattants + Assistants ---
        main_layout.addWidget(self._build_participants_area(), stretch=1)

        # --- Barre de statut ---
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        self._status_bar.showMessage("Prêt")

    def _build_file_toolbar(self) -> QGroupBox:
        """Construit la barre de boutons Nouveau/Ouvrir/Enregistrer/PDF."""
        group = QGroupBox("Fichier et export")
        layout = QHBoxLayout(group)
        layout.setSpacing(6)

        self.btn_new = QPushButton("Nouveau")
        self.btn_open = QPushButton("Ouvrir")
        self.btn_save = QPushButton("Enregistrer")
        self.btn_save_as = QPushButton("Enregistrer sous")

        # Séparateur visuel
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)

        # Export PDF
        self.combo_page_size = QComboBox()
        self.combo_page_size.addItems(["A4 Paysage", "A4 Portrait", "A3 Paysage", "A3 Portrait"])
        self.btn_generate_pdf = QPushButton("Générer PDF")
        self.btn_generate_pdf.setProperty("success", "true")
        self.btn_generate_pdf.style().unpolish(self.btn_generate_pdf)
        self.btn_generate_pdf.style().polish(self.btn_generate_pdf)

        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_open)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_save_as)
        layout.addWidget(sep)
        layout.addWidget(QLabel("Format :"))
        layout.addWidget(self.combo_page_size)
        layout.addWidget(self.btn_generate_pdf)
        layout.addStretch()

        return group

    def _build_project_info_group(self) -> QGroupBox:
        """Construit le groupe des informations générales du projet."""
        group = QGroupBox("Informations du projet")
        grid = QGridLayout(group)
        grid.setSpacing(6)

        # Titre
        grid.addWidget(QLabel("Titre :"), 0, 0)
        self.edit_titre = QLineEdit()
        self.edit_titre.setPlaceholderText("Titre de la chorégraphie...")
        grid.addWidget(self.edit_titre, 0, 1)

        # Durée
        grid.addWidget(QLabel("Durée :"), 0, 2)
        self.edit_duree = QLineEdit()
        self.edit_duree.setPlaceholderText("00m:00s")
        self.edit_duree.setMaximumWidth(100)
        grid.addWidget(self.edit_duree, 0, 3)

        # Durée d'opposition
        grid.addWidget(QLabel("Durée d'opposition :"), 0, 4)
        self.edit_duree_opposition = QLineEdit()
        self.edit_duree_opposition.setPlaceholderText("00m:00s")
        self.edit_duree_opposition.setMaximumWidth(100)
        grid.addWidget(self.edit_duree_opposition, 0, 5)

        # Nom du club
        grid.addWidget(QLabel("Club :"), 1, 0)
        self.edit_nom_club = QLineEdit()
        self.edit_nom_club.setPlaceholderText("Nom du club...")
        grid.addWidget(self.edit_nom_club, 1, 1)

        # Mouvement d'ensemble
        self.chk_mouvement_ensemble = QCheckBox("Mouvement d'ensemble")
        grid.addWidget(self.chk_mouvement_ensemble, 1, 2, 1, 2)

        # Catégorie (calculée automatiquement)
        self.lbl_categorie = QLabel("Catégorie : —")
        self.lbl_categorie.setStyleSheet("font-weight: bold; color: #333;")
        grid.addWidget(self.lbl_categorie, 1, 4, 1, 2)

        grid.setColumnStretch(1, 3)

        return group

    def _build_content_area(self) -> QGroupBox:
        """Construit la zone centrale : intrigue + bouton édition chorégraphie."""
        group = QGroupBox("Contenu")
        layout = QHBoxLayout(group)

        # Zone d'intrigue
        intrigue_layout = QVBoxLayout()
        intrigue_layout.addWidget(QLabel("Intrigue :"))
        self.edit_intrigue = QTextEdit()
        self.edit_intrigue.setPlaceholderText("Décrivez l'intrigue de la chorégraphie...")
        intrigue_layout.addWidget(self.edit_intrigue)
        layout.addLayout(intrigue_layout, stretch=3)

        # Panneau droit : bouton chorégraphie
        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)

        self.btn_editer_chore = QPushButton("Éditer la\nChorégraphie")
        self.btn_editer_chore.setMinimumHeight(60)
        self.btn_editer_chore.setMinimumWidth(160)
        self.btn_editer_chore.setToolTip("Ouvrir l'éditeur de phrases d'armes et d'actions")
        right_layout.addWidget(self.btn_editer_chore)
        right_layout.addStretch()
        layout.addLayout(right_layout, stretch=1)

        return group

    def _build_participants_area(self) -> QSplitter:
        """Construit la zone des participants (combattants + assistants) en deux panneaux."""
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Panneau Combattants ---
        combattants_group = QGroupBox("Combattants / Chorégraphe")
        c_layout = QVBoxLayout(combattants_group)

        self.list_combattants = QListWidget()
        self.list_combattants.setAlternatingRowColors(True)
        c_layout.addWidget(self.list_combattants)

        self.btn_edit_combattants = QPushButton("Éditer les combattants")
        c_layout.addWidget(self.btn_edit_combattants)

        splitter.addWidget(combattants_group)

        # --- Panneau Assistants ---
        assistants_group = QGroupBox("Assistants Plateau")
        a_layout = QVBoxLayout(assistants_group)

        self.list_assistants = QListWidget()
        self.list_assistants.setAlternatingRowColors(True)
        a_layout.addWidget(self.list_assistants)

        self.btn_edit_assistants = QPushButton("Éditer les assistants")
        a_layout.addWidget(self.btn_edit_assistants)

        splitter.addWidget(assistants_group)
        splitter.setSizes([450, 450])

        return splitter

    def _build_menu(self) -> None:
        """Construit la barre de menus."""
        menubar = self.menuBar()

        # Menu Fichier
        menu_fichier = menubar.addMenu("Fichier")

        action_nouveau = QAction("Nouveau", self)
        action_nouveau.setShortcut("Ctrl+N")
        action_nouveau.triggered.connect(self._on_new)
        menu_fichier.addAction(action_nouveau)

        action_ouvrir = QAction("Ouvrir...", self)
        action_ouvrir.setShortcut("Ctrl+O")
        action_ouvrir.triggered.connect(self._on_open)
        menu_fichier.addAction(action_ouvrir)

        menu_fichier.addSeparator()

        action_enregistrer = QAction("Enregistrer", self)
        action_enregistrer.setShortcut("Ctrl+S")
        action_enregistrer.triggered.connect(self._on_save)
        menu_fichier.addAction(action_enregistrer)

        action_enregistrer_sous = QAction("Enregistrer sous...", self)
        action_enregistrer_sous.setShortcut("Ctrl+Shift+S")
        action_enregistrer_sous.triggered.connect(self._on_save_as)
        menu_fichier.addAction(action_enregistrer_sous)

        menu_fichier.addSeparator()

        action_quitter = QAction("Quitter", self)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.triggered.connect(self.close)
        menu_fichier.addAction(action_quitter)

        # Menu Aide
        menu_aide = menubar.addMenu("Aide")
        action_a_propos = QAction("À propos", self)
        action_a_propos.triggered.connect(self._on_about)
        menu_aide.addAction(action_a_propos)

    def _connect_signals(self) -> None:
        """Connecte les signaux des widgets à leurs slots."""
        # Boutons de fichier
        self.btn_new.clicked.connect(self._on_new)
        self.btn_open.clicked.connect(self._on_open)
        self.btn_save.clicked.connect(self._on_save)
        self.btn_save_as.clicked.connect(self._on_save_as)
        self.btn_generate_pdf.clicked.connect(self._on_generate_pdf)

        # Boutons d'édition
        self.btn_editer_chore.clicked.connect(self._on_edit_choreographie)
        self.btn_edit_combattants.clicked.connect(self._on_edit_combattants)
        self.btn_edit_assistants.clicked.connect(self._on_edit_assistants)

        # Champs de saisie → marquer le projet comme modifié
        self.edit_titre.textChanged.connect(self._on_field_changed)
        self.edit_intrigue.textChanged.connect(self._on_field_changed)
        self.edit_duree.textChanged.connect(self._on_field_changed)
        self.edit_duree_opposition.textChanged.connect(self._on_field_changed)
        self.edit_nom_club.textChanged.connect(self._on_field_changed)
        self.chk_mouvement_ensemble.toggled.connect(self._on_ensemble_toggled)

    # =========================================================================
    # GESTION DE L'ÉTAT DU PROJET
    # =========================================================================

    def _new_project(self, confirm: bool = True) -> bool:
        """
        Crée un nouveau projet vide.

        Paramètres
        ----------
        confirm : bool
            Si True, demande confirmation en cas de modifications non sauvegardées.

        Retourne
        --------
        bool : True si le nouveau projet a bien été créé.
        """
        if confirm and not self._check_unsaved_changes():
            return False

        self._current_projet = ProjetChoregraphique()
        self._current_file_path = ""
        self._is_dirty = False
        self._refresh_ui()
        self._update_title()
        self._status_bar.showMessage("Nouveau projet créé.")
        return True

    def mark_as_dirty(self) -> None:
        """
        Marque le projet comme ayant des modifications non sauvegardées.
        Appelé depuis les dialogues enfants pour propager l'état "dirty".
        """
        self._is_dirty = True
        self._update_title()

    def _check_unsaved_changes(self) -> bool:
        """
        Vérifie s'il y a des modifications non sauvegardées et propose de les sauvegarder.

        Retourne
        --------
        bool : True si on peut continuer (sauvegardé ou abandonné), False si annulé.
        """
        if not self._is_dirty:
            return True

        reply = QMessageBox.question(
            self,
            "Modifications non sauvegardées",
            "Des modifications non enregistrées seront perdues.\n"
            "Voulez-vous enregistrer avant de continuer ?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Cancel,
        )

        if reply == QMessageBox.StandardButton.Yes:
            return self._save_project()
        elif reply == QMessageBox.StandardButton.No:
            return True
        else:  # Cancel
            return False

    def _update_title(self) -> None:
        """Met à jour le titre de la fenêtre principale."""
        titre = "Éditeur Chorégraphique ASL-FFE"
        if self._current_projet.titre:
            titre += f" — {self._current_projet.titre}"
        elif self._current_file_path:
            titre += f" — {os.path.splitext(os.path.basename(self._current_file_path))[0]}"
        if self._is_dirty:
            titre += " *"
        self.setWindowTitle(titre)

    def _update_categorie(self) -> None:
        """Met à jour l'affichage de la catégorie (calculée automatiquement)."""
        # Récupérer l'état de la checkbox avant de calculer
        self._current_projet.is_mouvement_ensemble = self.chk_mouvement_ensemble.isChecked()
        categorie = self._current_projet.calculer_categorie()
        self.lbl_categorie.setText(f"Catégorie : {categorie}")

        # Afficher/masquer la checkbox selon le nombre de combattants
        nb = len(self._current_projet.liste_combattants)
        self.chk_mouvement_ensemble.setVisible(nb > 2)

    # =========================================================================
    # MISE À JOUR DE L'INTERFACE ↔ DONNÉES
    # =========================================================================

    def _refresh_ui(self) -> None:
        """
        Rafraîchit tous les contrôles de l'interface avec les données du projet courant.
        Équivalent de DisplayCurrentProjectData() dans Form1.vb.
        """
        # Bloquer les signaux pour éviter de déclencher _on_field_changed
        for widget in [self.edit_titre, self.edit_duree,
                       self.edit_duree_opposition, self.edit_nom_club]:
            widget.blockSignals(True)
        self.edit_intrigue.blockSignals(True)
        self.chk_mouvement_ensemble.blockSignals(True)

        self.edit_titre.setText(self._current_projet.titre)
        self.edit_intrigue.setPlainText(self._current_projet.intrigue)
        self.edit_duree.setText(self._current_projet.duree)
        self.edit_duree_opposition.setText(self._current_projet.duree_opposition)
        self.edit_nom_club.setText(self._current_projet.nom_du_club)
        self.chk_mouvement_ensemble.setChecked(self._current_projet.is_mouvement_ensemble)

        # Rétablir les signaux
        for widget in [self.edit_titre, self.edit_duree,
                       self.edit_duree_opposition, self.edit_nom_club]:
            widget.blockSignals(False)
        self.edit_intrigue.blockSignals(False)
        self.chk_mouvement_ensemble.blockSignals(False)

        # Listes des participants
        self._refresh_combattants_list()
        self._refresh_assistants_list()

        # Catégorie
        self._update_categorie()

    def _refresh_combattants_list(self) -> None:
        """Rafraîchit la liste des combattants dans le widget."""
        self.list_combattants.clear()
        for c in self._current_projet.liste_combattants:
            self.list_combattants.addItem(str(c))

    def _refresh_assistants_list(self) -> None:
        """Rafraîchit la liste des assistants dans le widget."""
        self.list_assistants.clear()
        for a in self._current_projet.liste_assistants:
            self.list_assistants.addItem(str(a))

    def _collect_ui_data(self) -> None:
        """
        Collecte les données de l'interface et les écrit dans le projet courant.
        Équivalent de UpdateCurrentProjectDataFromUI() dans Form1.vb.
        """
        self._current_projet.titre = self.edit_titre.text()
        self._current_projet.intrigue = self.edit_intrigue.toPlainText()
        self._current_projet.duree = self.edit_duree.text()
        self._current_projet.duree_opposition = self.edit_duree_opposition.text()
        self._current_projet.nom_du_club = self.edit_nom_club.text()
        self._current_projet.is_mouvement_ensemble = self.chk_mouvement_ensemble.isChecked()
        self._current_projet.calculer_categorie()

    # =========================================================================
    # SLOTS — Événements de l'interface
    # =========================================================================

    @pyqtSlot()
    def _on_field_changed(self) -> None:
        """Appelé à chaque modification d'un champ de saisie."""
        self.mark_as_dirty()

    @pyqtSlot(bool)
    def _on_ensemble_toggled(self, checked: bool) -> None:
        """Appelé quand la checkbox 'Mouvement d'ensemble' change."""
        self._current_projet.is_mouvement_ensemble = checked
        self._update_categorie()
        self.mark_as_dirty()

    @pyqtSlot()
    def _on_new(self) -> None:
        """Bouton / menu Nouveau."""
        self._new_project(confirm=True)

    @pyqtSlot()
    def _on_open(self) -> None:
        """Bouton / menu Ouvrir."""
        if not self._check_unsaved_changes():
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un projet de chorégraphie",
            "",
            XmlSerializer.FILE_FILTER,
        )

        if not file_path:
            return  # Annulé

        try:
            self._current_projet = XmlSerializer.load(file_path)
            self._current_file_path = file_path
            self._is_dirty = False
            self._refresh_ui()
            self._update_title()
            self._status_bar.showMessage(f"Projet chargé : {os.path.basename(file_path)}")
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Erreur d'ouverture",
                f"Impossible de charger le fichier :\n{ex}",
            )

    @pyqtSlot()
    def _on_save(self) -> None:
        """Bouton / menu Enregistrer."""
        self._save_project()

    @pyqtSlot()
    def _on_save_as(self) -> None:
        """Bouton / menu Enregistrer sous."""
        self._save_project(save_as=True)

    def _save_project(self, save_as: bool = False) -> bool:
        """
        Sauvegarde le projet courant.

        Paramètres
        ----------
        save_as : bool
            Si True, affiche toujours la boîte de dialogue de chemin.

        Retourne
        --------
        bool : True si la sauvegarde a réussi.
        """
        # Récupérer les données de l'UI avant de sauvegarder
        self._collect_ui_data()

        # Déterminer le chemin de sauvegarde
        if not self._current_file_path or save_as:
            default_name = self._current_projet.titre or "NouveauProjet"
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Enregistrer le projet de chorégraphie",
                default_name + XmlSerializer.FILE_EXTENSION,
                XmlSerializer.FILE_FILTER,
            )
            if not file_path:
                return False  # Annulé
            # Assurer l'extension correcte
            if not file_path.endswith(XmlSerializer.FILE_EXTENSION):
                file_path += XmlSerializer.FILE_EXTENSION
            self._current_file_path = file_path

        # Sauvegarder
        try:
            XmlSerializer.save(self._current_projet, self._current_file_path)
            self._is_dirty = False
            self._update_title()
            self._status_bar.showMessage(
                f"Projet enregistré : {os.path.basename(self._current_file_path)}"
            )
            return True
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Erreur d'enregistrement",
                f"Impossible de sauvegarder le fichier :\n{ex}",
            )
            return False

    @pyqtSlot()
    def _on_generate_pdf(self) -> None:
        """Bouton Générer PDF."""
        self._collect_ui_data()

        if not self._current_projet:
            QMessageBox.warning(self, "Erreur", "Aucun projet chargé.")
            return

        # Déterminer le format de page
        page_size_str = self.combo_page_size.currentText()

        # Demander le chemin de sauvegarde du PDF
        default_name = f"Chorégraphie_{self._current_projet.titre or 'Sans titre'}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer le PDF",
            default_name,
            "Fichiers PDF (*.pdf)",
        )

        if not file_path:
            return  # Annulé

        if not file_path.endswith(".pdf"):
            file_path += ".pdf"

        try:
            PdfExporter.generate(self._current_projet, file_path, page_size_str)
            QMessageBox.information(
                self,
                "PDF généré",
                f"Le PDF a été généré avec succès :\n{file_path}",
            )
            self._status_bar.showMessage(f"PDF généré : {os.path.basename(file_path)}")
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Erreur PDF",
                f"Erreur lors de la génération du PDF :\n{ex}",
            )

    @pyqtSlot()
    def _on_edit_combattants(self) -> None:
        """Ouvre le dialogue d'édition des combattants."""
        dialog = DialogCombattants(self._current_projet.liste_combattants, parent=self)
        if dialog.exec():
            self._current_projet.liste_combattants = dialog.get_liste()
            self._refresh_combattants_list()
            self._update_categorie()
            self.mark_as_dirty()

    @pyqtSlot()
    def _on_edit_assistants(self) -> None:
        """Ouvre le dialogue d'édition des assistants."""
        dialog = DialogAssistants(self._current_projet.liste_assistants, parent=self)
        if dialog.exec():
            self._current_projet.liste_assistants = dialog.get_liste()
            self._refresh_assistants_list()
            self.mark_as_dirty()

    @pyqtSlot()
    def _on_edit_choreographie(self) -> None:
        """Ouvre le dialogue d'édition des phrases d'armes."""
        self._collect_ui_data()
        dialog = DialogPhrases(self._current_projet, parent=self)
        if dialog.exec():
            self.mark_as_dirty()

    @pyqtSlot()
    def _on_about(self) -> None:
        """Affiche la boîte de dialogue À propos."""
        QMessageBox.about(
            self,
            "À propos — Éditeur Chorégraphique ASL-FFE",
            "<h3>Éditeur Chorégraphique ASL-FFE</h3>"
            "<p><b>Auteur : Vincent Thivolle de l'académie de la force de Metz</b></p>"
            "<p><b>Version 2.0</b> — Python / PyQt6</p>"
            "<p>Migration multiplateforme de l'éditeur VB.NET original.</p>"
            "<p>Compatible Windows, macOS et Linux.</p>"
            "<p>Les fichiers <code>.chore</code> (XML) créés avec la V1 "
            "sont entièrement compatibles avec cette V2.</p>"
            "<hr>"
            "<p><small>ASL-FFE — Escrime Artistique</small></p>",
        )

    # =========================================================================
    # ÉVÉNEMENT DE FERMETURE
    # =========================================================================

    def closeEvent(self, event: QCloseEvent) -> None:
        """Intercepte la fermeture pour proposer de sauvegarder si nécessaire."""
        if self._check_unsaved_changes():
            event.accept()
        else:
            event.ignore()
