import streamlit as st
import pandas as pd
import joblib

# 🧠 Chargement du modèle avec mise en cache
@st.cache_resource
def load_model():
    return joblib.load("app/model/modele_credit_social.pkl")

# 📁 Chargement des données (profils) avec cache
@st.cache_data
def load_data():
    return pd.read_csv("app/data/profils_scores.csv")

# ⚙️ On charge le modèle et les données
model = load_model()
df = load_data()
df["source"] = df["source"].str.strip().str.lower()

# 🎬 Interface utilisateur Streamlit
st.title("💼 Simulateur de Score Social Cyberpunk")

mode = st.radio("Choisissez votre mode :", ["Personnage existant", "Créer mon profil"])

# ------------------------------
# 🔎 Mode : Personnage existant
# ------------------------------
if mode == "Personnage existant":
    persos = df[df["source"] == "manuel"]["nom"].unique()
    choix = st.selectbox("Choisissez un personnage :", persos)

    if st.button("🛰️ Soumettre à Arasaka™"):
        resultat = df[df["nom"] == choix]

        if not resultat.empty:
            perso = resultat.iloc[0]
            input_data = pd.DataFrame([{
                "chrome": perso["chrome"],
                "trauma_team": perso["trauma_team"],
                "kills": perso["kills"],
                "hacks_illegaux": perso["hacks_illegaux"],
                "relations_fixers": perso["relations_fixers"],
                "relation_nomades": perso["relation_nomades"],
                "relation_corpos": perso["relation_corpos"]
            }])

            prediction = model.predict(input_data)[0]

            st.subheader(f"Score social de **{choix}**")
            st.metric("Score prédit", f"{prediction:.1f} / 100")

            st.subheader("🧾 Rapport Arasaka™")
            if prediction > 90:
                st.success("Statut : **Légende corporatiste.** Vous êtes la main droite du Conseil exécutif.")
            elif prediction > 70:
                st.info("Statut : **Corpo confirmé.** Vous avez votre badge et votre neurodôme privé.")
            elif prediction > 50:
                st.warning("Statut : **Agent instable.** Vos résultats plaisent mais vos fréquentations inquiètent.")
            else:
                st.error("Statut : **Cyber-déchet.** Recyclage programmé à 18h42.")
        else:
            st.warning("⚠️ Ce personnage n'a pas été trouvé dans les profils manuels.")

# ------------------------------
# ✍️ Mode : Création manuelle
# ------------------------------
else:
    st.subheader("📊 Paramétrez votre profil :")

    chrome = st.slider("Niveau de Chrome (implants)", 0, 10, 5)
    trauma = st.slider("Couverture Trauma Team", 0, 3, 1)
    kills = st.slider("Kills confirmés", 0, 100, 10)
    hacks = st.slider("Hacks illégaux", 0, 10, 2)
    fixers = st.slider("Relations avec des fixers", 0, 5, 2)
    nomades = st.slider("Relations avec les nomades", 0, 5, 2)
    corpos = st.slider("Relations avec les corpos", 0, 5, 2)

    if st.button("🛰️ Soumettre à Arasaka™"):
        input_data = pd.DataFrame([{
            "chrome": chrome,
            "trauma_team": trauma,
            "kills": kills,
            "hacks_illegaux": hacks,
            "relations_fixers": fixers,
            "relation_nomades": nomades,
            "relation_corpos": corpos
        }])

        prediction = model.predict(input_data)[0]

        st.subheader("📈 Résultat")
        st.metric("Score prédit", f"{prediction:.1f} / 100")

        st.subheader("🧾 Rapport Arasaka™")
        if prediction > 90:
            st.success("Statut : **Légende corporatiste.** Vous êtes la main droite du Conseil exécutif.")
        elif prediction > 70:
            st.info("Statut : **Corpo confirmé.** Vous avez votre badge et votre neurodôme privé.")
        elif prediction > 40:
            st.warning("Statut : **Agent instable.** Vos résultats plaisent mais vos fréquentations inquiètent.")
        else:
            st.error("Statut : **Cyber-déchet.** Recyclage programmé à 18h42.")
        
