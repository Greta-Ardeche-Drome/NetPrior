import subprocess
import sys

# Liste des bibliothèques nécessaires
REQUIRED_LIBRARIES = [
    "colorama",
    "prettytable", 
    "psutil",
    "pyfiglet",
    "speedtest-cli",
    "requests"
]

def install_packages():
    """
    Installe toutes les bibliothèques nécessaires.
    """
    print("🚀 Installation des bibliothèques NetPrior...\n")
    
    for package in REQUIRED_LIBRARIES:
        try:
            print(f"📦 Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installé avec succès.\n")
        except subprocess.CalledProcessError:
            print(f"❌ Erreur lors de l'installation de {package}.\n")
    
    print("🎉 Installation terminée !")
    print("\nPour utiliser NetPrior :")
    print("- Interface CLI : python main.py")
    print("- Interface GUI : python interf.py")

if __name__ == "__main__":
    install_packages()
