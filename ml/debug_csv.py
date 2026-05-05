# ml/debug_csv.py
import pandas as pd

input_path = '/home/ibrax976/projet-immo-ml/ml/data/DF.csv'

df = pd.read_csv(input_path, sep=';', low_memory=False, dtype=str)

print("=== COLONNES DISPONIBLES ===")
print(df.columns.tolist())

print("\n=== 5 PREMIÈRES LIGNES ===")
print(df.head())

print("\n=== VALEURS UNIQUES code_commune (20 premières) ===")
if 'code_commune' in df.columns:
    print(df['code_commune'].unique()[:20])
else:
    print("Colonne 'code_commune' introuvable !")

print("\n=== VALEURS UNIQUES nom_commune (20 premières) ===")
if 'nom_commune' in df.columns:
    print(df['nom_commune'].unique()[:20])
