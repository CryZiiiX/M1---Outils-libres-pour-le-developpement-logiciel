# Rapport final - Prédiction du risque de crédit bancaire

Rapport de projet pour l'UE **Outils libres pour le développement logiciel**
(Master 1 Informatique, Université Paris 8).

## Contenu du dossier

| Fichier / dossier        | Rôle                                                        |
|--------------------------|-------------------------------------------------------------|
| `rapport.tex`            | Source LaTeX principal du rapport                           |
| `references.bib`         | Bibliographie (BibTeX, style `plainnat`)                    |
| `diagrams/`              | Diagrammes TikZ inclus dans le rapport (`\input`)           |
| `images/`                | Captures d'écran de l'interface web (annexe C)              |
| `versions_exactes.md`    | Versions exactes des dépendances (`pip freeze`, `npm list`) |
| `archives/`              | Anciennes versions et fichiers auxiliaires conservés        |

Les graphiques d'évaluation (matrices de confusion, courbes ROC) sont lus
directement depuis `../../back-end/results/plots/` (voir `\graphicspath` dans
`rapport.tex`). Le pipeline ML doit donc avoir été exécuté au moins une fois
(`make all` à la racine du projet) avant de compiler le rapport.

## Compilation

Prérequis : `pdflatex` et `bibtex` (TeX Live), avec les paquets `babel-french`,
`lmodern` et `titlesec`.

```bash
pdflatex -interaction=nonstopmode rapport.tex
bibtex rapport
# Le style plainnat reconvertit les plages de pages en tirets longs (--) :
# on les ramène en tirets courts avant les passes finales.
sed -E -i 's/([0-9])--([0-9])/\1-\2/g' rapport.bbl
pdflatex -interaction=nonstopmode rapport.tex
pdflatex -interaction=nonstopmode rapport.tex
```

Le PDF produit (`rapport.pdf`) est ensuite renommé en :

```
RAPPORT - M1 - Outils libres -  Maxime BRONNY - 19009314.pdf
```
