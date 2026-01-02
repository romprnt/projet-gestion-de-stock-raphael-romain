"""
MODULE SPECIAL : AJOUT D'UN PRODUIT

"""

# --- STRUCTURE DE DONNEES (Dictionnaire Central) ---
entrepot = {
    "stock": {},       # Ex: {"A1": [{"type": "A", "vol": 1}, ...]}
    "alertes": [],     # Ex: ["A1", "B2"] (Max 3)
    "backorders": []   # Ex: ["C3"]
}

# --- FS-2.2 : GESTION DE LA SATURATION (Maintenance) ---
def fs_2_2_gerer_saturation_logistique(ent: dict):
    """
    Gere la taille du journal d'alertes (Max 3).
    Si le journal est plein, on supprime le plus ancien (index 0).
    """
    if len(ent["alertes"]) >= 3:
        # Suppression de l'alerte la plus ancienne (FIFO)
        ent["alertes"].pop(0) 

# --- FS-2.1 : VERIFICATION DU SEUIL (Surveillance) ---
def fs_2_1_verifier_seuil_alerte(ent: dict, id_p: str):
    """
    Verifie si le stock d'un produit est critique (< 2).
    Declenche la gestion de saturation si une alerte doit etre creee.
    """
    quantite = len(ent["stock"].get(id_p, []))
    
    # Condition : Stock < 2 et l'alerte n'existe pas deja
    if quantite < 2 and id_p not in ent["alertes"]:
        fs_2_2_gerer_saturation_logistique(ent)
        ent["alertes"].append(id_p)

# --- FS-1.2 : AJOUTER UN PRODUIT (Flux Entrant) ---
def fs_1_2_ajouter_un_produit(ent: dict, produit: dict):
    """
    Insere un produit dans le stock et lance la surveillance.
    Respecte la regle FIFO (ajout en fin de liste).
    """
    # Creation de l'ID (ex: "A" + "1" = "A1")
    id_p = f"{produit['type']}{produit['vol']}"
    
    # Initialisation de la liste si le produit est nouveau
    if id_p not in ent["stock"]:
        ent["stock"][id_p] = []
        
    # Insertion physique
    ent["stock"][id_p].append(produit)
    
    # Appel automatique de la surveillance (Lien vers FP-2)
    fs_2_1_verifier_seuil_alerte(ent, id_p)
    
    print(f"-> Produit {id_p} ajoute au stock.")

# --- FS-1.1 : PARSER SAISIE RAPIDE (Interface) ---
def fs_1_1_parser_saisie_rapide(ent: dict, chaine_saisie: str):
    """
    Transforme la saisie utilisateur (ex: 'A1, B2') en objets dictionnaires.
    """
    try:
        # Nettoyage et decoupage de la chaine
        items = chaine_saisie.replace(" ", "").split(",")
        
        for item in items:
            if not item:
                continue
            # Extraction des donnees
            type_p = item[0].upper()
            vol_p = int(item[1:])
            
            # Creation du dictionnaire produit (Message de retour du SD)
            nouveau_produit = {"type": type_p, "vol": vol_p}
            
            # Appel du service d'ajout
            fs_1_2_ajouter_un_produit(ent, nouveau_produit)
            
        return True # Succes
    except (ValueError, IndexError):
        print("Erreur de format. Utilisez le format 'A1, B2'.")
        return False

# --- EXEMPLE D'APPEL (SIMULATION INTERFACE) ---
if __name__ == "__main__":
    # Simulation de l'utilisateur qui tape "A1"
    SAISIE_UTILISATEUR = "A1"
    print(f"Utilisateur saisie : {SAISIE_UTILISATEUR}")
    
    # L'interface lance le processus
    fs_1_1_parser_saisie_rapide(entrepot, SAISIE_UTILISATEUR)
    
    # Verification de l'etat final
    print("\n--- ETAT FINAL DE L'ENTREPOT ---")
    print(f"Stock   : {entrepot['stock']}")
    print(f"Alertes : {entrepot['alertes']}")
