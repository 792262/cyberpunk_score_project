

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from math import sqrt


# 1. Chargement du dataset généré précédemment
# On lit le fichier CSV contenant les profils avec leurs scores calculés
df = pd.read_csv("app/data/profils_scores.csv")
# Debug temporaire pour voir les colonnes disponibles
print(df.columns.tolist())
df = df.dropna(subset=["score"])

# 2. Séparation des variables explicatives (features) et de la variable cible (score)
# X contient les colonnes numériques utilisées pour prédire le score
# y est la colonne "score" qu'on veut apprendre à prédire
# On retire les colonnes non-numériques ou non utiles pour l'apprentissage
X = df [[
    "chrome",
    "trauma_team",
    "kills",
    "hacks_illegaux",
    "relations_fixers",
    "relation_nomades",
    "relation_corpos"
]]
y = df["score"]

# 3. Division du dataset en deux parties :
# - 80% pour l'apprentissage (X_train / y_train)
# - 20% pour tester la capacité du modèle à généraliser (X_test / y_test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # random_state permet de toujours obtenir la même séparation


# 4. Création du modèle
# RandomForestRegressor utilise plusieurs arbres de décision en parallèle pour faire des prédictions plus robustes##
# Il est peu sensible à la distribution des données (pas besoin de normalisation) 
modele = RandomForestRegressor(n_estimators=100, random_state=42)

# 5. Entraînement du modèle
# Le modèle "apprend" à partir des exemples de X_train et y_train
modele.fit(X_train, y_train)

# 6. Évaluation du modèle sur les données de test
# R² mesure la proportion de variance expliquée par le modèle
# Un R² proche de 1 = très bon ; proche de 0 = modèle peu informatif
score_r2 = modele.score(X_test,y_test)
print(f"✅ Modèle entraîné avec R² = {round(score_r2, 3)}")

# 7. Sauvegarde du modèle entraîné
# Cela permet d'utiliser le modèle plus tard sans avoir à le réentraîner à chaque fois
# On le sauvegarde au format .pkl grâce à joblib (recommandé pour les modèles scikit-learn)
joblib.dump(modele, "app/model/modele_credit_social.pkl")  # On place le modèle dans le dossier prévu

print("✅ Modèle sauvegardé sous modele_credit_social.pkl")



