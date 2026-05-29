# -*- coding: utf-8 -*-
"""
Dialogue d'édition des assistants plateau.

Équivalent de FormEditAssistants.vb dans le projet VB.NET original.
Permet d'ajouter, modifier et supprimer des assistants dans le projet.
"""

import copy
from typing import List

from PyQt6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget,
    QGroupBox, QFormLayout, QLineEdit, QPushButton,
    QDialogButtonBox, QMessageBox, QLabel
)
from PyQt6.QtCore import Qt, pyqtSlot

from models.assistant import Assistant


class DialogAssistants(QDialog):
    """
    Dialogue modal pour gérer la liste des assistants plateau du projet.

    Reçoit une copie de la liste, l'utilisateur peut éditer librement,
    et la liste finale est récupérée via get_liste() si DialogResult.OK.
    """

    def __init__(self, liste_assistants: List[Assistant], parent=None):
        super().__init__(parent)

        # On travaille sur une copie profonde pour pouvoir annuler
        self._liste: List[Assistant] = copy.deepcopy(liste_assistants)
        # Assistant actuellement sélectionné pour édition
        self._selected: Assistant | None = None

        self.setWindowTitle("Édition des Assistants Plateau")
        self.setMinimumSize(720, 360)
        self.resize(760, 400)
        self.setModal(True)

        self._build_ui()
        self._connect_signals()
        self._refresh_list()
        self._clear_form()

    # =========================================================================
    # CONSTRUCTION DE L'INTERFACE
    # =========================================================================

    def _build_ui(self) -> None:
        """Construit l'interface du dialogue."""
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)

        # --- Liste des assistants (gauche) ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Assistants du projet :"))
        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setMinimumWidth(280)
        left_layout.addWidget(self.list_widget)
        main_layout.addLayout(left_layout, stretch=1)

        # --- Panneau de détails (droite) ---
        right_layout = QVBoxLayout()

        # Formulaire de détails
        details_group = QGroupBox("Détails de l'assistant")
        form = QFormLayout(details_group)
        form.setSpacing(8)

        self.edit_nom = QLineEdit()
        self.edit_nom.setPlaceholderText("Nom de famille...")
        form.addRow("Nom * :", self.edit_nom)

        self.edit_prenom = QLineEdit()
        self.edit_prenom.setPlaceholderText("Prénom...")
        form.addRow("Prénom * :", self.edit_prenom)

        self.edit_licence = QLineEdit()
        self.edit_licence.setPlaceholderText("Numéro de licence FFE...")
        form.addRow("Licence :", self.edit_licence)

        self.edit_role = QLineEdit()
        self.edit_role.setPlaceholderText("Ex: Narrateur, Figurant, Éclairagiste...")
        form.addRow("Rôle :", self.edit_role)

        right_layout.addWidget(details_group)

        # Boutons d'action sur la liste
        actions_layout = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter")
        self.btn_update = QPushButton("Mettre à jour")
        self.btn_update.setProperty("secondary", "true")
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.setProperty("danger", "true")

        for btn in [self.btn_add, self.btn_update, self.btn_delete]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        actions_layout.addWidget(self.btn_add)
        actions_layout.addWidget(self.btn_update)
        actions_layout.addWidget(self.btn_delete)
        actions_layout.addStretch()
        right_layout.addLayout(actions_layout)
        right_layout.addStretch()

        # Boutons OK / Annuler
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Valider et fermer")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Annuler")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        right_layout.addWidget(button_box)

        main_layout.addLayout(right_layout, stretch=1)

    def _connect_signals(self) -> None:
        """Connecte les signaux."""
        self.list_widget.currentRowChanged.connect(self._on_selection_changed)
        self.btn_add.clicked.connect(self._on_add)
        self.btn_update.clicked.connect(self._on_update)
        self.btn_delete.clicked.connect(self._on_delete)

    # =========================================================================
    # GESTION DE L'AFFICHAGE
    # =========================================================================

    def _refresh_list(self) -> None:
        """Rafraîchit la liste des assistants dans le widget."""
        self.list_widget.clear()
        for a in self._liste:
            self.list_widget.addItem(str(a))

    def _clear_form(self) -> None:
        """Vide le formulaire de détails et désactive les boutons d'édition."""
        self.edit_nom.setText("")
        self.edit_prenom.setText("")
        self.edit_licence.setText("")
        self.edit_role.setText("")
        self._selected = None
        self.btn_update.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.edit_nom.setFocus()

    def _display_assistant(self, assistant: Assistant) -> None:
        """Affiche les détails d'un assistant dans le formulaire."""
        self.edit_nom.setText(assistant.nom)
        self.edit_prenom.setText(assistant.prenom)
        self.edit_licence.setText(assistant.numero_licence)
        self.edit_role.setText(assistant.role)
        self._selected = assistant
        self.btn_update.setEnabled(True)
        self.btn_delete.setEnabled(True)

    def _validate_form(self) -> bool:
        """Vérifie que les champs obligatoires sont remplis."""
        if not self.edit_nom.text().strip():
            QMessageBox.warning(self, "Saisie incomplète", "Le nom est obligatoire.")
            self.edit_nom.setFocus()
            return False
        if not self.edit_prenom.text().strip():
            QMessageBox.warning(self, "Saisie incomplète", "Le prénom est obligatoire.")
            self.edit_prenom.setFocus()
            return False
        return True

    # =========================================================================
    # SLOTS
    # =========================================================================

    @pyqtSlot(int)
    def _on_selection_changed(self, row: int) -> None:
        """Affiche les détails de l'assistant sélectionné."""
        if row < 0 or row >= len(self._liste):
            self._clear_form()
            return
        self._display_assistant(self._liste[row])

    @pyqtSlot()
    def _on_add(self) -> None:
        """Ajoute un nouvel assistant à la liste."""
        if not self._validate_form():
            return

        nouveau = Assistant(
            nom=self.edit_nom.text().strip(),
            prenom=self.edit_prenom.text().strip(),
            numero_licence=self.edit_licence.text().strip(),
            role=self.edit_role.text().strip(),
        )
        self._liste.append(nouveau)
        self._refresh_list()
        self._clear_form()
        self.list_widget.setCurrentRow(len(self._liste) - 1)

    @pyqtSlot()
    def _on_update(self) -> None:
        """Met à jour l'assistant sélectionné avec les données du formulaire."""
        if self._selected is None:
            QMessageBox.information(self, "Attention", "Veuillez sélectionner un assistant.")
            return
        if not self._validate_form():
            return

        self._selected.nom = self.edit_nom.text().strip()
        self._selected.prenom = self.edit_prenom.text().strip()
        self._selected.numero_licence = self.edit_licence.text().strip()
        self._selected.role = self.edit_role.text().strip()

        current_row = self.list_widget.currentRow()
        self._refresh_list()
        self.list_widget.setCurrentRow(current_row)

    @pyqtSlot()
    def _on_delete(self) -> None:
        """Supprime l'assistant sélectionné après confirmation."""
        if self._selected is None:
            QMessageBox.information(self, "Attention", "Veuillez sélectionner un assistant.")
            return

        reply = QMessageBox.question(
            self,
            "Confirmer la suppression",
            f"Supprimer {self._selected.prenom} {self._selected.nom} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._liste.remove(self._selected)
            self._refresh_list()
            self._clear_form()

    # =========================================================================
    # API PUBLIQUE
    # =========================================================================

    def get_liste(self) -> List[Assistant]:
        """Retourne la liste des assistants éditée (après validation)."""
        return self._liste
