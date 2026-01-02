"""
MODULE FP-2 : MAINTENANCE & SURVEILLANCE
Rôle : Gère les alertes et l'affichage.
"""

def fs_2_2_gerer_saturation_logistique(ent: dict) -> None:
    """
    VA: Maintient la capacité du journal d'alertes à 3 places maximum.
    """
    if len(ent["alertes"]) >= 3:
        # Suppression de l'alerte la plus ancienne (FIFO : index 0)
        removed = ent["alertes"].pop(0)
        print(f"[LOG] Journal saturé : Suppression de l'alerte ancienne '{removed}'")

def fs_2_1_verifier_seuil_alerte(ent: dict, id_p: str) -> None:
    """
    VA: Anticipe les ruptures critiques (Seuil < 2).
    Déclenché automatiquement après chaque ajout.
    """
    quantite = len(ent["stock"].get(id_p, []))
    
    # Si stock critique et que l'alerte n'est pas déjà active
    if quantite < 2 and id_p not in ent["alertes"]:
        fs_2_2_gerer_saturation_logistique(ent)
        ent["alertes"].append(id_p)
        print(f"[ALERTE] Stock critique détecté sur {id_p} !")

def fs_2_3_afficher_etat_global(ent: dict) -> None:
    """
    VA: Offre une visibilité temps réel sur l'entrepôt pour l'opérateur.
    """
    print("\n" + "="*40)
    print(f"📦 STOCK ({len(ent['stock'])} réf) :")
    for k, v in ent["stock"].items():
        print(f"   - {k} : {len(v)} unités")
        
    print(f"\n⚠️  ALERTES ({len(ent['alertes'])}/3) : {ent['alertes']}")
    print(f"📋 BACKORDERS : {ent['backorders']}")
    print("="*40 + "\n")
