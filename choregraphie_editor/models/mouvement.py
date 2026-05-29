# -*- coding: utf-8 -*-
"""
Modèle Mouvement.

Représente le mouvement effectué par UN combattant lors d'UNE action.
Équivalent de la classe Mouvement.vb du projet VB.NET original.
"""


class Mouvement:
    """
    Décrit le mouvement d'un combattant pour une action donnée.

    Attributs
    ----------
    combattant_id : int
        Identifiant du combattant qui effectue ce mouvement.
    main_droite : str
        Technique ou geste de la main droite.
    zone_main_droite : str
        Zone corporelle ciblée par la main droite.
    cible_main_droite_id : int
        ID du combattant ciblé par la main droite (0 = aucune cible).
    main_gauche : str
        Technique ou geste de la main gauche.
    zone_main_gauche : str
        Zone corporelle ciblée par la main gauche.
    cible_main_gauche_id : int
        ID du combattant ciblé par la main gauche (0 = aucune cible).
    deplacement : str
        Type de déplacement effectué.
    pouvoir_force : str
        Indication de puissance ou de force appliquée.
    commentaire : str
        Commentaire libre sur le mouvement.
    """

    def __init__(
        self,
        combattant_id: int = 0,
        main_droite: str = "",
        zone_main_droite: str = "",
        cible_main_droite_id: int = 0,
        main_gauche: str = "",
        zone_main_gauche: str = "",
        cible_main_gauche_id: int = 0,
        deplacement: str = "",
        pouvoir_force: str = "",
        commentaire: str = "",
    ):
        """Constructeur par défaut — tous les champs sont optionnels."""
        self.combattant_id: int = combattant_id
        self.main_droite: str = main_droite
        self.zone_main_droite: str = zone_main_droite
        self.cible_main_droite_id: int = cible_main_droite_id
        self.main_gauche: str = main_gauche
        self.zone_main_gauche: str = zone_main_gauche
        self.cible_main_gauche_id: int = cible_main_gauche_id
        self.deplacement: str = deplacement
        self.pouvoir_force: str = pouvoir_force
        self.commentaire: str = commentaire

    def __repr__(self) -> str:
        return (
            f"Mouvement(combattant_id={self.combattant_id}, "
            f"main_droite='{self.main_droite}', "
            f"deplacement='{self.deplacement}')"
        )
