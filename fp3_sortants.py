"""
MODULE FP-3 : GESTION DES FLUX SORTANTS
Rôle : Préparation, Substitution, Backorders, Tri LIFO.
"""
from typing import List, Optional

def fs_3_2_chercher_substitut(ent: dict, type_p: str, vol_init: int) -> Optional[dict]:
    """
    VA: Résilience par surclassement de volume (Recherche V+1 à 9).
    """
    print(f"   >>> Recherche substitut pour {type_p}{vol_init}...")
    for vol in range(vol_init + 1, 10):
        id_sub = f"{type_p}{vol}"
        if id_sub in ent["stock"] and ent["stock"][id_sub]:
            print(f"   >>> Substitut trouvé : {id_sub}")
            return ent["stock"][id_sub].pop(0)
    return None

def fs_3_3_enregistrer_backorder(ent: dict, id_manquant: str) -> None:
    """
    VA: Trace les demandes non satisfaites.
    """
    ent["backorders"].append(id_manquant)
    print(f"   >>> Rupture totale : {id_manquant} ajouté aux Backorders.")

def fs_3_4_trier_colis_volume(colis: List[dict]) -> List[dict]:
    """
    VA: Sécurise le colisage (LIFO : volumes lourds en bas).
    Tri décroissant sur la clé 'vol'.
    """
    return sorted(colis, key=lambda x: x["vol"], reverse=True)

def fs_3_1_preparer_colis(ent: dict, demandes: List[str]) -> None:
    """
    VA: Orchestre l'expédition et les stratégies de rupture.
    """
    colis_temporaire = []
    
    for id_demande in demandes:
        id_p = id_demande.strip()
        if not id_p: continue
        
        # Cas 1 : Produit disponible
        if id_p in ent["stock"] and ent["stock"][id_p]:
            produit = ent["stock"][id_p].pop(0)
            colis_temporaire.append(produit)
        
        # Cas 2 : Rupture -> Tentative Substitution
        else:
            try:
                type_p = id_p[0]
                vol_p = int(id_p[1:])
                substitut = fs_3_2_chercher_substitut(ent, type_p, vol_p)
                
                if substitut:
                    colis_temporaire.append(substitut)
                else:
                    # Cas 3 : Echec total -> Backorder
                    fs_3_3_enregistrer_backorder(ent, id_p)
            except:
                print(f" ID invalide détecté : {id_p}")

    # Finalisation : Tri du colis
    colis_final = fs_3_4_trier_colis_volume(colis_temporaire)
    
    print(f"\n COLIS PRÊT À L'EXPÉDITION ({len(colis_final)} articles) :")
    print([f"{p['type']}{p['vol']}" for p in colis_final])
