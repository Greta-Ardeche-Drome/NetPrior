import sys
import os
sys.path.append(os.path.abspath('../Menu'))

from Menu.menu import main_menu

# ================================
# Point d'entrée du programme
# ================================
if __name__ == "__main__":
    """
    Ce fichier exécute le programme principal en appelant la fonction main_menu.
    Il importe le menu depuis menu.py et exécute la boucle interactive du menu principal.
    """
    main_menu()
    

