# Prédiction du Risque de Crédit Bancaire

**Projet académique - Techniques d'Apprentissage Artificiel**

Pipeline Python pour la prédiction du risque de défaut de paiement bancaire. Ce projet démontre la mise en œuvre d'un pipeline d'apprentissage automatique, depuis le chargement des données jusqu'à l'évaluation des modèles, en utilisant scikit-learn.

## Description

Le système classifie les emprunteurs en deux catégories :
- **Classe 0** : Absence de défaut de paiement (bon risque)
- **Classe 1** : Présence de défaut de paiement (mauvais risque)

### Architecture du projet

```
PROGRAMME/
├── back-end/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── predict.py
│   │   ├── preprocess.py
│   │   ├── requirements.txt
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── data/
│   │   ├── processed/
│   │   │   ├── split_info.txt
│   │   │   ├── test.csv
│   │   │   └── train.csv
│   │   └── raw/
│   │       ├── archive.zip
│   │       └── credit_risk_dataset.csv
│   ├── models/
│   │   ├── decision_tree.joblib
│   │   ├── logistic_regression.joblib
│   │   └── scaler.joblib
│   ├── results/
│   │   ├── metrics/
│   │   │   ├── decision_tree/
│   │   │   │   ├── dt_python_test_confusion_matrix.txt
│   │   │   │   ├── dt_python_test_metrics.txt
│   │   │   │   ├── dt_python_train_metrics.txt
│   │   │   │   └── dt_python_tree_stats.txt
│   │   │   └── logistic_regression/
│   │   │       ├── lr_python_test_confusion_matrix.txt
│   │   │       ├── lr_python_test_metrics.txt
│   │   │       └── lr_python_train_metrics.txt
│   │   └── plots/
│   │       ├── data/
│   │       │   ├── dt_python_roc_data.csv
│   │       │   ├── lr_python_cost_curve.csv
│   │       │   └── lr_python_roc_data.csv
│   │       ├── decision_tree/
│   │       │   ├── dt_python_confusion_matrix_test.png
│   │       │   ├── dt_python_metrics_train_vs_test.png
│   │       │   └── summary_dt_python.png
│   │       ├── logistic_regression/
│   │       │   ├── lr_dt_python_roc_curves_comparison.png
│   │       │   ├── lr_python_confusion_matrix_test.png
│   │       │   ├── lr_python_cost_curve_training.png
│   │       │   ├── lr_python_metrics_train_vs_test.png
│   │       │   └── summary_lr_python.png
│   │       └── summary_figure.png
│   ├── scripts/
│   │   ├── analyze_missing_values.py
│   │   ├── compare_with_sklearn.py
│   │   ├── detect_outliers.py
│   │   ├── explore_data.py
│   │   ├── plot_results.py
│   │   └── split_dataset.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_api.py
│   │   ├── test_predict.py
│   │   ├── test_preprocess.py
│   │   └── test_schemas.py
│   ├── Dockerfile.api
│   ├── pytest.ini
│   └── requirements.txt
├── docs/
│   ├── presentation/
│   │   └── DIAPO - M1 - Outils libres - Maxime BRONNY - 19009314.pdf
│   └── Rapport final/
│       └── RAPPORT - M1 - Outils libres -  Maxime BRONNY - 19009314.pdf
├── front-end/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── PredictionForm.vue
│   │   │   └── ResultCard.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── views/
│   │   │   ├── DetailView.vue
│   │   │   ├── HistoryView.vue
│   │   │   └── PredictView.vue
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── README.md
│   └── vite.config.js
├── .dockerignore
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── README.md
```

## Installation

### Prérequis

- Python 3.8+
- pip

### Installation des dépendances

```bash
pip install -r back-end/requirements.txt
```

## Utilisation

### Pipeline complet

```bash
make all
```

Exécute : split → train → plots

### Commandes individuelles

| Commande        | Description                                  |
| --------------- | -------------------------------------------- |
| `make split`    | Divise le dataset en train/test              |
| `make train`    | Entraîne les modèles (LR, arbre de décision) |
| `make plots`    | Génère les graphiques                        |
| `make explore`  | Exploration des données                      |
| `make outliers` | Détection des outliers                       |
| `make clean`    | Nettoie les fichiers générés                 |
| `make test`     | Exécute les tests unitaires (pytest)         |
| `make help`     | Affiche l'aide                               |

## Structure des données

- **Entrée** : `back-end/data/raw/credit_risk_dataset.csv`
- **Sortie** : `back-end/data/processed/train.csv`, `test.csv`
- **Résultats** : `back-end/results/metrics/`, `back-end/results/plots/`

## Technologies

- **Python 3** : pandas, numpy, matplotlib, seaborn, scikit-learn, Flask
- **Front-end** : Vue 3, Vite
- **Make** : Automatisation du pipeline ML
- **Docker Compose** : API + front-end + PostgreSQL

## Paramètres des modèles

### Régression logistique (scikit-learn)

| Paramètre     | Valeur   | Rôle                |
| ------------- | -------- | ------------------- |
| solver        | `lbfgs`  | Algorithme L-BFGS   |
| max_iter      | `1000`   | Nombre max d'itérations |
| random_state  | `42`     | Reproductibilité    |

### Arbre de décision (scikit-learn)

| Paramètre          | Valeur | Rôle                            |
| ------------------ | ------ | ------------------------------- |
| max_depth          | `7`    | Profondeur maximale             |
| min_samples_split  | `20`   | Min. échantillons pour diviser  |
| min_samples_leaf   | `10`   | Min. échantillons par feuille   |
| criterion         | `gini` | Critère d'impureté              |
| random_state      | `42`   | Reproductibilité                |

### Prétraitement

| Paramètre     | Valeur | Rôle                |
| ------------- | ------ | ------------------- |
| test_size     | `0.2`  | Proportion test (80 % train) |
| random_state  | `42`   | Graine pour le split |

## Versions et environnement

- **Python** : 3.8+ (3.11 recommandé)
- **Image Docker** : `python:3.11-slim`
- **Compatibilité** : Python 3.8 à 3.12 ; Linux, macOS, Windows

### Dépendances Python (version minimale)

| Package      | Version   |
| ------------ | --------- |
| pandas       | >= 1.5.0  |
| numpy        | >= 1.23.0 |
| matplotlib   | >= 3.6.0  |
| seaborn      | >= 0.12.0 |
| scikit-learn | >= 1.2.0  |

Installation : `pip install -r back-end/requirements.txt` (scripts ML) puis `pip install -r back-end/app/requirements.txt` (API).

## Tests

Les tests unitaires utilisent pytest. Prérequis : exécuter `make train` une fois pour générer les modèles.

```bash
make train   # une fois
make test    # pytest tests/ -v --tb=short
```

Tests purs (sans modèles) : `pytest tests/test_preprocess.py tests/test_predict.py tests/test_schemas.py`

## Déploiement Docker

```bash
docker compose up -d --build
```

Démarre : base PostgreSQL, API (port 8000), interface web (port 5173).

## Auteur

Maxime BRONNY
