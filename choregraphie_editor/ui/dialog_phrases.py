# -*- coding: utf-8 -*-
"""
Dialogue d'édition des phrases d'armes.

Équivalent de FormEditPhraseDArmes.vb dans le projet VB.NET original.
Permet de créer, modifier, réordonner et supprimer les phrases d'armes,
et d'ouvrir le dialogue d'édition des actions pour chaque phrase.
"""

from PyQt6.QtWidgets import (
    QDialog, QHBoxLayout, QVBoxLayout, QListWidget,
    QGroupBox, QFormLayout, QLineEdit, QTextEdit, QPushButton,
    QDialogButtonBox, QMessageBox, QLabel, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSlot

from models.projet_choregraphique import ProjetChoregraphique
from models.phrase_darmes import PhraseDArmes
from ui.dialog_actions import DialogActions


class DialogPhrases(QDialog):
    """
    Dialogue modal pour gérer les phrases d'armes de la chorégraphie.

    Modifie directement le ProjetChoregraphique passé en référence,
    puisque les actions sont imbriquées dans les phrases.
    """

    def __init__(self, projet: ProjetChoregraphique, parent=None):
        super().__init__(parent)

        # Référence directe au projet (les modifications sont appliquées en live)
        self._projet = projet
        # Phrase actuellement sélectionnée
        self._selected: PhraseDArmes | None = None

        self.setWindowTitle("Édition des Phrases d'Armes")
        self.setMinimumSize(800, 520)
        self.resize(900, 580)
        self.setModal(True)

        self._build_ui()
        self._connect_signals()
        self._reassign_numbers()
        self._refresh_list()
        self._clear_form()

    # =========================================================================
    # CONSTRUCTION DE L'INTERFACE
    # =========================================================================

    def _build_ui(self) -> None:
        """Construit l'interface du dialogue."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)

        # Splitter horizontal : liste à gauche, détails à droite
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Liste des phrases (gauche) ---
        left_widget = QGroupBox("Phrases d'armes")
        left_layout = QVBoxLayout(left_widget)

        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setMinimumWidth(260)
        left_layout.addWidget(self.list_widget)

        # Boutons de déplacement
        move_layout = QHBoxLayout()
        self.btn_move_up = QPushButton("▲ Monter")
        self.btn_move_up.setProperty("secondary", "true")
        self.btn_move_down = QPushButton("▼ Descendre")
        self.btn_move_down.setProperty("secondary", "true")
        for btn in [self.btn_move_up, self.btn_move_down]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        move_layout.addWidget(self.btn_move_up)
        move_layout.addWidget(self.btn_move_down)
        left_layout.addLayout(move_layout)

        splitter.addWidget(left_widget)

        # --- Détails de la phrase sélectionnée (droite) ---
        right_widget = QGroupBox("Détails de la phrase")
        right_layout = QVBoxLayout(right_widget)

        form = QFormLayout()
        form.setSpacing(8)

        self.edit_numero = QLineEdit()
        self.edit_numero.setReadOnly(True)
        self.edit_numero.setStyleSheet("background-color: #eeeeee;")
        self.edit_numero.setMaximumWidth(80)
        form.addRow("Numéro :", self.edit_numero)

        self.edit_description = QTextEdit()
        self.edit_description.setPlaceholderText(
            "Décrivez le contenu ou l'intention de cette phrase d'armes..."
        )
        self.edit_description.setMaximumHeight(120)
        form.addRow("Description :", self.edit_description)

        right_layout.addLayout(form)

        # Boutons CRUD de la phrase
        crud_layout = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter phrase")
        self.btn_update = QPushButton("Mettre à jour")
        self.btn_update.setProperty("secondary", "true")
        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.setProperty("danger", "true")
        self.btn_edit_actions = QPushButton("Éditer les Actions →")
        self.btn_edit_actions.setProperty("success", "true")

        for btn in [self.btn_add, self.btn_update, self.btn_delete, self.btn_edit_actions]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        crud_layout.addWidget(self.btn_add)
        crud_layout.addWidget(self.btn_update)
        crud_layout.addWidget(self.btn_delete)
        crud_layout.addStretch()
        crud_layout.addWidget(self.btn_edit_actions)

        right_layout.addLayout(crud_layout)
        right_layout.addStretch()

        # Résumé des actions de la phrase sélectionnée
        self.lbl_actions_count = QLabel("Aucune phrase sélectionnée.")
        self.lbl_actions_count.setStyleSheet("color: #666; font-style: italic;")
        right_layout.addWidget(self.lbl_actions_count)

        splitter.addWidget(right_widget)
        splitter.setSizes([280, 600])

        main_layout.addWidget(splitter, stretch=1)

        # Boutons de validation
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Valider et fermer")
        button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Fermer")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def _connect_signals(self) -> None:
        """Connecte les signaux."""
        self.list_widget.currentRowChanged.connect(self._on_selection_changed)
        self.btn_add.clicked.connect(self._on_add)
        self.btn_update.clicked.connect(self._on_update)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_move_up.clicked.connect(self._on_move_up)
        self.btn_move_down.clicked.connect(self._on_move_down)
        self.btn_edit_actions.clicked.connect(self._on_edit_actions)

    # =========================================================================
    # GESTION DE L'AFFICHAGE
    # =========================================================================

    def _reassign_numbers(self) -> None:
        """
        Réassigne les numéros séquentiels (1, 2, 3...) aux phrases
        après tout ajout, suppression ou déplacement.
        Équivalent de ReassignPhraseNumbers() dans FormEditPhraseDArmes.vb.
        """
        # Trier par numéro courant avant de renuméroter
        self._projet.choregraphie_sections.sort(key=lambda p: p.numero)
        for i, phrase in enumerate(self._projet.choregraphie_sections):
            phrase.numero = i + 1

    def _refresh_list(self) -> None:
        """Rafraîchit la liste des phrases dans le widget."""
        current_row = self.list_widget.currentRow()
        self.list_widget.clear()
        for phrase in self._projet.choregraphie_sections:
            self.list_widget.addItem(str(phrase))
        # Restaurer la sélection si possible
        if 0 <= current_row < self.list_widget.count():
            self.list_widget.setCurrentRow(current_row)
        self._update_move_buttons()

    def _clear_form(self) -> None:
        """Vide le formulaire et désactive les boutons dépendant d'une sélection."""
        self.edit_numero.setText("")
        self.edit_description.setPlainText("")
        self._selected = None
        self.btn_update.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_edit_actions.setEnabled(False)
        self.lbl_actions_count.setText("Aucune phrase sélectionnée.")
        self._update_move_buttons()

    def _display_phrase(self, phrase: PhraseDArmes) -> None:
        """Affiche les détails d'une phrase dans le formulaire."""
        self.edit_numero.setText(str(phrase.numero))
        self.edit_description.setPlainText(phrase.description_section)
        self._selected = phrase
        self.btn_update.setEnabled(True)
        self.btn_delete.setEnabled(True)
        self.btn_edit_actions.setEnabled(True)
        nb = len(phrase.liste_actions)
        self.lbl_actions_count.setText(f"{nb} action(s) dans cette phrase.")
        self._update_move_buttons()

    def _update_move_buttons(self) -> None:
        """Active/désactive les boutons Monter/Descendre selon la sélection."""
        row = self.list_widget.currentRow()
        count = self.list_widget.count()
        self.btn_move_up.setEnabled(row > 0)
        self.btn_move_down.setEnabled(0 <= row < count - 1)

    # =========================================================================
    # SLOTS
    # =========================================================================

    @pyqtSlot(int)
    def _on_selection_changed(self, row: int) -> None:
        """Affiche les détails de la phrase sélectionnée."""
        sections = self._projet.choregraphie_sections
        if row < 0 or row >= len(sections):
            self._clear_form()
            return
        self._display_phrase(sections[row])

    @pyqtSlot()
    def _on_add(self) -> None:
        """Ajoute une nouvelle phrase d'armes."""
        desc = self.edit_description.toPlainText().strip()
        if not desc:
            QMessageBox.warning(
                self, "Saisie incomplète",
                "La description de la phrase est obligatoire."
            )
            self.edit_description.setFocus()
            return

        # Calculer le prochain numéro
        sections = self._projet.choregraphie_sections
        next_num = max((p.numero for p in sections), default=0) + 1

        nouvelle = PhraseDArmes(numero=next_num, description_section=desc)
        sections.append(nouvelle)
        self._reassign_numbers()
        self._refresh_list()
        self.edit_description.setPlainText("")
        # Sélectionner la nouvelle phrase
        self.list_widget.setCurrentRow(len(sections) - 1)

        if self.parent():
            self.parent().mark_as_dirty()

    @pyqtSlot()
    def _on_update(self) -> None:
        """Met à jour la description de la phrase sélectionnée."""
        if self._selected is None:
            QMessageBox.information(self, "Attention", "Veuillez sélectionner une phrase.")
            return

        desc = self.edit_description.toPlainText().strip()
        if not desc:
            QMessageBox.warning(
                self, "Saisie incomplète",
                "La description de la phrase est obligatoire."
            )
            return

        self._selected.description_section = desc
        current_row = self.list_widget.currentRow()
        self._refresh_list()
        self.list_widget.setCurrentRow(current_row)

        if self.parent():
            self.parent().mark_as_dirty()

    @pyqtSlot()
    def _on_delete(self) -> None:
        """Supprime la phrase sélectionnée après confirmation."""
        if self._selected is None:
            QMessageBox.information(self, "Attention", "Veuillez sélectionner une phrase.")
            return

        reply = QMessageBox.question(
            self,
            "Confirmer la suppression",
            f"Supprimer '{str(self._selected)}' et toutes ses actions ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = self.list_widget.currentRow()
            self._projet.choregraphie_sections.remove(self._selected)
            self._reassign_numbers()
            self._refresh_list()

            # Sélectionner l'élément voisin
            count = self.list_widget.count()
            if count > 0:
                new_row = min(row, count - 1)
                self.list_widget.setCurrentRow(new_row)
            else:
                self._clear_form()

            if self.parent():
                self.parent().mark_as_dirty()

    @pyqtSlot()
    def _on_move_up(self) -> None:
        """Déplace la phrase sélectionnée d'un rang vers le haut."""
        row = self.list_widget.currentRow()
        if row <= 0:
            return

        sections = self._projet.choregraphie_sections
        # Échanger les numéros des deux phrases adjacentes
        sections[row].numero, sections[row - 1].numero = (
            sections[row - 1].numero,
            sections[row].numero,
        )
        self._reassign_numbers()
        self._refresh_list()
        self.list_widget.setCurrentRow(row - 1)

        if self.parent():
            self.parent().mark_as_dirty()

    @pyqtSlot()
    def _on_move_down(self) -> None:
        """Déplace la phrase sélectionnée d'un rang vers le bas."""
        row = self.list_widget.currentRow()
        sections = self._projet.choregraphie_sections
        if row < 0 or row >= len(sections) - 1:
            return

        # Échanger les numéros des deux phrases adjacentes
        sections[row].numero, sections[row + 1].numero = (
            sections[row + 1].numero,
            sections[row].numero,
        )
        self._reassign_numbers()
        self._refresh_list()
        self.list_widget.setCurrentRow(row + 1)

        if self.parent():
            self.parent().mark_as_dirty()

    @pyqtSlot()
    def _on_edit_actions(self) -> None:
        """Ouvre le dialogue d'édition des actions pour la phrase sélectionnée."""
        if self._selected is None:
            QMessageBox.information(
                self, "Aucune phrase",
                "Veuillez sélectionner une phrase d'armes pour éditer ses actions."
            )
            return

        dialog = DialogActions(
            phrase=self._selected,
            projet=self._projet,
            parent=self,
        )
        dialog.exec()

        # Mettre à jour le résumé des actions
        if self._selected:
            nb = len(self._selected.liste_actions)
            self.lbl_actions_count.setText(f"{nb} action(s) dans cette phrase.")

        if self.parent():
            self.parent().mark_as_dirty()
