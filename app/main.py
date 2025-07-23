import requests
import streamlit as st

st.set_page_config(page_title="Prédicteur de Retards de Vol", layout="centered")

# Base API URL
API_URL = "http://fastapi:8000"
PREDICT_ENDPOINT = f"{API_URL}/predict"
HEALTH_ENDPOINT = f"{API_URL}/health"

# ───────────────────────────────────────────────────────────────
# 🔍 API Health Check
# ───────────────────────────────────────────────────────────────
try:
    health = requests.get(HEALTH_ENDPOINT, timeout=3)
    if health.status_code == 200:
        st.success("✅ L'API est en ligne et opérationnelle.")
        api_ready = True
    else:
        st.error("❌ L'API a répondu, mais retourne une erreur.")
        api_ready = False
except Exception as e:
    st.error(f"❌ Impossible de contacter l'API FastAPI : {e}")
    api_ready = False

# ───────────────────────────────────────────────────────────────
# 🖥️ Streamlit App UI
# ───────────────────────────────────────────────────────────────
st.title("🛫 Application de Prédiction de Retard de Vol (via API)")

st.markdown(
    "Remplissez les informations ci-dessous pour estimer si le vol sera en retard de plus de 15 minutes."
)

# ───────────────────────────────────────────────────────────────
# ✈️ Input Form
# ───────────────────────────────────────────────────────────────
with st.form("delay_form"):
    col1, col2 = st.columns(2)

    with col1:
        month = st.selectbox("Mois", list(range(1, 13)))
        day_of_week = st.selectbox(
            "Jour de la semaine",
            [1, 2, 3, 4, 5, 6, 7],
            format_func=lambda x: [
                "Lundi",
                "Mardi",
                "Mercredi",
                "Jeudi",
                "Vendredi",
                "Samedi",
                "Dimanche",
            ][x - 1],
        )
        crs_dep_time = st.number_input(
            "Heure prévue de départ (HHMM)", min_value=0, max_value=2359, value=900
        )
        crs_elapsed_time = st.number_input(
            "Durée prévue du vol (minutes)", min_value=30, max_value=600, value=120
        )

    with col2:
        crs_arr_time = st.number_input(
            "Heure prévue d'arrivée (HHMM)", min_value=0, max_value=2359, value=1100
        )
        distance = st.number_input(
            "Distance (miles)", min_value=50, max_value=5000, value=500
        )
        dep_time_blk = st.selectbox(
            "Plage horaire de départ",
            [
                "0001-0559",
                "0600-0659",
                "0700-0759",
                "0800-0859",
                "0900-0959",
                "1000-1059",
                "1100-1159",
                "1200-1259",
                "1300-1359",
                "1400-1459",
                "1500-1559",
                "1600-1659",
                "1700-1759",
                "1800-1859",
                "1900-1959",
                "2000-2059",
                "2100-2159",
                "2200-2259",
                "2300-2359",
            ],
        )
        unique_carrier = st.selectbox(
            "Compagnie aérienne", ["AA", "DL", "UA", "WN", "B6", "AS", "NK", "F9"]
        )

    origin = st.selectbox(
        "Aéroport d'origine", ["JFK", "LAX", "ORD", "ATL", "DFW", "SFO", "MIA", "SEA"]
    )
    dest = st.selectbox(
        "Aéroport de destination",
        ["JFK", "LAX", "ORD", "ATL", "DFW", "SFO", "MIA", "SEA"],
    )

    submitted = st.form_submit_button("Prédire le retard")

# ───────────────────────────────────────────────────────────────
# 🔄 Prediction Logic (API call)
# ───────────────────────────────────────────────────────────────
if submitted and api_ready:
    # Prepare JSON payload for API
    payload = {
        "month": month,
        "day_of_week": day_of_week,
        "crs_dep_time": crs_dep_time,
        "crs_arr_time": crs_arr_time,
        "crs_elapsed_time": crs_elapsed_time,
        "distance": distance,
        "unique_carrier": unique_carrier,
        "origin": origin,
        "dest": dest,
        "dep_time_blk": dep_time_blk,
    }

    try:
        response = requests.post(PREDICT_ENDPOINT, json=payload)
        response.raise_for_status()
        result = response.json()

        # Show prediction result
        st.subheader("Résultat de la prédiction :")
        if result["prediction"] == 1:
            st.error(
                "❌ Le vol a une forte probabilité d'être en retard (> 15 minutes)."
            )
        else:
            st.success("✅ Le vol devrait arriver à l’heure.")

        st.markdown(f"**Probabilité de retard** : {result['delay_probability']:.2%}")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'appel à l'API de prédiction : {e}")
elif submitted and not api_ready:
    st.warning("🚨 Prédiction impossible : l'API n'est pas accessible.")
