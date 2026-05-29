# Éditeur Chorégraphique ASL-FFE — Version 2

Migration multiplateforme (Windows · macOS · Linux) du projet VB.NET original.  
Développé en **Python 3.10+** avec **PyQt6** (interface) et **ReportLab** (export PDF).

---

## Prérequis

- **Python 3.10 ou supérieur**  
  Télécharger sur https://www.python.org/downloads/

---

## Installation

Ouvrir un terminal dans le dossier `choregraphie_editor/` puis :

```bash
pip install -r requirements.txt
```

---

## Lancement

```bash
python main.py
```

---

## Structure du projet

```
choregraphie_editor/
├── main.py                        ← Point d'entrée
├── requirements.txt               ← Dépendances pip
├── OptionsMouvements.csv          ← Options des menus déroulants (éditable)
│
├── models/                        ← Modèles de données (classes métier)
│   ├── mouvement.py               ← class Mouvement
│   ├── action.py                  ← class Action
│   ├── combattant.py              ← class Combattant
│   ├── assistant.py               ← class Assistant
│   ├── phrase_darmes.py           ← class PhraseDArmes
│   ├── projet_choregraphique.py   ← class ProjetChoregraphique
│   └── mouvement_options_loader.py← Lecture du CSV
│
├── serialization/
│   └── xml_serializer.py          ← Lecture/écriture XML (.chore)
│
├── ui/                            ← Fenêtres et dialogues
│   ├── main_window.py             ← Fenêtre principale
│   ├── dialog_combattants.py      ← Édition des combattants
│   ├── dialog_assistants.py       ← Édition des assistants
│   ├── dialog_phrases.py          ← Édition des phrases d'armes
│   └── dialog_actions.py          ← Tableau des actions
│
└── export/
    └── pdf_exporter.py            ← Génération PDF (ReportLab)
```

---

## Rétrocompatibilité des fichiers XML (V1 → V2)

Les fichiers `.chore` créés avec la **version 1 (VB.NET)** s'ouvrent  
**directement** dans la V2 sans aucune conversion.

Les fichiers créés avec la V2 restent lisibles par la V1.

---

## Personnaliser les options de mouvements

Éditer le fichier `OptionsMouvements.csv` avec un éditeur de texte  
(LibreOffice Calc, Excel, Notepad++…).

Format attendu (séparateur `;`) :
```
Main;Deplacement;Zone
Attaque;Fente;Zone 1
Parade;Esquive;Zone 2
...
```

---

## Créer un exécutable autonome (optionnel)

Pour distribuer l'application sans que les utilisateurs installent Python :

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "EditeurChore" main.py
```

L'exécutable sera dans le dossier `dist/`.

---

## Dépendances

| Bibliothèque | Rôle | Équivalent V1 |
|---|---|---|
| PyQt6 | Interface graphique | WinForms (.NET) |
| ReportLab | Export PDF | iTextSharp |
