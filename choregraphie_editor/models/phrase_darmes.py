# -*- coding: utf-8 -*-
"""
Modèle PhraseDArmes.

Une Phrase d'Armes est une section de la chorégraphie regroupant
une séquence d'actions ordonnées.
Équivalent de la classe PhraseDArmes.vb du projet VB.NET original.
"""

from typing import List
from .action import Action


class PhraseDArmes:
    """
    Section de la chorégraphie contenant une séquence d'actions.

    Une chorégraphie complète est découpée en plusieurs phrases d'armes,
    chacune décrivant un enchaînement cohérent de mouvements.

    Attributs
    ----------
    numero : int
        Numéro d'ordre de la phrase dans la chorégraphie (commence à 1).
    description_section : str
        Description narrative ou technique de la phrase.
    liste_actions : list[Action]
        Séquence ordonnée des actions de cette phrase.
    """

    def __init__(self, numero: int = 0, description_section: str = ""):
        """
        Constructeur par défaut (nécessaire pour la désérialisation XML).

        Paramètres
        ----------
        numero : int
            Numéro de la phrase dans la chorégraphie.
        description_section : str
            Texte décrivant le contenu ou l'intention de la phrase.
        """
        self.numero: int = numero
        self.description_section: str = description_section
        # Liste des actions de cette phrase, ordonnée par numero_action
        self.liste_actions: List[Action] = []

    def __str__(self) -> str:
        """Affichage dans les listes de l'interface (tronqué à 40 caractères)."""
        desc = self.description_section
        if len(desc) > 40:
            desc = desc[:40] + "..."
        return f"Phrase {self.numero} : {desc}"

    def __repr__(self) -> str:
        return (
            f"PhraseDArmes(numero={self.numero}, "
            f"nb_actions={len(self.liste_actions)})"
        )
