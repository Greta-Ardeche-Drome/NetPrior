🚀 NetPrior - Gestion de la Qualité de Service (QoS) sous Windows

	Optimisez votre bande passante en gérant efficacement la priorité réseau de vos applications sous Windows grâce à des règles QoS automatisées via PowerShell.
	💻 Interface interactive et colorée – 🎨 Expérience utilisateur optimisée – ⚡ Contrôle total sur votre trafic réseau

📌 Description du Projet

	NetPrior permet de gérer la bande passante des applications sous Windows en appliquant des règles QoS via PowerShell.
	Grâce à une interface en ligne de commande ergonomique, vous pouvez facilement :
		✅ Lister les applications actives
		✅ Afficher la bande passante des cartes réseau
		✅ Limiter la bande passante d’une application
		✅ Visualiser et supprimer des règles QoS
		🔧 Installation et Exécution

🛠 1️⃣ Prérequis

	Avant d’utiliser NetPrior, assurez-vous d’avoir :

    		✅ Windows (obligatoire pour exécuter les commandes PowerShell)
    		✅ Python 3.x installé
    		✅ Speedtest CLI (inclus dans le projet)

📦 2️⃣ Installation des Dépendances

	Installez toutes les bibliothèques requises en exécutant :

	python InstallBibliotheques.py

	📌 Bibliothèques utilisées :

    		🖼️ pyfiglet → Affichage ASCII Art du titre
    		📊 prettytable → Affichage des tableaux formatés
    		🎨 colorama → Interface CLI colorée
    		⚙️ psutil → Gestion des processus système
    		🗂️ json → Manipulation de données JSON

👉 Installation manuelle des dépendances :

	pip install pyfiglet prettytable colorama psutil json

🚀 3️⃣ Lancer le Programme

	Une fois les dépendances installées, démarrez NetPrior avec :

		python main.py

	📜 Menu interactif :

	========================================
	            NETPRIOR - MENU
	========================================
	1 - Afficher les applications utilisateur lancées
	2 - Afficher la bande passante des cartes réseau
	3 - Limiter une application utilisateur
	4 - Afficher les règles QoS mises en place
	5 - Supprimer une règle QoS
	6 - Quitter
	========================================
	Entrez votre choix :

📝 Fonctionnalités

	✅ Lister les applications utilisateur actives
	✅ Afficher la bande passante des cartes réseau
	✅ Limiter la bande passante d’une application
	✅ Afficher et supprimer une règle QoS existante

✨ Exemple d'affichage des règles QoS actives :

	📌 RÈGLES QoS ACTIVES 📌
	========================================
	| ID | Nom de la règle  | Nom de l'application |
	|----|-----------------|----------------------|
	| 1  | qos_discord.exe | discord.exe         |
	========================================

📂 Structure du Projet

	NetPrior/
	│── CreationRegleQOS/
	│   ├── CreateQOS.py          
	│── InfoQOS/
	│── Menu/
	│   ├── menu.py               
	│── RecupInfos/
	│   ├── fonctionsRecupInfos.py  
	│── speedtest/
	│   ├── speedtest.exe         
	│── SuppressionRegleQOS/
	│   ├── SuppressionRegleQOS.py 
	│── InstallBibliotheques.py   
	│── main.py                   

📄 Explication des fichiers

    🏁 main.py → Point d’entrée du programme, affiche le menu interactif
    🎛️ menu.py → Gère l’interface CLI et les interactions utilisateur
    ⚙️ CreateQOS.py → Applique une règle QoS à une application
    ❌ SuppressionRegleQOS.py → Supprime une règle QoS active
    📡 fonctionsRecupInfos.py → Récupère les informations réseau et système
    🚀 speedtest.exe → Mesure la bande passante
    🛠️ InstallBibliotheques.py → Installe les bibliothèques requises

🎯 Pourquoi utiliser NetPrior ?

	✅ Simple et rapide : Interface intuitive pour configurer des règles QoS en quelques secondes
	✅ 100% Windows : Exploite les commandes PowerShell pour une compatibilité optimale
	✅ Boostez votre connexion : Priorisez les applications essentielles et évitez les ralentissements
	✅ Gestion automatique : Plus besoin de paramétrer manuellement votre QoS, NetPrior le fait pour vous !
	❓ Support & Améliorations

🔥 Vous avez des suggestions ? Trouvé un bug ? Envie d’améliorer le projet ? Contribuez ! 🚀

📧 Contact : [Ton Email ou Contact GitHub]

📢 NetPrior, votre allié pour une connexion optimisée