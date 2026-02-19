#!/usr/bin/env python3
"""
/*****************************************************************************************************

Nom : scripts/plot_results.py

Rôle : Script de visualisation des résultats du modèle (génération de graphiques)

Auteur : Maxime BRONNY

Version : V1

Licence : Réalisé dans le cadre du cours Technique d'intelligence artificiel M1 INFORMATIQUE BIG-DATA

Usage :

    Pour compiler : N/A (script Python)

    Pour executer : python3 scripts/plot_results.py

******************************************************************************************************/

Prérequis : make train (génère results/metrics/*.txt et results/plots/data/*.csv).
Structure attendue : results/metrics/logistic_regression/, decision_tree/,
results/plots/data/ (fichiers ROC, cost curve).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3


def plot_lr_python_confusion_matrix():
    """Génère la matrice de confusion LR depuis lr_python_test_confusion_matrix.txt.

    Parse le format "TN: X, FP: Y" / "FN: X, TP: Y". Sauvegarde PNG dans
    results/plots/logistic_regression/.

    Returns:
        True si succès, False si fichier absent.
    """
    print(" Génération de la matrice de confusion (Régression Logistique Python)...")
    
    try:
        with open(str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_confusion_matrix.txt"), 'r') as f:
            lines = f.readlines()
            
        tn = fp = fn = tp = 0
        for line in lines:
            if "TN:" in line:
                parts = line.split(',')
                tn = int(parts[0].split(':')[1].strip())
                fp = int(parts[1].split(':')[1].strip())
            elif "FN:" in line:
                parts = line.split(',')
                fn = int(parts[0].split(':')[1].strip())
                tp = int(parts[1].split(':')[1].strip())
        
        cm = np.array([[tn, fp], [fn, tp]])
        
        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(cm, interpolation='nearest', cmap='Blues', aspect='auto')
        
        thresh = cm.max() / 2.
        for i in range(2):
            for j in range(2):
                ax.text(j, i, format(cm[i, j], 'd'),
                       ha="center", va="center",
                       color="white" if cm[i, j] > thresh else "black",
                       fontweight='bold', fontsize=14)
        
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Prédit: Pas de défaut', 'Prédit: Défaut'])
        ax.set_yticklabels(['Réel: Pas de défaut', 'Réel: Défaut'])
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Nombre de prédictions', rotation=270, labelpad=20)
        
        ax.set_title('Matrice de Confusion - Régression Logistique (Python) - Test Set', 
                    fontsize=14, fontweight='bold', pad=20)
        
        total = cm.sum()
        for i in range(2):
            for j in range(2):
                pct = 100 * cm[i, j] / total
                ax.text(j, i+0.3, f'({pct:.1f}%)', 
                       ha='center', va='center', color='gray', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(str(BASE_DIR / "results" / "plots" / "logistic_regression" / "lr_python_confusion_matrix_test.png"), dpi=300)
        print("[OK] Graphique sauvegardé: results/plots/logistic_regression/lr_python_confusion_matrix_test.png")
        
        return True
    except FileNotFoundError:
        print("[WARNING] Fichier lr_python_test_confusion_matrix.txt non trouvé")
        return False


def plot_dt_python_confusion_matrix():
    """Génère la matrice de confusion DT depuis dt_python_test_confusion_matrix.txt."""
    print(" Génération de la matrice de confusion (Arbre de Décision Python)...")
    
    try:
        with open(str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_confusion_matrix.txt"), 'r') as f:
            lines = f.readlines()
            
        tn = fp = fn = tp = 0
        for line in lines:
            if "TN:" in line:
                parts = line.split(',')
                tn = int(parts[0].split(':')[1].strip())
                fp = int(parts[1].split(':')[1].strip())
            elif "FN:" in line:
                parts = line.split(',')
                fn = int(parts[0].split(':')[1].strip())
                tp = int(parts[1].split(':')[1].strip())
        
        cm = np.array([[tn, fp], [fn, tp]])
        
        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(cm, interpolation='nearest', cmap='Blues', aspect='auto')
        
        thresh = cm.max() / 2.
        for i in range(2):
            for j in range(2):
                ax.text(j, i, format(cm[i, j], 'd'),
                       ha="center", va="center",
                       color="white" if cm[i, j] > thresh else "black",
                       fontweight='bold', fontsize=14)
        
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['Prédit: Pas de défaut', 'Prédit: Défaut'])
        ax.set_yticklabels(['Réel: Pas de défaut', 'Réel: Défaut'])
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Nombre de prédictions', rotation=270, labelpad=20)
        
        ax.set_title('Matrice de Confusion - Arbre de Décision (Python) - Test Set', 
                    fontsize=14, fontweight='bold', pad=20)
        
        total = cm.sum()
        for i in range(2):
            for j in range(2):
                pct = 100 * cm[i, j] / total
                ax.text(j, i+0.3, f'({pct:.1f}%)', 
                       ha='center', va='center', color='gray', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(str(BASE_DIR / "results" / "plots" / "decision_tree" / "dt_python_confusion_matrix_test.png"), dpi=300)
        print("[OK] Graphique sauvegardé: results/plots/decision_tree/dt_python_confusion_matrix_test.png")
        
        return True
    except FileNotFoundError:
        print("[WARNING] Fichier dt_python_test_confusion_matrix.txt non trouvé")
        return False

def plot_lr_python_metrics_train_vs_test():
    """Compare métriques train vs test pour LR (barres groupées)."""
    print("\n Génération du graphique de comparaison train vs test (Régression Logistique Python)...")
    
    try:
        train_metrics = {}
        with open(str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_train_metrics.txt"), 'r') as f:
            for line in f:
                if "Accuracy" in line:
                    train_metrics['Accuracy'] = float(line.split(':')[1].strip())
                elif "Precision" in line:
                    train_metrics['Precision'] = float(line.split(':')[1].strip())
                elif "Recall" in line:
                    train_metrics['Recall'] = float(line.split(':')[1].strip())
                elif "F1-Score" in line:
                    train_metrics['F1-Score'] = float(line.split(':')[1].strip())
        
        test_metrics = {}
        with open(str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_metrics.txt"), 'r') as f:
            for line in f:
                if "Accuracy" in line:
                    test_metrics['Accuracy'] = float(line.split(':')[1].strip())
                elif "Precision" in line:
                    test_metrics['Precision'] = float(line.split(':')[1].strip())
                elif "Recall" in line:
                    test_metrics['Recall'] = float(line.split(':')[1].strip())
                elif "F1-Score" in line:
                    test_metrics['F1-Score'] = float(line.split(':')[1].strip())
        
        # Créer le graphique
        metrics_names = list(train_metrics.keys())
        train_values = list(train_metrics.values())
        test_values = list(test_metrics.values())
        
        x = np.arange(len(metrics_names))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars1 = ax.bar(x - width/2, train_values, width, label='Train', color='#3498db')
        bars2 = ax.bar(x + width/2, test_values, width, label='Test', color='#e74c3c')
        
        ax.set_xlabel('Métriques', fontweight='bold')
        ax.set_ylabel('Score', fontweight='bold')
        ax.set_title('Régression Logistique (Python) - Comparaison Train vs Test', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics_names)
        ax.legend()
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        
        # Ajouter les valeurs sur les barres
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(str(BASE_DIR / "results" / "plots" / "logistic_regression" / "lr_python_metrics_train_vs_test.png"), dpi=300)
        print("[OK] Graphique sauvegardé: results/plots/logistic_regression/lr_python_metrics_train_vs_test.png")
        
        return True
    except FileNotFoundError as e:
        print(f"[WARNING] Fichier de métriques non trouvé: {e}")
        return False

def plot_dt_python_metrics_train_vs_test():
    """Compare métriques train vs test pour DT (barres groupées)."""
    print("\n Génération du graphique de comparaison train vs test (Arbre de Décision Python)...")
    
    try:
        train_metrics = {}
        with open(str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_train_metrics.txt"), 'r') as f:
            for line in f:
                if "Accuracy" in line:
                    train_metrics['Accuracy'] = float(line.split(':')[1].strip())
                elif "Precision" in line:
                    train_metrics['Precision'] = float(line.split(':')[1].strip())
                elif "Recall" in line:
                    train_metrics['Recall'] = float(line.split(':')[1].strip())
                elif "F1-Score" in line:
                    train_metrics['F1-Score'] = float(line.split(':')[1].strip())
        
        test_metrics = {}
        with open(str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_metrics.txt"), 'r') as f:
            for line in f:
                if "Accuracy" in line:
                    test_metrics['Accuracy'] = float(line.split(':')[1].strip())
                elif "Precision" in line:
                    test_metrics['Precision'] = float(line.split(':')[1].strip())
                elif "Recall" in line:
                    test_metrics['Recall'] = float(line.split(':')[1].strip())
                elif "F1-Score" in line:
                    test_metrics['F1-Score'] = float(line.split(':')[1].strip())
        
        # Créer le graphique
        metrics_names = list(train_metrics.keys())
        train_values = list(train_metrics.values())
        test_values = list(test_metrics.values())
        
        x = np.arange(len(metrics_names))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars1 = ax.bar(x - width/2, train_values, width, label='Train', color='#3498db')
        bars2 = ax.bar(x + width/2, test_values, width, label='Test', color='#e74c3c')
        
        ax.set_xlabel('Métriques', fontweight='bold')
        ax.set_ylabel('Score', fontweight='bold')
        ax.set_title('Arbre de Décision (Python) - Comparaison Train vs Test', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics_names)
        ax.legend()
        ax.set_ylim([0, 1.1])
        ax.grid(axis='y', alpha=0.3)
        
        # Ajouter les valeurs sur les barres
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(str(BASE_DIR / "results" / "plots" / "decision_tree" / "dt_python_metrics_train_vs_test.png"), dpi=300)
        print("[OK] Graphique sauvegardé: results/plots/decision_tree/dt_python_metrics_train_vs_test.png")
        
        return True
    except FileNotFoundError as e:
        print(f"[WARNING] Fichier de métriques non trouvé: {e}")
        return False

def plot_lr_python_cost_curve():
    """Trace la courbe de coût LR depuis lr_python_cost_curve.csv."""
    print("\n Génération de la courbe de coût (Régression Logistique Python)...")
    
    cost_file = BASE_DIR / "results" / "plots" / "data" / "lr_python_cost_curve.csv"
    if not cost_file.exists():
        print(f"[WARNING] Fichier {cost_file} non trouvé")
        return False
    
    try:
        df = pd.read_csv(cost_file)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(df['iteration'], df['cost'], marker='o', linewidth=2, 
               markersize=6, color='#3498db', label='Coût (Cross-Entropy)')
        
        ax.set_xlabel('Itérations', fontweight='bold', fontsize=12)
        ax.set_ylabel('Coût (Cross-Entropy Loss)', fontweight='bold', fontsize=12)
        ax.set_title('Courbe de Coût - Régression Logistique (Python) - Entraînement', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        final_cost = df['cost'].iloc[-1]
        ax.axhline(y=final_cost, color='green', linestyle='--', 
                  alpha=0.5, label=f'Coût final: {final_cost:.4f}')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig(str(BASE_DIR / "results" / "plots" / "logistic_regression" / "lr_python_cost_curve_training.png"), dpi=300)
        print("[OK] Graphique sauvegardé: results/plots/logistic_regression/lr_python_cost_curve_training.png")
        
        return True
    except Exception as e:
        print(f"[WARNING] Erreur lors de la création de la courbe de coût: {e}")
        return False

def plot_python_roc_curves():
    print("\n Génération des courbes ROC (Python)...")
    
    lr_roc_file = BASE_DIR / "results" / "plots" / "data" / "lr_python_roc_data.csv"
    dt_roc_file = BASE_DIR / "results" / "plots" / "data" / "dt_python_roc_data.csv"
    
    if not lr_roc_file.exists() or not dt_roc_file.exists():
        print("[WARNING] Fichiers ROC Python non trouvés")
        return False
    
    try:
        lr_roc = pd.read_csv(lr_roc_file)
        dt_roc = pd.read_csv(dt_roc_file)
        
        lr_auc = 0.0
        dt_auc = 0.0
        
        try:
            with open(str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_metrics.txt"), 'r') as f:
                for line in f:
                    if "AUC-ROC" in line:
                        lr_auc = float(line.split(':')[1].strip())
        except:
            pass
        
        try:
            with open(str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_metrics.txt"), 'r') as f:
                for line in f:
                    if "AUC-ROC" in line:
                        dt_auc = float(line.split(':')[1].strip())
        except:
            pass
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        ax.plot([0, 1], [0, 1], 'k--', linewidth=1.5, alpha=0.5, label='AUC = 0.5 (aléatoire)')
        ax.plot(lr_roc['fpr'], lr_roc['tpr'], linewidth=2.5, 
               color='#3498db', label=f'Régression Logistique (AUC = {lr_auc:.4f})')
        ax.plot(dt_roc['fpr'], dt_roc['tpr'], linewidth=2.5, 
               color='#e74c3c', label=f'Arbre de Décision (AUC = {dt_auc:.4f})')
        
        ax.set_xlabel('Taux de Faux Positifs (FPR)', fontweight='bold', fontsize=12)
        ax.set_ylabel('Taux de Vrais Positifs (TPR)', fontweight='bold', fontsize=12)
        ax.set_title('Courbes ROC - LR vs DT (Python)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='lower right', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        
        plt.tight_layout()
        plt.savefig(str(BASE_DIR / "results" / "plots" / "logistic_regression" / "lr_dt_python_roc_curves_comparison.png"), dpi=300)
        print("[OK] Graphique sauvegardé: results/plots/logistic_regression/lr_dt_python_roc_curves_comparison.png")
        
        return True
    except Exception as e:
        print(f"[WARNING] Erreur lors de la création des courbes ROC Python: {e}")
        return False

def load_metrics(train_file, test_file):
    """Parse les fichiers métriques (format key: value) et retourne deux dicts."""
    train_metrics = {}
    test_metrics = {}
    
    def parse_metrics(file_path, metrics_dict):
        try:
            if file_path and Path(file_path).exists():
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if "Accuracy" in line and ":" in line:
                            metrics_dict['Accuracy'] = float(line.split(':')[1].strip())
                        elif "Precision" in line and ":" in line:
                            metrics_dict['Precision'] = float(line.split(':')[1].strip())
                        elif "Recall" in line and ":" in line:
                            metrics_dict['Recall'] = float(line.split(':')[1].strip())
                        elif "F1-Score" in line and ":" in line:
                            metrics_dict['F1-Score'] = float(line.split(':')[1].strip())
                        elif "AUC-ROC" in line and ":" in line:
                            metrics_dict['AUC-ROC'] = float(line.split(':')[1].strip())
        except:
            pass
    
    parse_metrics(train_file, train_metrics)
    parse_metrics(test_file, test_metrics)
    
    return train_metrics, test_metrics

def load_confusion_matrix(file_path):
    """Parse TN, FP, FN, TP depuis un fichier texte. Retourne np.array 2x2 ou None."""
    try:
        if not Path(file_path).exists():
            return None
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        tn = fp = fn = tp = 0
        for line in lines:
            if "TN:" in line:
                parts = line.split(',')
                tn = int(parts[0].split(':')[1].strip())
                fp = int(parts[1].split(':')[1].strip())
            elif "FN:" in line:
                parts = line.split(',')
                fn = int(parts[0].split(':')[1].strip())
                tp = int(parts[1].split(':')[1].strip())
        
        return np.array([[tn, fp], [fn, tp]])
    except:
        return None

def plot_confusion_matrix_ax(ax, cm, title):
    """Dessine une heatmap de confusion sur l'axe matplotlib donné."""
    if cm is None:
        ax.text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
        return
    
    im = ax.imshow(cm, interpolation='nearest', cmap='Blues', aspect='auto')
    thresh = cm.max() / 2.
    for i in range(2):
        for j in range(2):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black",
                   fontweight='bold', fontsize=10)
    
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['Pas de défaut', 'Défaut'])
    ax.set_yticklabels(['Pas de défaut', 'Défaut'])
    ax.set_title(title, fontweight='bold', fontsize=10)
    ax.set_xlabel('Prédiction')
    ax.set_ylabel('Réalité')

def create_summary_figure():
    """Crée une figure récapitulative (métriques, ROC, matrices de confusion LR et DT)."""
    print("\n Génération de la figure récapitulative générale...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3)
    
    # Charger les métriques Python uniquement
    lr_python_train, lr_python_test = load_metrics(
        str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_train_metrics.txt"),
        str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_metrics.txt")
    )
    dt_python_train, dt_python_test = load_metrics(
        str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_train_metrics.txt"),
        str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_metrics.txt")
    )
    
    # Graphique 1: Comparaison des 2 modèles (Accuracy, Precision, Recall, F1, AUC-ROC)
    ax1 = fig.add_subplot(gs[0, 0])
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    x = np.arange(len(metrics))
    width = 0.35
    
    lr_python_vals = [lr_python_test.get(m, 0) for m in metrics]
    dt_python_vals = [dt_python_test.get(m, 0) for m in metrics]
    
    ax1.bar(x - width/2, lr_python_vals, width, label='LR Python', color='#3498db')
    ax1.bar(x + width/2, dt_python_vals, width, label='DT Python', color='#e74c3c')
    
    ax1.set_xlabel('Métriques')
    ax1.set_ylabel('Score')
    ax1.set_title('Comparaison des Modèles - Métriques Test', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics, rotation=45, ha='right')
    ax1.set_ylim([0, 1.1])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Graphique 2: Comparaison Train vs Test (Accuracy)
    ax2 = fig.add_subplot(gs[0, 1])
    models = ['LR Python', 'DT Python']
    train_acc = [
        lr_python_train.get('Accuracy', 0),
        dt_python_train.get('Accuracy', 0)
    ]
    test_acc = [
        lr_python_test.get('Accuracy', 0),
        dt_python_test.get('Accuracy', 0)
    ]
    
    x = np.arange(len(models))
    width = 0.35
    ax2.bar(x - width/2, train_acc, width, label='Train', color='#3498db')
    ax2.bar(x + width/2, test_acc, width, label='Test', color='#e74c3c')
    ax2.set_xlabel('Modèles')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Train vs Test - Accuracy', fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, rotation=45, ha='right')
    ax2.set_ylim([0, 1.1])
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # Matrices de confusion (ligne 1-2)
    cm_lr_python = load_confusion_matrix(str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_confusion_matrix.txt"))
    cm_dt_python = load_confusion_matrix(str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_confusion_matrix.txt"))
    
    ax3 = fig.add_subplot(gs[0, 2])
    plot_confusion_matrix_ax(ax3, cm_lr_python, 'LR Python - Test')
    
    ax4 = fig.add_subplot(gs[1, 0])
    plot_confusion_matrix_ax(ax4, cm_dt_python, 'DT Python - Test')
    
    # Tableau récapitulatif (ligne 2)
    ax5 = fig.add_subplot(gs[1, 1:])
    ax5.axis('off')
    
    # Créer le tableau
    table_data = []
    table_data.append(['Modèle', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC'])
    table_data.append(['LR Python (Test)',
                      f"{lr_python_test.get('Accuracy', 0):.4f}",
                      f"{lr_python_test.get('Precision', 0):.4f}",
                      f"{lr_python_test.get('Recall', 0):.4f}",
                      f"{lr_python_test.get('F1-Score', 0):.4f}",
                      f"{lr_python_test.get('AUC-ROC', 0):.4f}"])
    table_data.append(['DT Python (Test)',
                      f"{dt_python_test.get('Accuracy', 0):.4f}",
                      f"{dt_python_test.get('Precision', 0):.4f}",
                      f"{dt_python_test.get('Recall', 0):.4f}",
                      f"{dt_python_test.get('F1-Score', 0):.4f}",
                      f"{dt_python_test.get('AUC-ROC', 0):.4f}"])
    
    table = ax5.table(cellText=table_data[1:], colLabels=table_data[0],
                     cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style du tableau
    for i in range(len(table_data[0])):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax5.set_title('Tableau Récapitulatif - Métriques de Test', fontweight='bold', fontsize=12, pad=20)
    
    plt.suptitle('Vue d\'Ensemble - Modèles Python (scikit-learn)', 
                fontsize=18, fontweight='bold', y=0.995)
    
    plt.savefig(str(BASE_DIR / "results" / "plots" / "summary_figure.png"), dpi=300, bbox_inches='tight')
    print("[OK] Figure récapitulative sauvegardée: results/plots/summary_figure.png")

def create_lr_python_summary():
    """Figure récapitulative LR : métriques, courbe coût, ROC, matrice de confusion."""
    print("\n Génération du résumé LR Python...")
    
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3)
    
    # Charger les métriques
    train_metrics, test_metrics = load_metrics(
        str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_train_metrics.txt"),
        str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_metrics.txt")
    )
    
    # Graphique 1: Métriques train vs test (barres groupées)
    ax1 = fig.add_subplot(gs[0, 0])
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    x = np.arange(len(metrics))
    width = 0.35
    
    train_vals = [train_metrics.get(m, 0) for m in metrics]
    test_vals = [test_metrics.get(m, 0) for m in metrics]
    
    ax1.bar(x - width/2, train_vals, width, label='Train', color='#3498db')
    ax1.bar(x + width/2, test_vals, width, label='Test', color='#e74c3c')
    ax1.set_xlabel('Métriques')
    ax1.set_ylabel('Score')
    ax1.set_title('Métriques Train vs Test', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics, rotation=45, ha='right')
    ax1.set_ylim([0, 1.1])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Graphique 2: Matrice de confusion
    ax2 = fig.add_subplot(gs[0, 1])
    cm = load_confusion_matrix(str(BASE_DIR / "results" / "metrics" / "logistic_regression" / "lr_python_test_confusion_matrix.txt"))
    plot_confusion_matrix_ax(ax2, cm, 'Matrice de Confusion - Test')
    
    # Graphique 3: Courbe de convergence
    ax3 = fig.add_subplot(gs[0, 2])
    try:
        cost_file = BASE_DIR / "results" / "plots" / "data" / "lr_python_cost_curve.csv"
        if cost_file.exists():
            df = pd.read_csv(cost_file)
            ax3.plot(df['iteration'], df['cost'], marker='o', linewidth=2, 
                    markersize=3, color='#e74c3c')
            ax3.set_xlabel('Itérations', fontweight='bold')
            ax3.set_ylabel('Coût (Cross-Entropy Loss)', fontweight='bold')
            ax3.set_title('Convergence - Courbe de Coût', fontweight='bold')
            ax3.grid(True, alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
    except:
        ax3.text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
    
    # Graphique 4: Comparaison train vs test (lignes)
    ax4 = fig.add_subplot(gs[1, 0])
    metrics_full = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    train_vals_full = [train_metrics.get(m, 0) for m in metrics_full]
    test_vals_full = [test_metrics.get(m, 0) for m in metrics_full]
    
    x_pos = np.arange(len(metrics_full))
    ax4.plot(x_pos, train_vals_full, marker='o', linewidth=2, 
            markersize=8, label='Train', color='#3498db')
    ax4.plot(x_pos, test_vals_full, marker='s', linewidth=2, 
            markersize=8, label='Test', color='#e74c3c')
    ax4.set_xlabel('Métriques')
    ax4.set_ylabel('Score')
    ax4.set_title('Évolution Train vs Test', fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(metrics_full, rotation=45, ha='right')
    ax4.set_ylim([0, 1.1])
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Graphique 5: Courbe ROC
    ax5 = fig.add_subplot(gs[1, 1])
    try:
        roc_file = BASE_DIR / "results" / "plots" / "data" / "lr_python_roc_data.csv"
        if roc_file.exists():
            df_roc = pd.read_csv(roc_file)
            ax5.plot(df_roc['fpr'], df_roc['tpr'], linewidth=2, color='#e74c3c', 
                    label=f'ROC (AUC = {test_metrics.get("AUC-ROC", 0):.3f})')
            ax5.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')
            ax5.set_xlabel('Taux de Faux Positifs', fontweight='bold')
            ax5.set_ylabel('Taux de Vrais Positifs', fontweight='bold')
            ax5.set_title('Courbe ROC', fontweight='bold')
            ax5.legend()
            ax5.grid(True, alpha=0.3)
        else:
            ax5.text(0.5, 0.5, 'Données ROC non disponibles', ha='center', va='center')
    except:
        ax5.text(0.5, 0.5, 'Données ROC non disponibles', ha='center', va='center')
    
    # Graphique 6: Tableau de métriques
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    table_data = []
    table_data.append(['Métrique', 'Train', 'Test'])
    for metric in metrics_full:
        table_data.append([
            metric,
            f"{train_metrics.get(metric, 0):.4f}",
            f"{test_metrics.get(metric, 0):.4f}"
        ])
    
    table = ax6.table(cellText=table_data[1:], colLabels=table_data[0],
                     cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    for i in range(len(table_data[0])):
        table[(0, i)].set_facecolor('#3498db')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax6.set_title('Tableau Récapitulatif', fontweight='bold', fontsize=12, pad=20)
    
    plt.suptitle('Résumé Détaillé - Régression Logistique (Python)', 
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(str(BASE_DIR / "results" / "plots" / "logistic_regression" / "summary_lr_python.png"), dpi=300, bbox_inches='tight')
    print("[OK] Résumé LR Python sauvegardé: results/plots/logistic_regression/summary_lr_python.png")

def create_dt_python_summary():
    """Figure récapitulative DT : métriques, ROC, matrice de confusion."""
    print("\n Génération du résumé DT Python...")
    
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3)
    
    # Charger les métriques
    train_metrics, test_metrics = load_metrics(
        str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_train_metrics.txt"),
        str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_metrics.txt")
    )
    
    # Charger les statistiques de l'arbre
    tree_stats = {}
    try:
        with open(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_tree_stats.txt", 'r') as f:
            for line in f:
                if "Profondeur réelle:" in line:
                    tree_stats['depth'] = line.split(':')[1].strip()
                elif "Nombre total de nœuds:" in line:
                    tree_stats['nodes'] = line.split(':')[1].strip()
                elif "Temps d'entraînement:" in line:
                    tree_stats['time'] = line.split(':')[1].strip()
    except:
        pass
    
    # Graphique 1: Métriques train vs test (barres groupées)
    ax1 = fig.add_subplot(gs[0, 0])
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    x = np.arange(len(metrics))
    width = 0.35
    
    train_vals = [train_metrics.get(m, 0) for m in metrics]
    test_vals = [test_metrics.get(m, 0) for m in metrics]
    
    ax1.bar(x - width/2, train_vals, width, label='Train', color='#f39c12')
    ax1.bar(x + width/2, test_vals, width, label='Test', color='#e74c3c')
    ax1.set_xlabel('Métriques')
    ax1.set_ylabel('Score')
    ax1.set_title('Métriques Train vs Test', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics, rotation=45, ha='right')
    ax1.set_ylim([0, 1.1])
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Graphique 2: Matrice de confusion
    ax2 = fig.add_subplot(gs[0, 1])
    cm = load_confusion_matrix(str(BASE_DIR / "results" / "metrics" / "decision_tree" / "dt_python_test_confusion_matrix.txt"))
    plot_confusion_matrix_ax(ax2, cm, 'Matrice de Confusion - Test')
    
    # Graphique 3: Importance des caractéristiques (si disponible)
    ax3 = fig.add_subplot(gs[0, 2])
    try:
        feature_file = BASE_DIR / "results" / "plots" / "feature_importance.txt"
        if feature_file.exists():
            with open(feature_file, 'r') as f:
                lines = f.readlines()
                features = []
                importances = []
                for line in lines[2:]:  # Skip header
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        features.append(parts[0].strip())
                        importances.append(float(parts[1].strip()))
            
            if features:
                y_pos = np.arange(len(features))
                ax3.barh(y_pos, importances, color='#f39c12')
                ax3.set_yticks(y_pos)
                ax3.set_yticklabels(features)
                ax3.set_xlabel('Importance', fontweight='bold')
                ax3.set_title('Importance des Caractéristiques', fontweight='bold')
                ax3.grid(axis='x', alpha=0.3)
            else:
                ax3.text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
        else:
            ax3.text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
    except:
        ax3.text(0.5, 0.5, 'Données non disponibles', ha='center', va='center')
    
    # Graphique 4: Comparaison train vs test (lignes)
    ax4 = fig.add_subplot(gs[1, 0])
    metrics_full = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC-ROC']
    train_vals_full = [train_metrics.get(m, 0) for m in metrics_full]
    test_vals_full = [test_metrics.get(m, 0) for m in metrics_full]
    
    x_pos = np.arange(len(metrics_full))
    ax4.plot(x_pos, train_vals_full, marker='o', linewidth=2, 
            markersize=8, label='Train', color='#f39c12')
    ax4.plot(x_pos, test_vals_full, marker='s', linewidth=2, 
            markersize=8, label='Test', color='#e74c3c')
    ax4.set_xlabel('Métriques')
    ax4.set_ylabel('Score')
    ax4.set_title('Évolution Train vs Test', fontweight='bold')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(metrics_full, rotation=45, ha='right')
    ax4.set_ylim([0, 1.1])
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # Graphique 5: Courbe ROC
    ax5 = fig.add_subplot(gs[1, 1])
    try:
        roc_file = BASE_DIR / "results" / "plots" / "data" / "dt_python_roc_data.csv"
        if roc_file.exists():
            df_roc = pd.read_csv(roc_file)
            ax5.plot(df_roc['fpr'], df_roc['tpr'], linewidth=2, color='#f39c12', 
                    label=f'ROC (AUC = {test_metrics.get("AUC-ROC", 0):.3f})')
            ax5.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')
            ax5.set_xlabel('Taux de Faux Positifs', fontweight='bold')
            ax5.set_ylabel('Taux de Vrais Positifs', fontweight='bold')
            ax5.set_title('Courbe ROC', fontweight='bold')
            ax5.legend()
            ax5.grid(True, alpha=0.3)
        else:
            ax5.text(0.5, 0.5, 'Données ROC non disponibles', ha='center', va='center')
    except:
        ax5.text(0.5, 0.5, 'Données ROC non disponibles', ha='center', va='center')
    
    # Graphique 6: Statistiques de l'arbre
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    # Tableau avec métriques et statistiques
    table_data = []
    table_data.append(['Métrique', 'Train', 'Test'])
    for metric in metrics_full:
        table_data.append([
            metric,
            f"{train_metrics.get(metric, 0):.4f}",
            f"{test_metrics.get(metric, 0):.4f}"
        ])
    
    table_data.append(['', '', ''])
    table_data.append(['Statistique', 'Valeur', ''])
    table_data.append(['Profondeur réelle', tree_stats.get('depth', 'N/A'), ''])
    table_data.append(['Nombre de nœuds', tree_stats.get('nodes', 'N/A'), ''])
    table_data.append(['Temps d\'entraînement', tree_stats.get('time', 'N/A'), ''])
    
    table = ax6.table(cellText=table_data[1:], colLabels=table_data[0],
                     cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    for i in range(len(table_data[0])):
        table[(0, i)].set_facecolor('#f39c12')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax6.set_title('Tableau Récapitulatif', fontweight='bold', fontsize=12, pad=20)
    
    plt.suptitle('Résumé Détaillé - Arbre de Décision (Python)', 
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(str(BASE_DIR / "results" / "plots" / "decision_tree" / "summary_dt_python.png"), dpi=300, bbox_inches='tight')
    print("[OK] Résumé DT Python sauvegardé: results/plots/decision_tree/summary_dt_python.png")

def main():
    """Orchestre la génération de tous les graphiques (LR, DT, récapitulatifs)."""
    (BASE_DIR / "results" / "plots" / "logistic_regression").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "results" / "plots" / "decision_tree").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "results" / "plots" / "data").mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("VISUALISATION DES RÉSULTATS")
    print("=" * 60 + "\n")
    
    # Générer tous les graphiques (Python uniquement)
    success_count = 0
    
    if plot_lr_python_cost_curve():
        success_count += 1
    
    if plot_lr_python_confusion_matrix():
        success_count += 1
    
    if plot_dt_python_confusion_matrix():
        success_count += 1
    
    if plot_python_roc_curves():
        success_count += 1
    
    if plot_lr_python_metrics_train_vs_test():
        success_count += 1
    
    if plot_dt_python_metrics_train_vs_test():
        success_count += 1
    
    create_summary_figure()
    success_count += 1
    
    create_lr_python_summary()
    success_count += 1
    
    create_dt_python_summary()
    success_count += 1
    
    print("\n" + "=" * 60)
    print(f"[OK] VISUALISATION TERMINÉE ({success_count}/9 graphiques générés)")
    print("=" * 60)
    print("\nFichiers générés:")
    print("  - results/plots/logistic_regression/lr_python_cost_curve_training.png")
    print("  - results/plots/logistic_regression/lr_python_confusion_matrix_test.png")
    print("  - results/plots/decision_tree/dt_python_confusion_matrix_test.png")
    print("  - results/plots/logistic_regression/lr_dt_python_roc_curves_comparison.png")
    print("  - results/plots/logistic_regression/lr_python_metrics_train_vs_test.png")
    print("  - results/plots/decision_tree/dt_python_metrics_train_vs_test.png")
    print("  - results/plots/summary_figure.png")
    print("  - results/plots/logistic_regression/summary_lr_python.png")
    print("  - results/plots/decision_tree/summary_dt_python.png")
    print()


if __name__ == "__main__":
    main()

