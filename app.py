import streamlit as st
from . import utils

# UI Streamlit
st.title("PillsChek ")

drugs_input = st.text_area("Inserisci i nomi dei farmaci separati da una virgola:")

drugs = [drug.strip() for drug in drugs_input.split(",") if drug.strip()]

if st.button("Verifica Interazioni"):
    if len(drugs) < 2:
        st.error("Inserisci almeno due farmaci per la verifica.")
    else:
        with st.spinner("Analizzando le interazioni..."):
            result = utils.check_drug_interactions(drugs)
            st.subheader("Risultati:")
            
            # Formatta la risposta con Streamlit
            for section in result.split("\n\n"):
                st.markdown(section)