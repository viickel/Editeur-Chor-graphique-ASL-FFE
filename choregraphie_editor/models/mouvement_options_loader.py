# -*- coding: utf-8 -*-
"""
Chargeur des options de mouvements depuis le fichier CSV.

Lit le fichier OptionsMouvements.csv et expose les listes d'options
pour les menus déroulants de l'éditeur.
Équivalent de la classe MouvementOptionsLoader.vb du projet VB.NET original.

Le fichier CSV attend un en-tête "Main;Deplacement;Zone" (séparateur point-virgule).
"""

import os
import csv
from typing import List


# Nom du fichier de configuration des mouvements (identique à la V1)
OPTIONS_FILE_NAME = "OptionsMouvements.csv"

# Séparateur CSV (identique à la V1)
CSV_SEPARATOR = ";"

# Contenu par défaut si le fichier est absent (identique à la V1)
DEFAULT_CSV_CONTENT = [
    ["Main", "Deplacement", "Zone"],
    ["", "", ""],
    ["Amputer", "Appel", "Zone 1"],
    ["Attaque", "Balestra", "Zone 2"],
    ["Attaque latérale", "Bond arrière", "Zone 3"],
    ["Blocage avec la main", "Bond avant", "Zone 4"],
    ["Parade", "Fente", "Zone 5"],
    ["Estoc", "Esquive", "Zone 6"],
    ["Feinte", "Volte", "Zone 1-2"],
    ["Coup de poing", "Pas chassé", "Zone 3-5"],
    ["Coup de pied", "Roulade", ""],
    ["Désarmer", "Saut", ""],
]


class MouvementOptionsLoader:
    """
    Charge et expose les options de mouvements depuis le fichier CSV.

    Les listes sont utilisées pour peupler les menus déroulants du tableau
    d'édition des actions (dialog_actions.py).

    Attributs
    ----------
    mains : list[str]
        Options disponibles pour les colonnes "Main Droite" et "Main Gauche".
    deplacements : list[str]
        Options disponibles pour la colonne "Déplacement".
    zones : list[str]
        Options disponibles pour les colonnes "Zone MD" et "Zone MG".
    """

    def __init__(self, base_dir: str = None):
        """
        Constructeur — charge les options immédiatement.

        Paramètres
        ----------
        base_dir : str | None
            Répertoire dans lequel chercher le fichier CSV.
            Si None, utilise le dossier du script courant.
        """
        self.mains: List[str] = []
        self.deplacements: List[str] = []
        self.zones: List[str] = []

        # Déterminer le répertoire de base pour trouver le CSV
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self._file_path = os.path.join(base_dir, OPTIONS_FILE_NAME)
        self._load_options()

    def _load_options(self) -> None:
        """Charge les options depuis le fichier CSV, ou crée un fichier par défaut."""
        # Si le fichier n'existe pas, créer le fichier par défaut
        if not os.path.exists(self._file_path):
            self._create_default_options_file()

        # Tenter de lire le fichier
        try:
            with open(self._file_path, encoding="utf-8-sig", newline="") as f:
                reader = csv.reader(f, delimiter=CSV_SEPARATOR)
                rows = list(reader)

            if not rows:
                raise ValueError("Le fichier CSV est vide.")

            # Lire les en-têtes (première ligne)
            headers = [h.strip() for h in rows[0]]

            # Trouver les indices des colonnes
            try:
                idx_main = headers.index("Main")
                idx_deplacement = headers.index("Deplacement")
                idx_zone = headers.index("Zone")
            except ValueError as e:
                raise ValueError(
                    f"En-tête manquant dans '{OPTIONS_FILE_NAME}': {e}. "
                    f"Attendu: Main;Deplacement;Zone"
                )

            # Réinitialiser les listes
            self.mains.clear()
            self.deplacements.clear()
            self.zones.clear()

            # Parcourir les lignes de données (à partir de la ligne 1)
            for row in rows[1:]:
                if not row:
                    continue

                # Colonne Main
                if idx_main < len(row):
                    val = row[idx_main].strip()
                    if val and val not in self.mains:
                        self.mains.append(val)

                # Colonne Deplacement
                if idx_deplacement < len(row):
                    val = row[idx_deplacement].strip()
                    if val and val not in self.deplacements:
                        self.deplacements.append(val)

                # Colonne Zone
                if idx_zone < len(row):
                    val = row[idx_zone].strip()
                    if val and val not in self.zones:
                        self.zones.append(val)

        except Exception as e:
            # En cas d'erreur de lecture, on charge les valeurs minimales
            print(f"[MouvementOptionsLoader] Erreur de chargement CSV : {e}")
            self._load_fallback_options()

    def _load_fallback_options(self) -> None:
        """Charge des options minimales codées en dur en cas d'échec du CSV."""
        self.mains = ["Attaque", "Parade", "Estoc", "Feinte", "Désarmer"]
        self.deplacements = ["Fente", "Esquive", "Volte", "Balestra", "Pas chassé"]
        self.zones = ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6"]

    def _create_default_options_file(self) -> None:
        """Crée le fichier CSV par défaut si absent (identique au comportement V1)."""
        try:
            with open(self._file_path, encoding="utf-8-sig", newline="", mode="w") as f:
                writer = csv.writer(f, delimiter=CSV_SEPARATOR)
                for row in DEFAULT_CSV_CONTENT:
                    writer.writerow(row)
            print(f"[MouvementOptionsLoader] Fichier par défaut créé : {self._file_path}")
        except Exception as e:
            print(f"[MouvementOptionsLoader] Impossible de créer le fichier par défaut : {e}")

    def get_mains_avec_vide(self) -> List[str]:
        """Retourne la liste des mains précédée d'une entrée vide (pour les ComboBox)."""
        return [""] + self.mains

    def get_deplacements_avec_vide(self) -> List[str]:
        """Retourne la liste des déplacements précédée d'une entrée vide."""
        return [""] + self.deplacements

    def get_zones_avec_vide(self) -> List[str]:
        """Retourne la liste des zones précédée d'une entrée vide."""
        return [""] + self.zones
