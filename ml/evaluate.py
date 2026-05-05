# ml/evaluate.py
import os
import joblib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Créer le dossier figures si besoin
os.makedirs('ml/figures', exist_ok=True)

# 1. Chargement du modèle et des données test
print("Chargement du modèle et des données...")
pipeline = joblib.load('ml/model.pkl')
X_test = np.load('ml/X_test.npy')
y_test = np.load('ml/y_test.npy')
feature_names = np.load('ml/feature_names.npy', allow_pickle=True)

# 2. Prédictions
y_pred = pipeline.predict(X_test)

# 3. Calcul des métriques
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n===== RÉSULTATS DU MODÈLE =====")
print(f"R²   : {r2:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"MAE  : {mae:.4f}")
print(f"MSE  : {mse:.4f}")
print("================================\n")

# 4. Sauvegarde des métriques
with open('ml/metrics.txt', 'w') as f:
    f.write("===== RÉSULTATS DU MODÈLE =====\n")
    f.write(f"R²   : {r2:.4f}\n")
    f.write(f"RMSE : {rmse:.4f}\n")
    f.write(f"MAE  : {mae:.4f}\n")
    f.write(f"MSE  : {mse:.4f}\n")
print("Métriques sauvegardées : ml/metrics.txt")

# 5. Graphique 1 : Valeurs réelles vs prédites
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.3, color='steelblue', edgecolors='none', s=10)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
         'r--', linewidth=2, label='Prédiction parfaite')
plt.xlabel('Prix réels (x$100k)', fontsize=12)
plt.ylabel('Prix prédits (x$100k)', fontsize=12)
plt.title(f'Valeurs réelles vs Prédites — R² = {r2:.3f}', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('ml/figures/real_vs_predicted.png', dpi=150)
plt.close()
print("Graphique 1 sauvegardé : ml/figures/real_vs_predicted.png")

# 6. Graphique 2 : Feature importances
model = pipeline.named_steps['model']
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(9, 5))
plt.bar(range(len(feature_names)), importances[indices], color='steelblue')
plt.xticks(range(len(feature_names)), feature_names[indices], rotation=30, ha='right')
plt.xlabel('Features', fontsize=12)
plt.ylabel("Importance", fontsize=12)
plt.title("Importance des variables dans la prédiction du prix", fontsize=14)
plt.tight_layout()
plt.savefig('ml/figures/feature_importances.png', dpi=150)
plt.close()
print("Graphique 2 sauvegardé : ml/figures/feature_importances.png")

print("\nÉvaluation terminée. Vérifie ml/figures/ pour les graphiques.")
