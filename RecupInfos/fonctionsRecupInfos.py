import os  # Module pour interagir avec le système d'exploitation
import time  # Module pour gérer les délais et l'affichage de l'heure
import subprocess  # Module pour exécuter des commandes système
from prettytable import PrettyTable  # Module pour formater les tableaux en console
from colorama import Fore, Style  # Module pour ajouter des couleurs au texte
import psutil  # Module pour interagir avec les processus système
import json  # Module pour manipuler les données JSON
import platform  # Module pour détecter l'OS utilisé
import speedtest
import sys
import requests
def list_user_launched_applications(display=True):
    """
    Liste les applications utilisateur lancées sur Windows en utilisant PowerShell.
    Regroupe les applications identiques pour n'afficher qu'une seule entrée par application.
    """
    try:
        print(Fore.BLUE + "🔍 Recherche des applications utilisateur..." + Style.RESET_ALL)
        command = """
        Get-Process | Where-Object {
            ($_.MainWindowHandle -ne 0) -and 
            ($_.StartInfo.UserName -notmatch '^(NT AUTHORITY|SYSTEM|LOCAL SERVICE|NETWORK SERVICE)$') -and 
            ($_.MainWindowTitle -ne "")
        } | Select-Object -Property Id, ProcessName | Sort-Object -Property ProcessName
        """
        result = subprocess.run(["powershell", "-Command", command], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            raise Exception(Fore.RED + f"Erreur PowerShell : {result.stderr.strip()}" + Style.RESET_ALL)
        
        # Dictionnaire pour stocker les applications uniques
        unique_apps = {}
        
        lines = result.stdout.strip().splitlines()
        for line in lines[3:]:  # Ignorer les en-têtes (3 premières lignes)
            parts = line.split()
            if len(parts) >= 2:
                process_id = parts[0]
                process_name = " ".join(parts[1:])
                
                # Si l'application n'a pas déjà été ajoutée, l'ajouter
                if process_name not in unique_apps:
                    unique_apps[process_name] = process_id
        
        # Créer la liste des applications à partir du dictionnaire
        app_list = [{"ProcessName": name, "ProcessId": pid} for name, pid in unique_apps.items()]
        
        if display:
            table = PrettyTable()
            table.field_names = ["N°", "Nom de l'application", "PID"]
            for idx, app in enumerate(app_list, start=1):
                table.add_row([idx, app["ProcessName"], app["ProcessId"]])
            print(Fore.GREEN + str(table) + Style.RESET_ALL)
        return app_list
    except Exception as e:
        print(Fore.RED + f"❌ Erreur lors de la récupération des applications utilisateur : {e}" + Style.RESET_ALL)
        return []
def list_network_adapters():
    """
    Liste toutes les interfaces réseau disponibles sur le système.
    """
    try:
        print(Fore.BLUE + "🌐 Recherche des interfaces réseau..." + Style.RESET_ALL)
        command = "Get-NetAdapter | Select-Object -ExpandProperty Name"
        result = subprocess.run(["powershell", "-Command", command], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            raise Exception(Fore.RED + result.stderr.strip() + Style.RESET_ALL)
        
        adapters = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
        if not adapters:
            print(Fore.YELLOW + "⚠ Aucune interface réseau détectée." + Style.RESET_ALL)
        return adapters
    except Exception as e:
        print(Fore.RED + f"❌ Erreur lors de la récupération des interfaces réseau : {e}" + Style.RESET_ALL)
        return []

def get_network_bandwidth(selected_adapter_index=None):
    """
    Mesure la bande passante d'une carte réseau.
    
    Args:
        selected_adapter_index (int, optional): Index de l'adaptateur à utiliser. Si None, demande à l'utilisateur.
    """
    try:
        print(Fore.BLUE + "📶 Mesure de la bande passante en cours..." + Style.RESET_ALL)
        adapters = list_network_adapters()
        if not adapters:
            print(Fore.YELLOW + "⚠ Aucune interface réseau disponible." + Style.RESET_ALL)
            return {}
        
        # Si l'index n'est pas fourni, demander à l'utilisateur
        if selected_adapter_index is None:
            print("\nCartes réseau disponibles :")
            for idx, adapter in enumerate(adapters, start=1):
                print(Fore.CYAN + f"{idx} - {adapter}" + Style.RESET_ALL)
            
            choice = int(input(Fore.BLUE + "\nEntrez le numéro de la carte réseau pour le test : " + Style.RESET_ALL).strip())
        else:
            choice = selected_adapter_index
            
        if not (1 <= choice <= len(adapters)):
            print(Fore.RED + "❌ Choix invalide." + Style.RESET_ALL)
            return {}
        
        selected_adapter = adapters[choice - 1]
        print(Fore.GREEN + f"\nInterface sélectionnée : {selected_adapter}" + Style.RESET_ALL)
        
        # Le reste de votre code de test speedtest reste inchangé
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        speedtest_path = os.path.join(base_dir, "speedtest", "speedtest.exe")
        
        print(Fore.BLUE + "Exécution de Speedtest CLI... Cela peut prendre quelques secondes." + Style.RESET_ALL)
        
        result = subprocess.run([speedtest_path, "--format", "json"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if result.returncode != 0:
            raise Exception(Fore.RED + result.stderr.strip() + Style.RESET_ALL)
        
        data = json.loads(result.stdout)
        download_speed = data["download"]["bandwidth"] * 8 / 1_000_000  # Convertir en Mbps
        upload_speed = data["upload"]["bandwidth"] * 8 / 1_000_000  # Convertir en Mbps
        
        print(Fore.GREEN + f"📥 Débit descendant (Download) : {round(download_speed, 2)} Mbps" + Style.RESET_ALL)
        print(Fore.GREEN + f"📤 Débit montant (Upload) : {round(upload_speed, 2)} Mbps" + Style.RESET_ALL)
        
        return {
            "adapter": selected_adapter,
            "download_mbps": round(download_speed, 2),
            "upload_mbps": round(upload_speed, 2)
        }
    except Exception as e:
        print(Fore.RED + f"❌ Erreur lors de la mesure de la bande passante : {e}" + Style.RESET_ALL)
        return {}
def get_app_path(app_name):
    """
    Recherche et retourne le chemin complet d'un exécutable en fonction de son nom.
    Utilise `psutil` pour parcourir les processus actifs et récupérer le chemin du binaire.
    
    Args:
        app_name (str): Nom de l'application à rechercher.
    
    Returns:
        str: Chemin de l'exécutable de l'application, ou None si introuvable.
    """
    try:
        # Parcourir tous les processus en cours d'exécution
        for proc in psutil.process_iter(['name', 'exe']):
            # Vérifier si le nom de l'application correspond
            if proc.info['name'] and app_name.lower() in proc.info['name'].lower():
                return proc.info['exe']  # Retourner le chemin de l'exécutable
    except Exception as e:
        print(f"❌ Erreur lors de la récupération du chemin de l'application : {e}")
    return None  # Retourner None si l'application n'a pas été trouvée

if __name__ == "__main__":
    print("Ce fichier contient des fonctions et n'est pas destiné à être exécuté directement.")
    get_network_bandwidth()