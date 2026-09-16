# Inizializzazione dello stato di autenticazione
if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

# Sidebar per la navigazione e sicurezza
st.sidebar.title("🎾 Padel Hub - Accesso")
modalita = st.sidebar.radio(
    "Seleziona Area:",
    ["👤 Area Giocatore", "📋 Area Allenatore (Coach)"]
)

if modalita == "📋 Area Allenatore (Coach)":
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Area Riservata Mister")
    
    COACH_PASSWORD = "padelcoach2026" 
    
    if not st.session_state.authenticated_coach:
        pwd_input = st.sidebar.text_input("Inserisci Password Allenatore", type="password")
        if st.sidebar.button("Accedi"):
            if pwd_input == COACH_PASSWORD:
                st.session_state.authenticated_coach = True
                st.rerun()
            else:
                st.sidebar.error("Password errata!")
    else:
        st.sidebar.success("✅ Accesso Autorizzato (Mister)")
        if st.sidebar.button("🔒 Logout"):
            st.session_state.authenticated_coach = False
            st.rerun()

# CONTROLLO ACCESSO AGGIORNATO CORRETTAMENTE
if modalita == "📋 Area Allenatore (Coach)" and not st.session_state.authenticated_coach:
    st.title("🔒 Area Riservata all'Allenatore")
    st.warning("Inserisci la password corretta nella barra laterale a sinistra per visualizzare la panoramica e i gruppi di lavoro della squadra.")

elif modalita == "👤 Area Giocatore":
    # (Qui sotto continua tutto il codice HTML della dashboard giocatore che ti ho inviato prima)
