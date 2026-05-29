# -*- coding: utf-8 -*-
"""
Modèle Assistant.

Représente un assistant plateau / figurant de la chorégraphie.
Équivalent de la classe Assistant.vb du projet VB.NET original.
"""


class Assistant:
    """
    Assistant plateau ou figurant participant à la chorégraphie.

    Attributs
    ----------
    nom : str
        Nom de famille.
    prenom : str
        Prénom.
    numero_licence : str
        Numéro de licence FFE (optionnel).
    role : str
        Rôle spécifique dans la chorégraphie (ex: "Narrateur", "Figurant").
    """

    def __init__(
        self,
        nom: str = "",
        prenom: str = "",
        numero_licence: str = "",
        role: str = "",
    ):
        """
        Constructeur par défaut (nécessaire pour la désérialisation XML).

        Paramètres
        ----------
        nom : str
            Nom de famille de l'assistant.
        prenom : str
            Prénom de l'assistant.
        numero_licence : str
            Numéro de licence FFE (optionnel).
        role : str
            Rôle dans la chorégraphie (optionnel).
        """
        self.nom: str = nom
        self.prenom: str = prenom
        self.numero_licence: str = numero_licence
        self.role: str = role

    def __str__(self) -> str:
        """Affichage lisible dans les listes de l'interface."""
        licence_str = f" (Licence: {self.numero_licence})" if self.numero_licence else ""
        role_str = f" — {self.role}" if self.role else ""
        return f"{self.prenom} {self.nom}{licence_str}{role_str}"

    def __repr__(self) -> str:
        return (
            f"Assistant(nom='{self.nom}', prenom='{self.prenom}', "
            f"role='{self.role}')"
        )
