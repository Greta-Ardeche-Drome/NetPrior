import os  # Module pour interagir avec le système d'exploitation
import time  # Module pour gérer les délais et l'affichage de l'heure
import subprocess  # Module pour exécuter des commandes système
from prettytable import PrettyTable  # Module pour formater les tableaux en console
from colorama import Fore, Style  # Module pour ajouter des couleurs au texte
import psutil  # Module pour interagir avec les processus système
import json  # Module pour manipuler les données JSON
import platform  # Module pour détecter l'OS utilisé

def verifier_regle_qos(app_name):
    """
    Vérifie si une règle de Qualité de Service (QoS) est appliquée à une application sous Windows.
    
    Args:
        app_name (str): Nom de l'application à vérifier.
    
    Returns:
        bool: True si une règle QoS est active, False sinon.
    """
    policy_name = f"QoS_{app_name}"  # Définir le nom de la politique QoS
    command = f"Get-NetQosPolicy -Name '{policy_name}' -PolicyStore ActiveStore"  # Commande PowerShell
    
    print(Fore.BLUE + f"🔎 Vérification de la QoS pour {app_name}..." + Style.RESET_ALL)

    # Exécuter la commande PowerShell pour vérifier l'existence de la règle
    result = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True)

    # Vérifier si une limitation de bande passante est définie
    if "ThrottleRateActionBitsPerSecond" in result.stdout:
        print(Fore.GREEN + f"✅ Une règle QoS est bien appliquée à {app_name}." + Style.RESET_ALL)
        return True
    else:
        print(Fore.YELLOW + f"⚠ Aucune règle QoS trouvée pour {app_name}." + Style.RESET_ALL)
        return False
    
def show_qos_policies():
    """
    Affiche les règles QoS actives avec un affichage structuré et coloré.
    """
    rules_data = get_qos_policies()
    if not rules_data:
        print(Fore.YELLOW + "\n📌 Aucune règle QoS active trouvée.\n" + Style.RESET_ALL)
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Nom de la règle", "Nom de l'application"]
    table.align = "l"
    
    for rule in rules_data:
        table.add_row([Fore.CYAN + str(rule["ID"]) + Style.RESET_ALL, 
                       Fore.GREEN + rule["RuleName"] + Style.RESET_ALL, 
                       Fore.BLUE + rule["AppName"] + Style.RESET_ALL])
    
    print("\n" + Fore.MAGENTA + "=" * 50)
    print("            📌 RÈGLES QoS ACTIVES 📌")
    print("=" * 50 + "\n" + Style.RESET_ALL)
    print(table)
    print(Fore.MAGENTA + "=" * 50 + "\n" + Style.RESET_ALL)

def get_qos_policies():
    """
    Récupère toutes les règles QoS actives et les retourne sous forme de liste.
    
    Returns:
        list: Liste des règles QoS actives sous forme de dictionnaire.
    """
    try:
        print(Fore.BLUE + "🔍 Récupération des règles QoS actives..." + Style.RESET_ALL)
        
        # Commande PowerShell pour récupérer les règles QoS
        command = (
            "Get-NetQosPolicy -PolicyStore ActiveStore | "
            "Select-Object Name, AppPathNameMatchCondition | ConvertTo-Csv -NoTypeInformation"
        )
        result = subprocess.run(["powershell", "-Command", command], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0 or not result.stdout.strip():
            print(Fore.YELLOW + "⚠ Aucune règle QoS active trouvée." + Style.RESET_ALL)
            return []
        
        lines = result.stdout.strip().splitlines()
        if len(lines) <= 1:
            print(Fore.YELLOW + "⚠ Aucune règle QoS active trouvée." + Style.RESET_ALL)
            return []
        
        rules_data = []
        for idx, line in enumerate(lines[1:], start=1):
            parts = line.split(',')
            if len(parts) < 2:
                continue  # Ignorer les entrées invalides
            
            rule_name = parts[0].strip().replace('"', '')
            app_path = parts[1].strip().replace('"', '')
            app_name = os.path.basename(app_path) if app_path and app_path.lower() != 'n/a' else "N/A"
            
            rules_data.append({
                "ID": idx,
                "RuleName": rule_name,
                "AppName": app_name
            })
        
        print(Fore.GREEN + f"✅ {len(rules_data)} règles QoS trouvées." + Style.RESET_ALL)
        return rules_data
    except Exception as e:
        print(Fore.RED + f"❌ Erreur lors de la récupération des règles QoS : {e}" + Style.RESET_ALL)
        return []

if __name__ == "__main__":
    print("Ce fichier contient des fonctions et n'est pas destiné à être exécuté directement.")