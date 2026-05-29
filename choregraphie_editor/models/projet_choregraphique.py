# -*- coding: utf-8 -*-
"""
Modèle ProjetChoregraphique.

Objet racine contenant l'intégralité des données d'un projet chorégraphique.
Équivalent de la classe ProjetChoregraphique.vb du projet VB.NET original.
"""

from typing import List
from .combattant import Combattant
from .assistant import Assistant
from .phrase_darmes import PhraseDArmes


class ProjetChoregraphique:
    """
    Conteneur principal d'un projet de chorégraphie d'escrime.

    C'est cet objet qui est sérialisé/désérialisé en XML pour la sauvegarde.

    Attributs
    ----------
    titre : str
        Titre de la chorégraphie.
    intrigue : str
        Texte décrivant l'intrigue scénaristique.
    duree : str
        Durée totale de la chorégraphie (format libre, ex: "03m:45s").
    duree_opposition : str
        Durée de la phase d'opposition (format libre).
    nom_du_club : str
        Nom du club présentant la chorégraphie.
    categorie : str
        Catégorie calculée automatiquement ("Kata", "Duel", "Bataille", "Ensemble").
    is_mouvement_ensemble : bool
        True si la catégorie est "Ensemble" (plus de 2 combattants en formation).
    liste_combattants : list[Combattant]
        Liste des combattants du projet.
    liste_assistants : list[Assistant]
        Liste des assistants plateau.
    choregraphie_sections : list[PhraseDArmes]
        Séquence ordonnée des phrases d'armes de la chorégraphie.
    """

    def __init__(self):
        """
        Constructeur par défaut.
        Initialise toutes les listes pour éviter les NullReferenceException
        lors de la désérialisation (cohérent avec la V1 VB.NET).
        """
        self.titre: str = ""
        self.intrigue: str = ""
        self.duree: str = "00m:00s"           # Valeur par défaut identique à la V1
        self.duree_opposition: str = "00m:00s" # Valeur par défaut identique à la V1
        self.nom_du_club: str = ""
        self.categorie: str = ""
        self.is_mouvement_ensemble: bool = False

        # Listes de participants
        self.liste_combattants: List[Combattant] = []
        self.liste_assistants: List[Assistant] = []

        # Contenu chorégraphique
        self.choregraphie_sections: List[PhraseDArmes] = []

    def calculer_categorie(self) -> str:
        """
        Calcule et retourne la catégorie de la chorégraphie
        en fonction du nombre de combattants.

        Logique identique à la méthode DetermineAndSetCategorie() de Form1.vb.

        Retourne
        --------
        str
            "Kata", "Duel", "Bataille", "Ensemble" ou un message par défaut.
        """
        nb = len(self.liste_combattants)
        if nb == 1:
            categorie = "Kata"
        elif nb == 2:
            categorie = "Duel"
        elif nb > 2 and not self.is_mouvement_ensemble:
            categorie = "Bataille"
        elif nb > 2 and self.is_mouvement_ensemble:
            categorie = "Ensemble"
        else:
            categorie = "Non définie (Ajoutez des combattants)"

        # Mémoriser la catégorie calculée dans l'objet
        self.categorie = categorie
        return categorie

    def __repr__(self) -> str:
        return (
            f"ProjetChoregraphique(titre='{self.titre}', "
            f"categorie='{self.categorie}', "
            f"nb_combattants={len(self.liste_combattants)}, "
            f"nb_phrases={len(self.choregraphie_sections)})"
        )
