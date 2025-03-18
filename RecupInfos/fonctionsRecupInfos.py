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
        
        app_list = []
        lines = result.stdout.strip().splitlines()
        for line in lines[3:]:
            parts = line.split()
            if len(parts) >= 2:
                app_list.append({"ProcessName": " ".join(parts[1:]), "ProcessId": parts[0]})
        
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

def get_network_bandwidth():
    """
    Demande à l'utilisateur de choisir une carte réseau pour tester la bande passante.
    Utilise speedtest-cli pour mesurer la vitesse de connexion internet.
    """
    try:
        print(Fore.BLUE + "📶 Mesure de la bande passante en cours..." + Style.RESET_ALL)
        adapters = list_network_adapters()
        if not adapters:
            print(Fore.YELLOW + "⚠ Aucune interface réseau disponible." + Style.RESET_ALL)
            return {}
        
        print("\nCartes réseau disponibles :")
        for idx, adapter in enumerate(adapters, start=1):
            print(Fore.CYAN + f"{idx} - {adapter}" + Style.RESET_ALL)1
        
        choice = int(input(Fore.BLUE + "\nEntrez le numéro de la carte réseau pour le test : " + Style.RESET_ALL).strip())
        if not (1 <= choice <= len(adapters)):
            print(Fore.RED + "❌ Choix invalide." + Style.RESET_ALL)
            return {}
        
        selected_adapter = adapters[choice - 1]
        print(Fore.GREEN + f"\nInterface sélectionnée : {selected_adapter}" + Style.RESET_ALL)
        
        # Vérifier si speedtest-cli est installé, sinon l'installer
        try:
            import speedtest
        except ImportError:
            print(Fore.YELLOW + "⚠ Module speedtest-cli non trouvé. Installation en cours..." + Style.RESET_ALL)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "speedtest-cli"])
            import speedtest
        
        print(Fore.BLUE + "Exécution du test de vitesse... Cela peut prendre quelques secondes." + Style.RESET_ALL)
        
        # Créer l'objet Speedtest
        st = speedtest.Speedtest()
        
        # Trouver le meilleur serveur
        print(Fore.CYAN + "Recherche du meilleur serveur..." + Style.RESET_ALL)
        st.get_best_server()
        
        # Mesurer la vitesse de téléchargement
        print(Fore.CYAN + "Mesure de la vitesse de téléchargement..." + Style.RESET_ALL)
        download_speed = st.download() / 1_000_000  # Convertir en Mbps
        
        # Mesurer la vitesse d'envoi
        print(Fore.CYAN + "Mesure de la vitesse d'envoi..." + Style.RESET_ALL)
        upload_speed = st.upload() / 1_000_000  # Convertir en Mbps
        
        # Mesurer la latence (ping)
        latency = st.results.ping
        
        print(Fore.GREEN + f"📥 Débit descendant (Download) : {round(download_speed, 2)} Mbps" + Style.RESET_ALL)
        print(Fore.GREEN + f"📤 Débit montant (Upload) : {round(upload_speed, 2)} Mbps" + Style.RESET_ALL)
        print(Fore.GREEN + f"🔄 Latence (Ping) : {round(latency, 2)} ms" + Style.RESET_ALL)
        
        return {
            "adapter": selected_adapter,
            "download_mbps": round(download_speed, 2),
            "upload_mbps": round(upload_speed, 2),
            "latency_ms": round(latency, 2)
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