import streamlit as st

# Esempio di dati dei giocatori (puoi sostituirli con i tuoi dati reali)
players = [
    {"id": 1, "name": "Andrea", "role": "Capitano / Drive", "overall": 85, "condition": "Ottima"},
    {"id": 2, "name": "Carlos", "role": "Revés", "overall": 88, "condition": "Buona"},
    {"id": 3, "name": "Javier", "role": "Drive", "overall": 82, "condition": "Buona"}
]

st.title("Gestione Squadra Padel")

# Inizializza lo stato per tenere traccia del giocatore selezionato
if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = None

# --- CREAZIONE DEI SUBTAB ---
tab_overview, tab_list = st.tabs(["Panoramica", "Lista Giocatori"])

with tab_overview:
    st.header("Panoramica Area Giocatore")
    st.write("Contenuti generali dell'area...")

with tab_list:
    st.header("Directory Giocatori")
    
    # Se un giocatore è stato selezionato, mostra la scheda di dettaglio
    if st.session_state.selected_player_id is not None:
        # Trova il giocatore selezionato
        player = next((p for p in players if p["id"] == st.session_state.selected_player_id), None)
        
        if player:
            if st.button("← Torna alla lista"):
                st.session_state.selected_player_id = None
                st.rerun()
                
            st.markdown(f"## Scheda Dettaglio: {player['name']}")
            st.write(f"**Ruolo:** {player['role']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Valore Generale", value=player["overall"])
            with col2:
                st.metric(label="Condizione", value=player["condition"])
    else:
        # Mostra la tabella/elenco dei giocatori con un pulsante per ciascuno
        for player in players:
            cols = st.columns([3, 2, 2])
            with cols[0]:
                st.write(f"**{player['name']}**")
            with cols[1]:
                st.write(player['role'])
            with cols[2]:
                if st.button("Visualizza Scheda", key=f"btn_{player['id']}"):
                    st.session_state.selected_player_id = player["id"]
                    st.rerun()
