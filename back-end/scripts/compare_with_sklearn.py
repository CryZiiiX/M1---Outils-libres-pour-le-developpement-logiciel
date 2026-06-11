#!/usr/bin/env python3
# =============================================================================
# Fichier : back-end/scripts/compare_with_sklearn.py
# Rôle    : Entraîner et évaluer les modèles scikit-learn (régression logistique
#           et arbre de décision) : imputation anti-fuite, validation croisée
#           de max_depth, variantes class_weight, métriques et sérialisation.
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Entraîner et évaluer les modèles scikit-learn (régression logistique et arbre de décision) : imputation anti-fuite, validation croisée de max_depth, variantes class_weight, métriques et sérialisation."""

import pandas as pd
import numpy as np
import time
import os
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
LR_MODEL_PATH = MODELS_DIR / "logistic_regression.joblib"
SCALER_PATH = MODELS_DIR / "scaler.joblib"
DT_MODEL_PATH = MODELS_DIR / "decision_tree.joblib"


def _encode_dataframe(df):
    """Applique uniquement l'encodage catégoriel (sans imputation).

    Aligné avec app.preprocess.encode_input pour cohérence API/scripts.
    Invariant : l'ordre des colonnes après drop('loan_status') doit correspondre
    à FEATURE_ORDER dans preprocess.py (modèles et scaler attendent cet ordre).

    Args:
        df: DataFrame pandas brut.

    Returns:
        DataFrame encodé (les valeurs manquantes sont conservées telles quelles).
    """
    df = df.copy()
    home_mapping = {'RENT': 0, 'OWN': 1, 'MORTGAGE': 2, 'OTHER': 3}
    df['person_home_ownership'] = df['person_home_ownership'].map(home_mapping)
    intent_mapping = {'PERSONAL': 0, 'EDUCATION': 1, 'MEDICAL': 2,
                     'VENTURE': 3, 'HOMEIMPROVEMENT': 4, 'DEBTCONSOLIDATION': 5}
    df['loan_intent'] = df['loan_intent'].map(intent_mapping)
    grade_mapping = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}
    df['loan_grade'] = df['loan_grade'].map(grade_mapping)
    default_mapping = {'N': 0, 'Y': 1}
    df['cb_person_default_on_file'] = df['cb_person_default_on_file'].map(default_mapping)
    return df


def compute_imputation_values(df_train):
    """Calcule les valeurs d'imputation (moyennes) sur le train set UNIQUEMENT.

    Anti-fuite de données : les statistiques d'imputation ne doivent jamais
    inclure le test set, sinon des informations du test contaminent le
    prétraitement (data leakage). Les mêmes valeurs sont ensuite appliquées
    au train et au test.

    Args:
        df_train: DataFrame d'entraînement encodé (peut contenir des NaN).

    Returns:
        Series pandas des moyennes par colonne numérique, apprises sur le train.
    """
    return df_train.mean(numeric_only=True)


def apply_imputation(df, impute_values):
    """Remplace les valeurs manquantes par les moyennes apprises sur le train.

    Args:
        df: DataFrame encodé (train ou test).
        impute_values: Series produite par compute_imputation_values (train).

    Returns:
        DataFrame sans valeur manquante.
    """
    return df.fillna(impute_values)


def load_train_test_from_files():
    """Charge les ensembles train et test préparés par make split.

    Les CSV de data/processed/ sont bruts (catégories en texte, valeurs
    manquantes conservées) : on encode donc chaque ensemble, puis on impute
    les valeurs manquantes avec des moyennes calculées sur le train
    uniquement, appliquées ensuite aux deux ensembles. Calculer ces moyennes
    sur le test (ou sur le tout) serait une fuite de données : le test doit
    rester totalement inconnu du prétraitement.

    Returns:
        tuple: (X_train, X_test, y_train, y_test) prêts pour l'entraînement,
        ou None si les fichiers n'existent pas (le main bascule alors sur le
        dataset brut).
    """
    train_path = BASE_DIR / "data" / "processed" / "train.csv"
    test_path = BASE_DIR / "data" / "processed" / "test.csv"

    if not train_path.exists() or not test_path.exists():
        return None

    print(" Chargement des datasets train.csv et test.csv...")
    df_train = pd.read_csv(train_path)
    df_test = pd.read_csv(test_path)

    print(f"[OK] Train: {len(df_train)} échantillons, Test: {len(df_test)} échantillons")
    df_train = _encode_dataframe(df_train)
    df_test = _encode_dataframe(df_test)

    X_train = df_train.drop('loan_status', axis=1)
    y_train = df_train['loan_status']
    X_test = df_test.drop('loan_status', axis=1)
    y_test = df_test['loan_status']

    # Imputation anti-fuite : moyennes apprises sur le train, appliquées aux deux
    impute_values = compute_imputation_values(X_train)
    X_train = apply_imputation(X_train, impute_values)
    X_test = apply_imputation(X_test, impute_values)
    print("[OK] Imputation des valeurs manquantes (moyennes du train uniquement)")

    print("[OK] Datasets chargés et séparés (X, y)")

    return X_train, X_test, y_train, y_test


def load_and_preprocess_data():
    """Charge le dataset brut et applique l'encodage catégoriel SANS imputation.

    L'imputation est volontairement absente ici : elle doit être réalisée
    APRÈS le split train/test, avec des statistiques apprises sur le train
    uniquement (voir main), pour éviter toute fuite de données.

    Returns:
        Tuple (X, y) features encodées (NaN conservés) et labels.
    """
    print(" Chargement du dataset...")
    df = pd.read_csv(BASE_DIR / "data" / "raw" / "credit_risk_dataset.csv")

    print(f"[OK] Dataset chargé: {df.shape[0]} lignes, {df.shape[1]} colonnes")
    print("\n Encodage des variables catégorielles...")
    df = _encode_dataframe(df)
    print("[OK] Variables catégorielles encodées (imputation différée après split)")
    X = df.drop('loan_status', axis=1)
    y = df['loan_status']

    return X, y


def train_sklearn_model(X_train, y_train, X_test, y_test):
    """Entraîne la régression logistique et trace sa courbe de coût.

    Deux choses importantes ici. D'abord la normalisation : le StandardScaler
    est ajusté (fit) sur le train uniquement, puis appliqué (transform) au
    test - ajuster le scaler sur le test serait une fuite de données. Ensuite
    la courbe de coût : on réentraîne le modèle avec un nombre croissant
    d'itérations (50 à 1000) et on mesure la log loss à chaque palier, ce qui
    permet de visualiser la convergence de l'optimiseur L-BFGS dans le
    rapport. Le modèle final utilise 1000 itérations.

    Args:
        X_train, y_train: Données d'entraînement.
        X_test, y_test: Données de test (utilisées seulement pour le transform).

    Returns:
        tuple: (modèle entraîné, scaler ajusté, X_train normalisé,
        X_test normalisé).
    """
    print("\n Entraînement du modèle scikit-learn...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    (BASE_DIR / "results" / "plots").mkdir(parents=True, exist_ok=True)
    iteration_points = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    cost_data = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for max_iter in iteration_points:
            model = LogisticRegression(
                solver='lbfgs',
                max_iter=max_iter,
                random_state=42
            )
            model.fit(X_train_scaled, y_train)
            y_train_proba = model.predict_proba(X_train_scaled)[:, 1]
            loss = calculate_cross_entropy_loss(y_train, y_train_proba)
            cost_data.append({'iteration': max_iter, 'cost': loss})
    final_model = LogisticRegression(
        solver='lbfgs',
        max_iter=1000,
        random_state=42
    )
    final_model.fit(X_train_scaled, y_train)
    (BASE_DIR / "results" / "plots" / "data").mkdir(parents=True, exist_ok=True)
    cost_df = pd.DataFrame(cost_data)
    cost_df.to_csv(BASE_DIR / "results" / "plots" / "data" / "lr_python_cost_curve.csv", index=False)
    print("[OK] Courbe de coût sauvegardée: back-end/results/plots/data/lr_python_cost_curve.csv")
    
    print("[OK] Modèle entraîné")
    
    return final_model, scaler, X_train_scaled, X_test_scaled


def train_sklearn_decision_tree(X_train, y_train, X_test, y_test):
    """Entraîne l'arbre de décision avec des garde-fous contre le
    surapprentissage.

    Un arbre sans contrainte apprendrait le train par cœur. On limite donc
    la profondeur à 7 (valeur justifiée par validation croisée, voir
    cross_validate_max_depth), et on impose un minimum de 20 échantillons
    pour diviser un nœud et de 10 par feuille : cela empêche l'arbre de
    créer des règles à partir de quelques cas particuliers. Le temps
    d'entraînement est mesuré pour les statistiques du rapport.

    Returns:
        tuple: (modèle entraîné, durée d'entraînement en secondes).
    """
    print("\n Entraînement de l'arbre de décision scikit-learn...")
    model = DecisionTreeClassifier(
        max_depth=7,
        min_samples_split=20,
        min_samples_leaf=10,
        criterion='gini',
        random_state=42
    )
    start_time = time.time()
    model.fit(X_train, y_train)
    end_time = time.time()
    training_time = end_time - start_time
    
    print("[OK] Arbre de décision entraîné")
    
    return model, training_time


def cross_validate_max_depth(X_train, y_train):
    """Validation croisée stratifiée 5-fold pour justifier le choix de max_depth.

    Compare les profondeurs 3, 5, 7, 9 et 11 (mêmes autres hyperparamètres que
    le modèle final) sur le train set uniquement, avec F1, recall et AUC-ROC.
    Le test set n'est jamais utilisé ici : il reste réservé à l'évaluation finale.

    Returns:
        Liste de dicts {depth, f1, recall, auc} (moyennes sur les 5 folds).
    """
    print("\n Validation croisée (StratifiedKFold 5) pour max_depth...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scoring = {"f1": "f1", "recall": "recall", "auc": "roc_auc"}
    rows = []
    for depth in [3, 5, 7, 9, 11]:
        model = DecisionTreeClassifier(
            max_depth=depth,
            min_samples_split=20,
            min_samples_leaf=10,
            criterion='gini',
            random_state=42,
        )
        scores = cross_validate(model, X_train, y_train, cv=cv, scoring=scoring)
        rows.append({
            "depth": depth,
            "f1": scores["test_f1"].mean(),
            "f1_std": scores["test_f1"].std(),
            "recall": scores["test_recall"].mean(),
            "auc": scores["test_auc"].mean(),
        })
        print(f"  max_depth={depth:2d} : F1={rows[-1]['f1']:.4f} "
              f"(±{rows[-1]['f1_std']:.4f})  recall={rows[-1]['recall']:.4f}  "
              f"AUC={rows[-1]['auc']:.4f}")

    output_path = BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_cv_max_depth.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write("VALIDATION CROISEE STRATIFIEE 5-FOLD (train set uniquement)\n")
        f.write("Choix de max_depth - autres hyperparametres identiques au modele final\n\n")
        f.write(f"{'max_depth':>9} {'F1':>8} {'F1 std':>8} {'Recall':>8} {'AUC-ROC':>8}\n")
        for r in rows:
            f.write(f"{r['depth']:>9} {r['f1']:>8.4f} {r['f1_std']:>8.4f} "
                    f"{r['recall']:>8.4f} {r['auc']:>8.4f}\n")
    print(f"[OK] Résultats CV sauvegardés: {output_path}")
    return rows


def compare_class_weight_variants(X_train_scaled, y_train, X_test_scaled, y_test,
                                  X_train, X_test):
    """Compare les modèles standards à des variantes class_weight='balanced'.

    Le déséquilibre des classes (78/22) pénalise le recall des modèles non
    pondérés. Cette fonction entraîne une LR et un DT avec
    class_weight='balanced' (mêmes hyperparamètres par ailleurs) et sauvegarde
    les métriques de test des quatre modèles pour comparaison dans le rapport.
    Les modèles pondérés ne remplacent pas les modèles déployés : ils servent
    d'étude de variante documentée.
    """
    print("\n Comparaison class_weight='balanced' (LR et DT)...")
    variants = {}

    lr_bal = LogisticRegression(solver='lbfgs', max_iter=1000, random_state=42,
                                class_weight='balanced')
    lr_bal.fit(X_train_scaled, y_train)
    variants['LR balanced'] = (lr_bal.predict(X_test_scaled),
                               lr_bal.predict_proba(X_test_scaled)[:, 1])

    dt_bal = DecisionTreeClassifier(max_depth=7, min_samples_split=20,
                                    min_samples_leaf=10, criterion='gini',
                                    random_state=42, class_weight='balanced')
    dt_bal.fit(X_train, y_train)
    variants['DT balanced'] = (dt_bal.predict(X_test),
                               dt_bal.predict_proba(X_test)[:, 1])

    output_path = BASE_DIR / "results" / "metrics" / "class_weight_comparison.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write("COMPARAISON class_weight='balanced' (metriques sur le test set)\n")
        f.write("Les modeles 'balanced' sont des variantes d'etude, non deployees.\n\n")
        f.write(f"{'Modele':<14} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} "
                f"{'F1':>8} {'AUC-ROC':>8}\n")
        for name, (y_pred, y_proba) in variants.items():
            f.write(f"{name:<14} {accuracy_score(y_test, y_pred):>9.4f} "
                    f"{precision_score(y_test, y_pred, zero_division=0):>10.4f} "
                    f"{recall_score(y_test, y_pred, zero_division=0):>8.4f} "
                    f"{f1_score(y_test, y_pred, zero_division=0):>8.4f} "
                    f"{roc_auc_score(y_test, y_proba):>8.4f}\n")
            print(f"  {name:<14}: recall="
                  f"{recall_score(y_test, y_pred, zero_division=0):.4f}  "
                  f"precision={precision_score(y_test, y_pred, zero_division=0):.4f}  "
                  f"F1={f1_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"[OK] Comparaison class_weight sauvegardée: {output_path}")


def load_or_train_lr(X_train, y_train, X_test, y_test, force_retrain):
    """Charge la régression logistique depuis models/ ou l'entraîne si besoin.

    Ce mécanisme de cache évite de réentraîner à chaque exécution : si les
    fichiers .joblib existent déjà, on les recharge simplement (et on
    recalcule les versions normalisées des données avec le scaler sauvegardé).
    La variable d'environnement FORCE_RETRAIN=1 (cible make train-force)
    permet de forcer un réentraînement complet.

    Returns:
        tuple: (modèle, scaler, X_train normalisé, X_test normalisé).
    """
    if force_retrain or not LR_MODEL_PATH.exists() or not SCALER_PATH.exists():
        model, scaler, X_train_scaled, X_test_scaled = train_sklearn_model(
            X_train, y_train, X_test, y_test
        )
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, LR_MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)
        print("[OK] Modèle LR sauvegardé dans models/")
        return model, scaler, X_train_scaled, X_test_scaled
    else:
        model = joblib.load(LR_MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        print("[OK] Modèle LR chargé depuis models/")
        return model, scaler, X_train_scaled, X_test_scaled


def load_or_train_dt(X_train, y_train, X_test, y_test, force_retrain):
    """Charge l'arbre de décision depuis models/ ou l'entraîne si besoin.

    Même logique de cache que pour la régression logistique. Le temps
    d'entraînement vaut 0.0 quand le modèle est rechargé depuis le disque.

    Returns:
        tuple: (modèle, durée d'entraînement en secondes).
    """
    if force_retrain or not DT_MODEL_PATH.exists():
        dt_model, training_time = train_sklearn_decision_tree(
            X_train, y_train, X_test, y_test
        )
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        joblib.dump(dt_model, DT_MODEL_PATH)
        print("[OK] Modèle DT sauvegardé dans models/")
        return dt_model, training_time
    else:
        dt_model = joblib.load(DT_MODEL_PATH)
        print("[OK] Modèle DT chargé depuis models/")
        return dt_model, 0.0


def save_sklearn_lr_metrics(sklearn_metrics):
    """Sauvegarde accuracy, precision, recall, f1, auc_roc dans lr_python_test_metrics.txt."""
    output_path = BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_metrics.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("REGRESSION LOGISTIQUE - SCIKIT-LEARN (PYTHON)\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Accuracy:  {sklearn_metrics['accuracy']:.6f}\n")
        f.write(f"Precision: {sklearn_metrics['precision']:.6f}\n")
        f.write(f"Recall:    {sklearn_metrics['recall']:.6f}\n")
        f.write(f"F1-Score:  {sklearn_metrics['f1']:.6f}\n")
        f.write(f"AUC-ROC:   {sklearn_metrics['auc_roc']:.6f}\n")
    
    print(f"[OK] Métriques sklearn LR sauvegardées: {output_path}")


def save_sklearn_dt_metrics(sklearn_metrics):
    """Sauvegarde les métriques DT dans dt_python_test_metrics.txt."""
    output_path = BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_metrics.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("ARBRE DE DÉCISION - SCIKIT-LEARN (PYTHON)\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Accuracy:  {sklearn_metrics['accuracy']:.6f}\n")
        f.write(f"Precision: {sklearn_metrics['precision']:.6f}\n")
        f.write(f"Recall:    {sklearn_metrics['recall']:.6f}\n")
        f.write(f"F1-Score:  {sklearn_metrics['f1']:.6f}\n")
        f.write(f"AUC-ROC:   {sklearn_metrics['auc_roc']:.6f}\n")
    
    print(f"[OK] Métriques sklearn DT sauvegardées: {output_path}")


def save_decision_tree_stats(model, training_time, filename):
    """Sauvegarde profondeur, nœuds, temps et hyperparamètres dans un fichier texte."""
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    actual_depth = model.tree_.max_depth
    total_nodes = model.tree_.node_count
    
    with open(output_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("STATISTIQUES ARBRE DE DÉCISION - SCIKIT-LEARN (PYTHON)\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Profondeur réelle: {actual_depth}\n")
        f.write(f"Nombre total de nœuds: {total_nodes}\n")
        f.write(f"Temps d'entraînement: environ {training_time:.3f} secondes\n")
        f.write("\n")
        f.write("Hyperparamètres:\n")
        f.write(f"  - max_depth: {model.max_depth}\n")
        f.write(f"  - min_samples_split: {model.min_samples_split}\n")
        f.write(f"  - min_samples_leaf: {model.min_samples_leaf}\n")
        f.write(f"  - criterion: {model.criterion}\n")
    
    print(f"[OK] Statistiques arbre de décision sauvegardées: {output_path}")


def save_python_train_metrics(y_true, y_pred, filename):
    """Calcule et sauvegarde accuracy, precision, recall, f1 sur le train set."""
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(f"Accuracy: {accuracy:.6f}\n")
        f.write(f"Precision: {precision:.6f}\n")
        f.write(f"Recall: {recall:.6f}\n")
        f.write(f"F1-Score: {f1:.6f}\n")
    print(f"[OK] Métriques train sauvegardées: {output_path}")


def calculate_cross_entropy_loss(y_true, y_pred_proba):
    """Calcule la perte d'entropie croisée (log loss) de la régression
    logistique.

    C'est la fonction de coût que la régression logistique minimise pendant
    l'entraînement : elle pénalise fortement les prédictions confiantes mais
    fausses. Les probabilités sont bornées à [1e-15, 1 - 1e-15] avant le
    logarithme, car log(0) vaudrait moins l'infini et ferait planter le calcul.

    Args:
        y_true: Labels réels (0 ou 1).
        y_pred_proba: Probabilités prédites par le modèle.

    Returns:
        float: Valeur moyenne de la perte sur l'ensemble fourni.
    """
    epsilon = 1e-15
    y_pred_proba = np.clip(y_pred_proba, epsilon, 1 - epsilon)
    loss = -np.mean(y_true * np.log(y_pred_proba) + (1 - y_true) * np.log(1 - y_pred_proba))
    return loss


def save_python_confusion_matrix(cm, filename):
    """Sauvegarde la matrice de confusion au format TN, FP, FN, TP."""
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(f"TN: {cm[0,0]}, FP: {cm[0,1]}\n")
        f.write(f"FN: {cm[1,0]}, TP: {cm[1,1]}\n")
    print(f"[OK] Matrice de confusion sauvegardée: {output_path}")


def save_roc_data(y_true, y_proba, filename):
    """Calcule et sauvegarde fpr, tpr (roc_curve) dans un CSV."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    df = pd.DataFrame({'fpr': fpr, 'tpr': tpr})
    output_path = Path(filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[OK] Données ROC sauvegardées: {filename}")


def main():
    """Orchestre tout le pipeline d'entraînement et d'évaluation.

    Déroulement : chargement des données (fichiers préparés ou dataset brut
    en secours, avec imputation anti-fuite dans les deux cas), entraînement
    ou rechargement des deux modèles, analyses de justification (validation
    croisée de max_depth, variantes class_weight), puis calcul et sauvegarde
    des métriques, matrices de confusion et données ROC pour chaque modèle.
    FORCE_RETRAIN=1 force le réentraînement complet.
    """
    force_retrain = os.environ.get("FORCE_RETRAIN", "").lower() in ("1", "true", "yes")
    
    print("\n" + "=" * 60)
    print("VALIDATION AVEC SCIKIT-LEARN")
    print("=" * 60 + "\n")
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    result = load_train_test_from_files()
    
    if result is None:
        print("\n[INFO] Fichiers train.csv et test.csv non trouvés. Génération depuis le dataset brut...")
        X, y = load_and_preprocess_data()
        # Split AVANT imputation : les moyennes d'imputation sont apprises sur
        # le train uniquement puis appliquées au test (anti-fuite de données)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        impute_values = compute_imputation_values(X_train)
        X_train = apply_imputation(X_train, impute_values)
        X_test = apply_imputation(X_test, impute_values)
        print(f"[OK] Split effectué: Train={len(X_train)}, Test={len(X_test)}")
        print("[OK] Imputation post-split (moyennes du train uniquement)")
    else:
        X_train, X_test, y_train, y_test = result
    model, scaler, X_train_scaled, X_test_scaled = load_or_train_lr(
        X_train, y_train, X_test, y_test, force_retrain
    )

    # Analyses de justification (CV max_depth, variantes class_weight) :
    # exécutées si absentes ou si réentraînement forcé
    cv_path = BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_cv_max_depth.txt"
    cw_path = BASE_DIR / "results" / "metrics" / "class_weight_comparison.txt"
    if force_retrain or not cv_path.exists():
        cross_validate_max_depth(X_train, y_train)
    if force_retrain or not cw_path.exists():
        compare_class_weight_variants(X_train_scaled, y_train, X_test_scaled,
                                      y_test, X_train, X_test)
    y_train_pred = model.predict(X_train_scaled)
    save_python_train_metrics(y_train, y_train_pred, str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_train_metrics.txt"))
    print("\n Prédictions sur le test set...")
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    (BASE_DIR / "results" / "plots" / "data").mkdir(parents=True, exist_ok=True)
    save_roc_data(y_test, y_pred_proba, str(BASE_DIR / "results" / "plots" / "data" / "lr_python_roc_data.csv"))
    sklearn_metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, zero_division=0),
        'recall': recall_score(y_test, y_pred, zero_division=0),
        'f1': f1_score(y_test, y_pred, zero_division=0),
        'auc_roc': roc_auc_score(y_test, y_pred_proba)
    }
    
    print("\n Métriques scikit-learn:")
    print(f"  Accuracy:  {sklearn_metrics['accuracy']:.4f}")
    print(f"  Precision: {sklearn_metrics['precision']:.4f}")
    print(f"  Recall:    {sklearn_metrics['recall']:.4f}")
    print(f"  F1-Score:  {sklearn_metrics['f1']:.4f}")
    print(f"  AUC-ROC:   {sklearn_metrics['auc_roc']:.4f}")
    cm = confusion_matrix(y_test, y_pred)
    print(f"\n  Confusion Matrix:")
    print(f"    TN: {cm[0,0]}, FP: {cm[0,1]}")
    print(f"    FN: {cm[1,0]}, TP: {cm[1,1]}")
    save_python_confusion_matrix(cm, str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_confusion_matrix.txt"))
    save_sklearn_lr_metrics(sklearn_metrics)
    print("\n\n" + "=" * 60)
    print("ARBRE DE DÉCISION")
    print("=" * 60 + "\n")
    dt_model, dt_training_time = load_or_train_dt(
        X_train, y_train, X_test, y_test, force_retrain
    )
    save_decision_tree_stats(dt_model, dt_training_time, str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_tree_stats.txt"))
    dt_y_train_pred = dt_model.predict(X_train)
    save_python_train_metrics(y_train, dt_y_train_pred, str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_train_metrics.txt"))
    print("\n Prédictions sur le test set...")
    dt_y_pred = dt_model.predict(X_test)
    dt_y_proba = dt_model.predict_proba(X_test)[:, 1]
    (BASE_DIR / "results" / "plots" / "data").mkdir(parents=True, exist_ok=True)
    save_roc_data(y_test, dt_y_proba, str(BASE_DIR / "results" / "plots" / "data" / "dt_python_roc_data.csv"))
    dt_sklearn_metrics = {
        'accuracy': accuracy_score(y_test, dt_y_pred),
        'precision': precision_score(y_test, dt_y_pred, zero_division=0),
        'recall': recall_score(y_test, dt_y_pred, zero_division=0),
        'f1': f1_score(y_test, dt_y_pred, zero_division=0),
        'auc_roc': roc_auc_score(y_test, dt_y_proba)
    }
    
    print("\n Métriques arbre de décision scikit-learn:")
    print(f"  Accuracy:  {dt_sklearn_metrics['accuracy']:.4f}")
    print(f"  Precision: {dt_sklearn_metrics['precision']:.4f}")
    print(f"  Recall:    {dt_sklearn_metrics['recall']:.4f}")
    print(f"  F1-Score:  {dt_sklearn_metrics['f1']:.4f}")
    print(f"  AUC-ROC:   {dt_sklearn_metrics['auc_roc']:.4f}")
    dt_cm = confusion_matrix(y_test, dt_y_pred)
    print(f"\n  Confusion Matrix:")
    print(f"    TN: {dt_cm[0,0]}, FP: {dt_cm[0,1]}")
    print(f"    FN: {dt_cm[1,0]}, TP: {dt_cm[1,1]}")
    save_python_confusion_matrix(dt_cm, str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_confusion_matrix.txt"))
    save_sklearn_dt_metrics(dt_sklearn_metrics)
    
    print("\n" + "=" * 60)
    print("[OK] ENTRAÎNEMENT TERMINÉ")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

