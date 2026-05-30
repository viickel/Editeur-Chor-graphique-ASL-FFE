{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "editeur-choregraphique-env";

  # Bibliothèques nécessaires à l'exécution et au rendu graphique
  buildInputs = [
    # Interpréteur et bibliothèques Python gérées par Nix
    pkgs.python3
    pkgs.python3Packages.pyqt6
    pkgs.python3Packages.reportlab
    
    # Dépendances système pour Qt6 et OpenGL
    pkgs.qt6.qtbase
    pkgs.qt6.qtsvg
    pkgs.qt6.qtwayland
    pkgs.mesa
    pkgs.libGL
    pkgs.xorg.libX11
  ];

  # Outils de compilation/packaging
  nativeBuildInputs = [
    pkgs.qt6.wrapQtAppsHook
  ];

  # Configuration de l'environnement au lancement
  shellHook = ''
    echo "--- Environnement Nix (PyQt6 + OpenGL) activé ---"
    
    # 1. Chemin vers les bibliothèques OpenGL/Mesa pour éviter l'erreur libGL.so.1
    export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.mesa pkgs.libGL pkgs.xorg.libX11 ]}:$LD_LIBRARY_PATH
    
    # 2. Chemin vers les plugins Qt pour éviter l'erreur de rendu des fenêtres
    export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt6.qtbase}/lib/qt-6/plugins/platforms"
    
    # 3. Création automatique de l'environnement virtuel pour les autres dépendances pip
    if [ ! -d ".venv" ]; then
      python3 -m venv .venv
    fi
    source .venv/bin/activate
    
    # Installation/Mise à jour des outils via pip
    pip install --upgrade pip
    if [ -f "choregraphie_editor/requirements.txt" ]; then
        pip install -r choregraphie_editor/requirements.txt
    fi
    
    echo "Python $(python --version) est prêt."
  '';
}