import streamlit as st
import pandas as pd
import json

# Streamlit page configuration
st.set_page_config(
    page_title="Padel Performance Hub",
    page_icon="🎾",
    layout="wide"
)

# --- TRADUZIONI (1) ---
TRANSLATIONS = {
    "Italiano": {
        "welcome": "Benvenuto in Padel Performance Hub",
        "select_area": "Seleziona la tua area di accesso per continuare:",
        "player_area": "Area Giocatore",
        "player_desc": "Accedi al tuo profilo protetto da password per visualizzare e aggiornare le tue valutazioni.",
        "btn_player": "Accedi come Giocatore",
        "coach_area": "Area Coach",
        "coach_desc": "Accesso riservato allo staff tecnico per gestire dati, sessioni e abbinamenti.",
        "btn_coach": "Accedi come Coach",
        "logout": "Esci",
        "back_home": "Torna alla Home",
        "tech_skills": "Competenze Tecniche",
        "mental_skills": "Tattica e Mentale",
        "coach_eval": "Valutazione Coach & Confronto",
        "diff_table": "Tabella delle Differenze (Tu vs Coach)",
        "partner_ranking": "Ranking Partner",
        "comments": "Commenti tra Giocatori",
        "radar_progress": "Storico e Miglioramenti",
        "matches": "Gestione Partite & Risultati"
    },
    "Inglese": {
        "welcome": "Welcome to Padel Performance Hub",
        "select_area": "Select your access area to continue:",
        "player_area": "Player Area",
        "player_desc": "Access your password-protected personal profile to view and update your evaluations.",
        "btn_player": "Log in as Player",
        "coach_area": "Coach Area",
        "coach_desc": "Restricted access for coaching staff to manage data, plan training sessions, and generate team pairings.",
        "btn_coach": "Log in as Coach",
        "logout": "Log Out",
        "back_home": "Back to Home",
        "tech_skills": "Technical Skills",
        "mental_skills": "Attitude & Tactics",
        "coach_eval": "Coach Evaluation & Comparison",
        "diff_table": "Differences Table (You vs Coach)",
        "partner_ranking": "Partner Ranking",
        "comments": "Player Comments",
        "radar_progress": "Progress History",
        "matches": "Matches & Results"
    },
    "Spagnolo": {
        "welcome": "Bienvenido a Padel Performance Hub",
        "select_area": "Selecciona tu área de acceso para continuar:",
        "player_area": "Área de Jugador",
        "player_desc": "Accede a tu perfil personal protegido para ver y actualizar tus evaluaciones.",
        "btn_player": "Iniciar sesión como Jugador",
        "coach_area": "Área de Entrenador",
        "coach_desc": "Acceso restringido para el cuerpo técnico para gestionar datos y emparejamientos.",
        "btn_coach": "Iniciar sesión como Entrenador",
        "logout": "Cerrar sesión",
        "back_home": "Volver al inicio",
        "tech_skills": "Habilidades Técnicas",
        "mental_skills": "Táctica y Mental",
        "coach_eval": "Evaluación del Entrenador y Comparación",
        "diff_table": "Tabla de Diferencias (Tú vs Entrenador)",
        "partner_ranking": "Ranking de Compañeros",
        "comments": "Comentarios de Jugadores",
        "radar_progress": "Historial de Mejoras",
        "matches": "Partidos y Resultados"
    },
    "Danese": {
        "welcome": "Velkommen til Padel Performance Hub",
        "select_area": "Vælg dit adgangsområde for at fortsætte:",
        "player_area": "Spillerområde",
        "player_desc": "Få adgang til din personlige profil for at se og opdatere dine evalueringer.",
        "btn_player": "Log ind som spiller",
        "coach_area": "Trænerområde",
        "coach_desc": "Begrænset adgang for trænerstab.",
        "btn_coach": "Log ind som træner",
        "logout": "Log ud",
        "back_home": "Tilbage til start",
        "tech_skills": "Tekniske færdigheder",
        "mental_skills": "Taktik & Mentalt",
        "coach_eval": "Trænerevaluering & Sammenligning",
        "diff_table": "Forskellen tabel (Dig vs Træner)",
        "partner_ranking": "Partner Ranking",
        "comments": "Spillerkommentarer",
        "radar_progress": "Fremgangshistorik",
        "matches": "Kampe & Resultater"
    },
    "Svedese": {
        "welcome": "Välkommen till Padel Performance Hub",
        "select_area": "Välj ditt åtkomstområde för att fortsätta:",
        "player_area": "Spelardagar",
        "player_desc": "Åtkomst till din personliga profil för att se och uppdatera dina utvärderingar.",
        "btn_player": "Logga in som spelare",
        "coach_area": "Tränarområde",
        "coach_desc": "Begränsad åtkomst för tränarstab.",
        "btn_coach": "Logga in som tränare",
        "logout": "Logga ut",
        "back_home": "Tillbaka till start",
        "tech_skills": "Tekniska färdigheter",
        "mental_skills": "Taktik & Mentalt",
        "coach_eval": "Tränarutvärdering & Jämförelse",
        "diff_table": "Skillnadstabell (Du vs Tränare)",
        "partner_ranking": "Partnerranking",
        "comments": "Spelarkommentarer",
        "radar_progress": "Utvecklingshistorik",
        "matches": "Matcher & Resultat"
    },
    "Olandese": {
        "welcome": "Welkom bij Padel Performance Hub",
        "select_area": "Selecteer je toegangsgebied om door te gaan:",
        "player_area": "Spelersgebied",
        "player_desc": "Toegang tot je persoonlijke profiel om evaluaties te bekijken en bij te werken.",
        "btn_player": "Inloggen als speler",
        "coach_area": "Coachgebied",
        "coach_desc": "Beperkte toegang voor technische staf.",
        "btn_coach": "Inloggen als coach",
        "logout": "Uitloggen",
        "back_home": "Terug naar start",
        "tech_skills": "Technische vaardigheden",
        "mental_skills": "Tactiek & Mentaal",
        "coach_eval": "Coach Evaluatie & Vergelijking",
        "diff_table": "Verschillentabel (Jij vs Coach)",
        "partner_ranking": "Partner Ranking",
        "comments": "Spelersopmerkingen",
        "radar_progress": "Voortgangshistorie",
        "matches": "Wedstrijden & Resultaten"
    }
}

# Language Selector in Sidebar (1)
with st.sidebar:
    selected_lang = st.selectbox("🌐 Lingua / Language / Idioma", ["Italiano", "Inglese", "Spagnolo", "Danese", "Svedese", "Olandese"])
t = TRANSLATIONS[selected_lang]

# Initialize navigation state
if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "Home"

if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

if "authenticated_player" not in st.session_state:
    st.session_state.authenticated_player = None

# Initialize squad roster and history tracker
if "squad_players" not in st.session_state:
    st.session_state.squad_players = [
        {"fname": "Álvaro", "lname": "Gomez", "side": "Left", "tech": [7, 7, 7, 6, 8, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 6, 5, 7, 5], "c_mental": [7, 6, 6, 6, 7, 6]},
        {"fname": "Yannik", "lname": "Langeslag", "side": "Left", "tech": [8, 6, 7, 7, 7, 5], "mental": [7, 6, 8, 6, 7, 6], "c_tech": [7, 5, 6, 6, 6, 4], "c_mental": [6, 5, 7, 5, 6, 5]},
        {"fname": "Josu", "lname": "Usabiaga", "side": "Right", "tech": [6, 8, 7, 7, 6, 7], "mental": [6, 8, 6, 8, 7, 7], "c_tech": [5, 7, 6, 6, 5, 6], "c_mental": [5, 7, 5, 7, 6, 6]},
        {"fname": "Benjamin", "lname": "Thyrell", "side": "Left", "tech": [7, 7, 8, 6, 7, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 7, 5, 6, 5], "c_mental": [7, 6, 6, 6, 7, 6]},
        {"fname": "Alexander", "lname": "Wennstam", "side": "Left", "tech": [8, 8, 7, 7, 8, 6], "mental": [7, 7, 8, 8, 7, 7], "c_tech": [7, 7, 6, 6, 7, 5], "c_mental": [6, 6, 7, 7, 6, 6]},
        {"fname": "Andrea", "lname": "Lonoce", "side": "Right", "tech": [8, 7, 8, 7, 9, 6], "mental": [9, 7, 8, 8, 9, 7], "c_tech": [8, 7, 8, 7, 9, 6], "c_mental": [9, 7, 8, 8, 9, 7]},
        {"fname": "Mikkel", "lname": "Hoff", "side": "Right", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]},
        {"fname": "Pedro", "lname": "Rios", "side": "Right", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7]},
        {"fname": "Hector", "lname": "Guerrero", "side": "Right", "tech": [7, 7, 7, 7, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 6, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6]},
        {"fname": "Gonzalo", "lname": "Diez de Onate", "side": "Left", "tech": [8, 7, 8, 7, 8, 6], "mental": [8, 7, 8, 8, 8, 7], "c_tech": [7, 6, 7, 6, 7, 5], "c_mental": [7, 6, 7, 7, 7, 6]},
        {"fname": "Julio", "lname": "Morales", "side": "Right", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]},
        {"fname": "Lars", "lname": "Mikkelsen", "side": "Left", "tech": [7, 7, 7, 6, 8, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 6, 5, 7, 5], "c_mental": [7, 6, 6, 6, 7, 6]},
        {"fname": "Joahn", "lname": "Lohman", "side": "Left", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]},
        {"fname": "Nacho", "lname": "Saracho", "side": "Right", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7]},
        {"fname": "Peter", "lname": "Gustafsson", "side": "Left", "tech": [7, 7, 7, 6, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6]},
        {"fname": "Juanjo", "lname": "Lopez Benitez", "side": "Left", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7]},
        {"fname": "Sascha", "lname": "Van De Bilt", "side": "Right", "tech": [7, 7, 7, 6, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6]},
        {"fname": "Fernando", "lname": "Oribe", "side": "Right", "tech": [8, 7, 8, 7, 8, 6], "mental": [8, 7, 8, 8, 8, 7], "c_tech": [7, 6, 7, 6, 7, 5], "c_mental": [7, 6, 7, 7, 7, 6]},
        {"fname": "Doug", "lname": "Ramsay", "side": "Left", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]}
    ]

# Inizializzazione storico valutazioni coach (7) e partite (4) e commenti (5, 6)
if "evaluation_history" not in st.session_state:
    st.session_state.evaluation_history = {f"{p['fname']} {p['lname']}": [p['c_tech'].copy()] for p in st.session_state.squad_players}

if "matches_db" not in st.session_state:
    st.session_state.matches_db = []

if "player_comments" not in st.session_state:
    st.session_state.player_comments = []

if "match_partnerships" not in st.session_state:
    # Simulazione dati storici per il ranking partner (2)
    st.session_state.match_partnerships = {
        "Andrea Lonoce": {"Josu Usabiaga": 5, "Pedro Rios": 4, "Álvaro Gomez": 2},
        "Álvaro Gomez": {"Yannik Langeslag": 6, "Benjamin Thyrell": 3},
        "Josu Usabiaga": {"Andrea Lonoce": 5, "Nacho Saracho": 4}
    }

# --- HOME SELECTION SCREEN ---
if st.session_state.nav_mode == "Home":
    st.title(f"🎾 {t['welcome']}")
    st.markdown(t['select_area'])
    
    col_home1, col_home2 = st.columns(2)
    with col_home1:
        st.markdown(f"### 👤 {t['player_area']}")
        st.markdown(t['player_desc'])
        if st.button(t['btn_player'], use_container_width=True, type="primary"):
            st.session_state.nav_mode = "Player_Login"
            st.rerun()
            
    with col_home2:
        st.markdown(f"### 📋 {t['coach_area']}")
        st.markdown(t['coach_desc'])
        if st.button(t['btn_coach'], use_container_width=True):
            st.session_state.nav_mode = "Coach_Login"
            st.rerun()

# --- PLAYER LOGIN ---
elif st.session_state.nav_mode == "Player_Login":
    st.title("🔐 Player Area Access")
    player_options = [f"{p['fname']} {p['lname']} ({p['side']})" for p in st.session_state.squad_players]
    selected_player_str = st.selectbox("Select your profile:", player_options)
    selected_fname = selected_player_str.split(" ")[0]
    player_pwd_input = st.text_input("Password (Enter your first name)", type="password")
    
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        if st.button("Enter My Profile", type="primary", use_container_width=True):
            if player_pwd_input.strip().lower() == selected_fname.lower():
                st.session_state.authenticated_player = selected_fname
                st.session_state.nav_mode = "Player_Dashboard"
                st.rerun()
            else:
                st.error("❌ Incorrect password!")
    with col_pl2:
        if st.button(t['back_home'], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- COACH LOGIN ---
elif st.session_state.nav_mode == "Coach_Login":
    st.title("🔒 Coach Area Authentication")
    COACH_PASSWORD = "padelcoach2026"
    pwd_input = st.text_input("Coach Password", type="password")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Verify Password", type="primary", use_container_width=True):
            if pwd_input == COACH_PASSWORD:
                st.session_state.authenticated_coach = True
                st.session_state.nav_mode = "Coach_Dashboard"
                st.rerun()
            else:
                st.error("❌ Incorrect password!")
    with col_btn2:
        if st.button(t['back_home'], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- COACH MANAGEMENT DASHBOARD ---
elif st.session_state.nav_mode == "Coach_Dashboard":
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title("📋 Coach Dashboard - Squad, Match Tracking & Comments")
    with col_top2:
        if st.button(t['logout']):
            st.session_state.authenticated_coach = False
            st.session_state.nav_mode = "Home"
            st.rerun()
            
    st.markdown("---")
    
    # Sezioni della Coach Dashboard: Valutazioni, Gestione Partite (4), Visualizzazione Commenti (6)
    coach_tab1, coach_tab2, coach_tab3 = st.tabs(["Valutazioni Squadra", "Gestione Partite & Risultati", "Commenti Giocatori"])
    
    with coach_tab1:
        player_options = [f"{p['fname']} {p['lname']} ({p['side']})" for p in st.session_state.squad_players]
        selected_player_str = st.selectbox("Seleziona giocatore da valutare:", player_options)
        selected_idx = player_options.index(selected_player_str)
        current_player = st.session_state.squad_players[selected_idx]
        p_full_name = f"{current_player['fname']} {current_player['lname']}"
        
        with st.form("coach_edit_form"):
            st.subheader(f"Modifica Valutazioni Coach: {p_full_name}")
            c_tech_inputs = []
            tech_labels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita']
            cols = st.columns(3)
            for i, label in enumerate(tech_labels):
                with cols[i % 3]:
                    val = st.slider(f"{label} (Coach)", 1, 10, int(current_player['c_tech'][i]), key=f"c_t_{i}")
                    c_tech_inputs.append(val)
                    
            c_mental_inputs = []
            mental_labels = ['Chemistry', 'Error Management', 'Positioning', 'Focus', 'Stamina', 'Intensity']
            cols2 = st.columns(3)
            for i, label in enumerate(mental_labels):
                with cols2[i % 3]:
                    val = st.slider(f"{label} (Coach)", 1, 10, int(current_player['c_mental'][i]), key=f"c_m_{i}")
                    c_mental_inputs.append(val)
                    
            submitted_coach = st.form_submit_button("💾 Salva Modifiche Coach", type="primary")
            if submitted_coach:
                st.session_state.squad_players[selected_idx]['c_tech'] = c_tech_inputs
                st.session_state.squad_players[selected_idx]['c_mental'] = c_mental_inputs
                # Traccia lo storico modifiche per il radar (7)
                if p_full_name not in st.session_state.evaluation_history:
                    st.session_state.evaluation_history[p_full_name] = []
                st.session_state.evaluation_history[p_full_name].append(c_tech_inputs.copy())
                st.success(f"Valutazioni aggiornate per {p_full_name}!")

    with coach_tab2:
        # Nuova dashboard inserimento partite e risultati (4)
        st.subheader("Inserisci e Traccia Partite / Match")
        with st.form("match_form"):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                match_date = st.date_input("Data Partita")
                team_a = st.text_input("Coppia 1 (es. Andrea / Josu)")
            with col_m2:
                team_b = st.text_input("Coppia avversaria (es. Alvaro / Yannik)")
                score = st.text_input("Risultato (es. 6-4, 3-6, 7-6)")
            
            submitted_match = st.form_submit_button("Aggiungi Partita")
            if submitted_match:
                st.session_state.matches_db.append({
                    "date": str(match_date),
                    "team_a": team_a,
                    "team_b": team_b,
                    "score": score
                })
                st.success("Partita registrata con successo!")
        
        st.markdown("### Storico Partite Registrate")
        if st.session_state.matches_db:
            df_matches = pd.DataFrame(st.session_state.matches_db)
            st.dataframe(df_matches, use_container_width=True)
        else:
            st.info("Nessuna partita registrata.")

    with coach_tab3:
        # Visualizzazione di tutti i commenti dei giocatori (6)
        st.subheader("Tutti i commenti inseriti dai giocatori")
        if st.session_state.player_comments:
            for comment in st.session_state.player_comments:
                st.info(f"**Da:** {comment['author']} | **Su:** {comment['target']} | **Data:** {comment['date']}\n\n\"{comment['text']}\"")
        else:
            st.info("Nessun commento presente al momento.")

    if st.button(t['back_home']):
        st.session_state.nav_mode = "Home"
        st.rerun()

# --- INDIVIDUAL PLAYER DASHBOARD ---
elif st.session_state.nav_mode == "Player_Dashboard":
    current_player = next((p for p in st.session_state.squad_players if p['fname'] == st.session_state.authenticated_player), None)
    p_full_name = f"{current_player['fname']} {current_player['lname']}"
    
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title(f"👤 Dashboard Personale: {p_full_name} ({current_player['side']})")
    with col_top2:
        if st.button(t['logout']):
            st.session_state.authenticated_player = None
            st.session_state.nav_mode = "Home"
            st.rerun()
            
    st.markdown("---")
    
    # Tabs del giocatore inclusi i nuovi requisiti (2, 5, 7)
    pl_tab1, pl_tab2, pl_tab3, pl_tab4 = st.tabs(["Valutazioni & Confronto", "Ranking Partner (2)", "Commenti Altri Giocatori (5)", "Storico & Grafico Radar (7)"])
    
    with pl_tab1:
        st.subheader("Le tue autovalutazioni e confronto con il Coach")
        p_tech = current_player['tech']
        c_tech = current_player['c_tech']
        
        tech_labels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita']
        
        # Modifica autovalutazione
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### Autovalutazione Tecnica")
            new_p_tech = []
            for i, label in enumerate(tech_labels):
                val = st.slider(label, 1, 10, int(p_tech[i]), key=f"pl_tech_{i}")
                new_p_tech.append(val)
            current_player['tech'] = new_p_tech
            
        with col_s2:
            st.markdown(f"#### 📊 {t['diff_table']}")
            diff_data = []
            for i, label in enumerate(tech_labels):
                self_val = current_player['tech'][i]
                coach_val = current_player['c_tech'][i]
                delta = self_val - coach_val
                # Evidenzia in rosso se c'è discrepanza (3)
                discrepancy = abs(delta) >= 2
                diff_data.append({
                    "Skill": label,
                    "Tuo Valore": self_val,
                    "Coach": coach_val,
                    "Delta": delta,
                    "Discrepanza": "⚠️" if discrepancy else "OK"
                })
            
            df_diff = pd.DataFrame(diff_data)
            
            def color_discrepancy(val):
                color = 'color: red; font-weight: bold;' if val == "⚠️" else ''
                return color

            st.dataframe(df_diff.style.applymap(color_discrepancy, subset=['Discrepanza']), use_container_width=True)

    with pl_tab2:
        # Ranking dei giocatori con cui si gioca di più (2)
        st.subheader("🎾 Ranking Partner Più Frequenti")
        st.markdown("Ecco i giocatori con cui hai disputato più match in squadra:")
        
        partners = st.session_state.match_partnerships.get(p_full_name, {"Josu Usabiaga": 4, "Pedro Rios": 3, "Álvaro Gomez": 2})
        df_partners = pd.DataFrame(list(partners.items()), columns=["Partner", "Partite Giocate"]).sort_values(by="Partite Giocate", ascending=False)
        st.table(df_partners)

    with pl_tab3:
        # Campo commenti su altri giocatori (5)
        st.subheader("💬 Lascia un commento su un compagno di squadra")
        all_other_players = [f"{p['fname']} {p['lname']}" for p in st.session_state.squad_players if f"{p['fname']} {p['lname']}" != p_full_name]
        
        with st.form("comment_form"):
            target_player = st.selectbox("Seleziona compagno:", all_other_players)
            comment_text = st.text_area("Scrivi il tuo commento o feedback:")
            submit_comment = st.form_submit_button("Invia Commento")
            if submit_comment and comment_text.strip():
                st.session_state.player_comments.append({
                    "author": p_full_name,
                    "target": target_player,
                    "text": comment_text,
                    "date": str(pd.Timestamp.now().date())
                })
                st.success("Commento inviato con successo!")
        
        st.markdown("### Commenti ricevuti o pubblicati")
        for c in st.session_state.player_comments:
            if c['author'] == p_full_name or c['target'] == p_full_name:
                st.write(f"- **Da {c['author']} a {c['target']}**: *\"{c['text']}\"* ({c['date']})")

    with pl_tab4:
        # Grafico a tela di ragno / storico miglioramenti (7)
        st.subheader("📈 Storico dei Miglioramenti (Modifiche Coach)")
        history = st.session_state.evaluation_history.get(p_full_name, [current_player['c_tech']])
        
        if len(history) > 1:
            st.markdown("Il coach ha aggiornato la tua valutazione nel tempo. Ecco l'evoluzione dei punteggi tecnici:")
            df_history = pd.DataFrame(history, columns=tech_labels)
            df_history.index = [f"Revisione {i+1}" for i in range(len(history))]
            st.line_chart(df_history)
        else:
            st.info("Non ci sono ancora abbastanza revisioni storiche registrate dal coach per generare il grafico evolutivo. Verrà aggiornato non appena il coach modificherà le valutazioni.")

    if st.button(t['back_home']):
        st.session_state.nav_mode = "Home"
        st.rerun()
