# Analyse Consultative pour une Nouvelle Entreprise NTIC Telecom — Recommandations StratégiquesRapport de Projet — Business Intelligence Avancée (Module BIA

**Titre du projet (Rapport BIA.pdf)** : *Analyse Consultative pour une Nouvelle Entreprise NTIC Telecom — Recommandations Stratégiques en Technologies, Salaires et Adoption IA, Basées sur les Données Stack Overflow (Europe, 2018–2025)*

**Titre du projet (Rapport DOCX)** : *Système Décisionnel d'Analyse des Ventes — Application BI pour le pilotage commercial d'une entreprise de distribution (DistribAlgeria)*

Projet complet de Master 1 SDSI (Module *Business Intelligence Avancée*) — Université Frères Mentouri, Constantine 2. Ce dépôt rassemble les deux rapports de projet BI ainsi que leur pipeline ETL, leurs sources de données, leur entrepôt de données et leurs tableaux de bord interactifs Power BI.

---

## 📁 Contenu du dossier

| Dossier / Fichier                         | Description                                                                                                                        |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `Report/BIA.pdf`                        | Rapport de projet **Analyse Consultative NTIC Telecom** — étude stratégique basées sur Stack Overflow Europe (2018-2025) |
| `Report/Rapport_BI_Analyse_Ventes.docx` | Rapport **Système Décisionnel d'Analyse des Ventes** — pilotage commercial de *DistribAlgeria*                          |
| `CSV/`                                  | Sources brutes : `ventes_brutes.csv`, `catalogue_produits.csv`, `clients.csv`, `regions.csv`                               |
| `DataWherehouse/`                       | Pipeline ETL Python (`etl.py`), base SQLite (`datawarehouse.db`), journal (`etl.log`)                                        |
| `BI Dashboards/`                        | Fichier Power BI (`Interactive dashboard.pbix`) + images d'aperçu (`overview/`)                                               |
| `venv/`                                 | Environnement Python virtuel (pandas, numpy, etc.)                                                                                 |

---

## 1. Projet 1 — Analyse Consultative NTIC Telecom (`Report/BIA.pdf`)

### Contexte

Une nouvelle entreprise NTIC Telecom se positionne sur 5 pôles complémentaires : **Chatbot**, **Logiciel Telecom**, **Site Web**, **Application Mobile**, **Cybersécurité**. L’objectif est de fournir des recommandations stratégiques (technologies, salaires, adoption IA) basées sur des données réelles du marché européen des développeurs (enquête Stack Overflow 2018-2025).

### Ce que nous avons travaillé / livré

| Étape                            | Détail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Modélisation DW**        | Schéma en **flocon** (Snowflake) — table de faits `Fact_Developer` + dimensions (`Dim_Profile`, `Dim_Technology`, `Dim_Geography`, `Dim_Time`, `Dim_Work`, `Dim_DevType`). Sous-dimensions : `Language`, `Database`. Focus géographique : Europe.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **ETL / Intégration**      | Extraction multi-années CSV → nettoyage → standardisation des salaires en USD → création de la variable binaire `Is_AI_User` → filtrage Europe. Outils : Python / Pandas, Power BI Desktop, DAX.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Volume**                  | ~248 000 répondants (toutes années) → ~60 000 après filtrage Europe. 5 pages de visualisation interactive.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **BI Dashboard (Power BI)** | **4 onglets thématiques** :• **Global** — KPIs principaux (CA moyen 141K USD, taux IA 16%, satisfaction 6,37/10, répartition genre 69,37% M / 30,63% F, pic 2023 → 41K répondants, satisfaction max en télétravail).• **System** — types de développeurs par pôle, langages dominants (C# 41K, HTML/CSS 29K, Bash/Shell 28K, C 21K), distribution par expérience (11-20 ans = 64,43K).• **Developer** — grille salariale par expérience (3-5 ans : 95K ; 6-10 : 139K ; 11-20 : 141K ; 20+ : 146K), recommandations par pôle, croissance salariale par langage (Bash/Shell +226,29%).• **AI** — adoption IA passée de ~50% (2023) à ~80% (2025), impact salarial mesurable (+10-30K USD pour utilisateurs IA), langages à fort taux IA (Nim, Prolog, Bash/Shell). |
| **Analyse prédictive**     | Régression linéaire + modèle ARIMA sur données 2023-2025 : prédiction du taux d’adoption IA, croissance salariale (Python, Kotlin, Bash/Shell), popularité future des langages.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

### Recommandations clés (pour la présentation BI / décision)

- **Pôle Chatbot** : Python obligatoire (NLP/IA, LangChain, Rasa) — budget 95K-139K — IA obligatoire.
- **Pôle Logiciel Telecom** : C / C# / Rust — budget 100K-141K — IA recommandée.
- **Pôle Site Web** : Python + JavaScript (frontend) / C# (backend) — budget 90K-139K — IA obligatoire (taux >80%).
- **Pôle Application Mobile** : Kotlin / Java — budget 95K-135K — IA recommandée.
- **Pôle Cybersécurité** : Bash/Shell + Python — budget 116K-146K — IA sélective (outils spécialisés, vigilance risques).
- **Politique transversale** : travail flexible dès le lancement (premier levier d’attractivité sur le marché européen).

---

## 2. Projet 2 — Système Décisionnel d'Analyse des Ventes (`Report/Rapport_BI_Analyse_Ventes.docx`)

### Contexte

Entreprise fictive de distribution **DistribAlgeria** — multi-produits (Électronique, Alimentaire, Textile), 5 wilayas d’Algérie, clients professionnels et particuliers. Objectif : piloter le commercial via un système décisionnel complet.

### Ce que nous avons travaillé / livré

| Étape                             | Détail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Modélisation DW**         | Schéma en **étoile** (Star Schema) — 1 table de faits (`FAIT_VENTES`) + 4 dimensions (`DIM_TEMPS`, `DIM_PRODUIT`, `DIM_CLIENT`, `DIM_REGION`). Justification : requêtes analytiques (agrégations, filtres) sans hiérarchies complexes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Sources**                  | Générées réalistes via Python : `ventes_brutes.csv` (~50 000 lignes, 2023-2024), `catalogue_produits.csv` (180 produits), `clients.csv` (500 clients), `regions.csv` (5 régions/wilayas).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **ETL (Python)**             | `DataWherehouse/etl.py` — pipeline complet avec extraction CSV, transformation (nettoyage des doublons, valeurs négatives, standardisation dates en français, enrichissement marge brute, clés de substitution, intégrité référentielle stricte), chargement incrémental SQLite, journalisation (`etl.log`). Automatisation possible (cron / Planificateur Windows, 02h00, rapport email SMTP, rafraîchissement Power BI API).                                                                                                                                                                                                                                                                                                           |
| **Qualité / Traçabilité** | Suppression automatique des transactions aberrantes (`montant_ht > 0`, `quantite > 0`), contrôle d’intégrité référentielle avant insertion, fichier `etl.log` complet (lignes extraites / rejetées / chargées).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Dashboard Power BI**       | **3 tableaux de bord interactifs** connectés directement à la base SQLite :• **Performance Commerciale Globale** — carte choroplèthe des ventes par wilaya, histogramme CA mensuel 24 mois, KPI cards (CA total, marge brute, transactions, panier moyen), courbe marge nette vs CA (axe double).• **Analyse Produits** — top 10 produits par CA/marge, treemap catégories/sous-catégories, matrice produit/mois (saisonnalité), courbe de Pareto (80% des ventes générées par X% des produits).• **Analyse Client et Région** — segmentation RFM (Récence, Fréquence, Montant), comparatif performances par wilaya, acquisition/rétention par trimestre, drill-down région → wilaya → zone commerciale. |

### Résultats clés (extraits du rapport / log etl)

- **CA total** : 10 626 571 846,66 DA
- **Marge totale** : 3 626 156 225,57 DA
- **Transactions** : 50 000
- **Produits** : 180 | **Clients** : 500 | **Dates couvertes** : 731 jours distincts
- **Top régions** (par CA) : Constantine (32% du CA total), suivi d’autres wilayas.
- **Saisonnalité** : pic de +45% pour la catégorie Alimentaire pendant le mois de Ramadhan.
- **Clientèle** : Grands Comptes (15% du portefeuille) contribuent à 58% des marges.

---

## 3. Pipeline ETL — détails techniques (`DataWherehouse/`)

```text
CSV sources → Python Pandas → Nettoyage / Enrichissement
                  ↓
          SQLite (datawarehouse.db)
              Schéma étoile
                  ↓
          Power BI Desktop (.pbix)
```

- **Fichier script** : `etl.py` (297 lignes, documenté)
- **Base** : `datawarehouse.db` (SQLite)
- **Log** : `etl.log` (timestampé, niveaux INFO/ERROR)
- **Actions clés dans le log** : création schéma, 50 000 lignes de ventes nettoyées (0 supprimées), 731 dates, intégrité référentielle conservée (50 000 → 50 000), chargement des 5 tables avec remplacement (`if_exists="replace"`), vérification des KPIs et top 5 régions.

---

## 4. Notre présentation BI (Power BI)

Les deux projets sont présentés via des **tableaux de bord interactifs Power BI** (`Interactive dashboard.pbix` + aperçus `BI Dashboards/overview/` : System, Global, Developer, AI, etc.).

### Caractéristiques de la présentation

- **Filtres croisés** : année, trimestre, région / wilaya, catégorie de produit, langage, type de développeur.
- **Visualisations variées** : cartes géographiques, histogrammes, courbes, treemaps, matrices, KPI cards, graphiques de Pareto, drill-downs hiérarchiques.
- **Interactivité** : sélection d’éléments, mise à jour dynamique des agrégations DAX, navigation multi-pages (Global / System / Developer / AI pour NTIC ; Performance / Produits / Client-Région pour Ventes).
- **Source de données** : connexion directe SQLite (projet ventes) / modèle relationnel en mémoire (projet NTIC avec données Stack Overflow).

---

## 5. Technologies utilisées

| Domaine                   | Outil / Technologie                                                                    |
| ------------------------- | -------------------------------------------------------------------------------------- |
| Modélisation DW          | Schéma en étoile / flocon (Power BI / SQLite)                                        |
| Extraction / Nettoyage    | Python 3, Pandas, NumPy                                                                |
| Base de données          | SQLite (`datawarehouse.db`)                                                          |
| Visualisation / BI        | Microsoft Power BI Desktop (`.pbix`)                                                 |
| Calculs avancés          | DAX (KPIs : `Avg Salary`, `AIAdoption%`, `TotalRespondents`, `Growth%`)        |
| Qualité / Automatisation | Python Logging, contrôle d’intégrité référentielle, cron / Planificateur Windows |
| Données                  | CSV (Stack Overflow Europe 2018-2025 ; données fictives de distribution 2023-2024)    |

---

## 6. Conclusion / Bilan de notre travail

Nous avons réalisé une **chaîne BI complète** pour deux scénarios décisionnels :

1. **NTIC Telecom** : recommandation stratégique (langages, salaires, IA) à partir d’une analyse de marché Europe (Stack Overflow) — projet analytique et consultatif.
2. **DistribAlgeria** : système opérationnel de pilotage des ventes — projet technique (ETL + DW + dashboards) avec données simulées et automatisation.

Les deux projets mobilisent les concepts du module *BI Avancée* : conception de DW (étoile / flocon), pipeline ETL avec qualité et traçabilité, visualisation interactive multi-pages, calcul de KPIs métier, et introduction à l’analyse predictive (ARIMA / régression). Les présentations Power BI intègrent des filtres croisés, des drill-downs et des visualisations adaptées aux besoins des décideurs (CTO, DRH, Chef de Projet, Responsable Cybersécurité, Analyste BI, Direction Commerciale).

---

*Projet réalisé dans le cadre du Master 1 SDSI — Module Business Intelligence Avancée — Groupe 2 (Constante 2, 2025-2026).*
*Encadrants : Pr. Benchikha-Magra Fouzia, Dr. Aymen Hamoud.*
