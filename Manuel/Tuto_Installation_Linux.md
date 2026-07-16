# Éditeur Chorégraphique ASL-FFE — Guide d'installation Linux

**Version source Python — Toutes distributions**

| | |
|---|---|
| 🐧 Distributions | Ubuntu · Debian · Fedora · Arch · Mint · NixOS · et autres |
| 🐍 Prérequis | Python 3.10 ou supérieur |
| 📦 Dépendances | PyQt6 · ReportLab (installées en 1 commande) |
| ⏱️ Durée | 5 à 10 minutes selon la connexion internet |

---

## Étape 1 — Télécharger les fichiers du projet

Le logiciel est distribué sous forme de code source Python. Récupérez le dossier `choregraphie_editor/` depuis le dépôt GitHub du projet ou via l'archive ZIP fournie.

### Option A — Via Git (recommandé)

```bash
# Cloner le dépôt dans votre dossier personnel
git clone https://github.com/viickel/Editeur-Chor-graphique-ASL-FFE.git
cd choregraphie_editor
```

### Option B — Via l'archive ZIP

```bash
# Décompresser l'archive
cd ~/Téléchargements
unzip Editeur-Chor-graphique-ASL-FFE-master.zip

# Se placer dans le dossier du projet
cd Editeur-Chor-graphique-ASL-FFE-master\choregraphie_editor
```

> 💡 Vous pouvez aussi décompresser le ZIP via votre gestionnaire de fichiers graphique
> (Nautilus, Dolphin, Thunar…) avec un clic droit → **Extraire ici**,
> puis ouvrir un terminal dans le dossier extrait.

---

## Étape 2 — Vérifier / Installer Python 3.10+

Python est souvent déjà installé sur les distributions Linux modernes. Vérifiez d'abord la version disponible :

```bash
python3 --version
# Résultat attendu : Python 3.10.x ou supérieur
```

Si la version est inférieure à 3.10 ou si la commande est introuvable, installez Python avec le gestionnaire de paquets de votre distribution :

| Distribution | Commande d'installation |
|---|---|
| Ubuntu 22.04+ · Debian 12+ · Linux Mint | `sudo apt update && sudo apt install python3 python3-pip python3-venv` |
| Fedora 38+ · RHEL 9+ | `sudo dnf install python3 python3-pip` |
| Arch Linux · Manjaro | `sudo pacman -S python python-pip` |
| openSUSE | `sudo zypper install python3 python3-pip` |
| NixOS | Voir section NixOS en bas de ce document |

---

## Étape 3 — Installer les dépendances Python

Le logiciel nécessite deux bibliothèques : **PyQt6** pour l'interface graphique et **ReportLab** pour l'export PDF.

### Méthode recommandée — Environnement virtuel

Un environnement virtuel isole les dépendances du projet du reste de votre système. C'est la méthode la plus propre et elle évite tout conflit avec d'autres projets Python.

```bash
# Depuis le dossier du projet
cd ~/Téléchargements/choregraphie_editor_v3

# Créer l'environnement virtuel (une seule fois)
python3 -m venv .venv

# Activer l'environnement virtuel
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Vérifier l'installation
pip list | grep -E 'PyQt6|reportlab'
```

> 💡 Une fois activé, votre terminal affiche `(.venv)` au début de chaque ligne.
> Pour désactiver l'environnement : tapez `deactivate`.

### Méthode alternative — Installation globale

Si vous ne souhaitez pas utiliser d'environnement virtuel :

```bash
pip3 install PyQt6 reportlab

# Sur Ubuntu 23.04+ et Debian 12+ (pip refuse l'installation globale par défaut)
pip3 install PyQt6 reportlab --break-system-packages
```

> ⚠️ Sur Ubuntu 23.04+ et Debian 12+, pip refuse d'installer des paquets globalement
> par défaut. Utilisez `--break-system-packages` ou préférez l'environnement virtuel.

---

## Étape 4 — Lancer le logiciel

```bash
# Si vous utilisez un environnement virtuel : l'activer d'abord
source .venv/bin/activate

# Lancer l'application
python3 main.py
```

L'interface graphique de l'éditeur chorégraphique s'ouvre.

---

## Étape 5 — Créer un raccourci dans le menu d'application

Sur toutes les distributions Linux avec un bureau graphique (GNOME, KDE, XFCE, Cinnamon…),
le standard **XDG Desktop Entry** permet de créer une icône dans le menu sans aucun outil
supplémentaire. C'est la méthode universelle compatible avec toutes les distributions.

### 1 — Créer le script de lancement

Ce script gère automatiquement l'activation de l'environnement virtuel avant de lancer le logiciel.

```bash
# Créer le script — adaptez le chemin si nécessaire
cat > ~/Téléchargements/choregraphie_editor_v3/lancer_chore.sh << 'EOF'
#!/bin/bash
# Script de lancement de l'Éditeur Chorégraphique ASL-FFE
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Activer l'environnement virtuel s'il existe
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

exec python3 "$SCRIPT_DIR/main.py"
EOF

# Rendre le script exécutable
chmod +x ~/Téléchargements/choregraphie_editor_v3/lancer_chore.sh
```

### 2 — Créer l'entrée de menu .desktop

```bash
# Créer le dossier s'il n'existe pas
mkdir -p ~/.local/share/applications

# Créer le fichier .desktop
# IMPORTANT : remplacez /home/VOTRE_NOM par votre chemin réel
# Pour connaître votre chemin exact : tapez pwd depuis le dossier du projet
cat > ~/.local/share/applications/editeur-chore.desktop << 'EOF'
[Desktop Entry]
Name=Éditeur Chorégraphique ASL-FFE
Name[fr]=Éditeur Chorégraphique ASL-FFE
Comment=Éditeur de chorégraphies d'escrime artistique
Comment[fr]=Éditeur de chorégraphies d'escrime artistique
Exec=/home/VOTRE_NOM/Téléchargements/choregraphie_editor_v3/lancer_chore.sh
Icon=applications-education
Terminal=false
Type=Application
Categories=Education;Sports;
StartupNotify=true
EOF
```

### 3 — Mettre à jour la base des applications

```bash
update-desktop-database ~/.local/share/applications
```

| Bureau | Comportement après update-desktop-database |
|---|---|
| GNOME | Rafraîchir via `Alt+F2` → `r` ou redémarrer la session |
| KDE Plasma | Le menu se met à jour automatiquement |
| XFCE | Clic droit sur le bureau → Actualiser les menus |
| Cinnamon | Le menu se met à jour automatiquement |

L'application apparaît dans le menu sous le nom **Éditeur Chorégraphique ASL-FFE**
dans la catégorie Éducation ou Sports.

---

## NixOS — Méthode via nix-shell (lancement rapide)

Sur NixOS, la méthode universelle ci-dessus fonctionne aussi.
Vous pouvez aussi lancer directement le logiciel via un `nix-shell` sans rien installer de permanent :

```bash
# Depuis le dossier du projet
nix-shell --packages 'python312.withPackages(ps: [ps.pyqt6 ps.reportlab])'

# Puis dans le shell Nix :
python3 main.py
```

Pour une intégration complète avec entrée de menu KDE/GNOME automatique via Flake,
utilisez le fichier `default.nix` fourni avec le projet et intégrez-le dans votre
`configuration.nix` ou Home Manager (voir documentation dédiée NixOS).

---

## Dépannage — Problèmes fréquents

### ❌ `ModuleNotFoundError: No module named 'PyQt6'`

L'environnement virtuel n'est pas activé ou les dépendances n'ont pas été installées.

```bash
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### ❌ `qt.qpa.plugin: Could not load the Qt platform plugin`

Les bibliothèques Qt système sont manquantes.

```bash
# Ubuntu / Debian
sudo apt install libxcb-xinerama0 libxcb-icccm4 libxcb-image0 \
    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0

# Fedora
sudo dnf install xcb-util-wm xcb-util-image xcb-util-keysyms

# Arch Linux
sudo pacman -S xcb-util-wm xcb-util-image xcb-util-keysyms
```

### ❌ Le fichier .desktop n'apparaît pas dans le menu

```bash
# Vérifier les droits d'exécution
chmod +x ~/.local/share/applications/editeur-chore.desktop

# Forcer la mise à jour
update-desktop-database ~/.local/share/applications
```

### ❌ `Permission denied` sur lancer_chore.sh

```bash
chmod +x /chemin/vers/choregraphie_editor_v3/lancer_chore.sh
```

### ❌ L'interface s'ouvre mais est vide ou grise

Variable d'environnement Qt manquante. Ajoutez ces lignes dans `lancer_chore.sh`
juste avant la ligne `exec python3` :

```bash
export QT_QPA_PLATFORM=xcb
export DISPLAY=:0
```

---

## Mettre à jour le logiciel

Pour mettre à jour vers une nouvelle version, remplacez les fichiers `.py` par les nouveaux.
Vos fichiers `.chore` (chorégraphies sauvegardées) ne sont jamais touchés.

```bash
# Via Git
cd ~/Téléchargements/Editeur-Chor-graphique-ASL-FFE
git pull

# Via ZIP — extraire par-dessus l'ancien dossier
cd ~/Téléchargements
unzip -o choregraphie_editor_nouvelle_version.zip

# Mettre à jour les dépendances si nécessaire
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

> 💡 Le fichier `OptionsMouvements.csv` (vos options personnalisées) n'est jamais
> sauvegarder par `unzip -o`. Faites-en une sauvegarde avant toute mise à jour par précaution. si vous utilisez un fichier personnaliser

---

*Éditeur Chorégraphique ASL-FFE — Version 2.2*
