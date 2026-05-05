import pandas as pd

# Chargement avec gestion des types pour éviter les erreurs
df = pd.read_csv('ml/data/DF.csv', low_memory=False, sep=',')

# Filtrage sur Toulouse (Code commune 31555)
# Note : Adapte le nom de la colonne si nécessaire (souvent 'code_commune' ou 'Code commune')
df_toulouse = df[df['code_commune'] == 31555].copy()

# Sélection des colonnes utiles pour le Machine Learning
colonnes_cles = [
    'valeur_fonciere', 'surface_reelle_bati', 
    'nombre_pieces_principales', 'surface_terrain', 
    'latitude', 'longitude'
]
df_final = df_toulouse[colonnes_cles].dropna()

# Sauvegarde du dataset prêt pour l'entraînement
df_final.to_csv('ml/data/dvf_toulouse_clean.csv', index=False)
print(f"Extraction terminée : {len(df_final)} ventes valides à Toulouse.")
