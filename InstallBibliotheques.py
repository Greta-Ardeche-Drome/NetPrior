import subprocess
import sys

# Liste des bibliothèques nécessaires
REQUIRED_LIBRARIES = [
    "colorama",         # Ajout de couleurs dans le terminal
    "prettytable",      # Affichage de tableaux
    "psutil",           # Gestion des processus système
    "pyfiglet",         # Affichage ASCII Art du titre
    "json",             # Manipulation de données JSON
]

def install_packages():
    """
    Vérifie et installe les bibliothèques nécessaires dynamiquement.
    """
    for package in REQUIRED_LIBRARIES:
        try:
            # Vérifie si le package est déjà installé
            __import__(package)
            print(f"✅ {package} est déjà installé.")
        except ImportError:
            print(f"📦 Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    print("\n✅ Toutes les bibliothèques sont installées et à jour.")

if __name__ == "__main__":
    install_packages()
