🚀 NetPrior - Gestion QoS Windows

	Gérez la bande passante de vos applications Windows avec des règles QoS automatisées via PowerShell.

📌 Description
	NetPrior permet de contrôler et limiter la bande passante des applications Windows en temps réel. Interface CLI colorée et GUI moderne incluses.

✨ Fonctionnalités
	✅ Lister les applications actives
	✅ Afficher la bande passante des cartes réseau
	✅ Limiter la bande passante d'applications
	✅ Gérer les règles QoS (créer/supprimer)
	✅ Interface CLI et GUI
	✅ Test de bande passante intégré

🛠 Installation
	Prérequis
		Windows (obligatoire)
		Python 3.X
		Droits administrateur (recommandé)

	Installation des bibliothèques Python nécessaires
		python InstallBibliotheques.py
	Installation manuelle
		pip install colorama prettytable psutil pyfiglet speedtest-cli requests

🚀 Utilisation
	Interface CLI
		python main.py
	Interface graphique
		python interf.py

📜 Menu CLI
	========================================
	            NETPRIOR - MENU
	========================================
	[1] Afficher les applications lancées
	[2] Afficher la bande passante
	[3] Limiter une application
	[4] Afficher les règles QoS
	[5] Supprimer une règle QoS
	[6] Quitter
	========================================

📂 Structure
	NetPrior/
	├── CreationRegleQOS/CreateQOS.py      # Création règles QoS
	├── InfoQOS/PolicyQOS.py               # Gestion politiques QoS
	├── Menu/menu.py                       # Interface CLI
	├── RecupInfos/fonctionsRecupInfos.py  # Infos système
	├── SuppressionRegleQOS/               # Suppression règles
	├── speedtest/speedtest.exe            # Test bande passante
	├── InstallBibliotheques.py            # Installation dépendances Python
	├── main.py                            # Point d'entrée CLI
	└── interf.py                          # Interface graphique


🎯 Exemple d'usage
		Limiter Discord à 500 Kbps
	1.python main.py
	2.Choisir [3] Limiter une application
	3.ntrer discord.exe
	4.Limite : 500 Kbits/sec

🐛 Problèmes courants

	Erreur PowerShell : Exécuter en tant qu'administrateur
	Application non trouvée : Vérifier que l'app est lancée
	Speedtest échoue : Vérifier la connexion Internet

🤝 Contribution
	Fork le projet
	Créer une feature branch
	Commit les changements
	Push et ouvrir une Pull Request


	NetPrior - Votre allié pour une connexion optimisée ! 🚀
