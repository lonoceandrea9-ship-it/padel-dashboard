import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Streamlit page configuration
st.set_page_config(
    page_title="Padel Performance Hub",
    page_icon="🎾",
    layout="wide"
)

# --- CUSTOM CSS: SFONDO BLU SCURO, TESTO BIANCO, HEADER, BOTTONI E TABELLE PERSONALIZZATI ---
st.markdown("""
    <style>
    /* Sfondo generale dell'applicazione */
    .stApp {
        background-color: #0d1b2a;
        color: #ffffff;
    }
    
    /* Rimozione della barra bianca superiore (Header di Streamlit) e colorazione in blu scuro */
    header[data-testid="stHeader"] {
        background-color: #0d1b2a !important;
    }
    
    /* Colore dei testi principali, intestazioni e label */
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown, div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1b263b;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Pulsanti specifici di accesso (Allenatore / Giocatore) in rosso brillante */
    .element-container:has(button:contains("Allenatore")) button,
    .element-container:has(button:contains("Giocatore")) button {
        background-color: #dc2626 !important;
        color: white !important;
        border-color: #b91c1c !important;
    }
    .element-container:has(button:contains("Allenatore")) button:hover,
    .element-container:has(button:contains("Giocatore")) button:hover {
        background-color: #b91c1c !important;
        color: white !important;
    }

    /* Tutti i bottoni Esci / Logout / Torna alla Home in Blu scuro (inclusi login giocatore/allenatore) */
    .element-container:has(button:contains("Esci")) button,
    .element-container:has(button:contains("Logout")) button,
    .element-container:has(button:contains("Torna alla Home")) button,
    div.stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #1d4ed8 !important;
    }
    
    /* Forza lo stile blu scuro per il bottone secondario/Torna alla Home nei form di login */
    div.stFormSubmitButton > button, 
    button[kind="secondary"] {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #1d4ed8 !important;
    }

    .element-container:has(button:contains("Esci")) button:hover,
    .element-container:has(button:contains("Logout")) button:hover,
    .element-container:has(button:contains("Torna alla Home")) button:hover,
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* Stile personalizzato per le tabelle / data_editor in tema scuro */
    div[data-testid="stDataFrame"] > div, div[data-testid="stTable"] {
        background-color: #1b263b !important;
        border: 1px solid #334155 !important;
        border-radius: 8px;
    }
    
    table {
        color: #ffffff !important;
        background-color: #1b263b !important;
    }
    
    th {
        background-color: #0d1b2a !important;
        color: #ffffff !important;
        border-bottom: 2px solid #334155 !important;
    }
    
    td {
        background-color: #1b263b !important;
        color: #ffffff !important;
        border-bottom: 1px solid #334155 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- TRADUZIONI (LINGUE) ---
translations = {
    "Italiano": {
        "welcome": "Benvenuto nel Padel Performance Hub",
        "select_area": "Seleziona la tua area di accesso per continuare:",
        "player_area": "Area Giocatore",
        "player_desc": "Accedi alla tua scheda personale protetta da password per visualizzare e aggiornare le tue valutazioni.",
        "player_btn": "Accedi come Giocatore",
        "coach_area": "Area Allenatore",
        "coach_desc": "Accesso riservato allo staff tecnico per la gestione dei dati, la pianificazione e le partite.",
        "coach_btn": "Accedi come Allenatore",
        "login_player_title": "Accesso Area Giocatore",
        "login_player_sub": "Seleziona il tuo nome e inserisci la tua password (il tuo nome di battesimo).",
        "profile_select": "Seleziona il tuo profilo:",
        "pwd_label": "Password (Il tuo nome di battesimo)",
        "enter_card": "Entra nella mia scheda",
        "back_home": "Torna alla Home",
        "wrong_pwd": "Password errata! Ricorda che la password è il tuo nome di battesimo.",
        "coach_login_title": "Autenticazione Area Allenatore",
        "coach_login_sub": "Inserisci la password di sicurezza per accedere alle funzioni di gestione.",
        "coach_pwd_label": "Password Allenatore",
        "verify_pwd": "Verifica Password",
        "logout": "Esci",
        "tech_skills": "Competenze Tecniche",
        "mental_skills": "Attitudine e Tattica (Mentali)",
        "partners_tab": "Ranking Partner",
        "history_tab": "Storico & Miglioramenti",
        "comments_tab": "Commenti & Feedback",
        "matches_dash": "Gestione Partite (Coach)",
        "all_comments": "Tutti i Commenti (Coach)"
    }
}

# --- LISTA DELLE SKILLS AGGIORNATE ---
TECH_SKILLS = ["Volley", "Bandeja", "Remate", "Smash", "Bajada", "Chiquita", "Lob"]
MENTAL_SKILLS = ["Attitudine positiva", "Supporto partner", "Gestione errori", "Posizionamento", "Resistenza", "Intensità", "Coachability"]
ALL_SKILLS = TECH_SKILLS + MENTAL_SKILLS

# --- INIZIALIZZAZIONE STATO ---
if "language" not in st.session_state:
    st.session_state.language = "Italiano"

if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "Home"

if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

if "authenticated_player" not in st.session_state:
    st.session_state.authenticated_player = None

# Lista giocatori con supporto per mano, stile di gioco e note coach
if "squad_data" not in st.session_state:
    st.session_state.squad_data = [
        {"fname": "Álvaro", "lname": "Gomez", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1,
         "tech": [7, 7, 6, 7, 6, 6, 7], "mental": [8, 7, 7, 7, 8, 7, 8], "c_tech": [6, 6, 5, 6, 5, 5, 6], "c_mental": [7, 6, 6, 6, 7, 6, 7], "play_style": "equilibrated", "player_play_style": "equilibrated", "history": [], "coach_note": "", "partners": {"Yannik Langeslag": 12, "Josu Usabiaga": 8}, "comments": []},
        {"fname": "Yannik", "lname": "Langeslag", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1,
         "tech": [8, 6, 7, 7, 7, 5, 6], "mental": [7, 6, 8, 6, 7, 6, 7], "c_tech": [7, 5, 6, 6, 6, 4, 5], "c_mental": [6, 5, 7, 5, 6, 5, 6], "play_style": "offensive", "player_play_style": "offensive", "history": [], "coach_note": "", "partners": {"Álvaro Gomez": 12}, "comments": []},
        {"fname": "Josu", "lname": "Usabiaga", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1,
         "tech": [6, 8, 7, 7, 6, 7, 7], "mental": [6, 8, 6, 8, 7, 7, 8], "c_tech": [5, 7, 6, 6, 5, 6, 6], "c_mental": [5, 7, 5, 7, 6, 6, 7], "play_style": "defensive", "player_play_style": "defensive", "history": [], "coach_note": "", "partners": {"Álvaro Gomez": 8}, "comments": []},
        {"fname": "Benjamin", "lname": "Thyrell", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1,
         "tech": [7, 7, 8, 6, 7, 6, 7], "mental": [8, 7, 7, 7, 8, 7, 8], "c_tech": [6, 6, 7, 5, 6, 5, 6], "c_mental": [7, 6, 6, 6, 7, 6, 7], "play_style": "counterattack", "player_play_style": "counterattack", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Alexander", "lname": "Wennstam", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1,
         "tech": [8, 8, 7, 7, 8, 6, 7], "mental": [7, 7, 8, 8, 7, 7, 8], "c_tech": [7, 7, 6, 6, 7, 5, 6], "c_mental": [6, 6, 7, 7, 6, 6, 7], "play_style": "equilibrated", "player_play_style": "equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Andrea", "lname": "Lonoce", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1,
         "tech": [8, 7, 8, 7, 9, 6, 8], "mental": [9, 7, 8, 8, 9, 7, 9], "c_tech": [8, 7, 8, 7, 9, 6, 8], "c_mental": [9, 7, 8, 8, 9, 7, 9], "play_style": "offensive", "player_play_style": "offensive", "history": [], "coach_note": "", "partners": {"Alexander Wennstam": 14}, "comments": []},
        {"fname": "Mikkel", "lname": "Hoff", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1,
         "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "defensive", "player_play_style": "defensive", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Pedro", "lname": "Rios", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1,
         "tech": [8, 8, 8, 7, 8, 7, 7], "mental": [8, 8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6, 6], "c_mental": [7, 7, 7, 7, 7, 7, 7], "play_style": "equilibrated", "player_play_style": "equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Hector", "lname": "Guerrero", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1,
         "tech": [7, 7, 7, 7, 7, 6, 7], "mental": [7, 7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 6, 6, 5, 6], "c_mental": [6, 6, 6, 6, 6, 6, 6], "play_style": "counterattack", "player_play_style": "counterattack", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Gonzalo", "lname": "Diez de Onate", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1,
         "tech": [8, 7, 8, 7, 8, 6, 7], "mental": [8, 7, 8, 8, 8, 7, 8], "c_tech": [7, 6, 7, 6, 7, 5, 6], "c_mental": [7, 6, 7, 7, 7, 6, 7], "play_style": "equilibrated", "player_play_style": "equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Julio", "lname": "Morales", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1,
         "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "offensive", "player_play_style": "offensive", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Lars", "lname": "Mikkelsen", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0,
         "tech": [7, 7, 7, 6, 8, 6, 7], "mental": [8, 7, 7, 7, 8, 7, 8], "c_tech": [6, 6, 6, 5, 7, 5, 6], "c_mental": [7, 6, 6, 6, 7, 6, 7], "play_style": "equilibrated", "player_play_style": "equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Jairo", "lname": "Lopez", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0,
         "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "defensive", "player_play_style": "defensive", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Nacho", "lname": "Saracho", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 0,
         "tech": [8, 8, 8, 7, 8, 7, 7], "mental": [8, 8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6, 6], "c_mental": [7, 7, 7, 7, 7, 7, 7], "play_style": "counterattack", "player_play_style": "counterattack", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Peter", "lname": "Gustafsson", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0,
         "tech": [7, 7, 7, 6, 7, 6, 7], "mental": [7, 7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5, 6], "c_mental": [6, 6, 6, 6, 6, 6, 6], "play_style": "equilibrated", "player_play_style": "equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Juanjo", "lname": "Lopez Benitez", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0,
         "tech": [8, 8, 8, 7, 8, 7, 7], "mental": [8, 8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6, 6], "c_mental": [7, 7, 7, 7, 7, 7, 7], "play_style": "offensive", "player_play_style": "offensive", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Sascha", "lname": "Van De Bilt", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 0,
         "tech": [7, 7, 7, 6, 7, 6, 7], "mental": [7, 7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5, 6], "c_mental": [6, 6, 6, 6, 6, 6, 6], "play_style": "defensive", "player_play_style": "defensive", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Fernando", "lname": "Oribe", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 0,
         "tech": [8, 7, 8, 7, 8, 6, 7], "mental": [8, 7, 8, 8, 8, 7, 8], "c_tech": [7, 6, 7, 6, 7, 5, 6], "c_mental": [7, 6, 7, 7, 7, 6, 7], "play_style": "counterattack", "player_play_style": "counterattack", "history": [], "coach_note": "", "partners": {}, "comments": []},
        {"fname": "Doug", "lname": "Ramsay", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0,
         "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "equilibrated", "player_play_style": "equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": []}
    ]

# Controllo e correzione automatica per sessioni salvate
for p in st.session_state.squad_data:
    if "hand" not in p: p["hand"] = "Mancino" if p.get("side") == "Left" else "Destro"
    if "coach_note" not in p: p["coach_note"] = ""
    if "play_style" not in p: p["play_style"] = "equilibrated"
    if "player_play_style" not in p: p["player_play_style"] = p.get("play_style", "equilibrated")
    if "trainings" not in p: p["trainings"] = 1
    if "participated" not in p: p["participated"] = 1
    
    if len(p["tech"]) != len(TECH_SKILLS): p["tech"] = [7] * len(TECH_SKILLS)
    if len(p["mental"]) != len(MENTAL_SKILLS): p["mental"] = [7] * len(MENTAL_SKILLS)
    if len(p["c_tech"]) != len(TECH_SKILLS): p["c_tech"] = [6] * len(TECH_SKILLS)
    if len(p["c_mental"]) != len(MENTAL_SKILLS): p["c_mental"] = [6] * len(MENTAL_SKILLS)

if "match_results" not in st.session_state:
    st.session_state.match_results = []

squad_players = st.session_state.squad_data
lang_dict = translations.get(st.session_state.language, translations["Italiano"])

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/padel.png", width=64)
    st.title("Padel Hub")
    selected_lang = st.selectbox("🌐 Lingua / Language", ["Italiano"], index=0)
    
    st.markdown("---")
    if st.session_state.authenticated_coach:
        st.success("🔒 Coach Logged In")
        if st.button("Logout Coach"):
            st.session_state.authenticated_coach = False
            st.session_state.nav_mode = "Home"
            st.rerun()
    elif st.session_state.authenticated_player:
        st.success(f"👤 Player: {st.session_state.authenticated_player}")
        if st.button("Logout Player"):
            st.session_state.authenticated_player = None
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- HOME SELECTION ---
if st.session_state.nav_mode == "Home":
    st.title(f"🎾 {lang_dict['welcome']}")
    st.markdown(lang_dict['select_area'])
    
    col_home1, col_home2 = st.columns(2)
    with col_home1:
        st.markdown(f"### 👤 {lang_dict['player_area']}")
        st.markdown(lang_dict['player_desc'])
        if st.button(lang_dict['player_btn'], use_container_width=True, type="primary"):
            st.session_state.nav_mode = "Player_Login"
            st.rerun()
            
    with col_home2:
        st.markdown(f"### 📋 {lang_dict['coach_area']}")
        st.markdown(lang_dict['coach_desc'])
        if st.button(lang_dict['coach_btn'], use_container_width=True, type="primary"):
            st.session_state.nav_mode = "Coach_Login"
            st.rerun()

# --- LOGIN GIOCATORE ---
elif st.session_state.nav_mode == "Player_Login":
    st.title(f"🔐 {lang_dict['login_player_title']}")
    st.markdown(lang_dict['login_player_sub'])
    
    player_options = [f"{p['fname']} {p['lname']} ({p['side']})" for p in squad_players]
    selected_player_str = st.selectbox(lang_dict['profile_select'], player_options)
    selected_fname = selected_player_str.split(" ")[0]
    
    player_pwd_input = st.text_input(lang_dict['pwd_label'], type="password")
    
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        if st.button(lang_dict['enter_card'], type="primary", use_container_width=True):
            if player_pwd_input.strip().lower() == selected_fname.lower():
                st.session_state.authenticated_player = selected_fname
                st.session_state.nav_mode = "Player_Dashboard"
                st.rerun()
            else:
                st.error(f"❌ {lang_dict['wrong_pwd']}")
    with col_pl2:
        if st.button(lang_dict['back_home'], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- LOGIN ALLENATORE ---
elif st.session_state.nav_mode == "Coach_Login":
    st.title(f"🔒 {lang_dict['coach_login_title']}")
    st.markdown(lang_dict['coach_login_sub'])
    
    COACH_PASSWORD = "padelcoach2026"
    pwd_input = st.text_input(lang_dict['coach_pwd_label'], type="password")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(lang_dict['verify_pwd'], type="primary", use_container_width=True):
            if pwd_input == COACH_PASSWORD:
                st.session_state.authenticated_coach = True
                st.session_state.nav_mode = "Coach"
                st.rerun()
            else:
                st.error("❌ Password errata! Riprova.")
    with col_btn2:
        if st.button(lang_dict['back_home'], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- DASHBOARD GIOCATORE ---
elif st.session_state.nav_mode == "Player_Dashboard":
    current_player = next((p for p in squad_players if p['fname'] == st.session_state.authenticated_player), None)
    
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title(f"👤 {current_player['fname']} {current_player['lname']} ({current_player['side']})")
    with col_top2:
        if st.button(lang_dict['logout']):
            st.session_state.authenticated_player = None
            st.session_state.nav_mode = "Home"
            st.rerun()
            
    st.markdown("---")
    
    tab_eval, tab_partners, tab_history, tab_comments = st.tabs([
        "📊 Autovalutazione & Coach", 
        f"🏆 {lang_dict['partners_tab']}", 
        f"📈 {lang_dict['history_tab']}", 
        f"💬 {lang_dict['comments_tab']}"
    ])
    
    with tab_eval:
        st.subheader("📊 Gestione e Confronto Valutazioni")
        st.markdown("Regola i cursori e seleziona il tuo stile di gioco per la tua autovalutazione. A sinistra trovi le competenze **Tecniche** e a destra quelle **Mentali**.")
        
        style_options = ["offensive", "defensive", "equilibrated", "counterattack"]
        
        col_eval_left, col_eval_right = st.columns(2)
        
        new_tech_vals = []
        new_mental_vals = []
        
        with col_eval_left:
            st.markdown(f"**{lang_dict['tech_skills']}**")
            for i, skill in enumerate(TECH_SKILLS):
                c1, c2 = st.columns(2)
                with c1:
                    val = st.slider(f"Tu - {skill}", 1, 10, int(current_player['tech'][i]), key=f"p_tech_{i}")
                    new_tech_vals.append(val)
                with c2:
                    st.slider(f"Coach - {skill}", 1, 10, int(current_player['c_tech'][i]), disabled=True, key=f"c_tech_view_{i}")

        with col_eval_right:
            st.markdown(f"**{lang_dict['mental_skills']}**")
            for i, skill in enumerate(MENTAL_SKILLS):
                c1, c2 = st.columns(2)
                with c1:
                    val = st.slider(f"Tu - {skill}", 1, 10, int(current_player['mental'][i]), key=f"p_mental_{i}")
                    new_mental_vals.append(val)
                with c2:
                    st.slider(f"Coach - {skill}", 1, 10, int(current_player['c_mental'][i]), disabled=True, key=f"c_mental_view_{i}")
                
        st.markdown("---")
        current_p_style = current_player.get("player_play_style", "equilibrated")
        if current_p_style not in style_options: current_p_style = "equilibrated"
        new_player_style = st.selectbox("Seleziona il tuo Stile di Gioco (Autovalutazione):", options=style_options, index=style_options.index(current_p_style))
                
        if st.button("Salva Autovalutazione", type="primary"):
            current_player['tech'] = new_tech_vals
            current_player['mental'] = new_mental_vals
            current_player['player_play_style'] = new_player_style
            st.success("Autovalutazione salvata con successo!")
            st.rerun()

        st.markdown("---")
        st.subheader("🕸️ Grafici a Tela di Ragno (Confronto Separato)")
        
        all_skills_labels = TECH_SKILLS + MENTAL_SKILLS
        player_full_vals = current_player['tech'] + current_player['mental']
        coach_full_vals = current_player['c_tech'] + current_player['c_mental']
        
        categories = all_skills_labels + [all_skills_labels[0]]
        p_vals_radar = player_full_vals + [player_full_vals[0]]
        c_vals_radar = coach_full_vals + [coach_full_vals[0]]
        
        radar_col1, radar_col2 = st.columns(2)
        
        with radar_col1:
            st.markdown("### Autovalutazione Giocatore")
            p_style_display = current_player.get("player_play_style", "equilibrated").capitalize()
            st.markdown(f"**Stile di Gioco:** {p_style_display}")
            
            fig_player = go.Figure()
            fig_player.add_trace(go.Scatterpolar(
                r=p_vals_radar,
                theta=categories,
                fill='toself',
                name='Autovalutazione',
                line_color='#1f77b4'
            ))
            fig_player.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 10], color='white', gridcolor='#334155'),
                    angularaxis=dict(gridcolor='#334155')
                ),
                showlegend=False,
                height=420,
                margin=dict(l=40, r=40, t=10, b=20)
            )
            st.plotly_chart(fig_player, use_container_width=True)
            
        with radar_col2:
            st.markdown("### Valutazione Coach")
            play_style_display = current_player.get("play_style", "equilibrated").capitalize()
            st.markdown(f"**Stile di Gioco:** {play_style_display}")
            
            fig_coach = go.Figure()
            fig_coach.add_trace(go.Scatterpolar(
                r=c_vals_radar,
                theta=categories,
                fill='toself',
                name='Coach',
                line_color='#ff7f0e'
            ))
            fig_coach.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 10], color='white', gridcolor='#334155'),
                    angularaxis=dict(gridcolor='#334155')
                ),
                showlegend=False,
                height=420,
                margin=dict(l=40, r=40, t=10, b=20)
            )
            st.plotly_chart(fig_coach, use_container_width=True)

        st.markdown("---")
        st.subheader("📋 Tabelle delle Differenze (Tu vs Coach)")
        
        diff_tech_rows = []
        for i, skill in enumerate(TECH_SKILLS):
            p_v = current_player['tech'][i]
            c_v = current_player['c_tech'][i]
            diff = p_v - c_v
            
            if diff > 0:
                diff_display = f"<span style='color:#2ecc71; font-weight:bold;'>+{diff}</span>"
            elif diff < 0:
                diff_display = f"<span style='color:#e74c3c; font-weight:bold;'>{diff}</span>"
            else:
                diff_display = "<span style='color:#bdc3c7; font-weight:bold;'>0</span>"
                
            diff_tech_rows.append({"Tecnica": skill, "Tu": p_v, "Coach": c_v, "Diff": diff_display})

        diff_mental_rows = []
        for i, skill in enumerate(MENTAL_SKILLS):
            p_v = current_player['mental'][i]
            c_v = current_player['c_mental'][i]
            diff = p_v - c_v
            
            if diff > 0:
                diff_display = f"<span style='color:#2ecc71; font-weight:bold;'>+{diff}</span>"
            elif diff < 0:
                diff_display = f"<span style='color:#e74c3c; font-weight:bold;'>{diff}</span>"
            else:
                diff_display = "<span style='color:#bdc3c7; font-weight:bold;'>0</span>"
                
            diff_mental_rows.append({"Mentale": skill, "Tu": p_v, "Coach": c_v, "Diff": diff_display})

        t_col1, t_col2 = st.columns(2)
        with t_col1:
            st.markdown("#### 🎾 Caratteristiche Tecniche")
            st.markdown(pd.DataFrame(diff_tech_rows).to_html(escape=False, index=False), unsafe_allow_html=True)
            
        with t_col2:
            st.markdown("#### 🧠 Caratteristiche Mentali")
            st.markdown(pd.DataFrame(diff_mental_rows).to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab_partners:
        st.subheader("🏆 Gestione Ranking Partner (Fino a 5)")
        all_colleagues = [f"{p['fname']} {p['lname']}" for p in squad_players if p['fname'] != current_player['fname']]
        current_partners = current_player.get("partners", {})
        
        with st.form("partners_form"):
            new_partners_dict = {}
            for i in range(5):
                col_p1, col_p2 = st.columns([3, 1])
                existing_keys = list(current_partners.keys())
                default_partner = existing_keys[i] if i < len(existing_keys) else (all_colleagues[0] if all_colleagues else "")
                default_val = int(current_partners.get(default_partner, 5 - i))
                
                with col_p1:
                    p_sel = st.selectbox(f"Partner #{i+1}", all_colleagues, index=all_colleagues.index(default_partner) if default_partner in all_colleagues else 0, key=f"partner_sel_{i}")
                with col_p2:
                    p_score = st.number_input(f"Match #{i+1}", min_value=1, max_value=50, value=default_val, key=f"partner_val_{i}")
                
                if p_sel:
                    new_partners_dict[p_sel] = p_score
                    
            if st.form_submit_button("Salva Ranking Partner", type="primary"):
                current_player["partners"] = new_partners_dict
                st.success("Ranking partner aggiornato con successo!")
                st.rerun()
                
        st.markdown("### Classifica Attuale:")
        if current_player.get("partners"):
            st.table(pd.DataFrame(list(current_player["partners"].items()), columns=["Compagno", "Match / Preferenza"]).sort_values(by="Match / Preferenza", ascending=False).reset_index(drop=True))
        else:
            st.info("Nessun partner configurato.")

    with tab_history:
        st.subheader("📈 Storico & Evoluzione Valutazioni Coach")
        history_records = current_player.get("history", [])
        if history_records:
            for idx, hist in enumerate(history_records):
                st.markdown(f"**Aggiornamento #{idx+1} ({hist.get('date', '')})**")
                st.json(hist.get('values'))
        else:
            st.info("Nessuna modifica precedente registrata dal coach.")

    with tab_comments:
        st.subheader("💬 Commenti e Feedback")
        
        st.markdown("### 📋 Nota Ufficiale del Coach")
        coach_note_val = current_player.get("coach_note", "")
        if coach_note_val.strip():
            st.info(coach_note_val)
        else:
            st.markdown("*Nessuna nota inserita al momento dal coach.*")
            
        st.markdown("---")
        st.subheader("💬 Feedback dei compagni")
        target_colleagues = [f"{p['fname']} {p['lname']}" for p in squad_players if p['fname'] != current_player['fname']]
        selected_target = st.selectbox("Seleziona compagno:", target_colleagues)
        comment_text = st.text_area("Nota sul compagno:")
        if st.button("Invia Nota"):
            if comment_text.strip():
                target_p = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_target), None)
                if target_p:
                    target_p.setdefault("comments", []).append({
                        "from": f"{current_player['fname']} {current_player['lname']}",
                        "text": comment_text,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Nota inviata!")
            else:
                st.warning("Il testo non può essere vuoto.")
        
        st.markdown("### Ricevuti:")
        for c in current_player.get("comments", []):
            st.info(f"**Da {c['from']}** ({c['date']}): {c['text']}")

# --- AREA ALLENATORE ---
elif st.session_state.nav_mode == "Coach" and st.session_state.authenticated_coach:
    st.title("📋 Dashboard Allenatore")
    if st.button("Esci da Area Allenatore"):
        st.session_state.authenticated_coach = False
        st.session_state.nav_mode = "Home"
        st.rerun()
        
    coach_tab1, coach_tab_evals, coach_tab2, coach_tab3, coach_tab_pairing = st.tabs([
        "👥 Gestione Squadra & Presenze", 
        "✏️ Gestione Voti Coach",
        "📅 Gestione Partite", 
        "💬 Tutti i Commenti",
        "🤖 Pairing Coppie Automatico"
    ])
    
    with coach_tab1:
        st.subheader("👥 Elenco Intero Giocatori, Ruoli e Presenze")
        st.markdown("Modifica direttamente qui il **Role (Left/Right)**, la **Mano (Destro/Mancino)**, lo **Stile di Gioco (Play Style)**, i **Trainings** e i **Participated**. La colonna **Commitment (%)** si aggiorna in tempo reale.")
        
        df_summary_data = []
        for p in squad_players:
            t = int(p.get("trainings", 1))
            part = int(p.get("participated", 1))
            pct_val = int(round((part / t) * 100)) if t > 0 else 0
            df_summary_data.append({
                "Nome": p["fname"],
                "Cognome": p["lname"],
                "Role": p["side"],
                "Mano": p.get("hand", "Destro"),
                "Play Style": p.get("play_style", "equilibrated"),
                "Trainings": t,
                "Participated": part,
                "Commitment (%)": f"{pct_val}%"
            })
        
        df_editable = pd.DataFrame(df_summary_data)
        
        edited_df = st.data_editor(
            df_editable,
            column_config={
                "Role": st.column_config.SelectboxColumn(
                    "Role (Side)",
                    options=["Left", "Right"],
                    required=True
                ),
                "Mano": st.column_config.SelectboxColumn(
                    "Mano",
                    options=["Destro", "Mancino"],
                    required=True
                ),
                "Play Style": st.column_config.SelectboxColumn(
                    "Play Style",
                    options=["offensive", "defensive", "equilibrated", "counterattack"],
                    required=True
                ),
                "Trainings": st.column_config.NumberColumn("Trainings", min_value=0, max_value=50, step=1),
                "Participated": st.column_config.NumberColumn("Participated", min_value=0, max_value=50, step=1),
                "Commitment (%)": st.column_config.TextColumn("Commitment (%)", disabled=True)
            },
            hide_index=True,
            use_container_width=True,
            height=600,
            key="coach_squad_editor"
        )
        
        has_changed = False
        for idx, row in edited_df.iterrows():
            curr_t = int(row["Trainings"])
            curr_p = int(row["Participated"])
            curr_role = row["Role"]
            curr_hand = row["Mano"]
            curr_style = row["Play Style"]
            
            if (curr_t != squad_players[idx]["trainings"] or 
                curr_p != squad_players[idx]["participated"] or 
                curr_role != squad_players[idx]["side"] or
                curr_hand != squad_players[idx].get("hand", "Destro") or
                curr_style != squad_players[idx].get("play_style", "equilibrated")):
                
                squad_players[idx]["side"] = curr_role
                squad_players[idx]["hand"] = curr_hand
                squad_players[idx]["play_style"] = curr_style
                squad_players[idx]["trainings"] = curr_t
                squad_players[idx]["participated"] = curr_p
                calc_pct = int(round((curr_p / curr_t) * 100)) if curr_t > 0 else 0
                squad_players[idx]["commitment"] = f"{calc_pct}%"
                has_changed = True

        if has_changed:
            st.rerun()

        st.markdown("---")
        st.subheader("🎯 Gruppi di Lavoro e Miglioramento Mirato")
        st.markdown("Raggruppamento automatico di tutti i giocatori in base alle carenze comuni rilevate nelle valutazioni del coach (valori ≤ 6).")
        
        skill_groups = {skill: [] for skill in ALL_SKILLS}
        for p in squad_players:
            p_coach_vals = p['c_tech'] + p['c_mental']
            for i, skill in enumerate(ALL_SKILLS):
                if p_coach_vals[i] <= 6:
                    skill_groups[skill].append(f"{p['fname']} {p['lname']} (Voto: {p_coach_vals[i]})")
                    
        active_groups = {k: v for k, v in skill_groups.items() if len(v) > 0}
        
        if active_groups:
            cols = st.columns(2)
            col_idx = 0
            for skill, members in active_groups.items():
                with cols[col_idx % 2]:
                    with st.expander(f"📌 Area di miglioramento: **{skill}** ({len(members)} giocatori)"):
                        for m in members:
                            st.markdown(f"- {m}")
                col_idx += 1
        else:
            st.info("Nessuna criticità rilevata (tutti i giocatori hanno voti superiori a 6).")

    with coach_tab_evals:
        st.subheader("✏️ Gestione Voti Coach & Profilo di Gioco")
        st.markdown("Seleziona un giocatore per aggiornare le sue valutazioni, il profilo tattico e la nota ufficiale.")
        
        selected_player_name = st.selectbox("Seleziona giocatore da valutare:", [f"{p['fname']} {p['lname']}" for p in squad_players], key="coach_eval_select")
        p_obj = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_player_name), None)
        
        if p_obj:
            with st.form("coach_eval_form"):
                st.markdown(f"**Modifica voti e profilo per: {selected_player_name}**")
                
                style_options = ["offensive", "defensive", "equilibrated", "counterattack"]
                current_style = p_obj.get("play_style", "equilibrated")
                if current_style not in style_options:
                    current_style = "equilibrated"
                
                st.markdown("### Valutazione Coach")
                selected_style = st.selectbox(
                    "Stile di Gioco",
                    options=style_options,
                    index=style_options.index(current_style)
                )
                
                st.markdown("---")
                st.markdown("📝 **Nota / Commento Ufficiale del Coach (Visibile al giocatore)**")
                new_coach_note = st.text_area("Scrivi qui il commento per il giocatore...", value=p_obj.get("coach_note", ""), key="coach_note_input")
                
                st.markdown("---")
                col_c_left, col_c_right = st.columns(2)
                
                c_tech_new = []
                c_mental_new = []
                
                with col_c_left:
                    st.markdown("🎾 *Competenze Tecniche (Coach)*")
                    for idx, t_label in enumerate(TECH_SKILLS):
                        val = st.slider(f"Coach - {t_label}", 1, 10, int(p_obj['c_tech'][idx]), key=f"scoach_tech_{idx}")
                        c_tech_new.append(val)
                
                with col_c_right:
                    st.markdown("🧠 *Competenze Mentali (Coach)*")
                    for idx, m_label in enumerate(MENTAL_SKILLS):
                        val = st.slider(f"Coach - {m_label}", 1, 10, int(p_obj['c_mental'][idx]), key=f"scoach_mental_{idx}")
                        c_mental_new.append(val)
                        
                if st.form_submit_button("Salva Voti, Profilo e Nota Coach", type="primary"):
                    p_obj.setdefault("history", []).append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "values": c_tech_new + c_mental_new
                    })
                    p_obj['c_tech'] = c_tech_new
                    p_obj['c_mental'] = c_mental_new
                    p_obj['play_style'] = selected_style
                    p_obj['coach_note'] = new_coach_note
                    st.success(f"✅ Scheda aggiornata con successo per {selected_player_name}!")

    with coach_tab2:
        st.subheader("📅 Registrazione Partite")
        st.markdown("Seleziona i giocatori per ciascuna squadra (ciascun team richiede 1 giocatore di Sinistra e 1 di Destra).")
        
        left_list = [f"{p['fname']} {p['lname']}" for p in squad_players if p['side'] == "Left"]
        right_list = [f"{p['fname']} {p['lname']}" for p in squad_players if p['side'] == "Right"]
        
        with st.form("match_form"):
            m_date = st.date_input("Data Partita", datetime.now())
            
            st.markdown("#### 🔵 Team A")
            col_ta1, col_ta2 = st.columns(2)
            with col_ta1:
                team_a_left = st.selectbox("Team A - Sinistra (Left)", left_list, key="ta_left")
            with col_ta2:
                team_a_right = st.selectbox("Team A - Destra (Right)", right_list, key="ta_right")
                
            st.markdown("#### 🔴 Team B")
            col_tb1, col_tb2 = st.columns(2)
            with col_tb1:
                team_b_left = st.selectbox("Team B - Sinistra (Left)", left_list, key="tb_left")
            with col_tb2:
                team_b_right = st.selectbox("Team B - Destra (Right)", right_list, key="tb_right")
                
            score = st.text_input("Risultato (es. 6-4, 6-2)")
            
            if st.form_submit_button("Registra Partita", type="primary"):
                team_a_players = {team_a_left, team_a_right}
                team_b_players = {team_b_left, team_b_right}
                
                if len(team_a_players) < 2 or len(team_b_players) < 2:
                    st.error("⚠️ All'interno dello stesso team non puoi selezionare due volte lo stesso giocatore!")
                else:
                    team_a_str = f"{team_a_left} / {team_a_right}"
                    team_b_str = f"{team_b_left} / {team_b_right}"
                    
                    st.session_state.match_results.append({
                        "Data": str(m_date),
                        "Team A": team_a_str,
                        "Team B": team_b_str,
                        "Risultato": score
                    })
                    st.success("✅ Partita registrata con successo!")
                    
        if st.session_state.match_results:
            st.markdown("### 📋 Storico Partite Registrate")
            st.table(pd.DataFrame(st.session_state.match_results))

    with coach_tab3:
        st.subheader("💬 Vista Globale Note & Commenti")
        for p in squad_players:
            st.markdown(f"#### 👤 {p['fname']} {p['lname']} (Stile Coach: {p.get('play_style', 'equilibrated').capitalize()} | Stile Player: {p.get('player_play_style', 'equilibrated').capitalize()})")
            if p.get("coach_note"):
                st.markdown(f"**Nota Coach:** {p['coach_note']}")
            else:
                st.markdown("*Nessuna nota del coach.*")
            
            if p.get("comments"):
                st.markdown("**Note tra compagni:**")
                for c in p["comments"]:
                    st.markdown(f"- *Da {c['from']}*: {c['text']}")
            st.markdown("---")

    with coach_tab_pairing:
        st.subheader("🤖 Algoritmo Intelligente di Pairing per Coppie")
        st.markdown("Seleziona qui sotto i giocatori **disponibili per questa sessione**. L'algoritmo abbinerà esclusivamente tra loro i giocatori selezionati, rispettando il vincolo di ruolo (**1 Sinistra + 1 Destra**) e bilanciando:")
        st.markdown("- **Peso 1.0**: Valutazione complessiva del Coach.")
        st.markdown("- **Peso 0.5**: Volontà / preferenza reciproca dei giocatori.")
        
        all_player_names = [f"{p['fname']} {p['lname']} ({p['side']})" for p in squad_players]
        selected_available_str = st.multiselect(
            "Seleziona i giocatori disponibili oggi:",
            options=all_player_names,
            default=all_player_names
        )
        
        selected_names_only = [s.split(" (")[0] for s in selected_available_str]
        available_players = [p for p in squad_players if f"{p['fname']} {p['lname']}" in selected_names_only]
        
        left_players = [p for p in available_players if p["side"] == "Left"]
        right_players = [p for p in available_players if p["side"] == "Right"]
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"⬅️ **Sinistra (Left) disponibili: {len(left_players)}**\n" + ("\n".join([f"- {p['fname']} {p['lname']}" for p in left_players]) if left_players else "Nessuno"))
        with col_info2:
            st.info(f"➡️ **Destra (Right) disponibili: {len(right_players)}**\n" + ("\n".join([f"- {p['fname']} {p['lname']}" for p in right_players]) if right_players else "Nessuno"))
        
        if st.button("🚀 Genera Coppie Ottimali con i Disponibili", type="primary"):
            if not left_players or not right_players:
                st.error("⚠️ Per formare le coppie servono almeno un giocatore di sinistra e un giocatore di destra tra i selezionati!")
            else:
                def get_coach_score(player):
                    all_c = player['c_tech'] + player['c_mental']
                    return sum(all_c) / len(all_c) if all_c else 5.0

                pairs_matrix = []
                for l_p in left_players:
                    l_name = f"{l_p['fname']} {l_p['lname']}"
                    l_coach_val = get_coach_score(l_p)
                    l_partners = l_p.get("partners", {})
                    
                    for r_p in right_players:
                        r_name = f"{r_p['fname']} {r_p['lname']}"
                        r_coach_val = get_coach_score(r_p)
                        r_partners = r_p.get("partners", {})
                        
                        coach_affinity = (l_coach_val + r_coach_val) / 2.0
                        
                        vol_l_to_r = l_partners.get(r_name, 0)
                        vol_r_to_l = r_partners.get(l_name, 0)
                        
                        vol_score = 0.0
                        count_vol = 0
                        if vol_l_to_r > 0:
                            vol_score += min(vol_l_to_r / 5.0, 10.0)
                            count_vol += 1
                        if vol_r_to_l > 0:
                            vol_score += min(vol_r_to_l / 5.0, 10.0)
                            count_vol += 1
                        
                        willingness_affinity = (vol_score / count_vol) if count_vol > 0 else 5.0
                        
                        total_score = (1.0 * coach_affinity) + (0.5 * willingness_affinity)
                        
                        pairs_matrix.append({
                            "left": l_name,
                            "right": r_name,
                            "score": total_score,
                            "coach_avg": round(coach_affinity, 2),
                            "willingness": round(willingness_affinity, 2)
                        })
                
                pairs_matrix = sorted(pairs_matrix, key=lambda x: x["score"], reverse=True)
                
                matched_left = set()
                matched_right = set()
                final_pairs = []
                
                for item in pairs_matrix:
                    if item["left"] not in matched_left and item["right"] not in matched_right:
                        final_pairs.append(item)
                        matched_left.add(item["left"])
                        matched_right.add(item["right"])
                
                unmatched_l = [l for l in left_players if f"{l['fname']} {l['lname']}" not in matched_left]
                unmatched_r = [r for r in right_players if f"{r['fname']} {r['lname']}" not in matched_right]
                
                st.markdown("### 🏆 Risultato Pairing Consigliato:")
                
                pair_results_df = []
                for idx, fp in enumerate(final_pairs):
                    pair_results_df.append({
                        "Coppia #": idx + 1,
                        "Giocatore Sinistra (Left)": fp["left"],
                        "Giocatore Destra (Right)": fp["right"],
                        "Score Coach (Peso 1.0)": fp["coach_avg"],
                        "Volontà Reciproca (Peso 0.5)": fp["willingness"],
                        "Punteggio Totale": round(fp["score"], 2)
                    })
                
                if pair_results_df:
                    st.table(pd.DataFrame(pair_results_df))
                else:
                    st.info("Nessuna coppia generabile con i giocatori selezionati.")
                    
                if unmatched_l or unmatched_r:
                    st.warning("⚠️ Giocatori selezionati ma rimasti esclusi in questo turno per sbilanciamento numerico tra Destra e Sinistra:")
                    un_names = [f"{p['fname']} {p['lname']}" for p in unmatched_l + unmatched_r]
                    st.markdown("- " + "\n- ".join(un_names))
