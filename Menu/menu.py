import os  # Module pour interagir avec le système d'exploitation
import time  # Module pour gérer les délais et l'affichage de l'heure
import pyfiglet  # Module pour afficher du texte stylisé en ASCII Art
import subprocess  # Module pour exécuter des commandes système
from prettytable import PrettyTable  # Module pour formater les tableaux en console
from colorama import Fore, Style  # Module pour ajouter des couleurs au texte
import sys

# Correction des chemins d'imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Ajouter les chemins correctement
sys.path.extend([
    os.path.join(parent_dir, 'RecupInfos'),
    os.path.join(parent_dir, 'InfoQOS'),
    os.path.join(parent_dir, 'CreationRegleQOS'),
    os.path.join(parent_dir, 'SuppressionRegleQOS')
])

# Maintenant faire les imports
try:
    from RecupInfos.fonctionsRecupInfos import (
        list_user_launched_applications,
        list_network_adapters,
        get_network_bandwidth,
        get_app_path
    )
    from InfoQOS.PolicyQOS import (
        verifier_regle_qos,
        show_qos_policies,
        get_qos_policies
    )
    from CreationRegleQOS.CreateQOS import limit_application_bandwidth
    from SuppressionRegleQOS.FonctionsDeleteQOS import (
        remove_bandwidth_limit,
        handle_remove_qos_rule
    )
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Vérifiez que tous les fichiers sont présents dans les bons dossiers")
    sys.exit(1)

# ================================
# Fonction pour afficher la bannière stylisée façon "hacking"
# ================================
def print_banner():
    """
    Affiche une bannière stylisée avec un effet "hacking" en vert fluorescent.
    """
    os.system("cls" if os.name == "nt" else "clear")  # Efface l'écran pour une meilleure lisibilité
    banner = pyfiglet.figlet_format("NETPRIOR")
    print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)

# ================================
# Fonction pour afficher le menu principal avec un style hacking
# ================================
def main_menu():
    """
    Affiche le menu principal avec une interface style "hacker".
    """
    while True:
        print_banner()
        print(Fore.GREEN + "📡 Bienvenue " + os.getlogin() + " !" + Style.RESET_ALL)
        print(Fore.GREEN + "⌛ Date : " + time.strftime('%Y-%m-%d %H:%M:%S') + Style.RESET_ALL)
        print(Fore.LIGHTBLACK_EX + "=" * 50 + Style.RESET_ALL)
        print(Fore.CYAN + "[1] 📜 Afficher les applications utilisateur lancées")
        print("[2] 🌐 Afficher la bande passante en entrée des cartes réseaux")
        print("[3] 🎯 Limiter une application utilisateur")
        print("[4] 🔎 Afficher les règles QoS mises en place")
        print("[5] ❌ Supprimer une règle QoS")
        print("[6] 🛑 Quitter")
        print(Fore.LIGHTBLACK_EX + "=" * 50 + Style.RESET_ALL)

        choice = input(Fore.YELLOW + "🔹 Entrez votre choix : " + Style.RESET_ALL).strip()

        if choice == "1":
            list_user_launched_applications()
        elif choice == "2":
            get_network_bandwidth()
        elif choice == "3":
            app_name = input(Fore.MAGENTA + "🎯 Nom de l'application (ex: discord.exe) : " + Style.RESET_ALL).strip()
            try:
                limit_kbps = int(input("📉 Limite de bande passante en Kbits/sec : "))
                limit_application_bandwidth(app_name, limit_kbps)
            except ValueError:
                print(Fore.RED + "❌ Entrée invalide. Veuillez entrer un nombre entier." + Style.RESET_ALL)
        elif choice == "4":
            show_qos_policies()
        elif choice == "5":
            handle_remove_qos_rule()
        elif choice == "6":
            print(Fore.RED + "Merci d'avoir utilisé NETPRIOR !" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "❌ Choix invalide. Veuillez réessayer." + Style.RESET_ALL)

        input(Fore.LIGHTBLUE_EX + "\n🔷 Appuyez sur Entrée pour continuer..." + Style.RESET_ALL)

# ================================
# Point d'entrée principal du programme
# ================================
if __name__ == "__main__":
    main_menu()  # Lancer le menu principal