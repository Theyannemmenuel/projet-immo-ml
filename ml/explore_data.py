# ml/explore_data.py
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ─── CHEMINS ────────────────────────────────────────────────────────────────
input_path = os.path.join(os.path.dirname(__file__), 'data', 'DF.csv')
output_path = os.path.join(os.path.dirname(__file__), 'data', 'dvf_toulouse_clean.csv')
figures_path = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(figures_path, exist_ok=True)

# ─── CHARGEMENT ─────────────────────────────────────────────────────────────
print(f"Lecture de : {input_path}")
df = pd.read_csv(input_path, sep=',', low_memory=False, dtype=str)
print(f"Dataset brut : {len(df)} lignes, {len(df.columns)} colonnes")

# ─── NETTOYAGE ───────────────────────────────────────────────────────────────
# Garder uniquement appartements et maisons
df = df[df['type_local'].isin(['Appartement', 'Maison'])].copy()
print(f"Après filtre type_local : {len(df)} lignes")

# Conversion colonnes numériques
cols_numeriques = ['valeur_fonciere', 'surface_reelle_bati',
                   'nombre_pieces_principales', 'surface_terrain']
for col in cols_numeriques:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(',', '.', regex=False),
        errors='coerce'
    )

# Suppression valeurs aberrantes
df = df[df['valeur_fonciere'] > 10000]
df = df[df['valeur_fonciere'] < 3000000]
df = df[df['surface_reelle_bati'] > 9]
df = df[df['surface_reelle_bati'] < 500]

# Drop NaN sur colonnes essentielles
cols_essentielles = ['valeur_fonciere', 'surface_reelle_bati', 'nombre_pieces_principales']
df = df.dropna(subset=cols_essentielles)

print(f"Après nettoyage : {len(df)} lignes")

# ─── EXPORT ──────────────────────────────────────────────────────────────────
df.to_csv(output_path, index=False)
print(f"Dataset propre exporté : {output_path}")

# ─── STATS ───────────────────────────────────────────────────────────────────
print("\n=== STATISTIQUES ===")
print(df[cols_essentielles].describe().round(0))

# ─── GRAPHIQUE 1 : Distribution des prix ─────────────────────────────────────
plt.figure(figsize=(9, 5))
plt.hist(df['valeur_fonciere'] / 1000, bins=50, color='steelblue', edgecolor='none', alpha=0.85)
plt.xlabel('Prix de vente (k€)', fontsize=12)
plt.ylabel('Nombre de transactions', fontsize=12)
plt.title('Distribution des prix immobiliers — Toulouse', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(figures_path, 'distribution_prix.png'), dpi=150)
plt.close()
print("Graphique 1 : distribution_prix.png")

# ─── GRAPHIQUE 2 : Prix vs Surface ───────────────────────────────────────────
plt.figure(figsize=(9, 5))
plt.scatter(df['surface_reelle_bati'], df['valeur_fonciere'] / 1000,
            alpha=0.2, s=8, color='steelblue')
plt.xlabel('Surface (m²)', fontsize=12)
plt.ylabel('Prix (k€)', fontsize=12)
plt.title('Prix vs Surface — Toulouse', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(figures_path, 'prix_vs_surface.png'), dpi=150)
plt.close()
print("Graphique 2 : prix_vs_surface.png")

print("\nExploration terminée. Vérifie ml/figures/ pour les graphiques.")
