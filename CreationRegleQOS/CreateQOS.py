import os  # Module pour interagir avec le système d'exploitation
import time  # Module pour gérer les délais et l'affichage de l'heure
import subprocess  # Module pour exécuter des commandes système
from prettytable import PrettyTable  # Module pour formater les tableaux en console
from colorama import Fore, Style  # Module pour ajouter des couleurs au texte
import psutil  # Module pour interagir avec les processus système
import json  # Module pour manipuler les données JSON
import platform  # Module pour détecter l'OS utilisé
import sys
sys.path.extend([
    os.path.abspath('../RecupInfos'),
    os.path.abspath('../InfoQOS'),
    os.path.abspath('../AutreRepertoire')
])
from RecupInfos.fonctionsRecupInfos import get_app_path
from InfoQOS.PolicyQOS import verifier_regle_qos


def limit_application_bandwidth(app_name, limit_kbps):
    """
    Applique une règle QoS pour limiter la bande passante d'une application sous Windows.
    
    Args:
        app_name (str): Nom de l'application à limiter.
        limit_kbps (int): Limite de bande passante en kilobits par seconde.
    """
    if platform.system() != "Windows":
        print(Fore.RED + "❌ La QoS via NetQosPolicy est uniquement disponible sur Windows." + Style.RESET_ALL)
        return
    
    print(Fore.BLUE + f"📌 Application d'une règle QoS sur {app_name}..." + Style.RESET_ALL)

    # Obtenir le chemin de l'application
    app_path = get_app_path(app_name)
    if not app_path:
        print(Fore.RED + f"❌ Impossible de trouver {app_name}. Vérifiez que l'application est en cours d'exécution." + Style.RESET_ALL)
        return
    
    throttle_rate = limit_kbps * 1_000  # Convertir Kbps en bps
    policy_name = f"QoS_{app_name}"  # Nom de la règle QoS

    # Supprimer toute règle existante pour éviter les conflits
    subprocess.run(["powershell", "-NoProfile", "-Command", f"Remove-NetQosPolicy -Name '{policy_name}' -PolicyStore ActiveStore -Confirm:$false"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Ajouter la nouvelle règle QoS
    cmd = f'New-NetQosPolicy -Name "{policy_name}" -AppPathNameMatchCondition "{app_path}" -ThrottleRateActionBitsPerSecond {throttle_rate} -PolicyStore ActiveStore'
    
    print(Fore.CYAN + f"🔍 Commande exécutée : {cmd}" + Style.RESET_ALL)  # Afficher la commande exécutée pour debug

    # Exécuter la commande pour appliquer la règle QoS
    result = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True)

    if result.returncode == 0:
        print(Fore.GREEN + f"✅ QoS appliquée : {app_name} limité à {limit_kbps} Kbits/sec ({throttle_rate} bps)." + Style.RESET_ALL)
        time.sleep(2)  # Pause pour laisser Windows appliquer la règle
        if verifier_regle_qos(app_name):
            print(Fore.GREEN + f"✅ Vérification réussie : La QoS est bien active pour {app_name}." + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"⚠ La règle QoS ne semble pas active. Essayez de redémarrer l'interface réseau avec 'Restart-NetAdapter'." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ Erreur lors de l'application de la QoS : {result.stderr}" + Style.RESET_ALL)

if __name__ == "__main__":
    print("Ce fichier contient des fonctions et n'est pas destiné à être exécuté directement.")
