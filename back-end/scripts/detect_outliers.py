#!/usr/bin/env python3
"""
/*****************************************************************************************************

Nom : scripts/detect_outliers.py

Rôle : Script d'analyse des outliers dans le dataset (méthodes IQR et Z-score)

Auteur : Maxime BRONNY

Version : V1

Licence : Réalisé dans le cadre du cours Technique d'intelligence artificiel M1 INFORMATIQUE BIG-DATA

Usage :

    Pour compiler : N/A (script Python)

    Pour executer : python3 scripts/detect_outliers.py

******************************************************************************************************/
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def detect_outliers_iqr(df, col):
    """Détecte les outliers par IQR.

    Formule : [Q1 - 1.5×IQR, Q3 + 1.5×IQR]. Valeurs en dehors = outliers.
    Facteur 1.5 standard (règle de Tukey).

    Returns:
        Masque booléen (True = outlier).
    """
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (df[col] < lower_bound) | (df[col] > upper_bound)


def detect_outliers_zscore(df, col, threshold=3.0):
    """Détecte les outliers par Z-score.

    Formule : z = (x - mean) / std. |z| > threshold = outlier.
    Si std=0 (colonne constante), retourne False partout pour éviter division par zéro.

    Returns:
        Masque booléen (True = outlier).
    """
    mean = df[col].mean()
    std = df[col].std()
    if std == 0:
        return pd.Series([False] * len(df), index=df.index)
    z_scores = np.abs((df[col] - mean) / std)
    return z_scores > threshold


def analyze_outliers():
    """Analyse IQR et Z-score sur les variables numériques, sauvegarde dans data/stats/."""
    print("=" * 60)
    print("ANALYSE DES OUTLIERS")
    print("=" * 60)
    data_path = BASE_DIR / "data" / "raw" / "credit_risk_dataset.csv"
    print(f"\n Chargement du dataset: {data_path}")
    
    if not data_path.exists():
        print(f"[ERREUR] Fichier non trouvé: {data_path}")
        return
    
    df = pd.read_csv(data_path)
    print(f"[OK] Dataset chargé: {df.shape[0]} échantillons, {df.shape[1]} variables\n")
    numerical_cols = [
        'person_age',
        'person_income',
        'person_emp_length',
        'loan_amnt',
        'loan_int_rate',
        'loan_percent_income',
        'cb_person_cred_hist_length'
    ]
    numerical_cols = [col for col in numerical_cols if col in df.columns]
    
    print(f" Analyse de {len(numerical_cols)} variables numériques...\n")
    results = []
    
    for col in numerical_cols:
        col_data = df[col].dropna()
        
        if len(col_data) == 0:
            continue
        outliers_iqr_mask = detect_outliers_iqr(df, col)
        n_outliers_iqr = outliers_iqr_mask.sum()
        pct_outliers_iqr = 100 * n_outliers_iqr / len(df)
        outliers_zscore_mask = detect_outliers_zscore(df, col)
        n_outliers_zscore = outliers_zscore_mask.sum()
        pct_outliers_zscore = 100 * n_outliers_zscore / len(df)
        if n_outliers_iqr > 0:
            outliers_iqr_values = df.loc[outliers_iqr_mask, col]
            min_outlier_iqr = outliers_iqr_values.min()
            max_outlier_iqr = outliers_iqr_values.max()
            mean_outlier_iqr = outliers_iqr_values.mean()
            outlier_indices_iqr = outliers_iqr_mask[outliers_iqr_mask].index.tolist()[:10]
        else:
            min_outlier_iqr = None
            max_outlier_iqr = None
            mean_outlier_iqr = None
            outlier_indices_iqr = []
        if n_outliers_zscore > 0:
            outliers_zscore_values = df.loc[outliers_zscore_mask, col]
            min_outlier_zscore = outliers_zscore_values.min()
            max_outlier_zscore = outliers_zscore_values.max()
            mean_outlier_zscore = outliers_zscore_values.mean()
            outlier_indices_zscore = outliers_zscore_mask[outliers_zscore_mask].index.tolist()[:10]
        else:
            min_outlier_zscore = None
            max_outlier_zscore = None
            mean_outlier_zscore = None
            outlier_indices_zscore = []
        
        results.append({
            'Variable': col,
            'IQR_Count': n_outliers_iqr,
            'IQR_Pct': round(pct_outliers_iqr, 2),
            'ZScore_Count': n_outliers_zscore,
            'ZScore_Pct': round(pct_outliers_zscore, 2),
            'IQR_Min': min_outlier_iqr,
            'IQR_Max': max_outlier_iqr,
            'IQR_Mean': mean_outlier_iqr,
            'ZScore_Min': min_outlier_zscore,
            'ZScore_Max': max_outlier_zscore,
            'ZScore_Mean': mean_outlier_zscore,
            'IQR_Indices': outlier_indices_iqr,
            'ZScore_Indices': outlier_indices_zscore
        })
    print("=" * 60)
    print("RÉSULTATS")
    print("=" * 60)
    for result in results:
        print(f"\n{result['Variable']}:")
        print(f"  IQR: {result['IQR_Count']} outliers ({result['IQR_Pct']}%)")
        print(f"  Z-score: {result['ZScore_Count']} outliers ({result['ZScore_Pct']}%)")
    output_path = BASE_DIR / "data" / "stats" / "outliers_analysis.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("Figure : Détection des outliers - Analyse détaillée\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"Variable: {result['Variable']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Méthode IQR (Q1 - 1.5×IQR, Q3 + 1.5×IQR):\n")
            f.write(f"  Nombre d'outliers: {result['IQR_Count']}\n")
            f.write(f"  Pourcentage: {result['IQR_Pct']}%\n")
            if result['IQR_Count'] > 0:
                f.write(f"  Valeur min: {result['IQR_Min']:.2f}\n")
                f.write(f"  Valeur max: {result['IQR_Max']:.2f}\n")
                f.write(f"  Valeur moyenne: {result['IQR_Mean']:.2f}\n")
                if len(result['IQR_Indices']) > 0:
                    f.write(f"  Exemples d'indices (max 10): {result['IQR_Indices']}\n")
            f.write("\n")
            f.write(f"Méthode Z-score (|z| > 3):\n")
            f.write(f"  Nombre d'outliers: {result['ZScore_Count']}\n")
            f.write(f"  Pourcentage: {result['ZScore_Pct']}%\n")
            if result['ZScore_Count'] > 0:
                f.write(f"  Valeur min: {result['ZScore_Min']:.2f}\n")
                f.write(f"  Valeur max: {result['ZScore_Max']:.2f}\n")
                f.write(f"  Valeur moyenne: {result['ZScore_Mean']:.2f}\n")
                if len(result['ZScore_Indices']) > 0:
                    f.write(f"  Exemples d'indices (max 10): {result['ZScore_Indices']}\n")
            f.write("\n")
            f.write("=" * 80 + "\n\n")
        total_iqr = sum(r['IQR_Count'] for r in results)
        total_zscore = sum(r['ZScore_Count'] for r in results)
        f.write("RÉSUMÉ GLOBAL\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total d'outliers détectés (méthode IQR): {total_iqr}\n")
        f.write(f"Total d'outliers détectés (méthode Z-score): {total_zscore}\n")
        f.write(f"Nombre de variables analysées: {len(results)}\n")
    
    print(f"\n[OK] Analyse sauvegardée: {output_path}")
    
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    total_iqr = sum(r['IQR_Count'] for r in results)
    total_zscore = sum(r['ZScore_Count'] for r in results)
    print(f"Total d'outliers détectés (méthode IQR): {total_iqr}")
    print(f"Total d'outliers détectés (méthode Z-score): {total_zscore}")
    print(f"Nombre de variables analysées: {len(results)}")
    print()


if __name__ == "__main__":
    analyze_outliers()

