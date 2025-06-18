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

# Import conditionnel de speedtest avec gestion d'erreur
SPEEDTEST_AVAILABLE = False
try:
    import speedtest
    SPEEDTEST_AVAILABLE = True
    print("✅ Module speedtest-cli chargé avec succès")
except ImportError as e:
    print(f"⚠ Module speedtest-cli non disponible: {e}")
    SPEEDTEST_AVAILABLE = False
except Exception as e:
    print(f"⚠ Erreur lors du chargement de speedtest-cli: {e}")
    SPEEDTEST_AVAILABLE = False

def get_friendly_app_names():
    """
    Dictionnaire pour convertir les noms techniques en noms compréhensibles
    """
    return {
        # Navigateurs
        'chrome.exe': '🌐 Google Chrome',
        'firefox.exe': '🦊 Mozilla Firefox',
        'msedge.exe': '🔷 Microsoft Edge',
        'brave.exe': '🦁 Brave Browser',
        'opera.exe': '🎭 Opera Browser',
        'iexplore.exe': '🌐 Internet Explorer',
        
        # Éditeurs de code/texte
        'code.exe': '⚡ Visual Studio Code',
        'Code.exe': '⚡ Visual Studio Code',
        'notepad.exe': '📝 Bloc-notes',
        'notepad++.exe': '📝 Notepad++',
        'sublime_text.exe': '📝 Sublime Text',
        'atom.exe': '⚛️ Atom Editor',
        'vim.exe': '📝 Vim Editor',
        
        # Communication
        'discord.exe': '💬 Discord',
        'Discord.exe': '💬 Discord',
        'teams.exe': '👥 Microsoft Teams',
        'zoom.exe': '📹 Zoom',
        'skype.exe': '📞 Skype',
        'slack.exe': '💼 Slack',
        'whatsapp.exe': '💬 WhatsApp',
        'telegram.exe': '✈️ Telegram',
        
        # Média
        'spotify.exe': '🎵 Spotify',
        'vlc.exe': '🎬 VLC Media Player',
        'foobar2000.exe': '🎵 Foobar2000',
        'winamp.exe': '🎵 Winamp',
        'itunes.exe': '🎵 iTunes',
        'netflix.exe': '🎬 Netflix',
        'youtube.exe': '📺 YouTube',
        
        # Jeux
        'steam.exe': '🎮 Steam',
        'epicgameslauncher.exe': '🎮 Epic Games',
        'origin.exe': '🎮 EA Origin',
        'uplay.exe': '🎮 Ubisoft Connect',
        'battle.net.exe': '🎮 Battle.net',
        'minecraft.exe': '🧱 Minecraft',
        
        # Email
        'outlook.exe': '📧 Microsoft Outlook',
        'thunderbird.exe': '📧 Thunderbird',
        'mailspring.exe': '📧 Mailspring',
        
        # Bureau/Productivité
        'winword.exe': '📄 Microsoft Word',
        'excel.exe': '📊 Microsoft Excel',
        'powerpnt.exe': '📊 Microsoft PowerPoint',
        'soffice.exe': '📄 LibreOffice',
        'onenote.exe': '📔 OneNote',
        'notion.exe': '📋 Notion',
        
        # Graphisme/Design
        'photoshop.exe': '🎨 Adobe Photoshop',
        'illustrator.exe': '🎨 Adobe Illustrator',
        'gimp.exe': '🎨 GIMP',
        'paint.exe': '🎨 Paint',
        'mspaint.exe': '🎨 Paint',
        'canva.exe': '🎨 Canva',
        
        # Système
        'explorer.exe': '📁 Explorateur de fichiers',
        'calculator.exe': '🧮 Calculatrice',
        'calc.exe': '🧮 Calculatrice',
        'cmd.exe': '⚫ Invite de commandes',
        'powershell.exe': '🔷 PowerShell',
        
        # Développement
        'python.exe': '🐍 Python',
        'pythonw.exe': '🐍 Python',
        'python3.11.exe': '🐍 Python 3.11',
        'python3.11': '🐍 Python 3.11',
        'java.exe': '☕ Java',
        'node.exe': '🟢 Node.js',
        'git.exe': '📂 Git',
        'git-bash.exe': '📂 Git Bash',
        
        # Stockage/Cloud
        'onedrive.exe': '☁️ OneDrive',
        'googledrive.exe': '☁️ Google Drive',
        'dropbox.exe': '☁️ Dropbox',
        'sync.exe': '☁️ Sync',
        
        # Utilitaires
        'everything.exe': '🔍 Everything',
        'Everything.exe': '🔍 Everything',
        'winrar.exe': '📦 WinRAR',
        '7z.exe': '📦 7-Zip',
        'wireshark.exe': '🌐 Wireshark',
        'putty.exe': '🌐 PuTTY',
        
        # Sécurité
        'protonvpn.exe': '🔒 ProtonVPN',
        'ProtonVPN.exe': '🔒 ProtonVPN',
        'nordvpn.exe': '🔒 NordVPN',
        'expressvpn.exe': '🔒 ExpressVPN',
        
        # Applications spécifiques mentionnées dans votre interface
        'NLClientApp.exe': '📱 NL Client App',
        'NLClientApp': '📱 NL Client App',
        'Photos.exe': '📷 Photos',
        'GitHubDesktop.exe': '📂 GitHub Desktop',

        'CompPkgSrv.exe': '📦 Service de packages Windows',
        'RuntimeBroker.exe': '🔗 Gestionnaire d\'applications Windows',
        'explorer.exe': '📁 Explorateur Windows',
        'msedge.exe': '🌐 Microsoft Edge (processus)',
        'WUDFSvc': '🔧 Service de pilotes Windows',
        'svchost.exe': '⚙️ Service hôte Windows',
        'bits.exe': '📥 Service de transfert Windows',
        'OneDrive.exe': '☁️ OneDrive (synchronisation)',
        'MsMpEng.exe': '🛡️ Windows Defender',
        'WinStore.App.exe': '🏪 Microsoft Store (processus)',
    }

# ==========================================
# FONCTION POUR CONVERTIR LES NOMS
# ==========================================

def get_friendly_name(process_name):
    """
    Convertit un nom de processus technique en nom compréhensible
    
    Args:
        process_name (str): Nom technique du processus (ex: "msedge.exe")
    
    Returns:
        str: Nom compréhensible (ex: "🔷 Microsoft Edge")
    """
    friendly_names = get_friendly_app_names()
    
    # Recherche exacte d'abord
    if process_name in friendly_names:
        return friendly_names[process_name]
    
    # Recherche sans .exe
    name_without_exe = process_name.replace('.exe', '')
    if name_without_exe in friendly_names:
        return friendly_names[name_without_exe]
    
    # Recherche insensible à la casse
    for tech_name, friendly_name in friendly_names.items():
        if tech_name.lower() == process_name.lower():
            return friendly_name
    
    # Si aucune correspondance, nettoyer le nom technique
    clean_name = process_name.replace('.exe', '').replace('_', ' ').title()
    
    # Ajouter un icône générique selon le type
    if any(keyword in process_name.lower() for keyword in ['browser', 'chrome', 'firefox', 'edge']):
        return f"🌐 {clean_name}"
    elif any(keyword in process_name.lower() for keyword in ['code', 'editor', 'notepad']):
        return f"📝 {clean_name}"
    elif any(keyword in process_name.lower() for keyword in ['game', 'steam', 'epic']):
        return f"🎮 {clean_name}"
    elif any(keyword in process_name.lower() for keyword in ['music', 'audio', 'media']):
        return f"🎵 {clean_name}"
    elif any(keyword in process_name.lower() for keyword in ['python', 'java', 'node']):
        return f"💻 {clean_name}"
    else:
        return f"📱 {clean_name}"
def list_user_launched_applications(display=True):
    """
    Liste UNIQUEMENT les applications utilisateur lancées sur Windows.
    Exclut complètement les processus système.
    
    Args:
        display (bool): Si True, affiche le résultat dans la console.
    
    Returns:
        list: Liste des applications UTILISATEUR uniquement.
    """
    try:
        if display:
            print("🔍 Recherche des applications utilisateur...")
        
        # 1. UNIQUEMENT les applications utilisateur avec interface graphique
        user_apps_command = """
        Get-Process | Where-Object {
            ($_.MainWindowHandle -ne 0) -and 
            ($_.MainWindowTitle -ne "") -and
            ($_.ProcessName -notmatch '^(svchost|System|lsass|services|spoolsv|wininit|csrss|dwm|winlogon|audiodg|conhost|smss|MsMpEng|RuntimeBroker|WUDFSvc|WinStore|CompPkgSrv|bits|OneDrive|WUDFHost)$')
        } | Select-Object -Property Id, ProcessName, MainWindowTitle | Sort-Object -Property ProcessName
        """
        
        user_result = subprocess.run(
            ["powershell", "-Command", user_apps_command], 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        if user_result.returncode != 0:
            raise Exception(f"Erreur PowerShell : {user_result.stderr.strip()}")
        
        # Dictionnaire pour éviter les doublons
        unique_user_apps = {}
        
        # Traitement des applications utilisateur UNIQUEMENT
        user_lines = user_result.stdout.strip().splitlines()
        for line in user_lines[3:]:  # Ignorer les en-têtes PowerShell
            parts = line.split()
            if len(parts) >= 3:  # ID ProcessName MainWindowTitle
                process_id = parts[0]
                process_name = parts[1]
                
                # Liste blanche des applications utilisateur courantes
                user_app_patterns = [
                    'chrome', 'firefox', 'edge', 'brave', 'opera',  # Navigateurs
                    'code', 'notepad', 'wordpad', 'sublime', 'atom',  # Éditeurs
                    'discord', 'teams', 'zoom', 'skype', 'slack',  # Communication
                    'spotify', 'vlc', 'foobar', 'winamp',  # Média
                    'steam', 'origin', 'epic', 'uplay',  # Jeux
                    'outlook', 'thunderbird', 'mail',  # Email
                    'word', 'excel', 'powerpoint', 'libreoffice',  # Bureau
                    'photoshop', 'gimp', 'paint', 'mspaint',  # Graphisme
                    'explorer',  # Explorateur de fichiers
                    'calculator', 'calc',  # Calculatrice
                    'python', 'java', 'node',  # Développement
                ]
                
                # Vérifier si c'est une application utilisateur légitime
                is_user_app = any(pattern.lower() in process_name.lower() 
                                for pattern in user_app_patterns)
                
                # OU vérifier que ce n'est PAS un processus système
                system_processes = [
                    'svchost', 'system', 'lsass', 'services', 'spoolsv', 
                    'wininit', 'csrss', 'dwm', 'winlogon', 'audiodg', 
                    'conhost', 'smss', 'msmpeeng', 'runtimebroker', 
                    'wudfsvc', 'winstore', 'comppkgsrv', 'bits', 'wudfhost'
                ]
                
                is_system_process = any(sys_proc.lower() in process_name.lower() 
                                      for sys_proc in system_processes)
                
                # Ajouter seulement si c'est une app utilisateur ET pas un processus système
                if (process_name not in unique_user_apps and 
                    not is_system_process and
                    not process_name.lower().endswith('.scr')):  # Pas d'économiseurs d'écran
                    unique_user_apps[process_name] = process_id
        
        # Créer la liste finale - APPLICATIONS UTILISATEUR UNIQUEMENT
        app_list = [{"ProcessName": name, "ProcessId": pid, "Type": "user"} 
                   for name, pid in unique_user_apps.items()]
        
        if display:
            print(f"✅ Trouvé {len(app_list)} applications utilisateur")
            for app in app_list:
                print(f"  📱 {app['ProcessName']} (PID: {app['ProcessId']})")
        
        return app_list
        
    except Exception as e:
        if display:
            print(f"❌ Erreur lors de la récupération des applications : {e}")
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

def get_network_bandwidth2(selected_adapter_index=None):
    """
    Mesure la bande passante d'une carte réseau en utilisant speedtest-cli Python.
    
    Args:
        selected_adapter_index (int, optional): Index de l'adaptateur à utiliser. Si None, utilise l'interface par défaut.
    
    Returns:
        dict: Résultats du test de vitesse
    """
    try:
        print(Fore.BLUE + "🚀 Initialisation du test speedtest-cli Python..." + Style.RESET_ALL)
        
        # Sélection de l'interface réseau
        selected_interface_name = "Auto"
        selected_interface_ip = None
        
        # Si un index d'adaptateur est fourni, essayer de l'utiliser
        if selected_adapter_index is not None:
            adapters = list_network_adapters()
            if adapters and 1 <= selected_adapter_index <= len(adapters):
                selected_interface_name = adapters[selected_adapter_index - 1]
                
                # Obtenir l'IP de l'interface sélectionnée
                try:
                    # Utiliser psutil pour obtenir l'IP de l'interface
                    import psutil
                    import socket
                    
                    addrs = psutil.net_if_addrs()
                    if selected_interface_name in addrs:
                        for addr in addrs[selected_interface_name]:
                            if addr.family == socket.AF_INET:  # IPv4
                                selected_interface_ip = addr.address
                                break
                except Exception as e:
                    print(Fore.YELLOW + f"⚠ Impossible d'obtenir l'IP de l'interface: {e}" + Style.RESET_ALL)
        
        print(Fore.GREEN + f"\nInterface sélectionnée : {selected_interface_name}" + Style.RESET_ALL)
        if selected_interface_ip:
            print(Fore.GREEN + f"IP de l'interface : {selected_interface_ip}" + Style.RESET_ALL)
        
        # Créer l'objet speedtest avec ou sans interface spécifique
        import speedtest
        
        if selected_interface_ip and selected_interface_name != "Auto":
            print(Fore.CYAN + f"🔧 Configuration pour l'interface: {selected_interface_name}" + Style.RESET_ALL)
            st = speedtest.Speedtest(source_address=selected_interface_ip)
        else:
            print(Fore.CYAN + "🔧 Configuration automatique (interface par défaut)" + Style.RESET_ALL)
            st = speedtest.Speedtest()
        
        print(Fore.CYAN + "📡 Recherche du meilleur serveur..." + Style.RESET_ALL)
        # Obtenir la liste des serveurs et sélectionner le meilleur
        st.get_best_server()
        
        print(f"Serveur sélectionné: {st.results.server['sponsor']} - {st.results.server['name']}")
        print(f"Distance: {st.results.server['d']:.2f} km")
        print(f"Pays: {st.results.server['country']} - {st.results.server['cc']}")
        
        print(Fore.YELLOW + "📥 Test de téléchargement..." + Style.RESET_ALL)
        download_speed = st.download()
        download_mbps = download_speed / 1_000_000  # Convertir en Mbps
        
        print(Fore.YELLOW + "📤 Test d'upload..." + Style.RESET_ALL)
        upload_speed = st.upload()
        upload_mbps = upload_speed / 1_000_000  # Convertir en Mbps
        
        # Ping est déjà calculé lors de get_best_server()
        ping = st.results.ping
        
        print(Fore.GREEN + "\n" + "="*50)
        print(f"📥 Download: {download_mbps:.2f} Mbps")
        print(f"📤 Upload: {upload_mbps:.2f} Mbps") 
        print(f"🏓 Ping: {ping:.2f} ms")
        print(f"🌐 Interface: {selected_interface_name}")
        print("="*50 + Style.RESET_ALL)
        
        return {
            "adapter": selected_interface_name,
            "download_mbps": round(download_mbps, 2),
            "upload_mbps": round(upload_mbps, 2),
            "latency": round(ping, 2),
            "server": st.results.server['sponsor'],
            "location": st.results.server['name'],
            "country": st.results.server['country']
        }
        
    except ImportError:
        print(Fore.RED + "❌ Module speedtest-cli non installé. Installez-le avec: pip install speedtest-cli" + Style.RESET_ALL)
        return {}
    except speedtest.ConfigRetrievalError:
        print(Fore.RED + "❌ Erreur de configuration réseau" + Style.RESET_ALL)
        print(Fore.CYAN + "💡 Suggestions :" + Style.RESET_ALL)
        print("   - Vérifiez votre connexion Internet")
        print("   - Désactivez temporairement votre VPN")
        return {}
    except speedtest.NoMatchedServers:
        print(Fore.RED + "❌ Aucun serveur speedtest trouvé" + Style.RESET_ALL)
        print(Fore.CYAN + "💡 Suggestions :" + Style.RESET_ALL)
        print("   - Vérifiez votre connexion Internet")
        print("   - Réessayez dans quelques minutes")
        return {}
    except Exception as e:
        print(Fore.RED + f"❌ Erreur lors de la mesure de la bande passante : {e}" + Style.RESET_ALL)
        print(Fore.CYAN + "💡 Suggestions :" + Style.RESET_ALL)
        print("   - Désactivez temporairement votre VPN")
        print("   - Sélectionnez une interface réseau physique (Ethernet/WiFi)")
        print("   - Vérifiez votre connexion Internet")
        return {}

get_network_bandwidth = get_network_bandwidth2
if __name__ == "__main__":
    print("Ce fichier contient des fonctions et n'est pas destiné à être exécuté directement.")
    #get_network_bandwidth2()