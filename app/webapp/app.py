import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Titre principal de l'application
st.title("Bienvenue dans l'univers Cyberpunk 🦾")
st.write("Explorez les profils des légendes de Night City ou simulez votre propre score social !")

# --- CHOIX DU MODE : soit personnage existant, soit simulation utilisateur ---
mode = st.radio("Choisissez votre mode :", ["Personnage existant", "Créer mon profil"])

# Chargement du fichier CSV contenant les personnages
# Ce fichier contient les profils manuels + ceux générés automatiquement
# Il a été généré à partir de generate_dataset.py

df = pd.read_csv("app/data/profils_scores.csv")

# --- MODE 1 : AFFICHER UN PERSONNAGE EXISTANT ---
if mode == "Personnage existant":
    # Filtrer les personnages ajoutés manuellement (héros connus)
    persos_manuels = df[df["source"] == "manuel"]

    # Liste déroulante avec tous les noms
    noms_manuels = persos_manuels["nom"].tolist()
    choix = st.selectbox("Choisissez un personnage légendaire :", noms_manuels)

    # Sélection de la ligne correspondant au personnage
    perso_selectionne = persos_manuels[persos_manuels["nom"] == choix].iloc[0]
    narratif = perso_selectionne.get("narratif", "Pas de narratif disponible")
    score = round(perso_selectionne["score"], 2)

    # Affichage des infos
    st.markdown(f"## {perso_selectionne['nom']}")
    st.markdown(f"**Narratif :** {narratif}")
    st.markdown(f"<h2 style='color:#FF4B4B;'>Score social : {score} / 100</h2>", unsafe_allow_html=True)

    # Rapport Arasaka™ pour interpréter le score
    st.subheader("🧾 Rapport Arasaka™")
    if score > 90:
        st.success("Statut : **Légende corporatiste.** Vous êtes la main droite du Conseil exécutif.")
    elif score > 70:
        st.info("Statut : **Corpo confirmé.** Vous avez votre badge et votre neurodôme privé.")
    elif score > 40:
        st.warning("Statut : **Agent instable.** Vos résultats plaisent mais vos fréquentations inquiètent.")
    else:
        st.error("Statut : **Cyber-déchet.** Recyclage programmé à 18h42.")

    # Petites corrections narratives pour les profils spéciaux
    if perso_selectionne["nom"] == "Panam Palmer" and score > 70:
        st.markdown("⚠️ *Erreur de prédiction détectée : l'algorithme est clairement trop corpo pour comprendre Panam.*")
    if perso_selectionne["nom"] == "T-Bug" and score > 70:
        st.markdown("⚠️ *T-Bug aurait probablement hacké ce simulateur pour y glisser un meme de Bartmoss.*")

# --- MODE 2 : SIMULATION UTILISATEUR ---
else:
    st.header("🔧 Simule ton propre score social")

    # Chargement du modèle pré-entraîné
    model = joblib.load("app/model/modele_credit_social.pkl")

    # Sliders pour permettre à l'utilisateur d'entrer ses propres valeurs
    chrome = st.slider("Niveau de chrome", 0, 10, 3)
    trauma = st.slider("Assurance Trauma Team", 0, 3, 1)
    kills = st.slider("Nombre de kills", 0, 50, 5)
    hacks = st.slider("Hacks illégaux", 0, 10, 1)
    fixers = st.slider("Relations avec fixers", 0, 5, 2)
    nomades = st.slider("Relations avec nomades", 0, 5, 2)
    corpos = st.slider("Relations avec corpos", 0, 5, 2)

    # Attention : il faut respecter les noms EXACTS vus par le modèle (pas d'accents !) ✅
    X_new = pd.DataFrame([[chrome, trauma, kills, hacks, fixers, nomades, corpos]],
                         columns=["chrome", "trauma_team", "kills", "hacks_illegaux",
                                  "relations_fixers", "relation_nomades", "relation_corpos"])

    # Prédiction du score
    prediction = model.predict(X_new)[0]

    # Affichage du score simulé
    st.subheader("📈 Résultat de votre simulation")
    st.markdown(f"<h2 style='color:#4BB543;'>Votre score social simulé : {prediction:.2f} / 100</h2>", unsafe_allow_html=True)

    # Rapport Arasaka™ selon score
    st.subheader("🧾 Rapport Arasaka™")
    if prediction > 90:
        st.success("Statut : **Légende corporatiste.** Vous êtes la main droite du Conseil exécutif.")
    elif prediction > 70:
        st.info("Statut : **Corpo confirmé.** Vous avez votre badge et votre neurodôme privé.")
    elif prediction > 40:
        st.warning("Statut : **Agent instable.** Vos résultats plaisent mais vos fréquentations inquiètent.")
    else:
        st.error("Statut : **Cyber-déchet.** Recyclage programmé à 18h42.")

