#!/usr/bin/env python3
# =============================================================================
# Fichier : back-end/scripts/split_dataset.py
# Rôle    : Diviser le dataset en ensembles train/test stratifiés (80/20),
#           sauvegardés dans data/processed/.
# Projet  : Prédiction du risque de crédit bancaire
# UE      : Outils libres pour le développement logiciel
# Auteur  : Maxime BRONNY - 19009314
# Version : V1
# Cadre   : Master 1 Big Data - Université Paris 8
# =============================================================================
"""Diviser le dataset en ensembles train/test stratifiés (80/20), sauvegardés dans data/processed/."""

import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def split_and_save_dataset(input_file, output_dir, test_size=0.2, random_state=42):
    """Divise le dataset en ensembles d'entraînement et de test, et sauvegarde
    le résultat.

    Le split est stratifié sur loan_status : comme seulement 22 % des
    emprunteurs sont en défaut, un découpage purement aléatoire pourrait
    donner un test set avec une proportion de défauts différente du train,
    ce qui fausserait l'évaluation. La stratification garantit la même
    répartition des classes dans les deux ensembles (vérifiée et affichée).
    Les CSV sont sauvegardés bruts, sans encodage : le prétraitement est fait
    plus tard par le script d'entraînement. Un fichier split_info.txt trace
    les paramètres et les effectifs pour la reproductibilité.

    Args:
        input_file: Chemin du CSV brut (data/raw/credit_risk_dataset.csv).
        output_dir: Répertoire de sortie (data/processed).
        test_size (float): Proportion réservée au test (0.2 = 20 %).
        random_state (int): Graine aléatoire, fixée à 42 pour que le split
            soit identique à chaque exécution.
    """
    input_file = Path(input_file)
    output_dir = Path(output_dir)
    print("=" * 60)
    print("SPLIT STRATIFIÉ DU DATASET")
    print("=" * 60)
    print()
    print(f" Chargement du dataset: {input_file}")
    df = pd.read_csv(input_file)
    print(f"[OK] Dataset chargé: {df.shape[0]} lignes, {df.shape[1]} colonnes\n")
    if 'loan_status' not in df.columns:
        print("[ERROR] Erreur: Colonne 'loan_status' non trouvée!")
        return
    print("Distribution de la variable cible (loan_status):")
    target_counts = df['loan_status'].value_counts()
    for label, count in target_counts.items():
        pct = 100 * count / len(df)
        print(f"  Classe {label}: {count} ({pct:.2f}%)")
    print()
    print(f"  Split stratifié (train: {100*(1-test_size):.0f}%, test: {100*test_size:.0f}%)...")
    
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df['loan_status']
    )
    
    print(f"[OK] Train set: {len(train_df)} échantillons")
    print(f"[OK] Test set:  {len(test_df)} échantillons\n")
    print("Vérification de la stratification:")
    print("\nDistribution dans le train set:")
    train_counts = train_df['loan_status'].value_counts()
    for label, count in train_counts.items():
        pct = 100 * count / len(train_df)
        print(f"  Classe {label}: {count} ({pct:.2f}%)")
    
    print("\nDistribution dans le test set:")
    test_counts = test_df['loan_status'].value_counts()
    for label, count in test_counts.items():
        pct = 100 * count / len(test_df)
        print(f"  Classe {label}: {count} ({pct:.2f}%)")
    print()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    train_file = output_path / "train.csv"
    test_file = output_path / "test.csv"
    
    print("[INFO] Sauvegarde des fichiers...")
    train_df.to_csv(train_file, index=False)
    test_df.to_csv(test_file, index=False)
    
    print(f"[OK] Train set sauvegardé: {train_file}")
    print(f"[OK] Test set sauvegardé:  {test_file}")
    print()
    metadata_file = output_path / "split_info.txt"
    with open(metadata_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("INFORMATIONS SUR LE SPLIT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Fichier d'origine: {input_file}\n")
        f.write(f"Date de création: {pd.Timestamp.now()}\n")
        f.write(f"Random state: {random_state}\n")
        f.write(f"Test size: {test_size}\n\n")
        f.write(f"Nombre total d'échantillons: {len(df)}\n")
        f.write(f"Train set: {len(train_df)} ({100*len(train_df)/len(df):.2f}%)\n")
        f.write(f"Test set: {len(test_df)} ({100*len(test_df)/len(df):.2f}%)\n\n")
        f.write("Distribution des classes (dataset complet):\n")
        for label, count in target_counts.items():
            f.write(f"  Classe {label}: {count} ({100*count/len(df):.2f}%)\n")
        f.write("\nDistribution des classes (train set):\n")
        for label, count in train_counts.items():
            f.write(f"  Classe {label}: {count} ({100*count/len(train_df):.2f}%)\n")
        f.write("\nDistribution des classes (test set):\n")
        for label, count in test_counts.items():
            f.write(f"  Classe {label}: {count} ({100*count/len(test_df):.2f}%)\n")
    
    print(f"[OK] Métadonnées sauvegardées: {metadata_file}")
    print()
    
    print("=" * 60)
    print("[OK] SPLIT TERMINÉ")
    print("=" * 60)
    print("\nVous pouvez maintenant utiliser ces fichiers avec le pipeline Python:")
    print("  - make train")
    print()


def main():
    """Orchestre le split : charge data/raw/credit_risk_dataset.csv, sauvegarde dans data/processed.

    Prérequis : credit_risk_dataset.csv dans back-end/data/raw/.
    """
    input_file = BASE_DIR / "data" / "raw" / "credit_risk_dataset.csv"
    output_dir = BASE_DIR / "data" / "processed"
    test_size = 0.2
    random_state = 42
    if not Path(input_file).exists():
        print(f"[ERROR] Erreur: Fichier {input_file} non trouvé!")
        print("   Assurez-vous que le dataset est dans back-end/data/raw/")
        return
    split_and_save_dataset(input_file, output_dir, test_size, random_state)


if __name__ == "__main__":
    main()

