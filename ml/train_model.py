# ml/train_model.py
import joblib
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# 1. Chargement du dataset
print("Chargement du dataset California Housing...")
data = fetch_california_housing()
X, y = data.data, data.target
feature_names = data.feature_names

print(f"Dataset chargé : {X.shape[0]} lignes, {X.shape[1]} features")

# 2. Split train/test 80-20
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train : {X_train.shape[0]} lignes | Test : {X_test.shape[0]} lignes")

# 3. Pipeline : normalisation + modèle
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    ))
])

# 4. Entraînement
print("Entraînement en cours... (peut prendre 1-2 minutes)")
pipeline.fit(X_train, y_train)
print("Entraînement terminé !")

# 5. Export du modèle
joblib.dump(pipeline, 'ml/model.pkl')
print("Modèle exporté : ml/model.pkl")

# 6. Sauvegarde des données test pour evaluate.py
np.save('ml/X_test.npy', X_test)
np.save('ml/y_test.npy', y_test)
np.save('ml/feature_names.npy', np.array(feature_names))
print("Données test sauvegardées pour évaluation.")
