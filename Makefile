# =============================================================================
# Fichier : Makefile
# Rôle    : Automatiser les commandes du projet : préparation des données,
#           entraînement, graphiques, tests, couverture et déploiement Docker.
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
# Dépendances : split -> train -> plots. test dépend de train (modèles requis).

# Variables : PYTHON = interpréteur, BACKEND = répertoire des scripts
PYTHON = python3
BACKEND = back-end

.PHONY: all split train train-force plots explore outliers clean help test coverage docker-up

# Interpréteur de test : venv du projet s'il existe, python3 système sinon
PYTEST_PYTHON = $(shell [ -x .venv/bin/python ] && echo ../.venv/bin/python || echo $(PYTHON))

# Chaîne complète : split -> train -> plots
all: split train plots
	@echo ""
	@echo "============================================================"
	@echo "[OK] PIPELINE TERMINÉ"
	@echo "============================================================"

# Divise le dataset en train/test
split:
	@echo "============================================================"
	@echo "SPLIT DU DATASET"
	@echo "============================================================"
	@$(PYTHON) $(BACKEND)/scripts/split_dataset.py

# Entraîne les modèles et génère les métriques (réutilise les modèles sauvegardés si existants)
train: split
	@echo ""
	@echo "============================================================"
	@echo "ENTRAÎNEMENT DES MODÈLES"
	@echo "============================================================"
	@$(PYTHON) $(BACKEND)/scripts/compare_with_sklearn.py

# Force le réentraînement (ignore les modèles sauvegardés)
train-force: split
	@echo ""
	@echo "============================================================"
	@echo "ENTRAÎNEMENT FORCÉ DES MODÈLES"
	@echo "============================================================"
	@FORCE_RETRAIN=1 $(PYTHON) $(BACKEND)/scripts/compare_with_sklearn.py

# Génère les graphiques de visualisation
plots: train
	@echo ""
	@echo "============================================================"
	@echo "GÉNÉRATION DES GRAPHIQUES"
	@echo "============================================================"
	@$(PYTHON) $(BACKEND)/scripts/plot_results.py

# Exploration des données
explore:
	@$(PYTHON) $(BACKEND)/scripts/explore_data.py

# Détection des outliers
outliers:
	@$(PYTHON) $(BACKEND)/scripts/detect_outliers.py

# Tests unitaires et API (nécessite make train pour les modèles)
# Prérequis : créer .venv et installer deps (voir README)
# Le choix venv/système se fait sur l'existence du venv, pas sur le code
# retour de pytest : un échec de test reste visible et fait échouer la cible.
test: train
	@cd $(BACKEND) && $(PYTEST_PYTHON) -m pytest tests/ -v --tb=short

# Couverture de code des tests (pytest-cov), rapport terminal ligne à ligne
coverage: train
	@cd $(BACKEND) && $(PYTEST_PYTHON) -m pytest tests/ --cov=app --cov-report=term-missing

# Déploiement complet : entraîne les modèles PUIS lance les conteneurs.
# Évite le cas où l'API démarre sans modèles .joblib.
docker-up: train
	docker compose up -d --build

# Nettoie les fichiers générés (destructif : results, models, data/processed)
# À utiliser avec précaution. Réversible via make all.
clean:
	@echo "Nettoyage des fichiers générés..."
	@rm -rf $(BACKEND)/results/*
	@rm -f $(BACKEND)/models/*.bin $(BACKEND)/models/*.txt $(BACKEND)/models/*.joblib
	@rm -rf $(BACKEND)/data/processed/*
	@echo "Clean complete"

# Aide
help:
	@echo "Makefile - Prédiction du Risque de Crédit (Python)"
	@echo ""
	@echo "Cibles disponibles:"
	@echo "  make all     - Exécute le pipeline complet (split + train + plots)"
	@echo "  make split   - Divise le dataset en train/test"
	@echo "  make train   - Entraîne les modèles et génère les métriques (réutilise si existants)"
	@echo "  make train-force - Force le réentraînement (ignore les modèles sauvegardés)"
	@echo "  make plots   - Génère les graphiques"
	@echo "  make explore - Exploration des données"
	@echo "  make outliers - Détection des outliers"
	@echo "  make test    - Exécute les tests (pytest)"
	@echo "  make coverage - Tests avec mesure de couverture (pytest-cov)"
	@echo "  make docker-up - Entraîne les modèles puis lance docker compose"
	@echo "  make clean   - Nettoie les fichiers générés"
	@echo "  make help    - Affiche cette aide"
	@echo ""
