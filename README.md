# Prédiction du risque de crédit bancaire

## Présentation du projet

Ce projet met en place une application complète permettant d'estimer le risque
de défaut d'un emprunteur à partir d'un jeu de données de crédit. L'objectif
est de travailler sur une chaîne complète : préparation des données,
entraînement de modèles de classification, exposition des prédictions via une
API REST et affichage des résultats dans une interface web.

Il s'agit d'un projet académique : l'application illustre une démarche
d'apprentissage automatique de bout en bout avec des outils libres, elle n'est
pas destinée à un usage bancaire réel.

## Contexte universitaire

- Master 1 Big Data - Université Paris 8
- UE : Outils libres pour le développement logiciel
- Auteur : Maxime BRONNY - 19009314

Le rapport complet du projet se trouve dans
[`docs/Rapport final/`](docs/Rapport%20final/), et le support de soutenance
dans `docs/presentation/`.

## Objectifs

- Construire un pipeline de machine learning reproductible, orchestré par un
  Makefile.
- Entraîner et comparer deux modèles de classification (régression logistique
  et arbre de décision).
- Exposer les prédictions via une API Flask avec validation des entrées.
- Proposer une interface web Vue 3 pour saisir une demande et consulter
  l'historique.
- Conteneuriser l'ensemble avec Docker Compose (base PostgreSQL incluse).
- Tester le projet (pytest, couverture) et automatiser les tests (CI).
- N'utiliser que des outils libres, et documenter les choix dans le rapport.

## Fonctionnalités principales

- Split stratifié du dataset en ensembles d'entraînement et de test (80/20).
- Entraînement des deux modèles avec imputation des valeurs manquantes sans
  fuite de données, validation croisée pour le choix de la profondeur de
  l'arbre, et étude de variantes pondérées (`class_weight="balanced"`).
- Génération des métriques (accuracy, precision, recall, F1, AUC-ROC) et des
  graphiques d'évaluation (matrices de confusion, courbes ROC).
- API de prédiction : un payload JSON validé, une probabilité de défaut, un
  niveau de risque et une décision de crédit selon des seuils métier (30/60 %).
- Historique des prédictions persisté en base et consultable.
- Interface web : formulaire de demande, résultats des deux modèles,
  historique et vue de détail.
- Exécution complète via Docker Compose, avec healthchecks.
- 25 tests automatisés et mesure de couverture, rejoués par une CI GitHub
  Actions à chaque push.

## Technologies utilisées

**Pipeline ML (Python)**
- scikit-learn : entraînement des modèles, split stratifié, métriques.
- pandas / NumPy : manipulation des données.
- matplotlib / seaborn : graphiques d'évaluation et d'exploration.
- joblib : sérialisation des modèles entraînés.

**Back-end**
- Flask : API REST.
- Marshmallow : validation des payloads.
- SQLAlchemy : ORM pour la persistance des prédictions.
- Gunicorn : serveur WSGI dans le conteneur de l'API.
- PostgreSQL : base de données en déploiement Docker (SQLite en local/test).

**Front-end**
- Vue 3 : interface web (Composition API).
- Vite : serveur de développement et build.
- Tailwind CSS : styles.

**Outillage**
- Make : orchestration du pipeline et des tests.
- Docker / Docker Compose : conteneurisation des trois services.
- pytest / pytest-cov : tests et couverture.
- Git / GitHub Actions : versionnement et intégration continue.

## Architecture du projet

Le projet comporte deux parties reliées par les modèles sérialisés :

1. **Pipeline ML hors ligne** : `make all` enchaîne le split du dataset,
   l'entraînement des modèles et la génération des graphiques. Les modèles
   sont sauvegardés au format `.joblib` dans `back-end/models/`.
2. **Application web** : l'API Flask charge les `.joblib` au démarrage, le
   front-end Vue 3 communique avec elle en JSON, et les prédictions sont
   enregistrées dans PostgreSQL. Docker Compose orchestre les trois services
   (base de données, API, front-end).

## Arborescence du dépôt

```text
PROGRAMME/
├── back-end/
│   ├── app/            # API Flask (routes, validation, prédiction, ORM)
│   ├── scripts/        # Pipeline ML (split, entraînement, graphiques, analyses)
│   ├── tests/          # 25 tests pytest
│   ├── data/           # Dataset brut (raw/) et splitté (processed/)
│   ├── models/         # Modèles .joblib (LR, arbre, scaler)
│   ├── results/        # Métriques et graphiques générés
│   ├── Dockerfile.api
│   ├── pytest.ini
│   └── requirements.txt
├── front-end/
│   ├── src/            # Vues, composants, client API, routeur
│   ├── Dockerfile
│   └── package.json
├── docs/
│   ├── Rapport final/  # Rapport PDF + sources LaTeX
│   └── presentation/   # Support de soutenance
├── .github/workflows/  # CI (tests.yml)
├── Makefile
├── Dockerfile          # Reproduction du pipeline ML dans un conteneur
├── docker-compose.yml
├── LICENSE
└── README.md
```

## Installation locale

Prérequis : Python 3.11 (3.8+ accepté), pip, et Node.js 20 pour le front-end.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r back-end/requirements.txt       # scripts ML
pip install -r back-end/app/requirements.txt   # API + tests
```

## Exécution du pipeline ML

Le Makefile orchestre toutes les étapes :

```bash
make all          # pipeline complet : split -> train -> plots
```

Commandes individuelles :

| Commande | Description |
|---|---|
| `make split` | Split stratifié 80/20 du dataset |
| `make train` | Entraînement des modèles (réutilise les `.joblib` existants) |
| `make train-force` | Réentraînement forcé |
| `make plots` | Génération des graphiques d'évaluation |
| `make explore` | Exploration statistique du dataset |
| `make outliers` | Détection des valeurs aberrantes (IQR, Z-score) |
| `make test` | Tests pytest (entraîne d'abord si nécessaire) |
| `make coverage` | Tests avec mesure de couverture |
| `make docker-up` | Entraîne les modèles puis lance Docker Compose |
| `make clean` | Supprime les fichiers générés (destructif) |
| `make help` | Affiche l'aide |

## Lancement avec Docker Compose

L'API a besoin des modèles `.joblib` : il faut entraîner avant de déployer.
La cible `docker-up` enchaîne les deux étapes dans le bon ordre :

```bash
make docker-up    # équivalent à : make train && docker compose up -d --build
```

Trois services démarrent, dans un ordre garanti par des healthchecks
(PostgreSQL prêt avant l'API, API saine avant le front-end) :

| Service | Adresse |
|---|---|
| Interface web | http://localhost:5173 |
| API Flask | http://localhost:8000 |
| PostgreSQL | localhost:5432 |

Pour arrêter : `docker compose down`.

## Utilisation de l'application

Une fois les services lancés, l'interface est disponible sur
http://localhost:5173 :

- la page principale propose un formulaire de demande de crédit (11 champs,
  le ratio prêt/revenu est calculé automatiquement) ;
- après soumission, les résultats des deux modèles s'affichent : probabilité
  de défaut, niveau de risque et décision ;
- la page Historique liste les prédictions enregistrées, avec une vue de
  détail pour chacune.

Pour vérifier rapidement que l'API répond :
`curl http://localhost:8000/health` doit retourner `{"status": "ok"}`.

## API REST

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/health` | État de l'API |
| POST | `/predict` | Prédiction (corps JSON, modèle `lr`, `dt` ou `both`) |
| GET | `/predictions` | Historique (paramètre `limit`, défaut 50) |
| GET | `/predictions/<id>` | Détail d'une prédiction |

Exemple de requête :

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "person_age": 30, "person_income": 50000,
    "person_home_ownership": "RENT", "person_emp_length": 5,
    "loan_intent": "PERSONAL", "loan_grade": "B",
    "loan_amnt": 10000, "loan_int_rate": 10,
    "loan_percent_income": 0.2,
    "cb_person_default_on_file": "N",
    "cb_person_cred_hist_length": 5,
    "model_choice": "both"
  }'
```

Un payload invalide (champ manquant, valeur hors bornes) renvoie une erreur
400 avec le détail, et non une erreur serveur.

## Tests et qualité

```bash
make test       # 25 tests pytest
make coverage   # couverture du module app/ (actuellement 97 %)
```

Les tests couvrent la validation des entrées, l'encodage des features,
l'absence de fuite de données dans l'imputation, les seuils de classification
et les quatre endpoints de l'API (base SQLite en mémoire, aucune dépendance
externe).

Une CI GitHub Actions (`.github/workflows/tests.yml`) rejoue `make test` puis
`make coverage` à chaque push et pull request : comme le dataset et les
scripts sont versionnés, la CI réentraîne les modèles puis lance la suite
complète.

## Données et modèles

Le dataset utilisé est `credit_risk_dataset.csv` (Kaggle, licence CC0) :
32 581 demandes de crédit décrites par 11 variables (âge, revenu, montant et
objet du prêt, taux d'intérêt, grade, historique de crédit...) et une cible
binaire `loan_status` (défaut ou non). Les classes sont déséquilibrées :
environ 78 % de remboursements contre 22 % de défauts, ce qui explique
l'attention portée au recall et au F1-score plutôt qu'à la seule accuracy.

Deux modèles sont entraînés et comparés :

- **Régression logistique** (solver `lbfgs`, max_iter 1000, features
  normalisées par StandardScaler) ;
- **Arbre de décision** (profondeur 7 choisie par validation croisée
  stratifiée 5-fold, min_samples_split 20, min_samples_leaf 10).

L'imputation des valeurs manquantes utilise les moyennes du train uniquement
(pas de fuite de données), et des variantes `class_weight="balanced"` ont été
évaluées pour mesurer l'effet du déséquilibre (détail dans le rapport).

## Résultats principaux

Métriques sur le test set (6 517 demandes) :

| Modèle | Accuracy | Precision | Recall | F1 | AUC-ROC |
|---|---|---|---|---|---|
| Régression logistique | 0,849 | 0,736 | 0,482 | 0,582 | 0,852 |
| Arbre de décision | 0,927 | 0,950 | 0,704 | 0,809 | 0,906 |

L'arbre de décision est meilleur sur toutes les métriques ; la régression
logistique sert de référence linéaire. L'analyse complète (matrices de
confusion, courbes ROC, discussion du déséquilibre) est dans le rapport.

## Limites du projet

- L'API est publique : pas d'authentification, CORS ouvert.
- Le dataset est statique, sans réentraînement automatique.
- Seuls deux modèles classiques sont comparés (pas de méthodes d'ensemble).
- Le front-end Docker utilise le serveur de développement Vite, pas un build
  de production.
- Les identifiants PostgreSQL sont en clair dans `docker-compose.yml`.
- Application académique : elle ne doit pas servir à de vraies décisions de
  crédit.

## Licence

Le code de ce projet est distribué sous licence MIT (voir [LICENSE](LICENSE)).
Les dépendances et outils utilisés conservent leurs licences respectives
(BSD, MIT, Apache 2.0, GPL pour Make et Git utilisés comme outils de
développement).

## Auteur

Maxime BRONNY
Numéro étudiant : 19009314
Master 1 Big Data - Université Paris 8
