import streamlit as st
from modules import utils, graphic_utils
import json
# Title and heder
st.title("PillsCheck 💊")


###### sidebar info ######
graphic_utils.st_sidebar_info()

st.error("⚠️ L' applicazione è ancora in sviluppo ")
st.header("Verifica le interazioni tra i tuoi farmaci!")
st.markdown("""
**PillsCheck** è un assistente intelligente che ti aiuta a identificare **interazioni pericolose tra farmaci**, 
valutando il **livello di rischio** e suggerendo **soluzioni sicure**. Inserisci i nomi dei medicinali che stai assumendo 
per scoprire eventuali **controindicazioni** o **effetti indesiderati**.
""")


# Disclimer
with st.expander("📄 **Disclaimer medico**",expanded=False):
    st.warning("""
🔔 **Attenzione**  
PillsCheck utilizza **l’intelligenza artificiale** per fornire suggerimenti solo a **scopo informativo**.  

L’utente è consapevole che l’utilizzo del servizio **non costituisce o sostituisce in alcun modo una consulenza medica**, diagnosi o indicazione terapeutica.

Gli sviluppatori e i fornitori del servizio **declinano ogni responsabilità** per eventuali danni, diretti o indiretti, derivanti dall’uso improprio delle informazioni fornite.               

Prima di prendere decisioni sulla tua salute o modificare una terapia, **rivolgiti sempre al tuo medico o a un professionista sanitario qualificato**.
""")
st.divider()

# OpenAI key
st.markdown("#### 🔐 Inserisci la tua chiave OpenAI")
OPENAI_KEY = st.text_input("🔑 Inserisci la tua chiave OpenAI",
                           label_visibility="collapsed",
                           type="default",
                           placeholder="sk-...")


st.divider()
# Inizializza la lista dei farmaci nella sessione
if "drug_list" not in st.session_state:
    st.session_state.drug_list = [""]
if "interactions" not in st.session_state:
    st.session_state.interactions = [""]
if "generationDone" not in st.session_state:
    st.session_state.generationDone = False

# Mostra i campi di input per ciascun farmaco
st.markdown("#### 💊 Farmaci da analizzare")
st.markdown("Inserisci i farmaci di cui vuoi analizzare le interazioni (uno per ogni campo)")
for i in range(len(st.session_state.drug_list)):
    col1, col2 = st.columns([0.8,0.3])
    with col1:
        st.session_state.drug_list[i] = st.text_input(
            label= f"", 
            placeholder= f"Farmaco {i+1}",
            label_visibility="collapsed",
            value = st.session_state.drug_list[i], 
            #key=f"farmaco_{i}"
        )
    with col2:
         st.button("➖ Rimuovi farmaco",
                   on_click= lambda : utils.remove_last_drug_input(i),
                   key=f"rimuovi_farmaco_{i}"
                   )


# TODO let user add drug only if all fields are full 
col1, col2, _= st.columns(3)
with col1:
    st.button("➕ Aggiungi farmaco", on_click=utils.add_drug_input, use_container_width=True)
with col2:
    submit = st.button("✅ Verifica Interazioni", key="verifica_interazioni", use_container_width=True)

# Se si è premuto "Verifica Interazioni"
if submit:
    if len(st.session_state["drug_list"]) < 2:
        st.error("Inserisci almeno due farmaci per la verifica.")
    else:
        with st.spinner("Analizzando le interazioni..."):
            st.session_state["interactions"] = utils.check_drug_interactions(
                OPENAI_KEY, st.session_state["drug_list"]
            )
            st.session_state["generationDone"] = True

if st.session_state.get("generationDone"):
    for interaction in st.session_state["interactions"].get("iterazioni", []):
        with st.container(border=True):

            if interaction['rischio'] == "alto":
                st.markdown("**Rischio** : :red-badge[:material/Warning: Alto]")
            if interaction['rischio'] == "medio":
                st.markdown("**Rischio** : :orange-badge[:material/Notifications: Medio]")
            if interaction['rischio'] == "basso":
                st.markdown("**Rischio** : :green-badge[:material/Health_And_Safety: Basso]")

            col1, col2, _ = st.columns(3)
            with col1:
                st.markdown(f"**Farmaco 1**: _{interaction['farmaco_1']}_")
            with col2:
                st.markdown(f"**Farmaco 2**: _{interaction['farmaco_2']}_")

            st.markdown(f"**Controindicazione**: {interaction['controindicazione']}")
            st.markdown(f"**Soluzione** : {interaction['soluzione']}")
