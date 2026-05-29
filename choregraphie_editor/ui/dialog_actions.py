# -*- coding: utf-8 -*-
"""
Dialogue d'édition des actions d'une phrase d'armes.

Équivalent de FormEditActions.vb dans le projet VB.NET original.

Affiche un tableau (QTableWidget) dont :
- Les lignes représentent les actions (numérotées).
- Les colonnes représentent les champs de mouvement de chaque combattant
  (Main Droite, Zone MD, Cible MD*, Main Gauche, Zone MG, Cible MG*, Déplacement, Commentaire).
- Les colonnes Cible MD / Cible MG ne s'affichent que si le projet a > 2 combattants.

Les menus déroulants sont alimentés par le fichier OptionsMouvements.csv
via MouvementOptionsLoader.
"""

from typing import List, Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter, QListWidget,
    QTableWidget, QTableWidgetItem, QComboBox, QPushButton,
    QDialogButtonBox, QMessageBox, QLabel, QHeaderView,
    QAbstractItemView, QWidget, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QColor, QFont

from models.action import Action
from models.mouvement import Mouvement
from models.combattant import Combattant
from models.phrase_darmes import PhraseDArmes
from models.projet_choregraphique import ProjetChoregraphique
from models.mouvement_options_loader import MouvementOptionsLoader


class DialogActions(QDialog):
    """
    Dialogue d'édition des actions d'une phrase d'armes.

    Le tableau est construit dynamiquement selon le nombre de combattants.
    Chaque modification dans le tableau est directement répercutée dans
    les objets Action/Mouvement (pas de copie intermédiaire).
    """

    def __init__(
        self,
        phrase: PhraseDArmes,
        projet: ProjetChoregraphique,
        parent=None,
    ):
        super().__init__(parent)

        # Références directes (modifications en live)
        self._phrase = phrase
        self._projet = projet
        self._combattants: List[Combattant] = projet.liste_combattants

        # Charger les options de mouvements depuis le CSV
        self._options = MouvementOptionsLoader()

        # Indique si les colonnes "Cible" sont affichées (> 2 combattants)
        self._show_cible_cols: bool = len(self._combattants) > 2

        # Empêcher les boucles de mise à jour pendant le chargement du tableau
        self._loading: bool = False

        # Définition des colonnes par combattant
        self._build_column_definitions()

        self.setWindowTitle(f"Actions — Phrase {phrase.numero} : {phrase.description_section[:40]}")
        self.setMinimumSize(900, 560)
        self.resize(1100, 620)
        self.setModal(True)

        self._build_ui()
        self._connect_signals()
        self._populate_table()

    # =========================================================================
    # DÉFINITION DES COLONNES
    # =========================================================================

    def _build_column_definitions(self) -> None:
        """
        Construit la liste des colonnes en fonction des combattants.
        Chaque colonne est définie par un dict avec :
          - 'header': str   — texte de l'en-tête
          - 'combattant_id': int  — combattant associé
          - 'field': str    — nom du champ dans Mouvement
          - 'type': str     — 'combo' ou 'text'
          - 'options': list  — liste des options pour les ComboBox
        """
        self._col_defs = []  # [(header, combattant_id, field, type, options)]

        mains = self._options.get_mains_avec_vide()
        zones = self._options.get_zones_avec_vide()
        depls = self._options.get_deplacements_avec_vide()

        # Construire la liste des IDs pour les colonnes "Cible"
        cible_options = ["0"] + [str(c.id) for c in self._combattants]

        for c in self._combattants:
            short = f"{c.nom} {c.prenom} (ID:{c.id})"

            self._col_defs.append({
                "header": f"Main D\n{short}",
                "combattant_id": c.id,
                "field": "main_droite",
                "type": "combo",
                "options": mains,
            })
            self._col_defs.append({
                "header": f"Zone MD\n{short}",
                "combattant_id": c.id,
                "field": "zone_main_droite",
                "type": "combo",
                "options": zones,
            })
            if self._show_cible_cols:
                self._col_defs.append({
                    "header": f"Cible MD\n{short}",
                    "combattant_id": c.id,
                    "field": "cible_main_droite_id",
                    "type": "combo",
                    "options": cible_options,
                })
            self._col_defs.append({
                "header": f"Main G\n{short}",
                "combattant_id": c.id,
                "field": "main_gauche",
                "type": "combo",
                "options": mains,
            })
            self._col_defs.append({
                "header": f"Zone MG\n{short}",
                "combattant_id": c.id,
                "field": "zone_main_gauche",
                "type": "combo",
                "options": zones,
            })
            if self._show_cible_cols:
                self._col_defs.append({
                    "header": f"Cible MG\n{short}",
                    "combattant_id": c.id,
                    "field": "cible_main_gauche_id",
                    "type": "combo",
                    "options": cible_options,
                })
            self._col_defs.append({
                "header": f"Déplacement\n{short}",
                "combattant_id": c.id,
                "field": "deplacement",
                "type": "combo",
                "options": depls,
            })
            self._col_defs.append({
                "header": f"Commentaire\n{short}",
                "combattant_id": c.id,
                "field": "commentaire",
                "type": "text",
                "options": [],
            })

    # =========================================================================
    # CONSTRUCTION DE L'INTERFACE
    # =========================================================================

    def _build_ui(self) -> None:
        """Construit l'interface du dialogue."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(6)

        # Titre de la phrase
        title_lbl = QLabel(
            f"<b>Phrase {self._phrase.numero}</b> — {self._phrase.description_section}"
        )
        main_layout.addWidget(title_lbl)

        # Splitter : liste des combattants (info) | tableau des actions
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Panneau gauche : liste des combattants (lecture seule, pour référence) ---
        combattants_group = QGroupBox("Combattants")
        c_layout = QVBoxLayout(combattants_group)
        self.list_combattants = QListWidget()
        self.list_combattants.setMaximumWidth(200)
        for c in self._combattants:
            self.list_combattants.addItem(f"ID {c.id} — {c.prenom} {c.nom}")
        c_layout.addWidget(self.list_combattants)
        splitter.addWidget(combattants_group)

        # --- Panneau droit : tableau des actions ---
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Boutons de gestion des actions
        actions_btn_layout = QHBoxLayout()
        self.btn_add_action = QPushButton("+ Ajouter action")
        self.btn_delete_action = QPushButton("Supprimer action")
        self.btn_delete_action.setProperty("danger", "true")
        self.btn_move_up = QPushButton("▲ Monter")
        self.btn_move_up.setProperty("secondary", "true")
        self.btn_move_down = QPushButton("▼ Descendre")
        self.btn_move_down.setProperty("secondary", "true")

        for btn in [self.btn_add_action, self.btn_delete_action,
                    self.btn_move_up, self.btn_move_down]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        actions_btn_layout.addWidget(self.btn_add_action)
        actions_btn_layout.addWidget(self.btn_delete_action)
        actions_btn_layout.addWidget(self.btn_move_up)
        actions_btn_layout.addWidget(self.btn_move_down)
        actions_btn_layout.addStretch()
        right_layout.addLayout(actions_btn_layout)

        # Tableau des actions
        nb_cols = len(self._col_defs)
        self.table = QTableWidget(0, nb_cols)

        # En-têtes des colonnes
        headers = [col["header"] for col in self._col_defs]
        self.table.setHorizontalHeaderLabels(headers)

        # Style du tableau
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setMinimumSectionSize(80)
        self.table.verticalHeader().setDefaultSectionSize(30)
        # Numéros de ligne = numéros d'action
        self.table.verticalHeader().setVisible(True)

        right_layout.addWidget(self.table)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 880])

        main_layout.addWidget(splitter, stretch=1)

        # Boutons de fermeture
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Valider et fermer")
        button_box.button(QDialogButtonBox.StandardButton.Close).setText("Fermer")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def _connect_signals(self) -> None:
        """Connecte les signaux."""
        self.btn_add_action.clicked.connect(self._on_add_action)
        self.btn_delete_action.clicked.connect(self._on_delete_action)
        self.btn_move_up.clicked.connect(self._on_move_up)
        self.btn_move_down.clicked.connect(self._on_move_down)
        self.table.selectionModel().selectionChanged.connect(self._update_button_states)
        self.table.itemChanged.connect(self._on_item_changed)

    # =========================================================================
    # REMPLISSAGE DU TABLEAU
    # =========================================================================

    def _populate_table(self) -> None:
        """
        Remplit le tableau avec les données de la phrase d'armes.
        Équivalent de PopulateActionsDataTable() dans FormEditActions.vb.
        """
        self._loading = True
        self.table.setRowCount(0)  # Vider le tableau

        for action in sorted(self._phrase.liste_actions, key=lambda a: a.numero_action):
            self._add_row_for_action(action)

        self.table.resizeColumnsToContents()
        self._loading = False
        self._update_button_states()

    def _add_row_for_action(self, action: Action) -> int:
        """
        Ajoute une ligne dans le tableau pour une action donnée.
        Retourne l'index de la nouvelle ligne.
        """
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Numéro de ligne dans l'en-tête vertical = numéro d'action
        header_item = QTableWidgetItem(str(action.numero_action))
        self.table.setVerticalHeaderItem(row, header_item)

        # Remplir chaque colonne
        for col_idx, col_def in enumerate(self._col_defs):
            combattant_id = col_def["combattant_id"]
            field = col_def["field"]
            col_type = col_def["type"]
            options = col_def["options"]

            # Récupérer le mouvement du combattant pour cette action
            mouvement = action.get_mouvement_pour_combattant(combattant_id)

            # Valeur courante du champ
            if mouvement is not None:
                raw_val = getattr(mouvement, field, "")
                value = str(raw_val) if raw_val is not None else ""
            else:
                value = "0" if "cible" in field else ""

            if col_type == "combo":
                # Créer un widget ComboBox pour la cellule
                combo = QComboBox()
                combo.addItems(options)
                # Sélectionner la valeur courante
                idx = combo.findText(value)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
                else:
                    combo.setCurrentIndex(0)
                # Stocker (row, col_idx) pour identifier la cellule lors des changements
                combo.currentTextChanged.connect(
                    lambda text, r=row, c=col_idx: self._on_combo_changed(r, c, text)
                )
                self.table.setCellWidget(row, col_idx, combo)
            else:
                # Cellule texte simple
                item = QTableWidgetItem(value)
                self.table.setItem(row, col_idx, item)

        return row

    def _get_action_at_row(self, row: int) -> Optional[Action]:
        """Retourne l'action correspondant à une ligne du tableau."""
        if row < 0 or row >= len(self._phrase.liste_actions):
            return None
        return sorted(self._phrase.liste_actions, key=lambda a: a.numero_action)[row]

    def _update_button_states(self) -> None:
        """Active/désactive les boutons selon la sélection dans le tableau."""
        row = self.table.currentRow()
        count = self.table.rowCount()
        has_selection = row >= 0
        self.btn_delete_action.setEnabled(has_selection)
        self.btn_move_up.setEnabled(row > 0)
        self.btn_move_down.setEnabled(has_selection and row < count - 1)

    # =========================================================================
    # MISE À JOUR DES DONNÉES (Tableau → Objets)
    # =========================================================================

    def _ensure_mouvement(self, action: Action, combattant_id: int) -> Mouvement:
        """
        Retourne le mouvement d'un combattant dans une action,
        en le créant s'il n'existe pas encore.
        """
        mouvement = action.get_mouvement_pour_combattant(combattant_id)
        if mouvement is None:
            mouvement = Mouvement(combattant_id=combattant_id)
            action.mouvements.append(mouvement)
        return mouvement

    def _update_mouvement_field(self, row: int, col_idx: int, value: str) -> None:
        """
        Met à jour le champ d'un mouvement depuis le tableau.
        Appelé par _on_combo_changed et _on_item_changed.
        """
        if self._loading:
            return

        action = self._get_action_at_row(row)
        if action is None:
            return

        col_def = self._col_defs[col_idx]
        combattant_id = col_def["combattant_id"]
        field = col_def["field"]

        mouvement = self._ensure_mouvement(action, combattant_id)

        # Appliquer la valeur selon le type de champ
        if "cible" in field:
            # Les champs cible sont des entiers
            try:
                setattr(mouvement, field, int(value) if value else 0)
            except ValueError:
                setattr(mouvement, field, 0)
        else:
            setattr(mouvement, field, value)

    # =========================================================================
    # SLOTS
    # =========================================================================

    @pyqtSlot(int, int, str)
    def _on_combo_changed(self, row: int, col_idx: int, text: str) -> None:
        """Appelé quand la valeur d'un ComboBox change dans le tableau."""
        self._update_mouvement_field(row, col_idx, text)

    @pyqtSlot(QTableWidgetItem)
    def _on_item_changed(self, item: QTableWidgetItem) -> None:
        """Appelé quand un QTableWidgetItem (cellule texte) est modifié."""
        self._update_mouvement_field(item.row(), item.column(), item.text())

    @pyqtSlot()
    def _on_add_action(self) -> None:
        """Ajoute une nouvelle action vide à la phrase."""
        # Numéro de la nouvelle action = max existant + 1
        actions = self._phrase.liste_actions
        next_num = max((a.numero_action for a in actions), default=0) + 1

        new_action = Action(numero_action=next_num)

        # Initialiser un mouvement vide pour chaque combattant
        for c in self._combattants:
            new_action.mouvements.append(Mouvement(combattant_id=c.id))

        actions.append(new_action)

        # Ajouter la ligne dans le tableau
        self._loading = True
        self._add_row_for_action(new_action)
        self._loading = False

        # Sélectionner la nouvelle ligne
        self.table.setCurrentCell(self.table.rowCount() - 1, 0)
        self._update_button_states()

    @pyqtSlot()
    def _on_delete_action(self) -> None:
        """Supprime l'action sélectionnée."""
        row = self.table.currentRow()
        if row < 0:
            return

        action = self._get_action_at_row(row)
        if action is None:
            return

        reply = QMessageBox.question(
            self,
            "Confirmer la suppression",
            f"Supprimer l'action numéro {action.numero_action} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._phrase.liste_actions.remove(action)
            # Renuméroter les actions restantes
            for i, a in enumerate(
                sorted(self._phrase.liste_actions, key=lambda x: x.numero_action)
            ):
                a.numero_action = i + 1
            self._populate_table()

    @pyqtSlot()
    def _on_move_up(self) -> None:
        """Déplace l'action sélectionnée d'un rang vers le haut."""
        row = self.table.currentRow()
        if row <= 0:
            return

        actions = sorted(self._phrase.liste_actions, key=lambda a: a.numero_action)
        # Échanger les numéros des deux actions adjacentes
        actions[row].numero_action, actions[row - 1].numero_action = (
            actions[row - 1].numero_action,
            actions[row].numero_action,
        )
        self._populate_table()
        self.table.setCurrentCell(row - 1, self.table.currentColumn())

    @pyqtSlot()
    def _on_move_down(self) -> None:
        """Déplace l'action sélectionnée d'un rang vers le bas."""
        row = self.table.currentRow()
        actions = sorted(self._phrase.liste_actions, key=lambda a: a.numero_action)
        if row < 0 or row >= len(actions) - 1:
            return

        actions[row].numero_action, actions[row + 1].numero_action = (
            actions[row + 1].numero_action,
            actions[row].numero_action,
        )
        self._populate_table()
        self.table.setCurrentCell(row + 1, self.table.currentColumn())
