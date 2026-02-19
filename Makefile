# ============================================================================
# Makefile - Prédiction du Risque de Crédit (Python)
# ============================================================================
# Pipeline Python pour la prédiction du risque de défaut de paiement bancaire.
# Dépendances : split -> train -> plots. test dépend de train (modèles requis).
# ============================================================================

# Variables : PYTHON = interpréteur, BACKEND = répertoire des scripts
PYTHON = python3
BACKEND = back-end

.PHONY: all split train train-force plots explore outliers clean help test

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
test: train
	@cd $(BACKEND) && (../.venv/bin/python -m pytest tests/ -v --tb=short 2>/dev/null || $(PYTHON) -m pytest tests/ -v --tb=short)

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
	@echo "  make clean   - Nettoie les fichiers générés"
	@echo "  make help    - Affiche cette aide"
	@echo ""
