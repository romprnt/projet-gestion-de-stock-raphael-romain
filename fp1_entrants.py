"""
MODULE FP-1 : GESTION DES FLUX ENTRANTS
Rôle : Saisie, Parsing, Ajout et Persistance.
"""
from pathlib import Path
from fp2_maintenance import fs_2_1_verifier_seuil_alerte

def fs_1_4_charger_stock(path_fichier: Path) -> dict:
    """
    VA: Restaure l'état du stock au démarrage (Persistance).
    """
    ent = {"stock": {}, "alertes": [], "backorders": []}
    
    if not path_fichier.exists():
        print("[INFO] Aucun fichier de sauvegarde trouvé. Démarrage à vide.")
        return ent

    try:
        content = path_fichier.read_text(encoding="utf-8").strip()
        if not content: return ent
            
        for line in content.splitlines():
            # Format attendu dans le fichier : ID:Quantité (ex: A1:5)
            id_p, qte_str = line.split(":")
            qte = int(qte_str)
            
            # Reconstruction des objets dictionnaires
            p_dict = {"type": id_p[0], "vol": int(id_p[1:])}
            ent["stock"][id_p] = [p_dict] * qte
            
        print("[INFO] Données chargées avec succès.")
    except Exception as e:
        print(f"[ERREUR] Fichier corrompu : {e}")
        
    return ent

def fs_1_3_sauvegarder_stock(ent: dict, path_fichier: Path) -> None:
    """
    VA: Assure la survie des données sur disque.
    """
    # On sauvegarde sous la forme : CLE:QUANTITÉ
    lignes = [f"{k}:{len(v)}" for k, v in ent["stock"].items() if v]
    path_fichier.write_text("\n".join(lignes), encoding="utf-8")
    print("[INFO] Sauvegarde effectuée.")

def fs_1_2_ajouter_un_produit(ent: dict, p: dict) -> None:
    """
    VA: Insertion FIFO et déclenchement de la surveillance.
    """
    # Création de l'ID (ex: "A1")
    id_p = f"{p['type']}{p['vol']}"
    
    if id_p not in ent["stock"]:
        ent["stock"][id_p] = []
        
    # Ajout en fin de liste (Queue)
    ent["stock"][id_p].append(p)
    
    # Appel TRANSVERSE vers FP-2 (Surveillance)
    fs_2_1_verifier_seuil_alerte(ent, id_p)

def fs_1_1_parser_saisie_rapide(ent: dict, chaine: str) -> None:
    """
    VA: Sécurise et automatise l'entrée de masse (ex: 'A1, B2').
    """
    try:
        items = chaine.replace(" ", "").split(",")
        for item in items:
            if not item: continue
            # Extraction
            p = {"type": item[0].upper(), "vol": int(item[1:])}
            # Appel interne
            fs_1_2_ajouter_un_produit(ent, p)
        print(" Saisie traitée.")
    except (ValueError, IndexError):
        print(" Erreur de format. Utilisez : A1, B2")
