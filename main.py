"""
PROGRAMME PRINCIPAL : GESTION DE STOCK 2025
Auteur : [Votre Nom]
"""
from pathlib import Path

# Importation des modules fonctionnels
import fp1_entrants as fp1
import fp2_maintenance as fp2
import fp3_sortants as fp3

def main():
    """
    Fonction principale (Point d'entrée).
    Orchestre le menu et la boucle principale du programme.
    """
    # Définition du fichier de persistance
    fichier_db = Path("stock.txt")
    
    # 1. Chargement initial (FS-1.4)
    entrepot = fp1.fs_1_4_charger_stock(fichier_db)
    
    boucle_active = True
    
    while boucle_active:
        # 2. Affichage de l'état (FS-2.3)
        fp2.fs_2_3_afficher_etat_global(entrepot)
        
        print("MENU :")
        print("1. [Entree] Ajouter produits (ex: A1, B2)")
        print("2. [Sortie] Preparer colis (ex: A1, A1)")
        print("3. [Systeme] Sauvegarder")
        print("4. [Systeme] Quitter")
        
        choix = input("\nVotre choix > ")
        
        if choix == "1":
            saisie = input("Saisissez les produits : ")
            fp1.fs_1_1_parser_saisie_rapide(entrepot, saisie)
            
        elif choix == "2":
            saisie = input("Demandes clients : ")
            liste_demandes = saisie.replace(" ", "").split(",")
            fp3.fs_3_1_preparer_colis(entrepot, liste_demandes)
            
        elif choix == "3":
            fp1.fs_1_3_sauvegarder_stock(entrepot, fichier_db)
            
        elif choix == "4":
            fp1.fs_1_3_sauvegarder_stock(entrepot, fichier_db)
            print("Au revoir !")
            boucle_active = False
        else:
            print("[ERREUR] Choix invalide.")

if __name__ == "__main__":
    main()
