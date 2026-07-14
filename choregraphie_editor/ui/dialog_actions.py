# -*- coding: utf-8 -*-
"""
Dialogue d'édition des actions d'une phrase d'armes — Version 2.1

Améliorations ergonomiques v2.1 :
  - Colonnes colorées par combattant, adaptées au thème clair ET sombre
  - Légende visuelle (cartes colorées) dans le panneau gauche
  - ComboBox Cible affichant le nom du combattant au lieu de l'ID brut
  - Texte toujours lisible quel que soit le thème (contraste garanti)
"""

from typing import List, Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter, QListWidget,
    QTableWidget, QTableWidgetItem, QComboBox, QPushButton,
    QDialogButtonBox, QMessageBox, QLabel, QHeaderView,
    QAbstractItemView, QWidget, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QColor, QBrush, QFont

from models.action import Action
from models.mouvement import Mouvement
from models.combattant import Combattant
from models.phrase_darmes import PhraseDArmes
from models.projet_choregraphique import ProjetChoregraphique
from models.mouvement_options_loader import MouvementOptionsLoader
from ui.combattant_colors import (
    get_palette, get_bg, get_header, get_text,
    qt_bg, qt_header, qt_text, badge_style
)


class DialogActions(QDialog):
    """
    Dialogue d'édition des actions d'une phrase d'armes.

    Le tableau est construit dynamiquement selon le nombre de combattants.
    Les couleurs s'adaptent automatiquement au thème clair ou sombre actif.
    """

    def __init__(self, phrase: PhraseDArmes, projet: ProjetChoregraphique, parent=None):
        super().__init__(parent)

        self._phrase = phrase
        self._projet = projet
        self._combattants: List[Combattant] = projet.liste_combattants

        # Mapping ID combattant → index palette (stable, trié par ID)
        sorted_ids = sorted(c.id for c in self._combattants)
        self._color_index: dict[int, int] = {cid: i for i, cid in enumerate(sorted_ids)}

        self._options = MouvementOptionsLoader()
        self._show_cible_cols: bool = len(self._combattants) > 2
        self._loading: bool = False

        self._build_column_definitions()

        self.setWindowTitle(
            f"Actions — Phrase {phrase.numero} : {phrase.description_section[:50]}"
        )
        self.setMinimumSize(950, 580)
        self.resize(1200, 660)
        self.setModal(True)

        self._build_ui()
        self._connect_signals()
        self._populate_table()

    def _ci(self, combattant_id: int) -> int:
        """Index de palette pour un combattant donné."""
        return self._color_index.get(combattant_id, 0)

    # =========================================================================
    # DÉFINITION DES COLONNES
    # =========================================================================

    def _build_column_definitions(self) -> None:
        """
        Construit la liste des colonnes en fonction des combattants.
        Pour les colonnes "cible", le type est 'cible' (traitement spécial).
        """
        self._col_defs = []

        mains = self._options.get_mains_avec_vide()
        zones = self._options.get_zones_avec_vide()
        depls = self._options.get_deplacements_avec_vide()

        for c in self._combattants:
            ci = self._ci(c.id)
            short = c.prenom if len(c.prenom) <= 10 else c.prenom[:8] + "."

            # Options de cible : "— Aucune" + un item par combattant
            cible_options = ["— Aucune"] + [
                f"{other.prenom} {other.nom}" for other in self._combattants
            ]

            def col(header, field, col_type, options, _ci=ci):
                return {
                    "header": header,
                    "combattant_id": c.id,
                    "field": field,
                    "type": col_type,
                    "options": options,
                    "color_index": _ci,
                }

            self._col_defs.append(col(f"Main D\n{short}",      "main_droite",          "combo", mains))
            self._col_defs.append(col(f"Zone MD\n{short}",     "zone_main_droite",     "combo", zones))
            if self._show_cible_cols:
                self._col_defs.append(col(f"🎯 Cible MD\n{short}", "cible_main_droite_id", "cible", cible_options))
            self._col_defs.append(col(f"Main G\n{short}",      "main_gauche",          "combo", mains))
            self._col_defs.append(col(f"Zone MG\n{short}",     "zone_main_gauche",     "combo", zones))
            if self._show_cible_cols:
                self._col_defs.append(col(f"🎯 Cible MG\n{short}", "cible_main_gauche_id", "cible", cible_options))
            self._col_defs.append(col(f"Déplacement\n{short}", "deplacement",          "combo", depls))
            self._col_defs.append(col(f"Commentaire\n{short}", "commentaire",          "text",  []))

    # =========================================================================
    # CONSTRUCTION DE L'INTERFACE
    # =========================================================================

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Bandeau titre
        title_frame = QFrame()
        title_frame.setStyleSheet(
            "QFrame { background: #2c3e50; border-radius: 6px; padding: 4px; }"
        )
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(10, 4, 10, 4)
        lbl = QLabel(
            f"<span style='color:white; font-size:13px; font-weight:bold;'>"
            f"Phrase {self._phrase.numero}</span>"
            f"<span style='color:#aaa; font-size:12px;'>"
            f"  —  {self._phrase.description_section}</span>"
        )
        lbl.setTextFormat(Qt.TextFormat.RichText)
        title_layout.addWidget(lbl)
        main_layout.addWidget(title_frame)

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_legend_panel())

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)
        right_layout.addLayout(self._build_action_buttons())
        right_layout.addWidget(self._build_table())
        splitter.addWidget(right_widget)
        splitter.setSizes([230, 970])
        main_layout.addWidget(splitter, stretch=1)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close
        )
        button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Valider et fermer")
        button_box.button(QDialogButtonBox.StandardButton.Close).setText("Fermer")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def _build_legend_panel(self) -> QGroupBox:
        """
        Panneau gauche : une carte colorée par combattant.
        Les couleurs utilisées ici sont celles du thème actif (clair/sombre).
        """
        group = QGroupBox("Combattants")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 12, 8, 8)

        for c in self._combattants:
            ci = self._ci(c.id)
            bg     = get_bg(ci)
            header = get_header(ci)
            text   = get_text(ci)

            card = QFrame()
            card.setStyleSheet(
                f"QFrame {{"
                f"  background-color: {bg};"
                f"  border: 2px solid {header};"
                f"  border-radius: 8px;"
                f"}}"
            )
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(2)
            card_layout.setContentsMargins(8, 6, 8, 6)

            # Badge ID — toujours fond coloré + texte blanc
            lbl_id = QLabel(f"  ID {c.id}  ")
            lbl_id.setStyleSheet(badge_style(ci))
            lbl_id.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_id.setMaximumWidth(70)

            # Nom — couleur de texte adaptée au thème
            lbl_nom = QLabel(f"<b>{c.prenom} {c.nom}</b>")
            lbl_nom.setStyleSheet(f"color: {text}; font-size: 11px; background: transparent;")
            lbl_nom.setWordWrap(True)

            top_row = QHBoxLayout()
            top_row.addWidget(lbl_id)
            top_row.addWidget(lbl_nom, stretch=1)
            card_layout.addLayout(top_row)

            if c.numero_licence:
                lbl_lic = QLabel(f"Licence : {c.numero_licence}")
                lbl_lic.setStyleSheet(f"color: {text}; font-size: 9px; background: transparent;")
                card_layout.addWidget(lbl_lic)

            if c.capitaine:
                lbl_cap = QLabel("⭐ Capitaine")
                lbl_cap.setStyleSheet(
                    f"color: {header}; font-size: 9px; font-weight: bold; background: transparent;"
                )
                card_layout.addWidget(lbl_cap)

            layout.addWidget(card)

        layout.addStretch()

        if self._show_cible_cols:
            lbl_note = QLabel(
                "<i>🎯 Les colonnes Cible\nindiquent le combattant\nvisé par l'action.</i>"
            )
            lbl_note.setStyleSheet("font-size: 9px; background: transparent;")
            lbl_note.setWordWrap(True)
            layout.addWidget(lbl_note)

        group.setMaximumWidth(240)
        return group

    def _build_action_buttons(self) -> QHBoxLayout:
        """Barre de boutons d'action (Ajouter, Supprimer, Monter, Descendre)."""
        layout = QHBoxLayout()
        layout.setSpacing(6)

        self.btn_add_action = QPushButton("＋  Ajouter action")
        self.btn_add_action.setStyleSheet(
            "background-color: #1b5e20; color: white; font-weight: bold;"
            "border-radius: 4px; padding: 5px 12px; border: 1px solid #4caf50;"
        )
        self.btn_delete_action = QPushButton("✕  Supprimer")
        self.btn_delete_action.setStyleSheet(
            "background-color: #7f0000; color: white; font-weight: bold;"
            "border-radius: 4px; padding: 5px 12px; border: 1px solid #ef5350;"
        )
        self.btn_move_up = QPushButton("▲  Monter")
        self.btn_move_up.setStyleSheet(
            "background-color: #263238; color: #cfd8dc;"
            "border-radius: 4px; padding: 5px 12px; border: 1px solid #78909c;"
        )
        self.btn_move_down = QPushButton("▼  Descendre")
        self.btn_move_down.setStyleSheet(
            "background-color: #263238; color: #cfd8dc;"
            "border-radius: 4px; padding: 5px 12px; border: 1px solid #78909c;"
        )

        layout.addWidget(self.btn_add_action)
        layout.addWidget(self.btn_delete_action)
        layout.addWidget(self.btn_move_up)
        layout.addWidget(self.btn_move_down)
        layout.addStretch()

        self.lbl_count = QLabel("0 action(s)")
        self.lbl_count.setStyleSheet("font-style: italic;")
        layout.addWidget(self.lbl_count)
        return layout

    def _build_table(self) -> QTableWidget:
        """Construit et configure le QTableWidget principal."""
        self.table = QTableWidget(0, len(self._col_defs))
        self.table.setHorizontalHeaderLabels([d["header"] for d in self._col_defs])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(False)
        self.table.verticalHeader().setDefaultSectionSize(34)
        self.table.verticalHeader().setVisible(True)
        self.table.horizontalHeader().setDefaultSectionSize(110)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setMinimumSectionSize(70)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        return self.table

    def _connect_signals(self) -> None:
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
        """Remplit le tableau avec les données de la phrase d'armes."""
        self._loading = True
        self.table.setRowCount(0)

        for action in sorted(self._phrase.liste_actions, key=lambda a: a.numero_action):
            self._add_row_for_action(action)

        self.table.resizeColumnsToContents()
        for col_idx in range(self.table.columnCount()):
            if self.table.columnWidth(col_idx) < 90:
                self.table.setColumnWidth(col_idx, 90)
            if "ommentaire" in self._col_defs[col_idx]["header"]:
                self.table.setColumnWidth(col_idx, 160)

        self._loading = False
        self._update_button_states()
        self.lbl_count.setText(f"{self.table.rowCount()} action(s)")

    def _add_row_for_action(self, action: Action) -> int:
        """
        Ajoute une ligne dans le tableau pour une action.

        Le fond de chaque cellule est coloré selon le combattant propriétaire
        de la colonne. Les couleurs sont adaptées au thème actif (clair/sombre).
        """
        row = self.table.rowCount()
        self.table.insertRow(row)

        header_item = QTableWidgetItem(f" {action.numero_action} ")
        header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setVerticalHeaderItem(row, header_item)

        for col_idx, col_def in enumerate(self._col_defs):
            combattant_id = col_def["combattant_id"]
            field         = col_def["field"]
            col_type      = col_def["type"]
            options       = col_def["options"]
            ci            = col_def["color_index"]

            # Couleur de fond adaptée au thème
            bg_color = QColor(get_bg(ci))
            text_color = QColor(get_text(ci))

            mouvement = action.get_mouvement_pour_combattant(combattant_id)

            if col_type == "text":
                # ── Cellule texte (Commentaire) ────────────────────────────
                value = getattr(mouvement, field, "") if mouvement else ""
                item = QTableWidgetItem(str(value) if value else "")
                item.setBackground(QBrush(bg_color))
                item.setForeground(QBrush(text_color))
                self.table.setItem(row, col_idx, item)

            elif col_type == "cible":
                # ── ComboBox Cible ─────────────────────────────────────────
                raw_val = getattr(mouvement, field, 0) if mouvement else 0
                combo = self._make_cible_combo(options, raw_val, ci)
                combo.currentIndexChanged.connect(
                    lambda idx, r=row, c=col_idx: self._on_cible_combo_changed(r, c, idx)
                )
                self.table.setCellWidget(row, col_idx, combo)

            else:
                # ── ComboBox standard (Main, Zone, Déplacement) ────────────
                value = getattr(mouvement, field, "") if mouvement else ""
                combo = self._make_standard_combo(options, str(value), ci)
                combo.currentTextChanged.connect(
                    lambda text, r=row, c=col_idx: self._on_combo_changed(r, c, text)
                )
                self.table.setCellWidget(row, col_idx, combo)

        return row

    def _make_standard_combo(self, options: list, current_value: str, ci: int) -> QComboBox:
        """
        ComboBox standard avec fond coloré adapté au thème.
        Le texte est toujours contrasté : foncé sur clair, blanc sur sombre.
        """
        combo = QComboBox()
        combo.addItems(options)
        idx = combo.findText(current_value)
        combo.setCurrentIndex(idx if idx >= 0 else 0)

        bg     = get_bg(ci)
        text   = get_text(ci)
        header = get_header(ci)

        combo.setStyleSheet(
            f"QComboBox {{"
            f"  background-color: {bg};"
            f"  color: {text};"
            f"  border: none;"
            f"  padding: 2px 4px;"
            f"}}"
            f"QComboBox:focus {{"
            f"  border: 2px solid {header};"
            f"}}"
            f"QComboBox QAbstractItemView {{"
            f"  background-color: white;"
            f"  color: #222222;"
            f"  selection-background-color: {header};"
            f"  selection-color: white;"
            f"}}"
        )
        return combo

    def _make_cible_combo(self, options: list, current_id: int, ci: int) -> QComboBox:
        """
        ComboBox pour la sélection de cible.
        Chaque option est colorée dans la teinte du combattant correspondant.
        En thème sombre : fond sombre + texte blanc pour chaque option.
        """
        combo = QComboBox()
        combo.addItem("— Aucune")

        for i, c in enumerate(self._combattants):
            cible_ci = self._ci(c.id)
            cible_bg   = QColor(get_bg(cible_ci))
            cible_text = QColor(get_text(cible_ci))
            combo.addItem(f"  {c.prenom} {c.nom}")
            combo.setItemData(i + 1, cible_bg,   Qt.ItemDataRole.BackgroundRole)
            combo.setItemData(i + 1, cible_text,  Qt.ItemDataRole.ForegroundRole)

        # Sélectionner la valeur courante
        selected_idx = 0
        if current_id:
            for i, c in enumerate(self._combattants):
                if c.id == current_id:
                    selected_idx = i + 1
                    break
        combo.setCurrentIndex(selected_idx)

        bg     = get_bg(ci)
        text   = get_text(ci)
        header = get_header(ci)

        combo.setStyleSheet(
            f"QComboBox {{"
            f"  background-color: {bg};"
            f"  color: {text};"
            f"  border: none;"
            f"  padding: 2px 4px;"
            f"  font-weight: bold;"
            f"}}"
            f"QComboBox:focus {{"
            f"  border: 2px solid {header};"
            f"}}"
            f"QComboBox QAbstractItemView {{"
            f"  background-color: white;"
            f"  color: #222222;"
            f"  selection-background-color: {header};"
            f"  selection-color: white;"
            f"}}"
        )
        return combo

    # =========================================================================
    # UTILITAIRES
    # =========================================================================

    def _get_action_at_row(self, row: int) -> Optional[Action]:
        if row < 0 or row >= len(self._phrase.liste_actions):
            return None
        return sorted(self._phrase.liste_actions, key=lambda a: a.numero_action)[row]

    def _ensure_mouvement(self, action: Action, combattant_id: int) -> Mouvement:
        m = action.get_mouvement_pour_combattant(combattant_id)
        if m is None:
            m = Mouvement(combattant_id=combattant_id)
            action.mouvements.append(m)
        return m

    def _update_button_states(self) -> None:
        row   = self.table.currentRow()
        count = self.table.rowCount()
        self.btn_delete_action.setEnabled(row >= 0)
        self.btn_move_up.setEnabled(row > 0)
        self.btn_move_down.setEnabled(row >= 0 and row < count - 1)

    def _update_mouvement_field(self, row: int, col_idx: int, value: str) -> None:
        if self._loading:
            return
        action = self._get_action_at_row(row)
        if action is None:
            return
        col_def  = self._col_defs[col_idx]
        mouvement = self._ensure_mouvement(action, col_def["combattant_id"])
        field    = col_def["field"]
        if "cible" in field:
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
        self._update_mouvement_field(row, col_idx, text)

    @pyqtSlot(int, int, int)
    def _on_cible_combo_changed(self, row: int, col_idx: int, combo_index: int) -> None:
        """
        Convertit l'index du ComboBox en ID réel du combattant ciblé.
        Index 0 = Aucune → ID 0 / Index 1+ → ID du combattant à (index-1).
        """
        if self._loading:
            return
        action = self._get_action_at_row(row)
        if action is None:
            return
        col_def   = self._col_defs[col_idx]
        mouvement = self._ensure_mouvement(action, col_def["combattant_id"])
        if combo_index == 0:
            target_id = 0
        else:
            idx = combo_index - 1
            target_id = self._combattants[idx].id if idx < len(self._combattants) else 0
        setattr(mouvement, col_def["field"], target_id)

    @pyqtSlot(QTableWidgetItem)
    def _on_item_changed(self, item: QTableWidgetItem) -> None:
        self._update_mouvement_field(item.row(), item.column(), item.text())

    @pyqtSlot()
    def _on_add_action(self) -> None:
        actions  = self._phrase.liste_actions
        next_num = max((a.numero_action for a in actions), default=0) + 1
        new_action = Action(numero_action=next_num)
        for c in self._combattants:
            new_action.mouvements.append(Mouvement(combattant_id=c.id))
        actions.append(new_action)
        self._loading = True
        self._add_row_for_action(new_action)
        self._loading = False
        self.table.setCurrentCell(self.table.rowCount() - 1, 0)
        self._update_button_states()
        self.lbl_count.setText(f"{self.table.rowCount()} action(s)")

    @pyqtSlot()
    def _on_delete_action(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            return
        action = self._get_action_at_row(row)
        if action is None:
            return
        reply = QMessageBox.question(
            self, "Confirmer la suppression",
            f"Supprimer l'action numéro {action.numero_action} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._phrase.liste_actions.remove(action)
            for i, a in enumerate(
                sorted(self._phrase.liste_actions, key=lambda x: x.numero_action)
            ):
                a.numero_action = i + 1
            self._populate_table()

    @pyqtSlot()
    def _on_move_up(self) -> None:
        row = self.table.currentRow()
        if row <= 0:
            return
        actions = sorted(self._phrase.liste_actions, key=lambda a: a.numero_action)
        actions[row].numero_action, actions[row - 1].numero_action = (
            actions[row - 1].numero_action, actions[row].numero_action,
        )
        self._populate_table()
        self.table.setCurrentCell(row - 1, self.table.currentColumn())

    @pyqtSlot()
    def _on_move_down(self) -> None:
        row     = self.table.currentRow()
        actions = sorted(self._phrase.liste_actions, key=lambda a: a.numero_action)
        if row < 0 or row >= len(actions) - 1:
            return
        actions[row].numero_action, actions[row + 1].numero_action = (
            actions[row + 1].numero_action, actions[row].numero_action,
        )
        self._populate_table()
        self.table.setCurrentCell(row + 1, self.table.currentColumn())
