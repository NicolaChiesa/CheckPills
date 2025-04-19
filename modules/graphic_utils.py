import streamlit as st

def st_sidebar_info():
    with st.sidebar:
        st.title("Contatti")
        st.info(
            """
            **Nicola Chiesa** : ML & AI Engineer  \n 
            [Linkedin](https://www.linkedin.com/in/nicola-chiesa-5a93781a2/) 
            """
        )
        st.info(
            """
            **Andrea Chiesa** : Studio di produzioni foto, video & web \n
            [Linkedin](https://www.linkedin.com/in/chiesaandrea/) \n
            [WebSite](https://www.andreachiesa.it)
            """
        )
        # st.success("if any problem was found, thanks")
        # st.write('''---''')