from sklearn.datasets import fetch_california_housing
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Chargement du dataset California Housing
# Ce dataset contient 20 640 échantillons avec 8 variables explicatives.
data = fetch_california_housing()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['MedHouseVal'] = data.target # Variable cible : prix médian des maisons[cite: 1]

# 2. Exploration technique des données
# Affichage des informations structurelles et statistiques.
print("--- Structure des données (info) ---")
print(df.info()) 
print("\n--- Statistiques descriptives ---")
print(df.describe()) 
print("\n--- Vérification des valeurs nulles ---")
print(df.isnull().sum()) 

# 3. Génération de la matrice de corrélation
# On mesure la dépendance linéaire entre les variables et le prix[cite: 1].
plt.figure(figsize=(12, 8))
correlation = df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Matrice de Corrélation - California Housing")

# 4. Sauvegarde des livrables visuels
# Les graphiques doivent être exportés en PNG pour le rapport final.
output_path = 'ml/figures/correlation_matrix.png'
plt.savefig(output_path)
print(f"\n[SUCCÈS] Graphique sauvegardé : {output_path}")
