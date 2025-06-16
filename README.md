# 🦾 Cyberpunk Social Score Simulator

Bienvenue dans un futur aussi logique qu’absurde : ici, votre **valeur sociale** est calculée par une IA — comme si vos relations avec des fixers ou votre niveau de cyberware définissaient votre droit à exister.

## 🧠 Objectif

Ce projet de data science explore une question sérieuse avec des outils rigoureux... dans un univers débile : *Cyberpunk 2077*.

**Deux modes :**
- 🔍 *Explorer* des personnages emblématiques (V, Panam, Adam Smasher, etc.) avec leur score et un petit texte narratif.
- 🧪 *Simuler* ton propre score social à l’aide de sliders.

## ⚙️ Tech utilisée (en mode vulgarisé)

| Outil | À quoi ça sert |
|------|----------------|
| **Python** | Le cerveau du projet. |
| **Pandas** | Lire, trier, transformer les données comme un hacker avec un tableau Excel. |
| **NumPy** | Calculs plus rapides, surtout pour modérer les gros chiffres (genre 50 kills). |
| **scikit-learn** | Créer le modèle d’IA. En l’occurrence : un *Random Forest Regressor*. |
| **Streamlit** | Créer une app web sans galérer avec du HTML. On pose du Python, et ça clique. |
| **Docker** | Enfermer tout ça dans une boîte qui tourne partout pareil. |
| **joblib** | Enregistrer notre modèle pour ne pas devoir le réentraîner à chaque fois. |

## 🔍 Pourquoi Streamlit ?

Parce que c’est :
- Rapide
- Lisible
- Adapté à la data science
- Parfait pour montrer un projet à des humains normaux, et pas juste à son terminal.

## 🧪 Le pipeline 

1. **Générer des données**  
   - On invente 1500 profils cyberpunk.
   - Chaque perso a des attributs (chrome, kills, fixers...).
   - On ajoute aussi des vrais persos de l’univers avec un petit texte (merci l’amour du lore).

2. **Calculer un score “social”**  
   - Une formule artisanale, biaisée (exprès), corpo-friendly.
   - Ex. : trop de chrome = malus (cyberpsychose), mais relations corpos = jackpot.
   - Un petit bruit aléatoire pour simuler le chaos du capitalisme.

3. **Entraîner le modèle IA**  
   - Un modèle *Random Forest Regressor* (une forêt de décisions).
   - Prédit un score entre 0 et 100 selon les attributs.

4. **Afficher les résultats dans l'app**  
   - Tu choisis un perso ou tu simules ton score.
   - Le modèle prédit, et Arasaka te donne son verdict.

## 📦 Lancer l’app (en local)

```bash
git clone https://github.com/tonrepo/cyberpunk_score_project.git
cd cyberpunk_score_project
docker build -t cyberpunk-app .
docker run -p 8501:8501 cyberpunk-app
