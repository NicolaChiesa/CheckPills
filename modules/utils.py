import openai 
import json
import streamlit as st 



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
        response = client.responses.create(
            model="gpt-4.1-nano",
            input=[
                {"role": "system", "content": "Sei un esperto di farmacologia. Il tuo obbiettivo è quello di controllare le "
                "possibili controindicazioni che possono esserci tra l' assunzione di più farmaci. "},
                {"role": "user", "content": prompt}],
            temperature=0.3,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "iterazioni_schema",
                    "schema": {
                        "type": "object",
                        "properties": {
                        "iterazioni": {
                            "type": "array",
                            "description": "Una lista di oggetti che rappresentano le iterazioni tra farmaci.",
                            "items": {
                            "type": "object",
                            "properties": {
                                "farmaco_1": {
                                "type": "string",
                                "description": "Il primo farmaco coinvolto nell'iterazione."
                                },
                                "farmaco_2": {
                                "type": "string",
                                "description": "Il secondo farmaco coinvolto nell'iterazione."
                                },
                                "rischio": {
                                "type": "string",
                                "description": "Il rischio associato alla gravità dell' interazione tra i farmaci 'basso', medio' 'alto', 'ignoto'"
                                },
                                "controindicazione": {
                                "type": "string",
                                "description": "Controindicazione all'uso dei farmaci."
                                },
                                "soluzione": {
                                "type": "string",
                                "description": "La soluzione suggerita per affrontare il rischio."
                                }
                            },
                            "required": [
                                "farmaco_1",
                                "farmaco_2",
                                "rischio",
                                "controindicazione",
                                "soluzione"
                            ],
                            "additionalProperties": False
                            }
                        }
                        },
                        "required": [
                        "iterazioni"
                        ],
                        "additionalProperties": False
                    },
                    "strict": True
                    }
            }
        )
        return json.loads(response.output_text)
    except Exception as e:
        return f"Errore nella richiesta: {str(e)}"
    
# Funzione per aggiungere un nuovo campo
def add_drug_input():
    st.session_state.drug_list.append("")

# Funzione per rimuovere un campo (opzionale)
def remove_last_drug_input(i : int):
    if len(st.session_state.drug_list) > 0:
        st.session_state.drug_list.pop(i)
