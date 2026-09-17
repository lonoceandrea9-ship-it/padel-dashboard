import streamlit as st
import pandas as pd

st.title("🎾 Gestione Convocazioni e Pairing Padel")

# 1. Inizializziamo lo stato della sessione se non esiste
if "pairing_confermato" not in st.session_state:
    st.session_state.pairing_confermato = False
if "coppie_finali_modificate" not in st.session_state:
    st.session_state.coppie_finali_modificate = None

# Esempio di dati di pairing iniziali (simulati o generati dal tuo algoritmo)
if "pairing_iniziale" not in st.session_state:
    st.session_state.pairing_iniziale = [
        {"Campo": 1, "Giocatore 1": "Mario Rossi", "Giocatore 2": "Luca Bianchi"},
        {"Campo": 2, "Giocatore 1": "Giovanni Verdi", "Giocatore 2": "Marco Neri"},
    ]

st.subheader("📋 Risultato Pairing Consigliato")
st.markdown("Il coach può modificare direttamente i nomi dei giocatori nella tabella sottostante se desidera fare variazioni prima di confermare.")

# 2. Tabella modificabile con st.data_editor
df_pairs = pd.DataFrame(st.session_state.pairing_iniziale)

edited_df = st.data_editor(
    df_pairs,
    num_rows="dynamic",
    disabled=False,
    key="editor_coppie_tutto"
)

# 3. Pulsante di Conferma
col_btn1, col_btn2 = st.columns([1, 3])
with col_btn1:
    if st.button("✅ Conferma Selezione", type="primary"):
        st.session_state.pairing_confermato = True
        # Salviamo la versione modificata e confermata nello stato per usi futuri
        st.session_state.coppie_finali_modificate = edited_df.copy()
        st.success("Coppie confermate con successo dal coach!")

# 4. Stato di riscontro post-conferma
if st.session_state.pairing_confermato and st.session_state.coppie_finali_modificate is not None:
    st.divider()
    st.info("Le coppie sono state salvate e confermate. Il sistema è pronto per i passaggi successivi.")
