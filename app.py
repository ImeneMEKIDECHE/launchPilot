"""
Squelette minimal pour valider le déploiement Aiven Runtime CE SOIR.
Demain : remplacer par la vraie interface (tableau de bord, fil d'alertes, scénarios).
"""
import os
import streamlit as st

st.set_page_config(page_title="LaunchPilot", layout="wide")
st.title("LaunchPilot — copilote de lancement")
st.caption("Données synthétiques — marque fictive Maison Aurore")

url = os.environ.get("DATABASE_URL")
if not url:
    st.warning("DATABASE_URL non défini")
else:
    import psycopg, pandas as pd
    with psycopg.connect(url) as conn:
        df = pd.read_sql("SELECT * FROM supplier_reliability ORDER BY late_rate DESC", conn)
    st.subheader("Mémoire fournisseur")
    st.dataframe(df, use_container_width=True)
st.success("Déploiement OK" if url else "App lancée sans base")
