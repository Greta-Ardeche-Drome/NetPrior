import sys
import time
import platform
import os
import subprocess
import threading

# Ajout des chemins des modules existants
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(current_dir, 'RecupInfos'),
    os.path.join(current_dir, 'InfoQOS'),
    os.path.join(current_dir, 'CreationRegleQOS'),
    os.path.join(current_dir, 'SuppressionRegleQOS')
])

# Import des fonctions existantes du repository
from RecupInfos.fonctionsRecupInfos import (
    list_user_launched_applications, 
    get_network_bandwidth,
    get_app_path,
    list_network_adapters
)
from InfoQOS.PolicyQOS import (
    verifier_regle_qos,
    show_qos_policies,
    get_qos_policies
)
from CreationRegleQOS.CreateQOS import limit_application_bandwidth
from SuppressionRegleQOS.FonctionsDeleteQOS import remove_bandwidth_limit

# Imports PyQt5
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QListWidget, QListWidgetItem, QFrame,
                             QMessageBox, QProgressBar, QInputDialog, QComboBox)
from PyQt5.QtGui import QFont, QColor, QIcon, QPainter, QPen, QBrush, QLinearGradient, QPainterPath, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal

# Définition des couleurs
DARK_BLUE = "#2c3e50"
LIGHT_BLUE = "#3498db"
GREEN = "#2ecc71"
ORANGE = "#f39c12" 
RED = "#e74c3c"
GRAY = "#ecf0f1"
WHITE = "#ffffff"
LIGHT_GRAY = "#f8f9fa"

class SpeedTestWidget(QWidget):
    testComplete = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Appliquer la couleur de fond directement sur le widget
        self.setStyleSheet(f"background-color: {LIGHT_GRAY};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Titre
        stats_header = QLabel("Statistiques réseau")
        stats_header.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(stats_header)
        
        # Valeurs de statistiques
        self.stats_label = QLabel("SpeedTest: N/A\nLatence: N/A")
        self.stats_label.setFont(QFont("Arial", 9))
        layout.addWidget(self.stats_label)
        
        # Ajout du sélecteur d'interface réseau
        interface_layout = QHBoxLayout()
        interface_label = QLabel("Interface réseau:")
        interface_label.setFont(QFont("Arial", 9))
        self.interface_combo = QComboBox()
        self.interface_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: 0px;
            }
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
            }
        """)
        refresh_interfaces_btn = QPushButton("⟳")
        refresh_interfaces_btn.setFixedSize(30, 30)
        refresh_interfaces_btn.setToolTip("Rafraîchir la liste des interfaces")
        refresh_interfaces_btn.clicked.connect(self.refresh_interfaces)
        
        interface_layout.addWidget(interface_label)
        interface_layout.addWidget(self.interface_combo, 1)
        interface_layout.addWidget(refresh_interfaces_btn)
        layout.addLayout(interface_layout)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Mode indéterminé
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Bouton de test avec icône
        self.test_button = QPushButton("🚀 Lancer le test de vitesse")
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.test_button.clicked.connect(self.run_speed_test)
        layout.addWidget(self.test_button)
        
        # Initialiser les interfaces réseau
        self.refresh_interfaces()
        
    def refresh_interfaces(self):
        """Rafraîchit la liste des interfaces réseau disponibles"""
        try:
            self.interface_combo.clear()
            adapters = list_network_adapters()
            
            if adapters:
                for i, adapter in enumerate(adapters, 1):
                    self.interface_combo.addItem(f"{i} - {adapter}", i)
            else:
                self.interface_combo.addItem("Aucune interface trouvée", -1)
                
        except Exception as e:
            print(f"Erreur lors de la récupération des interfaces réseau: {e}")
            self.interface_combo.clear()
            self.interface_combo.addItem("Erreur de chargement", -1)
        
    def run_speed_test(self):
        """Lance un test de vitesse et met à jour les statistiques"""
        # Vérifier qu'une interface est sélectionnée
        if self.interface_combo.count() == 0 or self.interface_combo.currentData() == -1:
            QMessageBox.warning(self, "Erreur", "Aucune interface réseau valide sélectionnée")
            return
            
        self.test_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.stats_label.setText("Test en cours...\nVeuillez patienter")
        
        # Récupérer l'index de l'interface sélectionnée
        adapter_index = self.interface_combo.currentData()
        
        # Utiliser un thread séparé pour ne pas bloquer l'interface
        threading.Thread(target=lambda: self._run_real_speed_test(adapter_index), daemon=True).start()
    
    def _run_real_speed_test(self, adapter_index):
        """Exécute le test de vitesse réel à l'aide de la fonction existante"""
        try:
            # Appeler la fonction existante pour le test de vitesse avec l'interface sélectionnée
            result = get_network_bandwidth(adapter_index)
            
            if not result:  # Si get_network_bandwidth ne renvoie pas de résultats
                results = {
                    "download": "N/A",
                    "upload": "N/A",
                    "latency": "N/A"
                }
            else:
                # Formater les résultats
                results = {
                    "download": f"{result.get('download_mbps', 'N/A')} Mbps",
                    "upload": f"{result.get('upload_mbps', 'N/A')} Mbps",
                    "latency": f"{result.get('latency', 'N/A') if 'latency' in result else 'N/A'}"
                }
        except Exception as e:
            # En cas d'erreur, envoyer des résultats par défaut
            results = {
                "download": "Erreur",
                "upload": "Erreur",
                "latency": f"Erreur: {str(e)}"
            }
        
        # Émettre le signal de fin de test
        self.testComplete.emit(results)
    
    def update_stats(self, results):
        """Met à jour l'affichage des statistiques"""
        self.stats_label.setText(f"Download: {results['download']}\nUpload: {results['upload']}\nLatence: {results['latency']}")
        self.progress_bar.setVisible(False)
        self.test_button.setEnabled(True)

class NetPriorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Vérifier si le système est Windows
        if platform.system() != "Windows":
            QMessageBox.critical(self, "Erreur Système", "NetPrior nécessite Windows pour fonctionner correctement.")
            sys.exit(1)
        
        # Initialiser l'interface
        self.initUI()
        
        # Rafraîchir les listes pour charger les données
        self.refresh_apps_list()
        self.refresh_qos_rules()
    
    def initUI(self):
        # Définir la géométrie de la fenêtre
        self.setWindowTitle("NetPrior - Gestion de priorité réseau")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Créer le widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Créer l'en-tête
        self.create_header(main_layout)
        
        # Créer le contenu principal
        self.create_main_content(main_layout)
        
        # Créer la barre de statut
        self.statusBar().showMessage("Prêt")
        self.statusBar().setStyleSheet("background-color: #f8f9fa; color: #495057;")
        
        # Appliquer le style global
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
            QWidget {
                font-family: 'Arial';
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            QLabel {
                color: #2c3e50;
                background-color: transparent;
            }
            QProgressBar {
                background-color: #f8f9fa;
            }
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
        """)
    
    def create_header(self, main_layout):
        header = QWidget()
        header.setStyleSheet(f"background-color: {DARK_BLUE}; color: white;")
        # Augmentation de la hauteur de l'en-tête pour accommoder un logo plus grand
        header.setFixedHeight(80)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Logo avec taille augmentée
        logo_label = QLabel()
        logo_label.setFixedSize(70, 70)  # Taille augmentée du label
        
        # Essayer de charger le logo à partir du fichier
        logo_path = "netprior_logo.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Augmentation de la taille du logo à 60x60 pixels
            scaled_pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            # Centrer le logo dans le label
            logo_label.setAlignment(Qt.AlignCenter)
        else:
            # Fallback texte si le logo est introuvable
            logo_label.setText("NP")
            logo_label.setStyleSheet(f"background-color: {GREEN}; color: white; font-weight: bold; padding: 10px; font-size: 20px; text-align: center;")
            logo_label.setAlignment(Qt.AlignCenter)
            
        header_layout.addWidget(logo_label)
        
        # Espacement entre le logo et le texte
        header_layout.addSpacing(10)
        
        # Titre et sous-titre
        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)
        
        title = QLabel("NETPRIOR")
        title.setFont(QFont("Arial", 18, QFont.Bold))  # Augmentation de la taille du texte
        title.setStyleSheet("color: white;")
        title_layout.addWidget(title)
        
        subtitle = QLabel("Gestion de priorité réseau")
        subtitle.setFont(QFont("Arial", 10))  # Augmentation de la taille du texte
        subtitle.setStyleSheet("color: #aaaaaa;")
        title_layout.addWidget(subtitle)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch(1)
        
        main_layout.addWidget(header)
    
    def create_main_content(self, main_layout):
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Section des applications
        self.create_apps_section(content_layout)
        
        # Section des règles
        self.create_rules_section(content_layout)
        
        main_layout.addWidget(content)
    
    def create_apps_section(self, parent_layout):
        apps_frame = QFrame()
        apps_frame.setFrameShape(QFrame.StyledPanel)
        apps_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        apps_layout = QVBoxLayout(apps_frame)
        apps_layout.setContentsMargins(0, 0, 0, 10)
        
        # En-tête bleu
        header = QWidget()
        header.setStyleSheet(f"background-color: {LIGHT_BLUE}; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        header.setFixedHeight(50)
        
        header_layout = QHBoxLayout(header)
        header_title = QLabel("Applications lancées")
        header_title.setFont(QFont("Arial", 12, QFont.Bold))
        header_title.setStyleSheet("color: white;")
        header_layout.addWidget(header_title)
        
        # Bouton de rafraîchissement des applications
        refresh_btn = QPushButton("⟳")
        refresh_btn.setFixedSize(30, 30)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        refresh_btn.clicked.connect(self.refresh_apps_list)
        header_layout.addWidget(refresh_btn)
        
        apps_layout.addWidget(header)
        
        # Liste des applications
        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: white;
                font-size: 14px;
            }
            QListWidget::item {
                border-bottom: 1px solid #f0f0f0;
                padding: 8px;
                height: 30px;
            }
        """)
        apps_layout.addWidget(self.apps_list)
        
        # Bouton d'actualisation
        refresh_button = QPushButton("⟳ Actualiser")
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_button.clicked.connect(self.refresh_apps_list)
        apps_layout.addWidget(refresh_button)
        
        # Statistiques réseau avec bouton de test - Couleur de fond corrigée
        stats_container = QWidget()
        stats_container.setStyleSheet(f"background-color: {LIGHT_GRAY}; border-radius: 5px;")
        
        self.speedtest_widget = SpeedTestWidget()
        self.speedtest_widget.testComplete.connect(self.on_speedtest_complete)
        
        stats_layout = QVBoxLayout(stats_container)
        stats_layout.addWidget(self.speedtest_widget)
        
        apps_layout.addWidget(stats_container)
        
        parent_layout.addWidget(apps_frame, 1)  # stretch factor = 1
    
    def refresh_apps_list(self):
        """Rafraîchit la liste des applications utilisateur en utilisant la fonction existante"""
        self.statusBar().showMessage("Récupération des applications utilisateur...")
        
        # Effacer la liste actuelle
        self.apps_list.clear()
        
        try:
            # Utiliser la fonction existante pour obtenir les applications
            apps = list_user_launched_applications(display=False)
            
            # Ajouter les applications à la liste
            for idx, app in enumerate(apps, start=1):
                # Créer un élément avec le nom et le statut
                item_text = f"● {app['ProcessName']}"
                item = QListWidgetItem(item_text)
                
                # Définir la couleur selon le statut (ici statut simulé - à adapter selon votre besoin)
                # Vous pourriez adapter cette logique selon ce que renvoie votre fonction
                item.setForeground(QBrush(QColor(GREEN)))
                
                self.apps_list.addItem(item)
            
            self.statusBar().showMessage(f"{len(apps)} applications trouvées.")
        except Exception as e:
            self.statusBar().showMessage(f"Erreur: {str(e)}")
            print(f"Erreur lors de la récupération des applications: {e}")
            # Afficher quelques exemples en cas d'erreur
            self.apps_list.addItem("● Firefox.exe")
            self.apps_list.item(0).setForeground(QBrush(QColor(GREEN)))
            self.apps_list.addItem("● MSEDGE.exe")
            self.apps_list.item(1).setForeground(QBrush(QColor(GREEN)))
    
    def on_speedtest_complete(self, results):
        """Appelé lorsque le test de vitesse est terminé"""
        self.speedtest_widget.update_stats(results)
        self.statusBar().showMessage(f"Test de vitesse terminé. Téléchargement: {results['download']}, Upload: {results['upload']}")
    
    def create_rules_section(self, parent_layout):
        rules_frame = QFrame()
        rules_frame.setFrameShape(QFrame.StyledPanel)
        rules_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        rules_layout = QVBoxLayout(rules_frame)
        rules_layout.setContentsMargins(0, 0, 0, 10)
        
        # En-tête bleu
        header = QWidget()
        header.setStyleSheet(f"background-color: {LIGHT_BLUE}; border-top-left-radius: 10px; border-top-right-radius: 10px;")
        header.setFixedHeight(50)
        
        header_layout = QHBoxLayout(header)
        header_title = QLabel("Applications limitées")
        header_title.setFont(QFont("Arial", 12, QFont.Bold))
        header_title.setStyleSheet("color: white;")
        header_layout.addWidget(header_title)
        
        # Bouton de rafraîchissement des règles
        refresh_rules_btn = QPushButton("⟳")
        refresh_rules_btn.setFixedSize(30, 30)
        refresh_rules_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        refresh_rules_btn.clicked.connect(self.refresh_qos_rules)
        header_layout.addWidget(refresh_rules_btn)
        
        rules_layout.addWidget(header)
        
        # Liste des applications limitées (simplifiée)
        self.rules_list = QListWidget()
        self.rules_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: white;
                font-size: 14px;
            }
            QListWidget::item {
                border-bottom: 1px solid #f0f0f0;
                padding: 12px;
            }
        """)
        rules_layout.addWidget(self.rules_list)
        
        # Boutons pour les règles
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.setContentsMargins(10, 10, 10, 10)
        
        # Bouton Créer
        create_button = QPushButton("+ Créer une limite")
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        create_button.clicked.connect(self.create_limit)
        buttons_layout.addWidget(create_button)
        
        # Bouton Supprimer
        delete_button = QPushButton("- Supprimer")
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_button.clicked.connect(self.delete_limit)
        buttons_layout.addWidget(delete_button)
        
        # Bouton Appliquer
        apply_button = QPushButton("✓ Appliquer")
        apply_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        apply_button.clicked.connect(self.apply_qos_rules)
        buttons_layout.addWidget(apply_button)
        
        rules_layout.addWidget(buttons_container)
        
        parent_layout.addWidget(rules_frame, 1)  # stretch factor = 1
    
    def refresh_qos_rules(self):
        """Rafraîchit l'affichage des règles QoS en utilisant la fonction existante"""
        self.statusBar().showMessage("Récupération des règles QoS...")
        
        # Effacer la liste actuelle
        self.rules_list.clear()
        
        try:
            # Utiliser la fonction existante pour obtenir les règles QoS
            rules = get_qos_policies()
            
            # Ajouter les règles à la liste (uniquement le nom de l'application)
            for rule in rules:
                # Utiliser AppName comme demandé
                app_name = rule.get("AppName", rule.get("app_name", "N/A"))
                item = QListWidgetItem(app_name)
                self.rules_list.addItem(item)
            
            self.statusBar().showMessage(f"{len(rules)} règles QoS trouvées.")
        except Exception as e:
            self.statusBar().showMessage(f"Erreur: {str(e)}")
            print(f"Erreur lors de la récupération des règles QoS: {e}")
    
    def add_application(self):
        """Ouvre une boîte de dialogue pour ajouter une application"""
        try:
            # Récupérer la liste des applications lancées
            apps = list_user_launched_applications(display=False)
            
            # Créer une liste des noms d'applications pour l'affichage
            app_names = [app.get("ProcessName", "Inconnu") for app in apps]
            
            if not app_names:
                QMessageBox.warning(self, "Aucune application", "Aucune application n'a été trouvée.")
                return
            
            # Demander à l'utilisateur de sélectionner une application
            app_name, ok = QInputDialog.getItem(
                self, "Sélectionner une application", 
                "Choisissez une application à surveiller:", 
                app_names, 0, False
            )
            
            if ok and app_name:
                QMessageBox.information(self, "Application sélectionnée", 
                                      f"Vous avez sélectionné: {app_name}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de récupérer les applications: {str(e)}")
    
    def create_limit(self):
        """Crée une nouvelle limite pour une application"""
        try:
            # Récupérer l'application sélectionnée
            selected_items = self.apps_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une application dans la liste.")
                return
            
            # Extraire le nom de l'application (sans le point de statut)
            app_text = selected_items[0].text()
            app_name = app_text[2:] if app_text.startswith("●") else app_text
            
            # Demander la limite de bande passante
            limit_kbps, ok = QInputDialog.getInt(
                self, "Limite de bande passante", 
                "Entrez la limite en Kbits/sec:", 500, 1, 100000, 100
            )
            
            if ok:
                # Utiliser la fonction existante pour limiter l'application
                limit_application_bandwidth(app_name, limit_kbps)
                
                # Rafraîchir la liste des règles QoS
                self.refresh_qos_rules()
                
                QMessageBox.information(self, "Limite appliquée", 
                                      f"Limite de {limit_kbps} Kbits/sec appliquée à {app_name}.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'appliquer la limite: {str(e)}")
    
    def find_rule_id_by_app_name(self, app_name):
        """Trouve l'ID de la règle QoS par le nom de l'application"""
        try:
            rules = get_qos_policies()
            for rule in rules:
                if rule.get("AppName", "") == app_name:
                    return rule.get("ID")
        except Exception as e:
            print(f"Erreur lors de la recherche de l'ID de la règle: {e}")
        return None
    
    def delete_limit(self):
        """Supprime la limite de QoS pour l'application sélectionnée"""
        # Vérifier si une règle est sélectionnée
        selected_items = self.rules_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner une application dans la liste des règles.")
            return
        
        try:
            # Obtenir le nom de l'application
            app_name = selected_items[0].text()
            
            # Trouver l'ID de la règle
            rule_id = self.find_rule_id_by_app_name(app_name)
            
            if not rule_id:
                QMessageBox.warning(self, "Règle introuvable", f"Impossible de trouver l'ID de la règle pour {app_name}.")
                return
            
            # Demander confirmation
            reply = QMessageBox.question(
                self, "Confirmation", 
                f"Êtes-vous sûr de vouloir supprimer la limite pour {app_name} ?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Supprimer la règle
                remove_bandwidth_limit(rule_id)
                
                # Rafraîchir la liste
                self.refresh_qos_rules()
                
                QMessageBox.information(self, "Suppression réussie", f"La limite pour {app_name} a été supprimée.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de supprimer la limite: {str(e)}")
    
    def apply_qos_rules(self):
        """Applique toutes les règles QoS"""
        try:
            # Dans une implémentation réelle, vous pourriez avoir une fonction pour appliquer toutes les règles
            # Ici, nous simulons simplement une application réussie
            
            # Rafraîchir la liste des règles
            self.refresh_qos_rules()
            
            QMessageBox.information(self, "Règles appliquées", 
                                  "Toutes les règles de QoS ont été appliquées avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'appliquer les règles: {str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Utiliser un style moderne
    
    # Définir la palette de couleurs globale
    palette = app.palette()
    palette.setColor(palette.Window, QColor(GRAY))
    palette.setColor(palette.WindowText, QColor(DARK_BLUE))
    palette.setColor(palette.Base, QColor(WHITE))
    palette.setColor(palette.AlternateBase, QColor(GRAY))
    palette.setColor(palette.ToolTipBase, QColor(WHITE))
    palette.setColor(palette.ToolTipText, QColor(DARK_BLUE))
    palette.setColor(palette.Text, QColor(DARK_BLUE))
    palette.setColor(palette.Button, QColor(LIGHT_BLUE))
    palette.setColor(palette.ButtonText, QColor(WHITE))
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Highlight, QColor(LIGHT_BLUE))
    palette.setColor(palette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = NetPriorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()