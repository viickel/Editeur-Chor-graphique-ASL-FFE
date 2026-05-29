# -*- coding: utf-8 -*-
"""
Sérialiseur / Désérialiseur XML pour les projets chorégraphiques.

Assure la RÉTROCOMPATIBILITÉ complète avec les fichiers XML produits
par la version 1 (VB.NET / iTextSharp / XmlSerializer .NET).

Stratégie de rétrocompatibilité :
- Les noms de balises XML sont identiques entre V1 et V2.
- Les champs absents (nouvelles propriétés V2) reçoivent une valeur par défaut.
- Les champs supprimés (V1 uniquement) sont ignorés sans erreur.
- La désérialisation n'échoue jamais sur un champ inconnu ou manquant.

Format XML attendu (identique V1 et V2) :
    <ProjetChoregraphique>
        <Titre>...</Titre>
        <Intrigue>...</Intrigue>
        <Duree>...</Duree>
        <DureeOposition>...</DureeOposition>   ← Note : faute de frappe conservée pour compat V1
        <NomDuClub>...</NomDuClub>
        <Categorie>...</Categorie>
        <IsMouvementEnsemble>true</IsMouvementEnsemble>
        <ListeCombattants>
            <Combattant>
                <ID>1</ID>
                <Nom>...</Nom>
                <Prenom>...</Prenom>
                <NumeroLicence>...</NumeroLicence>
                <Capitaine>false</Capitaine>
            </Combattant>
            ...
        </ListeCombattants>
        <ListeAssistants>
            <Assistant>
                <Nom>...</Nom>
                <Prenom>...</Prenom>
                <NumeroLicence>...</NumeroLicence>
                <Role>...</Role>
            </Assistant>
            ...
        </ListeAssistants>
        <ChoregraphieSections>
            <PhraseDArmes>
                <Numero>1</Numero>
                <DescriptionSection>...</DescriptionSection>
                <ListeActions>
                    <Action>
                        <NumeroAction>1</NumeroAction>
                        <Mouvements>
                            <Mouvement>
                                <CombattantID>1</CombattantID>
                                <MainDroite>...</MainDroite>
                                <ZoneMainDroite>...</ZoneMainDroite>
                                <CibleMainDroiteID>0</CibleMainDroiteID>
                                <MainGauche>...</MainGauche>
                                <ZoneMainGauche>...</ZoneMainGauche>
                                <CibleMainGaucheID>0</CibleMainGaucheID>
                                <Deplacement>...</Deplacement>
                                <PouvoirForce>...</PouvoirForce>
                                <Commentaire>...</Commentaire>
                            </Mouvement>
                        </Mouvements>
                    </Action>
                </ListeActions>
            </PhraseDArmes>
        </ChoregraphieSections>
    </ProjetChoregraphique>
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Optional

from models.projet_choregraphique import ProjetChoregraphique
from models.combattant import Combattant
from models.assistant import Assistant
from models.phrase_darmes import PhraseDArmes
from models.action import Action
from models.mouvement import Mouvement


def _text(node: Optional[ET.Element], tag: str, default: str = "") -> str:
    """
    Lit le texte d'un sous-élément XML de façon sécurisée.

    Retourne `default` si l'élément est absent ou vide.
    Cette fonction est la clé de la rétrocompatibilité V1 : si un champ
    n'existe pas dans l'ancien fichier, on ne plante pas.
    """
    if node is None:
        return default
    child = node.find(tag)
    if child is None or child.text is None:
        return default
    return child.text.strip()


def _int(node: Optional[ET.Element], tag: str, default: int = 0) -> int:
    """Lit un entier depuis un nœud XML, avec valeur par défaut."""
    val = _text(node, tag, str(default))
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _bool(node: Optional[ET.Element], tag: str, default: bool = False) -> bool:
    """Lit un booléen depuis un nœud XML (format .NET : 'true'/'false')."""
    val = _text(node, tag, "false").lower()
    return val in ("true", "1", "yes", "oui")


def _sub(parent: ET.Element, tag: str) -> ET.SubElement:
    """Crée et retourne un sous-élément XML."""
    return ET.SubElement(parent, tag)


def _set(parent: ET.Element, tag: str, value: str) -> None:
    """Crée un sous-élément avec son contenu texte."""
    el = ET.SubElement(parent, tag)
    el.text = str(value) if value is not None else ""


class XmlSerializer:
    """
    Sérialiseur/Désérialiseur XML pour ProjetChoregraphique.

    Garantit la rétrocompatibilité totale avec les fichiers V1 (VB.NET).
    Les noms de balises reproduisent exactement ceux générés par
    System.Xml.Serialization.XmlSerializer du framework .NET.
    """

    # Extension de fichier (identique à la V1)
    FILE_EXTENSION = ".chore"
    FILE_FILTER = "Fichiers Chorégraphie (*.chore);;Tous les fichiers (*.*)"

    # -------------------------------------------------------------------------
    # DÉSÉRIALISATION (lecture XML → objet Python)
    # -------------------------------------------------------------------------

    @classmethod
    def load(cls, file_path: str) -> ProjetChoregraphique:
        """
        Charge un projet chorégraphique depuis un fichier XML.

        Compatible avec les fichiers produits par la V1 (VB.NET) ET la V2.

        Paramètres
        ----------
        file_path : str
            Chemin complet du fichier .chore à ouvrir.

        Retourne
        --------
        ProjetChoregraphique
            L'objet projet reconstruit depuis le XML.

        Lève
        ----
        ET.ParseError
            Si le fichier XML est malformé.
        FileNotFoundError
            Si le fichier est introuvable.
        """
        tree = ET.parse(file_path)
        root = tree.getroot()

        projet = ProjetChoregraphique()

        # --- Champs scalaires du projet ---
        # Note: "DureeOposition" conserve la faute de frappe de la V1 pour compat
        projet.titre = _text(root, "Titre")
        projet.intrigue = _text(root, "Intrigue")
        projet.duree = _text(root, "Duree", "00m:00s")
        projet.duree_opposition = _text(root, "DureeOposition", "00m:00s")  # Compat V1
        projet.nom_du_club = _text(root, "NomDuClub")
        projet.categorie = _text(root, "Categorie")
        projet.is_mouvement_ensemble = _bool(root, "IsMouvementEnsemble", False)

        # --- Liste des combattants ---
        liste_combattants_node = root.find("ListeCombattants")
        if liste_combattants_node is not None:
            for c_node in liste_combattants_node.findall("Combattant"):
                combattant = cls._deserialize_combattant(c_node)
                projet.liste_combattants.append(combattant)

        # --- Liste des assistants ---
        liste_assistants_node = root.find("ListeAssistants")
        if liste_assistants_node is not None:
            for a_node in liste_assistants_node.findall("Assistant"):
                assistant = cls._deserialize_assistant(a_node)
                projet.liste_assistants.append(assistant)

        # --- Sections chorégraphiques (phrases d'armes) ---
        sections_node = root.find("ChoregraphieSections")
        if sections_node is not None:
            for p_node in sections_node.findall("PhraseDArmes"):
                phrase = cls._deserialize_phrase_darmes(p_node)
                projet.choregraphie_sections.append(phrase)

        return projet

    @classmethod
    def _deserialize_combattant(cls, node: ET.Element) -> Combattant:
        """Désérialise un nœud <Combattant> en objet Python."""
        return Combattant(
            id=_int(node, "ID", 0),
            nom=_text(node, "Nom"),
            prenom=_text(node, "Prenom"),
            numero_licence=_text(node, "NumeroLicence"),
            capitaine=_bool(node, "Capitaine", False),
        )

    @classmethod
    def _deserialize_assistant(cls, node: ET.Element) -> Assistant:
        """
        Désérialise un nœud <Assistant> en objet Python.
        Le champ <Role> est optionnel (absent dans certaines versions V1).
        """
        return Assistant(
            nom=_text(node, "Nom"),
            prenom=_text(node, "Prenom"),
            numero_licence=_text(node, "NumeroLicence"),
            role=_text(node, "Role", ""),  # Optionnel — valeur par défaut si absent
        )

    @classmethod
    def _deserialize_phrase_darmes(cls, node: ET.Element) -> PhraseDArmes:
        """Désérialise un nœud <PhraseDArmes> en objet Python."""
        phrase = PhraseDArmes(
            numero=_int(node, "Numero", 0),
            description_section=_text(node, "DescriptionSection"),
        )

        # Actions de la phrase
        actions_node = node.find("ListeActions")
        if actions_node is not None:
            for a_node in actions_node.findall("Action"):
                action = cls._deserialize_action(a_node)
                phrase.liste_actions.append(action)

        return phrase

    @classmethod
    def _deserialize_action(cls, node: ET.Element) -> Action:
        """Désérialise un nœud <Action> en objet Python."""
        action = Action(numero_action=_int(node, "NumeroAction", 0))

        # Mouvements de l'action (un par combattant)
        mouvements_node = node.find("Mouvements")
        if mouvements_node is not None:
            for m_node in mouvements_node.findall("Mouvement"):
                mouvement = cls._deserialize_mouvement(m_node)
                action.mouvements.append(mouvement)

        return action

    @classmethod
    def _deserialize_mouvement(cls, node: ET.Element) -> Mouvement:
        """
        Désérialise un nœud <Mouvement> en objet Python.

        Les champs ZoneMainDroite, ZoneMainGauche, CibleMainDroiteID,
        CibleMainGaucheID sont optionnels pour assurer la rétrocompatibilité
        avec les fichiers V1 qui ne les avaient pas tous.
        """
        return Mouvement(
            combattant_id=_int(node, "CombattantID", 0),
            main_droite=_text(node, "MainDroite"),
            zone_main_droite=_text(node, "ZoneMainDroite", ""),   # Optionnel V1
            cible_main_droite_id=_int(node, "CibleMainDroiteID", 0),
            main_gauche=_text(node, "MainGauche"),
            zone_main_gauche=_text(node, "ZoneMainGauche", ""),   # Optionnel V1
            cible_main_gauche_id=_int(node, "CibleMainGaucheID", 0),
            deplacement=_text(node, "Deplacement"),
            pouvoir_force=_text(node, "PouvoirForce"),
            commentaire=_text(node, "Commentaire"),
        )

    # -------------------------------------------------------------------------
    # SÉRIALISATION (objet Python → XML)
    # -------------------------------------------------------------------------

    @classmethod
    def save(cls, projet: ProjetChoregraphique, file_path: str) -> None:
        """
        Sauvegarde un projet chorégraphique dans un fichier XML.

        Le format produit est compatible avec la V1 (VB.NET) : un fichier
        sauvegardé avec la V2 peut être relu par la V1 et vice-versa.

        Paramètres
        ----------
        projet : ProjetChoregraphique
            L'objet projet à sauvegarder.
        file_path : str
            Chemin complet du fichier de destination.

        Lève
        ----
        IOError / PermissionError
            Si le fichier ne peut pas être écrit.
        """
        root = ET.Element("ProjetChoregraphique")

        # --- Champs scalaires ---
        _set(root, "Titre", projet.titre)
        _set(root, "Intrigue", projet.intrigue)
        _set(root, "Duree", projet.duree)
        # Conserve la faute de frappe "DureeOposition" pour compat V1
        _set(root, "DureeOposition", projet.duree_opposition)
        _set(root, "NomDuClub", projet.nom_du_club)
        _set(root, "Categorie", projet.categorie)
        _set(root, "IsMouvementEnsemble", str(projet.is_mouvement_ensemble).lower())

        # --- Combattants ---
        liste_c_node = _sub(root, "ListeCombattants")
        for combattant in projet.liste_combattants:
            cls._serialize_combattant(liste_c_node, combattant)

        # --- Assistants ---
        liste_a_node = _sub(root, "ListeAssistants")
        for assistant in projet.liste_assistants:
            cls._serialize_assistant(liste_a_node, assistant)

        # --- Sections chorégraphiques ---
        sections_node = _sub(root, "ChoregraphieSections")
        for phrase in projet.choregraphie_sections:
            cls._serialize_phrase_darmes(sections_node, phrase)

        # Écriture du fichier avec indentation propre
        cls._write_pretty_xml(root, file_path)

    @classmethod
    def _serialize_combattant(cls, parent: ET.Element, c: Combattant) -> None:
        """Sérialise un Combattant en nœud XML."""
        node = _sub(parent, "Combattant")
        _set(node, "ID", str(c.id))
        _set(node, "Nom", c.nom)
        _set(node, "Prenom", c.prenom)
        _set(node, "NumeroLicence", c.numero_licence)
        _set(node, "Capitaine", str(c.capitaine).lower())

    @classmethod
    def _serialize_assistant(cls, parent: ET.Element, a: Assistant) -> None:
        """Sérialise un Assistant en nœud XML."""
        node = _sub(parent, "Assistant")
        _set(node, "Nom", a.nom)
        _set(node, "Prenom", a.prenom)
        _set(node, "NumeroLicence", a.numero_licence)
        _set(node, "Role", a.role)

    @classmethod
    def _serialize_phrase_darmes(cls, parent: ET.Element, p: PhraseDArmes) -> None:
        """Sérialise une PhraseDArmes et ses actions en nœuds XML."""
        node = _sub(parent, "PhraseDArmes")
        _set(node, "Numero", str(p.numero))
        _set(node, "DescriptionSection", p.description_section)

        actions_node = _sub(node, "ListeActions")
        for action in sorted(p.liste_actions, key=lambda a: a.numero_action):
            cls._serialize_action(actions_node, action)

    @classmethod
    def _serialize_action(cls, parent: ET.Element, a: Action) -> None:
        """Sérialise une Action et ses mouvements en nœuds XML."""
        node = _sub(parent, "Action")
        _set(node, "NumeroAction", str(a.numero_action))

        mouvements_node = _sub(node, "Mouvements")
        for mouvement in a.mouvements:
            cls._serialize_mouvement(mouvements_node, mouvement)

    @classmethod
    def _serialize_mouvement(cls, parent: ET.Element, m: Mouvement) -> None:
        """Sérialise un Mouvement en nœud XML."""
        node = _sub(parent, "Mouvement")
        _set(node, "CombattantID", str(m.combattant_id))
        _set(node, "MainDroite", m.main_droite)
        _set(node, "ZoneMainDroite", m.zone_main_droite)
        _set(node, "CibleMainDroiteID", str(m.cible_main_droite_id))
        _set(node, "MainGauche", m.main_gauche)
        _set(node, "ZoneMainGauche", m.zone_main_gauche)
        _set(node, "CibleMainGaucheID", str(m.cible_main_gauche_id))
        _set(node, "Deplacement", m.deplacement)
        _set(node, "PouvoirForce", m.pouvoir_force)
        _set(node, "Commentaire", m.commentaire)

    @classmethod
    def _write_pretty_xml(cls, root: ET.Element, file_path: str) -> None:
        """
        Écrit le XML avec une indentation propre (lisible par un humain).

        Utilise minidom pour reformater le XML généré par ElementTree,
        qui n'indente pas nativement.
        """
        raw_xml = ET.tostring(root, encoding="unicode", xml_declaration=False)
        # Passer par minidom pour l'indentation
        parsed = minidom.parseString(f'<?xml version="1.0" encoding="utf-8"?>{raw_xml}')
        pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")

        with open(file_path, "wb") as f:
            f.write(pretty_xml)
