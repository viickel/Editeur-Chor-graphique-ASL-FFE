# -*- coding: utf-8 -*-
"""
Modèle Combattant.

Représente un escrimeur participant à la chorégraphie.
Équivalent de la classe Combattant.vb du projet VB.NET original.
"""


class Combattant:
    """
    Escrimeur participant à la chorégraphie.

    Attributs
    ----------
    id : int
        Identifiant unique du combattant dans le projet.
    nom : str
        Nom de famille.
    prenom : str
        Prénom.
    numero_licence : str
        Numéro de licence FFE.
    capitaine : bool
        True si ce combattant est le capitaine de l'équipe.
    """

    def __init__(
        self,
        id: int = 0,
        nom: str = "",
        prenom: str = "",
        numero_licence: str = "",
        capitaine: bool = False,
    ):
        """
        Constructeur par défaut (nécessaire pour la désérialisation XML).

        Paramètres
        ----------
        id : int
            Identifiant unique (auto-incrémenté par le formulaire d'édition).
        nom : str
            Nom de famille du combattant.
        prenom : str
            Prénom du combattant.
        numero_licence : str
            Numéro de licence FFE (optionnel).
        capitaine : bool
            True si le combattant est désigné capitaine.
        """
        self.id: int = id
        self.nom: str = nom
        self.prenom: str = prenom
        self.numero_licence: str = numero_licence
        self.capitaine: bool = capitaine

    def __str__(self) -> str:
        """Affichage lisible dans les listes de l'interface."""
        licence_str = f" (Licence: {self.numero_licence})" if self.numero_licence else ""
        capitaine_str = " [Capitaine]" if self.capitaine else ""
        return f"{self.prenom} {self.nom}{licence_str}{capitaine_str}"

    def __repr__(self) -> str:
        return (
            f"Combattant(id={self.id}, nom='{self.nom}', "
            f"prenom='{self.prenom}', capitaine={self.capitaine})"
        )
