import streamlit as st
import pandas as pd

# Configurazione della pagina
st.set_page_config(
    page_title="Dashboard - Stile Playtomic",
    page_icon="🎾",
    layout="wide"
)

# --- GESTIONE DEL RUOLO UTENTE (Simulazione Auth) ---
if "user_role" not in st.session_state:
    st.session_state.user_role = "Giocatore"  # Valori possibili: "Giocatore", "Allenatore"

# Sidebar per il cambio ruolo (utile per testare)
with st.sidebar:
    st.markdown("### 🎾 SportApp")
    st.write("---")
    
    # Selettore per simulare chi sta visualizzando l'app
    st.markdown("**Controllo Accesso (Demo)**")
    st.session_state.user_role = st.selectbox(
        "Ruolo attuale:", 
        ["Giocatore", "Allenatore"],
        index=0 if st.session_state.user_role == "Giocatore" else 1
    )
    
    st.write("---")
    selected_menu = st.radio(
        "Menu",
        ["Dashboard", "Prenotazioni", "Coach Evaluation", "Analytics & Storico"]
    )
    
    st.write("---")
    st.markdown(f"**Andrea**")
    st.caption(f"Ruolo: {st.session_state.user_role}")

# Stili CSS personalizzati
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #f9fafb;
    }
    .playtomic-card {
        background-color: #ffffff;
        border: 1px solid #f3f4f6;
        border-radius: 1.5rem;
        padding: 1.5rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Sezione dedicata alla valutazione
if selected_menu == "Coach Evaluation":
    st.title("Coach Evaluation & Comparison")
    st.caption("Valutazioni tecniche, tattiche e comparazione dei progressi.")

    # Verifica se l'utente è un allenatore
    is_coach = (st.session_state.user_role == "Allenatore")

    if not is_coach:
        st.warning("⚠️ Visualizzazione in sola lettura: questa sezione può essere modificata esclusivamente dall'allenatore.")

    # Creazione del form o dei campi di valutazione
    with st.form("evaluation_form"):
        st.subheader("Parametri di Gioco")
        
        # Se non è l'allenatore, i campi vengono disabilitati (disabled=True)
        collegamento_tecnico = st.slider(
            "Livello Tecnico (Colpi / Impatto)", 
            min_value=1.0, max_value=10.0, value=7.5, step=0.5,
            disabled=not is_coach
        )
        
        lettura_gioco = st.slider(
            "Tattica e Posizionamento in Campo", 
            min_value=1.0, max_value=10.0, value=8.0, step=0.5,
            disabled=not is_coach
        )
        
        note_allenatore = st.text_area(
            "Note e Feedback dell'Allenatore",
            value="Ottimi progressi nel gioco a rete, lavorare sulla bandeja.",
            disabled=not is_coach
        )

        # Il pulsante di salvataggio compare o è attivo solo per l'allenatore
        if is_coach:
            submitted = st.form_submit_button("Salva Modifiche")
            if submitted:
                st.success("Valutazioni aggiornate con successo!")
        else:
            st.form_submit_button("Salva Modifiche", disabled=True)

else:
    # Vista Dashboard Standard
    st.title("Bentornato, Andrea!")
    st.caption("Ecco una panoramica delle attività e delle metriche di oggi.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="playtomic-card">
                <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Match Totali</p>
                <h3 style="font-size: 1.875rem; font-weight: 700; margin-top: 0.5rem;">128</h3>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="playtomic-card">
                <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Ore di Gioco</p>
                <h3 style="font-size: 1.875rem; font-weight: 700; margin-top: 0.5rem;">96.5</h3>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="playtomic-card">
                <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Tasso Vittorie</p>
                <h3 style="font-size: 1.875rem; font-weight: 700; margin-top: 0.5rem;">64%</h3>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="playtomic-card">
                <p style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Credito</p>
                <h3 style="font-size: 1.875rem; font-weight: 700; margin-top: 0.5rem;">45,00 €</h3>
            </div>
        """, unsafe_allow_html=True)
