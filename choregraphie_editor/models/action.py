# -*- coding: utf-8 -*-
"""
Modèle Action.

Une Action regroupe les mouvements de TOUS les combattants
pour un instant T de la chorégraphie.
Équivalent de la classe Action.vb du projet VB.NET original.
"""

from typing import List
from .mouvement import Mouvement


class Action:
    """
    Représente une action simultanée de la chorégraphie.

    Une action contient un mouvement par combattant participant,
    tous se déroulant au même temps T de la séquence.

    Attributs
    ----------
    numero_action : int
        Numéro d'ordre de l'action au sein d'une PhraseDArmes.
    mouvements : list[Mouvement]
        Liste des mouvements de chaque combattant pour cette action.
    """

    def __init__(self, numero_action: int = 0):
        """
        Constructeur par défaut (nécessaire pour la désérialisation XML).

        Paramètres
        ----------
        numero_action : int
            Numéro de séquence de l'action (commence à 1).
        """
        self.numero_action: int = numero_action
        # Liste des mouvements, un par combattant
        self.mouvements: List[Mouvement] = []

    def get_mouvement_pour_combattant(self, combattant_id: int):
        """
        Retourne le Mouvement associé à un combattant donné, ou None.

        Paramètres
        ----------
        combattant_id : int
            Identifiant du combattant recherché.

        Retourne
        --------
        Mouvement | None
        """
        for m in self.mouvements:
            if m.combattant_id == combattant_id:
                return m
        return None

    def __repr__(self) -> str:
        return (
            f"Action(numero={self.numero_action}, "
            f"nb_mouvements={len(self.mouvements)})"
        )
