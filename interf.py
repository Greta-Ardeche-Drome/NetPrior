import tkinter as tk
from tkinter import ttk, messagebox, font
import os
import sys
import time
import threading
import platform

# Ajouter les chemins des autres modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(current_dir, 'RecupInfos'),
    os.path.join(current_dir, 'InfoQOS'),
    os.path.join(current_dir, 'CreationRegleQOS'),
    os.path.join(current_dir, 'SuppressionRegleQOS')
])

# Importer les fonctions nécessaires
from RecupInfos.fonctionsRecupInfos import (
    list_user_launched_applications, 
    get_network_bandwidth
)
from InfoQOS.PolicyQOS import (
    verifier_regle_qos,
    get_qos_policies
)
from CreationRegleQOS.CreateQOS import limit_application_bandwidth
from SuppressionRegleQOS.FonctionsDeleteQOS import remove_bandwidth_limit

class NetPriorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NetPrior - Gestion QoS")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Vérifier si le système est Windows
        if platform.system() != "Windows":
            messagebox.showerror("Erreur Système", "NetPrior nécessite Windows pour fonctionner correctement.")
            self.root.destroy()
            return
        
        # Configuration des styles
        self.setup_styles()
        
        # Créer le carnet d'onglets principal
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Créer les différents onglets
        self.create_apps_tab()
        self.create_bandwidth_tab()
        self.create_rules_tab()
        
        # Ajouter une barre de statut
        self.status_bar = tk.Label(root, text="Prêt.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialiser les données
        self.apps_data = []
        self.qos_rules = []
        self.refresh_apps_list()
        self.refresh_qos_rules()

    def setup_styles(self):
        # Configurer le style de l'application
        style = ttk.Style()
        style.theme_use('clam')  # Utiliser un thème moderne
        
        # Couleurs
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=('Arial', 10))
        style.configure("TButton", font=('Arial', 10))
        style.configure("TNotebook", background="#f0f0f0", tabposition='n')
        style.configure("TNotebook.Tab", padding=[10, 5], font=('Arial', 10))
        
        # Style pour les titres
        self.title_font = font.Font(family="Arial", size=14, weight="bold")
        
        # Style pour les en-têtes
        self.header_font = font.Font(family="Arial", size=12, weight="bold")

    def create_apps_tab(self):
        # Onglet Applications
        self.apps_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.apps_tab, text="Applications")
        
        # Titre
        title = tk.Label(self.apps_tab, text="Applications Utilisateur", font=self.title_font)
        title.pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_frame = ttk.Frame(self.apps_tab)
        refresh_frame.pack(fill=tk.X, padx=10, pady=5)
        
        refresh_btn = ttk.Button(refresh_frame, text="Rafraîchir la liste", command=self.refresh_apps_list)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Créer la vue en arbre pour les applications
        columns = ("id", "name", "pid")
        self.apps_tree = ttk.Treeview(self.apps_tab, columns=columns, show="headings")
        
        # Définir les en-têtes de colonnes
        self.apps_tree.heading("id", text="#")
        self.apps_tree.heading("name", text="Nom de l'application")
        self.apps_tree.heading("pid", text="PID")
        
        # Définir les largeurs de colonnes
        self.apps_tree.column("id", width=50, anchor=tk.CENTER)
        self.apps_tree.column("name", width=350, anchor=tk.W)
        self.apps_tree.column("pid", width=100, anchor=tk.CENTER)
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(self.apps_tab, orient=tk.VERTICAL, command=self.apps_tree.yview)
        self.apps_tree.configure(yscroll=scrollbar.set)
        
        # Placer la vue et la barre de défilement
        self.apps_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cadre pour limiter une application
        limit_frame = ttk.LabelFrame(self.apps_tab, text="Limiter la bande passante")
        limit_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Entrée pour la limite de bande passante
        limit_label = ttk.Label(limit_frame, text="Limite (Kbits/sec):")
        limit_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.limit_entry = ttk.Entry(limit_frame, width=10)
        self.limit_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Bouton pour appliquer la limite
        apply_btn = ttk.Button(limit_frame, text="Appliquer la limite", command=self.apply_bandwidth_limit)
        apply_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Message d'information
        info_label = ttk.Label(limit_frame, text="Sélectionnez une application dans la liste ci-dessus, puis définissez une limite de bande passante.")
        info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W)

    def create_bandwidth_tab(self):
        # Onglet Bande Passante
        self.bandwidth_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.bandwidth_tab, text="Bande Passante")
        
        # Titre
        title = tk.Label(self.bandwidth_tab, text="Test de Bande Passante", font=self.title_font)
        title.pack(pady=10)
        
        # Cadre pour les informations réseau
        network_frame = ttk.LabelFrame(self.bandwidth_tab, text="Interfaces Réseau")
        network_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Liste des interfaces réseau
        self.network_listbox = tk.Listbox(network_frame, height=5)
        self.network_listbox.pack(fill=tk.X, padx=10, pady=5)
        
        # Bouton pour lister les interfaces
        list_btn = ttk.Button(network_frame, text="Lister les interfaces", command=self.list_network_interfaces)
        list_btn.pack(pady=5)
        
        # Cadre pour les résultats de test
        test_frame = ttk.LabelFrame(self.bandwidth_tab, text="Résultats du Test")
        test_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Bouton pour lancer le test
        test_btn = ttk.Button(test_frame, text="Tester la bande passante", command=self.test_bandwidth)
        test_btn.pack(pady=10)
        
        # Affichage des résultats
        results_frame = ttk.Frame(test_frame)
        results_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Débit descendant
        down_label = ttk.Label(results_frame, text="Débit descendant:")
        down_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.down_value = ttk.Label(results_frame, text="N/A")
        self.down_value.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Débit montant
        up_label = ttk.Label(results_frame, text="Débit montant:")
        up_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.up_value = ttk.Label(results_frame, text="N/A")
        self.up_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Barre de progression
        self.progress = ttk.Progressbar(test_frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=10)

    def create_rules_tab(self):
        # Onglet Règles QoS
        self.rules_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rules_tab, text="Règles QoS")
        
        # Titre
        title = tk.Label(self.rules_tab, text="Règles de Qualité de Service Actives", font=self.title_font)
        title.pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_frame = ttk.Frame(self.rules_tab)
        refresh_frame.pack(fill=tk.X, padx=10, pady=5)
        
        refresh_btn = ttk.Button(refresh_frame, text="Rafraîchir les règles", command=self.refresh_qos_rules)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Créer la vue en arbre pour les règles
        columns = ("id", "name", "app")
        self.rules_tree = ttk.Treeview(self.rules_tab, columns=columns, show="headings")
        
        # Définir les en-têtes de colonnes
        self.rules_tree.heading("id", text="ID")
        self.rules_tree.heading("name", text="Nom de la règle")
        self.rules_tree.heading("app", text="Nom de l'application")
        
        # Définir les largeurs de colonnes
        self.rules_tree.column("id", width=50, anchor=tk.CENTER)
        self.rules_tree.column("name", width=250, anchor=tk.W)
        self.rules_tree.column("app", width=200, anchor=tk.W)
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(self.rules_tab, orient=tk.VERTICAL, command=self.rules_tree.yview)
        self.rules_tree.configure(yscroll=scrollbar.set)
        
        # Placer la vue et la barre de défilement
        self.rules_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cadre pour supprimer une règle
        delete_frame = ttk.Frame(self.rules_tab)
        delete_frame.pack(fill=tk.X, padx=10, pady=10)
        
        delete_btn = ttk.Button(delete_frame, text="Supprimer la règle sélectionnée", command=self.delete_qos_rule)
        delete_btn.pack(side=tk.RIGHT)

    def refresh_apps_list(self):
        """Rafraîchit la liste des applications utilisateur"""
        self.update_status("Récupération des applications utilisateur...")
        
        # Effacer la liste actuelle
        for item in self.apps_tree.get_children():
            self.apps_tree.delete(item)
        
        # Obtenir la nouvelle liste
        try:
            self.apps_data = list_user_launched_applications(display=False)
            
            # Ajouter les applications à la vue en arbre
            for idx, app in enumerate(self.apps_data, start=1):
                self.apps_tree.insert("", tk.END, values=(
                    idx, 
                    app["ProcessName"], 
                    app["ProcessId"]
                ))
            
            self.update_status(f"{len(self.apps_data)} applications trouvées.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer la liste des applications : {e}")
            self.update_status("Erreur lors de la récupération des applications.")

    def refresh_qos_rules(self):
        """Rafraîchit la liste des règles QoS"""
        self.update_status("Récupération des règles QoS...")
        
        # Effacer la liste actuelle
        for item in self.rules_tree.get_children():
            self.rules_tree.delete(item)
        
        # Obtenir la nouvelle liste
        try:
            self.qos_rules = get_qos_policies()
            
            # Ajouter les règles à la vue en arbre
            for rule in self.qos_rules:
                self.rules_tree.insert("", tk.END, values=(
                    rule["ID"],
                    rule["RuleName"],
                    rule["AppName"]
                ))
            
            self.update_status(f"{len(self.qos_rules)} règles QoS trouvées.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les règles QoS : {e}")
            self.update_status("Erreur lors de la récupération des règles QoS.")

    def apply_bandwidth_limit(self):
        """Applique une limite de bande passante à l'application sélectionnée"""
        # Vérifier si une application est sélectionnée
        selection = self.apps_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une application.")
            return
        
        # Obtenir les valeurs de l'application sélectionnée
        item = self.apps_tree.item(selection[0])
        values = item['values']
        app_name = values[1]
        
        # Obtenir la limite de bande passante
        try:
            limit_kbps = int(self.limit_entry.get())
            if limit_kbps <= 0:
                raise ValueError("La limite doit être positive.")
        except ValueError as e:
            messagebox.showerror("Erreur", f"Valeur de limite invalide : {e}")
            return
        
        # Confirmer l'action
        confirm = messagebox.askyesno(
            "Confirmation", 
            f"Voulez-vous limiter l'application '{app_name}' à {limit_kbps} Kbits/sec?"
        )
        
        if confirm:
            self.update_status(f"Application de la limite sur {app_name}...")
            
            # Exécuter dans un thread séparé pour ne pas bloquer l'interface
            def apply_limit():
                try:
                    limit_application_bandwidth(app_name, limit_kbps)
                    # Rafraîchir la liste des règles QoS après l'opération
                    self.root.after(2000, self.refresh_qos_rules)
                    self.update_status(f"Limite appliquée sur {app_name}.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible d'appliquer la limite : {e}")
                    self.update_status("Erreur lors de l'application de la limite.")
            
            threading.Thread(target=apply_limit).start()

    def delete_qos_rule(self):
        """Supprime la règle QoS sélectionnée"""
        # Vérifier si une règle est sélectionnée
        selection = self.rules_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une règle QoS.")
            return
        
        # Obtenir les valeurs de la règle sélectionnée
        item = self.rules_tree.item(selection[0])
        values = item['values']
        rule_id = values[0]
        rule_name = values[1]
        
        # Confirmer la suppression
        confirm = messagebox.askyesno(
            "Confirmation", 
            f"Voulez-vous supprimer la règle '{rule_name}'?"
        )
        
        if confirm:
            self.update_status(f"Suppression de la règle {rule_name}...")
            
            # Exécuter dans un thread séparé pour ne pas bloquer l'interface
            def delete_rule():
                try:
                    remove_bandwidth_limit(rule_id)
                    # Rafraîchir la liste des règles QoS après l'opération
                    self.root.after(2000, self.refresh_qos_rules)
                    self.update_status(f"Règle {rule_name} supprimée.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Impossible de supprimer la règle : {e}")
                    self.update_status("Erreur lors de la suppression de la règle.")
            
            threading.Thread(target=delete_rule).start()

    def list_network_interfaces(self):
        """Liste les interfaces réseau disponibles"""
        self.update_status("Récupération des interfaces réseau...")
        
        # Effacer la liste actuelle
        self.network_listbox.delete(0, tk.END)
        
        # Obtenir la liste des interfaces
        try:
            from RecupInfos.fonctionsRecupInfos import list_network_adapters
            adapters = list_network_adapters()
            
            # Ajouter les interfaces à la liste
            for adapter in adapters:
                self.network_listbox.insert(tk.END, adapter)
            
            self.update_status(f"{len(adapters)} interfaces réseau trouvées.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les interfaces réseau : {e}")
            self.update_status("Erreur lors de la récupération des interfaces réseau.")

    def test_bandwidth(self):
        """Teste la bande passante de l'interface sélectionnée"""
        # Vérifier si une interface est sélectionnée
        selection = self.network_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une interface réseau.")
            return
        
        # Obtenir l'interface sélectionnée
        adapter = self.network_listbox.get(selection[0])
        
        # Lancer le test dans un thread séparé
        self.update_status(f"Test de bande passante sur {adapter}...")
        self.progress.start()
        
        def run_test():
            try:
                # Simuler un test de bande passante (à remplacer par l'appel réel)
                bandwidth_info = get_network_bandwidth()
                
                # Mettre à jour l'interface utilisateur
                self.root.after(0, lambda: self.update_bandwidth_results(bandwidth_info))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Erreur", f"Test de bande passante échoué : {e}"))
                self.root.after(0, lambda: self.update_status("Erreur lors du test de bande passante."))
            finally:
                self.root.after(0, self.progress.stop)
        
        threading.Thread(target=run_test).start()

    def update_bandwidth_results(self, results):
        """Met à jour l'affichage des résultats de bande passante"""
        if results and "download_mbps" in results and "upload_mbps" in results:
            self.down_value.config(text=f"{results['download_mbps']} Mbps")
            self.up_value.config(text=f"{results['upload_mbps']} Mbps")
            self.update_status("Test de bande passante terminé.")
        else:
            self.down_value.config(text="N/A")
            self.up_value.config(text="N/A")
            self.update_status("Aucun résultat de test disponible.")

    def update_status(self, message):
        """Met à jour la barre de statut"""
        timestamp = time.strftime("%H:%M:%S")
        self.status_bar.config(text=f"{timestamp} - {message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetPriorApp(root)
    root.mainloop()