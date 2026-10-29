"""
ETL complet — Système Décisionnel d'Analyse des Ventes
Université Constantine 2 — Master 1 SDSI — Module BIA
------------------------------------------------------
Étapes :
  1. Extraction   → lecture des fichiers CSV sources
  2. Transformation → nettoyage, enrichissement, construction des dimensions
  3. Chargement   → insertion dans le Data Warehouse SQLite (schéma étoile)
"""

import pandas as pd
import numpy as np
import sqlite3
import os
import logging
from datetime import datetime

# ─── Configuration ────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DW_PATH     = os.path.join(BASE_DIR, "datawarehouse.db")
LOG_PATH    = os.path.join(BASE_DIR, "etl.log")

CSV_VENTES   = os.path.join(BASE_DIR, "ventes_brutes.csv")
CSV_PRODUITS = os.path.join(BASE_DIR, "catalogue_produits.csv")
CSV_CLIENTS  = os.path.join(BASE_DIR, "clients.csv")
CSV_REGIONS  = os.path.join(BASE_DIR, "regions.csv")

# ─── Logger ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 0 — Création du schéma en étoile dans SQLite
# ══════════════════════════════════════════════════════════════════════════════
def create_schema(conn):
    log.info("Création du schéma en étoile...")
    conn.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS DIM_TEMPS (
            id_temps      INTEGER PRIMARY KEY,
            date_complete TEXT    NOT NULL,
            annee         INTEGER NOT NULL,
            trimestre     INTEGER NOT NULL,
            mois          INTEGER NOT NULL,
            nom_mois      TEXT    NOT NULL,
            semaine       INTEGER NOT NULL,
            jour_semaine  TEXT    NOT NULL,
            est_weekend   INTEGER NOT NULL   -- 0 ou 1
        );

        CREATE TABLE IF NOT EXISTS DIM_PRODUIT (
            id_produit     INTEGER PRIMARY KEY,
            code_produit   TEXT    NOT NULL,
            nom_produit    TEXT    NOT NULL,
            categorie      TEXT    NOT NULL,
            sous_categorie TEXT    NOT NULL,
            marque         TEXT    NOT NULL,
            prix_catalogue REAL    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS DIM_CLIENT (
            id_client          INTEGER PRIMARY KEY,
            code_client        TEXT    NOT NULL,
            nom                TEXT    NOT NULL,
            prenom             TEXT    NOT NULL,
            type_client        TEXT    NOT NULL,
            segment            TEXT    NOT NULL,
            anciennete_annees  INTEGER NOT NULL,
            id_region          INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS DIM_REGION (
            id_region        INTEGER PRIMARY KEY,
            wilaya           TEXT NOT NULL,
            zone_commerciale TEXT NOT NULL,
            responsable      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS FAIT_VENTES (
            id_vente      INTEGER PRIMARY KEY,
            id_temps      INTEGER NOT NULL REFERENCES DIM_TEMPS(id_temps),
            id_produit    INTEGER NOT NULL REFERENCES DIM_PRODUIT(id_produit),
            id_client     INTEGER NOT NULL REFERENCES DIM_CLIENT(id_client),
            id_region     INTEGER NOT NULL REFERENCES DIM_REGION(id_region),
            quantite      INTEGER NOT NULL,
            montant_ht    REAL    NOT NULL,
            remise        REAL    NOT NULL,
            cout_unitaire REAL    NOT NULL,
            marge_brute   REAL    NOT NULL
        );
    """)
    conn.commit()
    log.info("Schéma créé.")

# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 1 — EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════
def extract():
    log.info("── EXTRACTION ──────────────────────────────")

    for path in [CSV_VENTES, CSV_PRODUITS, CSV_CLIENTS, CSV_REGIONS]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fichier introuvable : {path}")

    ventes   = pd.read_csv(CSV_VENTES,   sep=";", encoding="utf-8")
    produits = pd.read_csv(CSV_PRODUITS, sep=",", encoding="utf-8")
    clients  = pd.read_csv(CSV_CLIENTS,  sep=",", encoding="utf-8")
    regions  = pd.read_csv(CSV_REGIONS,  sep=",", encoding="utf-8")

    log.info(f"  ventes_brutes     : {len(ventes):>6} lignes")
    log.info(f"  catalogue_produits: {len(produits):>6} lignes")
    log.info(f"  clients           : {len(clients):>6} lignes")
    log.info(f"  regions           : {len(regions):>6} lignes")

    return ventes, produits, clients, regions

# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 2 — TRANSFORMATION
# ══════════════════════════════════════════════════════════════════════════════
MOIS_FR = {
    1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril",
    5:"Mai", 6:"Juin", 7:"Juillet", 8:"Août",
    9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"
}
JOURS_FR = {
    "Monday":"Lundi", "Tuesday":"Mardi", "Wednesday":"Mercredi",
    "Thursday":"Jeudi", "Friday":"Vendredi", "Saturday":"Samedi", "Sunday":"Dimanche"
}

def transform(ventes, produits, clients, regions):
    log.info("── TRANSFORMATION ──────────────────────────")

    # ── Nettoyage ventes ──────────────────────────────────────────────────────
    avant = len(ventes)
    ventes.drop_duplicates(subset=["id_vente"], inplace=True)
    ventes.dropna(subset=["id_produit", "id_client", "id_region", "date"], inplace=True)
    ventes = ventes[ventes["montant_ht"] > 0]
    ventes = ventes[ventes["quantite"]   > 0]
    log.info(f"  Ventes nettoyées : {avant} → {len(ventes)} lignes ({avant - len(ventes)} supprimées)")

    # ── Conversion des types ──────────────────────────────────────────────────
    ventes["date"]        = pd.to_datetime(ventes["date"])
    ventes["id_produit"]  = ventes["id_produit"].astype(int)
    ventes["id_client"]   = ventes["id_client"].astype(int)
    ventes["id_region"]   = ventes["id_region"].astype(int)

    # ── DIM_TEMPS ─────────────────────────────────────────────────────────────
    dates_uniques = ventes["date"].dt.normalize().unique()
    dim_temps_rows = []
    for d in sorted(dates_uniques):
        ts = pd.Timestamp(d)
        dim_temps_rows.append({
            "id_temps"     : int(ts.strftime("%Y%m%d")),
            "date_complete": ts.strftime("%Y-%m-%d"),
            "annee"        : ts.year,
            "trimestre"    : ts.quarter,
            "mois"         : ts.month,
            "nom_mois"     : MOIS_FR[ts.month],
            "semaine"      : int(ts.isocalendar()[1]),
            "jour_semaine" : JOURS_FR[ts.day_name()],
            "est_weekend"  : 1 if ts.dayofweek >= 5 else 0
        })
    dim_temps = pd.DataFrame(dim_temps_rows)
    log.info(f"  DIM_TEMPS    : {len(dim_temps)} dates distinctes")

    # Ajouter id_temps à la table de faits
    ventes["id_temps"] = ventes["date"].apply(lambda d: int(d.strftime("%Y%m%d")))

    # ── DIM_PRODUIT ───────────────────────────────────────────────────────────
    produits.drop_duplicates(subset=["id_produit"], inplace=True)
    produits.dropna(inplace=True)
    dim_produit = produits[[
        "id_produit", "code_produit", "nom_produit",
        "categorie", "sous_categorie", "marque", "prix_catalogue"
    ]].copy()
    log.info(f"  DIM_PRODUIT  : {len(dim_produit)} produits")

    # ── DIM_CLIENT ────────────────────────────────────────────────────────────
    clients.drop_duplicates(subset=["id_client"], inplace=True)
    clients.dropna(inplace=True)
    dim_client = clients[[
        "id_client", "code_client", "nom", "prenom",
        "type_client", "segment", "anciennete_annees", "id_region"
    ]].copy()
    log.info(f"  DIM_CLIENT   : {len(dim_client)} clients")

    # ── DIM_REGION ────────────────────────────────────────────────────────────
    dim_region = regions[[
        "id_region", "wilaya", "zone_commerciale", "responsable"
    ]].copy()
    log.info(f"  DIM_REGION   : {len(dim_region)} régions")

    # ── FAIT_VENTES ───────────────────────────────────────────────────────────
    # Vérification intégrité référentielle
    ids_produits_valides = set(dim_produit["id_produit"])
    ids_clients_valides  = set(dim_client["id_client"])
    ids_regions_valides  = set(dim_region["id_region"])

    avant = len(ventes)
    ventes = ventes[ventes["id_produit"].isin(ids_produits_valides)]
    ventes = ventes[ventes["id_client"].isin(ids_clients_valides)]
    ventes = ventes[ventes["id_region"].isin(ids_regions_valides)]
    log.info(f"  Intégrité réf : {avant} → {len(ventes)} lignes")

    fait_ventes = ventes[[
        "id_vente", "id_temps", "id_produit", "id_client", "id_region",
        "quantite", "montant_ht", "remise", "cout_unitaire", "marge_brute"
    ]].copy()
    log.info(f"  FAIT_VENTES  : {len(fait_ventes)} transactions")

    return dim_temps, dim_produit, dim_client, dim_region, fait_ventes

# ══════════════════════════════════════════════════════════════════════════════
# ÉTAPE 3 — CHARGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def load(conn, dim_temps, dim_produit, dim_client, dim_region, fait_ventes):
    log.info("── CHARGEMENT ──────────────────────────────")

    # Ordre impératif : dimensions d'abord, faits ensuite
    tables = [
        ("DIM_TEMPS",    dim_temps),
        ("DIM_PRODUIT",  dim_produit),
        ("DIM_CLIENT",   dim_client),
        ("DIM_REGION",   dim_region),
        ("FAIT_VENTES",  fait_ventes),
    ]
    for nom, df in tables:
        df.to_sql(nom, conn, if_exists="replace", index=False)
        log.info(f"  {nom:<16} → {len(df):>6} lignes chargées")

    conn.commit()

# ══════════════════════════════════════════════════════════════════════════════
# VÉRIFICATION RAPIDE
# ══════════════════════════════════════════════════════════════════════════════
def verify(conn):
    log.info("── VÉRIFICATION ────────────────────────────")
    queries = {
        "CA total (DA)"            : "SELECT ROUND(SUM(montant_ht), 2) FROM FAIT_VENTES",
        "Marge totale (DA)"        : "SELECT ROUND(SUM(marge_brute), 2) FROM FAIT_VENTES",
        "Nb transactions"          : "SELECT COUNT(*) FROM FAIT_VENTES",
        "Nb produits"              : "SELECT COUNT(*) FROM DIM_PRODUIT",
        "Nb clients"               : "SELECT COUNT(*) FROM DIM_CLIENT",
        "Dates couvertes"          : "SELECT MIN(date_complete)||' → '||MAX(date_complete) FROM DIM_TEMPS",
    }
    for label, sql in queries.items():
        val = conn.execute(sql).fetchone()[0]
        log.info(f"  {label:<28}: {val}")

    log.info("── TOP 5 régions par CA ────────────────────")
    rows = conn.execute("""
        SELECT r.wilaya, ROUND(SUM(f.montant_ht),2) AS ca
        FROM   FAIT_VENTES f JOIN DIM_REGION r ON f.id_region = r.id_region
        GROUP  BY r.wilaya ORDER BY ca DESC LIMIT 5
    """).fetchall()
    for w, ca in rows:
        log.info(f"  {w:<16}: {ca:,.2f} DA")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    debut = datetime.now()
    log.info("=" * 50)
    log.info("  DÉMARRAGE DU PIPELINE ETL")
    log.info("=" * 50)

    # Supprimer l'ancienne base si elle existe (rechargement complet)
    if os.path.exists(DW_PATH):
        os.remove(DW_PATH)
        log.info("Ancienne base supprimée.")

    conn = sqlite3.connect(DW_PATH)

    try:
        create_schema(conn)
        ventes, produits, clients, regions = extract()
        dim_temps, dim_produit, dim_client, dim_region, fait_ventes = transform(ventes, produits, clients, regions)
        load(conn, dim_temps, dim_produit, dim_client, dim_region, fait_ventes)
        verify(conn)
    except Exception as e:
        log.error(f"ERREUR CRITIQUE : {e}")
        raise
    finally:
        conn.close()

    duree = (datetime.now() - debut).total_seconds()
    log.info(f"Pipeline terminé en {duree:.2f} secondes.")
    log.info(f"Base de données : {DW_PATH}")
