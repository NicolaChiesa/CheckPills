import openai
import streamlit as st 

# Inserisci qui la tua API Key di OpenAI
# streAPI_KEY = st.secrets["API_KEY"]

def check_drug_interactions(OPENAI_KEY, drugs):
    client = openai.OpenAI(api_key=OPENAI_KEY)
    prompt = f"""Verifica se ci sono controindicazioni tra i seguenti farmaci:
    {', '.join(drugs)}
    
    Fornisci la risposta con la seguente struttura per ogni coppia di farmaci:
    - Farmaco 1 con Farmaco 2:
      - **Rischio**: basso / medio / alto
      - **Controindicazione**: Spiegazione delle interazioni dannose tra i farmaci, e possibili conseguenze sul individuo
      - **Soluzione**: eventuali azioni da prendere (es. aspettare un intervallo di tempo prima di assumere il secondo farmaco)
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Sei un esperto di farmacologia."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Errore nella richiesta: {str(e)}"