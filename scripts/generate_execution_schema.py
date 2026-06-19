#!/usr/bin/env python3
# =============================================================================
# Fichier : scripts/generate_execution_schema.py
# Rôle    : Générer le schéma d'exécution des scripts du projet (SVG, PNG, PDF)
#           à partir d'une description Graphviz, avec une palette pastel.
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Génère docs/schema_execution_scripts_outils_libres.{svg,png,pdf}.

Le schéma reflète l'ordre d'exécution réel du projet (cibles du Makefile,
scripts du pipeline ML, tests, déploiement Docker et livrables). Il n'utilise
que l'outil libre Graphviz (binaire `dot`), sans dépendance Python externe.

Usage :
    python3 scripts/generate_execution_schema.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

# Racine du dépôt = dossier parent de scripts/
ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BASENAME = "schema_execution_scripts_outils_libres"

# ─── Palette pastel (fond, bordure légèrement plus foncée) ──────────────────
CMD     = ('#FEF3C7', '#E5C766')   # jaune  - commande manuelle
SCRIPT  = ('#DDEBFF', '#7FA8E0')   # bleu   - script Python
GEN     = ('#DCFCE7', '#7FCBA0')   # vert   - fichier / dossier généré
TEST    = ('#EDE9FE', '#A99CE0')   # violet - test
SERVICE = ('#FFEDD5', '#EBB57E')   # orange - service / déploiement
DELIV   = ('#FCE7F3', '#E89BC4')   # rose   - livrable final
DATA    = ('#F3F4F6', '#C2C7CF')   # gris   - données d'entrée / config / doc
TXT = '#1F2937'

# ─── Styles de flèches ──────────────────────────────────────────────────────
E_EXEC = 'color="#374151", penwidth=1.7, arrowsize=0.9'                       # ordre d'exécution
E_DATA = 'color="#5A8AD8", style=dashed, penwidth=1.3, arrowsize=0.8'         # flux de données
E_OPT  = 'color="#E8943A", style=dashed, penwidth=1.3, arrowsize=0.8'         # étape optionnelle
E_DOC  = 'color="#9CA3AF", style=dotted, penwidth=1.4, arrowsize=0.8'         # lien doc / livrable


def node(nid, label, kind, shape="box"):
    """Construit la déclaration DOT d'un bloc coloré."""
    fill, border = kind
    label = label.replace("\n", "\\n")
    return (f'{nid} [label="{label}", shape={shape}, fillcolor="{fill}", '
            f'color="{border}"];')


def main():
    if shutil.which("dot") is None:
        sys.exit("Erreur : Graphviz (binaire 'dot') introuvable. "
                 "Installez-le : sudo apt install graphviz")
    DOCS.mkdir(parents=True, exist_ok=True)

    title = ("Projet Outils libres - Schéma d&#8217;exécution "
             "des scripts")
    subtitle = ("Ordre d&#8217;exécution, fichiers manipulés et "
                "livrables du projet")

    dot = f"""digraph schema {{
  graph [rankdir=TB, fontname="Helvetica", bgcolor="white", compound=true,
         nodesep=0.32, ranksep=0.52, splines=spline, pad=0.3,
         label=<<FONT POINT-SIZE="24" COLOR="{TXT}"><B>{title}</B></FONT><BR/><BR/><FONT POINT-SIZE="13" COLOR="#6B7280">{subtitle}</FONT><BR/> >,
         labelloc="t", fontname="Helvetica"];
  node [fontname="Helvetica", fontsize=11, fontcolor="{TXT}",
        style="rounded,filled", shape=box, margin="0.16,0.10", penwidth=1.3];
  edge [fontname="Helvetica", fontsize=9, fontcolor="#4B5563"];

  // ===================== Phase 0 - Préparation =========================
  subgraph cluster_p0 {{
    label="Phase 0  -  Préparation de l'environnement";
    fontname="Helvetica"; fontsize=14; fontcolor="#374151";
    labeljust="l"; style="rounded,filled"; color="#D9DEE6";
    fillcolor="#FCFDFE"; margin=16;
    {node('p0_clone', 'git clone <dépôt>', CMD)}
    {node('p0_venv', "python3 -m venv .venv\nsource .venv/bin/activate", CMD)}
    {node('p0_pip', "pip install -r back-end/requirements.txt\npip install -r back-end/app/requirements.txt", CMD)}
    {node('p0_npm', "npm install\n(front-end/)", CMD)}
    p0_clone -> p0_venv -> p0_pip [{E_EXEC}];
    p0_pip -> p0_npm [{E_EXEC}];
  }}

  // ===================== Phase 1 - Pipeline ML ==========================
  subgraph cluster_p1 {{
    label="Phase 1  -  Pipeline ML hors ligne   (make all : split → train → plots)";
    fontname="Helvetica"; fontsize=14; fontcolor="#374151";
    labeljust="l"; style="rounded,filled"; color="#9DBBE6";
    fillcolor="#FBFDFF"; margin=16;

    {node('d_raw', "data/raw/\ncredit_risk_dataset.csv\n(32 581 lignes, 11 variables)", DATA, shape="folder")}

    {node('c_split', 'make split', CMD)}
    {node('s_split', 'split_dataset.py\nsplit stratifié 80/20', SCRIPT)}
    {node('d_proc', "data/processed/\ntrain.csv · test.csv", GEN, shape="folder")}

    {node('c_train', 'make train', CMD)}
    {node('s_train', "compare_with_sklearn.py\nrégression logistique + arbre\nimputation, validation croisée", SCRIPT)}
    {node('d_models', "back-end/models/\nlogistic_regression · decision_tree\nscaler  (.joblib)", GEN, shape="folder")}
    {node('d_metrics', "results/metrics/\naccuracy, precision, recall, F1, AUC-ROC", GEN, shape="folder")}

    {node('c_plots', 'make plots', CMD)}
    {node('s_plots', "plot_results.py\ngraphiques d'évaluation", SCRIPT)}
    {node('d_plots', "results/plots/\nmatrices de confusion, courbes ROC (.png)", GEN, shape="folder")}

    {node('c_expl', 'make explore · make outliers', CMD)}
    {node('s_expl', "explore_data.py · detect_outliers.py\nanalyze_missing_values.py", SCRIPT)}

    // ordre d'exécution (make all)
    c_split -> c_train -> c_plots [{E_EXEC}];
    c_split -> s_split [label="exécute", {E_EXEC}];
    c_train -> s_train [label="exécute", {E_EXEC}];
    c_plots -> s_plots [label="exécute", {E_EXEC}];
    // flux de données
    d_raw  -> s_split  [label="lit", {E_DATA}];
    s_split -> d_proc  [label="écrit", {E_DATA}];
    d_proc -> s_train  [label="lit", {E_DATA}];
    s_train -> d_models  [label="écrit", {E_DATA}];
    s_train -> d_metrics [label="écrit", {E_DATA}];
    d_metrics -> s_plots [label="lit", {E_DATA}];
    s_plots -> d_plots [label="écrit", {E_DATA}];
    // analyses optionnelles
    c_expl -> s_expl [label="optionnel", {E_OPT}];
    d_raw -> s_expl [{E_DATA}];
  }}

  // ===================== Phase 2 - Tests ================================
  subgraph cluster_p2 {{
    label="Phase 2  -  Tests & validation";
    fontname="Helvetica"; fontsize=14; fontcolor="#374151";
    labeljust="l"; style="rounded,filled"; color="#B7A7E0";
    fillcolor="#FDFCFF"; margin=16;
    {node('c_test', 'make test', CMD)}
    {node('t_pytest', "pytest - 25 tests\ntest_api · test_predict · test_preprocess\ntest_schemas · test_imputation", TEST)}
    {node('c_cov', 'make coverage', CMD)}
    {node('t_cov', "pytest-cov\ncouverture 97 % (module app/)", TEST)}
    c_test -> c_cov [{E_EXEC}];
    c_test -> t_pytest [label="exécute", {E_EXEC}];
    c_cov -> t_cov [label="exécute", {E_EXEC}];
  }}

  // ===================== Phase 3 - Déploiement ==========================
  subgraph cluster_p3 {{
    label="Phase 3  -  Déploiement de l'application web   (make docker-up)";
    fontname="Helvetica"; fontsize=14; fontcolor="#374151";
    labeljust="l"; style="rounded,filled"; color="#E6B98A";
    fillcolor="#FFFDFA"; margin=16;
    {node('c_docker', "make docker-up\n(= make train + docker compose up -d --build)", CMD)}
    {node('cfg_compose', 'docker-compose.yml', DATA, shape="note")}
    {node('svc_db', "PostgreSQL (db)\npostgres:16-alpine", SERVICE, shape="cylinder")}
    {node('svc_api', "API Flask + Gunicorn (api)\nback-end/app/ · port 8000", SERVICE)}
    {node('svc_web', "Front-end Vue 3 + Vite (web)\nport 5173", SERVICE)}
    {node('user', 'Utilisateur (navigateur)', DATA)}
    c_docker -> svc_db [{E_EXEC}];
    cfg_compose -> c_docker [label="configure", {E_DOC}];
    svc_web -> svc_api [label="JSON / REST", {E_DATA}];
    svc_api -> svc_db [label="SQL", {E_DATA}];
    user -> svc_web [label="HTTP", {E_EXEC}];
  }}

  // ===================== Phase 4 - Livrables ============================
  subgraph cluster_p4 {{
    label="Phase 4  -  Livrables";
    fontname="Helvetica"; fontsize=14; fontcolor="#374151";
    labeljust="l"; style="rounded,filled"; color="#E2A0C4";
    fillcolor="#FFFCFE"; margin=16;
    {node('l_app', 'Application web fonctionnelle', DELIV)}
    {node('l_report', "Rapport PDF\ndocs/Rapport final/", DELIV, shape="note")}
    {node('l_slides', "Présentation (DIAPO)\ndocs/presentation/", DELIV, shape="note")}
    {node('l_repo', 'Dépôt Git (GitHub)', DELIV)}
    {node('doc_readme', 'README.md', DATA, shape="note")}
    doc_readme -> l_repo [label="documente", {E_DOC}];
  }}

  // ===================== Enchaînement inter-phases ======================
  p0_pip -> c_split [{E_EXEC}];
  c_plots -> c_test [{E_EXEC}];
  c_test -> c_docker [{E_EXEC}];
  d_models -> svc_api [label="chargés au démarrage", {E_DATA}];
  d_models -> t_pytest [label="requis (make test)", {E_DATA}];
  svc_web -> l_app [{E_DOC}];
  d_plots -> l_report [label="figures du rapport", {E_DOC}];

  // ===================== Légende ========================================
  subgraph cluster_legend {{
    label="Légende";
    fontname="Helvetica"; fontsize=13; fontcolor="#374151";
    labeljust="l"; style="rounded,filled"; color="#D9DEE6";
    fillcolor="#FCFDFE"; margin=14;

    // types de flèches (mini-exemples)
    lx1 [shape=point, width=0.02, color="#374151"]; lx2 [shape=point, width=0.02, color="#374151"];
    ly1 [shape=point, width=0.02, color="#5A8AD8"]; ly2 [shape=point, width=0.02, color="#5A8AD8"];
    lz1 [shape=point, width=0.02, color="#E8943A"]; lz2 [shape=point, width=0.02, color="#E8943A"];
    lw1 [shape=point, width=0.02, color="#9CA3AF"]; lw2 [shape=point, width=0.02, color="#9CA3AF"];
    lx1 -> lx2 [label="ordre d'exécution", {E_EXEC}];
    ly1 -> ly2 [label="flux de données / fichiers", {E_DATA}];
    lz1 -> lz2 [label="étape optionnelle", {E_OPT}];
    lw1 -> lw2 [label="lien documentaire / livrable", {E_DOC}];
    {{ rank=same; lx1; ly1; lz1; lw1; }}

    // clé des couleurs (table HTML)
    key [shape=plaintext, fillcolor="none", color="none", label=<
      <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3" CELLPADDING="4">
        <TR>
          <TD BGCOLOR="{CMD[0]}" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="{TXT}">Commande manuelle</FONT></TD>
          <TD BGCOLOR="{SCRIPT[0]}" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="{TXT}">Script Python</FONT></TD>
          <TD BGCOLOR="{GEN[0]}" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="{TXT}">Fichier / dossier généré</FONT></TD>
          <TD BGCOLOR="{DATA[0]}" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="{TXT}">Données d'entrée / config / doc</FONT></TD>
        </TR>
        <TR>
          <TD BGCOLOR="{TEST[0]}" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="{TXT}">Test</FONT></TD>
          <TD BGCOLOR="{SERVICE[0]}" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="{TXT}">Service / déploiement</FONT></TD>
          <TD BGCOLOR="{DELIV[0]}" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="{TXT}">Livrable final</FONT></TD>
          <TD BGCOLOR="#FFFFFF" WIDTH="22"> </TD><TD ALIGN="LEFT"><FONT COLOR="#6B7280">Ordre déduit du Makefile / README</FONT></TD>
        </TR>
      </TABLE>
    >];
    lw2 -> key [style=invis];
  }}
  c_docker -> lx1 [style=invis];
  l_app -> key [style=invis];
}}
"""

    src = dot.encode("utf-8")
    targets = {
        "svg": ["dot", "-Tsvg"],
        "png": ["dot", "-Tpng", "-Gdpi=200"],
        "pdf": ["dot", "-Tpdf"],
    }
    produced = []
    for ext, cmd in targets.items():
        out = DOCS / f"{BASENAME}.{ext}"
        res = subprocess.run(cmd + ["-o", str(out)], input=src,
                             capture_output=True)
        if res.returncode != 0:
            sys.exit(f"Erreur dot ({ext}) : {res.stderr.decode(errors='replace')}")
        produced.append(out)
        print(f"[OK] {out.relative_to(ROOT)}")
    print(f"\n{len(produced)} fichiers générés dans {DOCS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
