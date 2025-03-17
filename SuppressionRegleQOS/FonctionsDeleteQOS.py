import os  # Module pour interagir avec le système d'exploitation
import time  # Module pour gérer les délais et l'affichage de l'heure
import subprocess  # Module pour exécuter des commandes système
from prettytable import PrettyTable  # Module pour formater les tableaux en console
from colorama import Fore, Style  # Module pour ajouter des couleurs au texte
import psutil  # Module pour interagir avec les processus système
import json  # Module pour manipuler les données JSON
import platform  # Module pour détecter l'OS utilisé
import sys
sys.path.append(os.path.abspath('../InfoQOS'))
from InfoQOS.PolicyQOS import get_qos_policies,show_qos_policies

def remove_bandwidth_limit(rule_id):
    """
    Supprime une règle QoS appliquée à une application en fonction de son ID.

    Args:
        rule_id (int): L'ID de la règle à supprimer.
    """
    try:
        rules = get_qos_policies()
        if not rules:
            print(Fore.YELLOW + "⚠ Aucune règle QoS active à supprimer." + Style.RESET_ALL)
            return
        
        rule_to_delete = next((rule for rule in rules if rule["ID"] == rule_id), None)
        if not rule_to_delete:
            print(Fore.RED + "❌ ID invalide. Aucune suppression effectuée." + Style.RESET_ALL)
            return
        
        policy_name = rule_to_delete["RuleName"]

        print(Fore.BLUE + f"🔍 Suppression de la règle QoS '{policy_name}'..." + Style.RESET_ALL)
        
        cmd = f"Remove-NetQosPolicy -Name '{policy_name}' -PolicyStore ActiveStore -Confirm:$false"
        result = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True)

        if result.returncode == 0:
            print(Fore.GREEN + f"✅ La règle QoS '{policy_name}' a été supprimée avec succès." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"❌ Erreur lors de la suppression de la règle QoS : {result.stderr}" + Style.RESET_ALL)
    
    except Exception as e:
        print(Fore.RED + f"❌ Une erreur s'est produite lors de la suppression de la règle QoS : {e}" + Style.RESET_ALL)

def handle_remove_qos_rule():
    """
    Gère la suppression d'une règle QoS depuis le menu principal.
    """
    rules = get_qos_policies()
    if not rules:
        print(Fore.YELLOW + "⚠ Aucune règle QoS active à supprimer." + Style.RESET_ALL)
        return
    
    show_qos_policies()  # Afficher la liste actuelle une seule fois avant suppression
    
    try:
        rule_id = int(input(Fore.BLUE + "🛑 Entrez l'ID de la règle à supprimer : " + Style.RESET_ALL).strip())
        
        # Vérifier si l'ID existe
        if any(rule["ID"] == rule_id for rule in rules):
            remove_bandwidth_limit(rule_id)  
            
            print(Fore.BLUE + "\n🔄 Mise à jour de la liste des règles QoS...\n" + Style.RESET_ALL)
            time.sleep(2)  # Pause pour rafraîchir l'affichage
            
            rules = get_qos_policies()  # Récupérer la nouvelle liste
            if rules:
                show_qos_policies()  # 🔥 Afficher uniquement si des règles restent
            else:
                print(Fore.YELLOW + "📌 Aucune règle QoS active restante.\n" + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ ID invalide. Veuillez entrer un ID existant." + Style.RESET_ALL)
    
    except ValueError:
        print(Fore.RED + "❌ Entrée invalide. Veuillez entrer un nombre entier." + Style.RESET_ALL)

if __name__ == "__main__":
    print("Ce fichier contient des fonctions et n'est pas destiné à être exécuté directement.")
