# Vérification de la bibliographie - 10 juin 2026

Fichier bibliographique source : `references.bib` (22 entrées), compilé avec
BibTeX et le style `plainnat` (`\bibliography{references}` dans `rapport.tex`).

Méthode : chaque URL a été testée avec `curl -I -L` (HEAD), puis `curl -L`
(GET) en cas d'échec, avec suivi des redirections. Le contenu des pages
(balise `<title>`) a été comparé à la source citée. Les 4 articles
scientifiques ont été vérifiés via leur DOI (`https://doi.org/...`).

## Liens des entrées web (@misc)

| Référence | URL initiale | Code HTTP | Statut | Action effectuée | URL finale |
|---|---|---|---|---|---|
| flask | https://flask.palletsprojects.com/ | 200 | OK | Aucune (redirige vers /en/stable/, comportement normal) | inchangée |
| sqlalchemy | https://www.sqlalchemy.org/ | 200 | OK | Aucune | inchangée |
| marshmallow | https://marshmallow.readthedocs.io/ | 200 | OK | Aucune | inchangée |
| gunicorn | https://gunicorn.org/ | 200 | OK | Aucune (titre conforme : « Gunicorn - Python WSGI HTTP Server for UNIX ») | inchangée |
| vuejs | https://vuejs.org/ | 200 | OK | Aucune | inchangée |
| vite | https://vite.dev/ | 200 | OK | Aucune | inchangée |
| tailwindcss | https://tailwindcss.com/ | 200 | OK | Aucune | inchangée |
| vuerouter | https://router.vuejs.org/ | 200 | OK | Aucune | inchangée |
| docker | https://www.docker.com/ | 200 | OK | Aucune | inchangée |
| dockercompose | https://docs.docker.com/compose/ | 200 | OK | Aucune | inchangée |
| postgresql | https://www.postgresql.org/ | 200 | OK | Aucune | inchangée |
| pytest | https://pytest.org/ | 200 | OK | Aucune (redirection officielle vers docs.pytest.org/en/stable/) | inchangée |
| gnumake | https://www.gnu.org/software/make/ | 200 | OK | Aucune | inchangée |
| kaggle-credit-risk | https://www.kaggle.com/datasets/laotse/credit-risk-dataset | 200 (GET) | OK | Aucune (HEAD bloqué par Kaggle, GET confirme « Credit Risk Dataset \| Kaggle ») | inchangée |
| joblib | https://joblib.readthedocs.io/ | 200 | OK | Aucune | inchangée |
| flaskcors | https://flask-cors.readthedocs.io/ | **404** | **Lien mort remplacé** | Voir détail ci-dessous | https://flask-cors.corydolphin.com/ |
| psycopg2 | https://www.psycopg.org/ | 200 | OK | Aucune (titre conforme : « Psycopg - PostgreSQL adapter for Python ») | inchangée |

## Articles scientifiques (DOI)

| Référence | DOI | Code HTTP | Statut | Cible |
|---|---|---|---|---|
| scikit-learn | (pas de DOI - article JMLR 2011, entrée vérifiée sur le fond) | - | OK | Journal of Machine Learning Research 12, p. 2825-2830 |
| pandas | 10.25080/Majora-92bf1922-00a | 200 | OK | proceedings.scipy.org |
| numpy | 10.1038/s41586-020-2649-2 | 200 | OK | nature.com |
| matplotlib | 10.1109/MCSE.2007.55 | 200 | OK | ieeexplore.ieee.org |
| seaborn | 10.21105/joss.03021 | 200 | OK | joss.theoj.org |

## Détail des corrections

### flaskcors - lien mort remplacé + auteur corrigé

- **Problème 1 :** `https://flask-cors.readthedocs.io/` redirige vers
  `/en/main/` qui renvoie **404**. Le projet ReadTheDocs est figé sur la
  version 3.0.10 (le projet actuel est en 6.x).
- **Solution :** le README officiel du dépôt `github.com/corydolphin/flask-cors`
  désigne `https://flask-cors.corydolphin.com/` comme documentation actuelle
  (vérifiée : 200, contenu conforme). C'est cette URL qui a été retenue
  (priorité à la documentation officielle).
- **Problème 2 :** l'auteur indiqué était « Cory Munroe ». Les métadonnées
  PyPI du paquet `flask-cors` confirment que l'auteur est **Cory Dolphin**
  (`corydolphin@gmail.com`). Corrigé.

### Dates de consultation

Une mention « Consulté en juin 2026 » a été ajoutée au champ `note` des
17 entrées web (`@misc`), conformément aux bonnes pratiques de citation de
ressources en ligne. Les 5 entrées d'articles scientifiques (datées et avec
DOI) n'en ont pas besoin.

### Nettoyage

`\nocite{*}` a été retiré de `rapport.tex` : les 22 entrées de `references.bib`
sont toutes citées explicitement dans le texte (vérifié par comptage des
`\cite{...}`), la directive était donc inutile. Aucune référence orpheline,
aucune citation sans entrée, aucun doublon.

## Bilan

- **22 références** au total ; **21 liens testés** (17 URL + 4 DOI), 1 article sans lien vérifié sur le fond.
- **20 liens valides** tels quels ; **1 lien mort remplacé** (flaskcors) ; **0 lien impossible à vérifier**.
- Cohérence citations/bibliographie : **22/22** entrées citées dans le texte.
