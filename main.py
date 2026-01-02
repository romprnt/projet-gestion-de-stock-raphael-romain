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
    # Définition du fichier de persistance
    FICHIER_DB = Path("stock.txt")
    
    # 1. Chargement initial (FS-1.4)
    entrepot = fp1.fs_1_4_charger_stock(FICHIER_DB)
    
    boucle_active = True
    
    while boucle_active:
        # 2. Affichage de l'état (FS-2.3)
        fp2.fs_2_3_afficher_etat_global(entrepot)
        
        print("MENU :")
        print("1. [Entrée] Ajouter produits (ex: A1, B2)")
        print("2. [Sortie] Préparer colis (ex: A1, A1)")
        print("3. [Système] Sauvegarder")
        print("4. [Système] Quitter")
        
        choix = input("\nVotre choix > ")
        
        if choix == "1":
            saisie = input("Saisissez les produits : ")
            fp1.fs_1_1_parser_saisie_rapide(entrepot, saisie)
            
        elif choix == "2":
            saisie = input("Demandes clients : ")
            liste_demandes = saisie.replace(" ", "").split(",")
            fp3.fs_3_1_preparer_colis(entrepot, liste_demandes)
            
        elif choix == "3":
            fp1.fs_1_3_sauvegarder_stock(entrepot, FICHIER_DB)
            
        elif choix == "4":
            fp1.fs_1_3_sauvegarder_stock(entrepot, FICHIER_DB)
            print("Au revoir !")
            boucle_active = False
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
