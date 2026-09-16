import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Dashboard - Stile Playtomic",
    page_icon="🎾",
    layout="wide"
)

# Applicazione di stili CSS personalizzati per replicare il design pulito e arrotondato (stile Playtomic)
st.markdown("""
    <style>
    /* Import Google Fonts - Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f9fafb;
    }

    /* Stile delle card KPI e contenitori */
    .playtomic-card {
        background-color: #ffffff;
        border: 1px solid #f3f4f6;
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
    }
    
    .playtomic-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR DI NAVIGAZIONE
with st.sidebar:
    st.markdown("### 🎾 SportApp")
    st.write("---")
    
    # Utilizziamo testo semplice senza emoji nel codice per evitare errori di sintassi
    selected_menu = st.radio(
        "Menu",
        ["Dashboard", "Prenotazioni", "Community & Match", "Analytics & Storico"]
    )
    
    st.write("---")
    st.markdown("**Andrea**")
    st.caption("Pro Member")

# HEADER PRINCIPALE
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.title("Bentornato, Andrea!")
    st.caption("Ecco una panoramica delle attività e delle metriche di oggi.")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("+ Nuova Prenotazione", type="primary", use_container_width=True):
        st.toast("Apertura modale prenotazione...")

st.write("")

# SEZIONE KPI CARDS
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="playtomic-card">
            <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Match Totali</p>
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin-top: 0.5rem;">
                <h3 style="font-size: 1.875rem; font-weight: 700; margin: 0;">128</h3>
                <span style="background-color: #ecfdf5; color: #059669; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.5rem; border-radius: 9999px;">+12%</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="playtomic-card">
            <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Ore di Gioco</p>
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin-top: 0.5rem;">
                <h3 style="font-size: 1.875rem; font-weight: 700; margin: 0;">96.5</h3>
                <span style="background-color: #ecfdf5; color: #059669; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.5rem; border-radius: 9999px;">+8%</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="playtomic-card">
            <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Tasso Vittorie</p>
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin-top: 0.5rem;">
                <h3 style="font-size: 1.875rem; font-weight: 700; margin: 0;">64%</h3>
                <span style="background-color: #fff1f2; color: #e11d48; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.5rem; border-radius: 9999px;">-2%</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="playtomic-card">
            <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Credito Disponibile</p>
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin-top: 0.5rem;">
                <h3 style="font-size: 1.875rem; font-weight: 700; margin: 0;">45,00 €</h3>
                <span style="background-color: #f0fdf4; color: #10b981; font-size: 0.75rem; font-weight: 600; padding: 0.25rem 0.5rem; border-radius: 9999px;">Attivo</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# TABELLA ATTIVITA / MATCH RECENTI
st.markdown("""
    <div class="playtomic-card">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem;">
            <h3 style="font-size: 1.125rem; font-weight: 700; margin: 0;">Prossimi Match & Prenotazioni</h3>
        </div>
    """, unsafe_allow_html=True)

# Dati di esempio per la tabella
import pandas as pd
data = {
    "Campo / Attività": ["Campo Padel 01 (Indoor)", "Campo Padel 03 (Panoramic)"],
    "Data & Ora": ["Oggi, 18:00 - 19:30", "Dom, 10:00 - 11:30"],
    "Partecipanti": ["4 / 4 giocatori", "2 / 4 giocatori"],
    "Stato": ["Confermato", "In attesa"]
}
df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)
