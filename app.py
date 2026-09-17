import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Streamlit page configuration
st.set_page_config(
    page_title="Padel Performance Hub",
    page_icon="🎾",
    layout="wide"
)

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
        "mental_skills": "Attitudine e Tattica",
        "self_eval": "Le mie Valutazioni (Autovalutazione)",
        "coach_eval": "Valutazione Coach & Confronto",
        "diff_table": "Tabella Differenze (Tu vs Coach)",
        "partners_tab": "Ranking Partner",
        "history_tab": "Storico & Miglioramenti",
        "comments_tab": "Commenti Compagni",
        "matches_dash": "Gestione Partite (Coach)",
        "all_comments": "Tutti i Commenti (Coach)"
    },
    "Inglese": {
        "welcome": "Welcome to Padel Performance Hub",
        "select_area": "Select your access area to continue:",
        "player_area": "Player Area",
        "player_desc": "Access your personal password-protected card to view and update your ratings.",
        "player_btn": "Log in as Player",
        "coach_area": "Coach Area",
        "coach_desc": "Restricted access for technical staff for data management, planning, and matches.",
        "coach_btn": "Log in as Coach",
        "login_player_title": "Player Area Login",
        "login_player_sub": "Select your name and enter your password (your first name).",
        "profile_select": "Select your profile:",
        "pwd_label": "Password (Your first name)",
        "enter_card": "Enter my card",
        "back_home": "Back to Home",
        "wrong_pwd": "Wrong password! Remember the password is your first name.",
        "coach_login_title": "Coach Area Authentication",
        "coach_login_sub": "Enter the security password to access management functions.",
        "coach_pwd_label": "Coach Password",
        "verify_pwd": "Verify Password",
        "logout": "Log out",
        "tech_skills": "Technical Skills",
        "mental_skills": "Attitude & Tactics",
        "self_eval": "My Ratings (Self-Evaluation)",
        "coach_eval": "Coach Evaluation & Comparison",
        "diff_table": "Differences Table (You vs Coach)",
        "partners_tab": "Partner Ranking",
        "history_tab": "History & Improvements",
        "comments_tab": "Teammate Comments",
        "matches_dash": "Match Management (Coach)",
        "all_comments": "All Comments (Coach)"
    },
    "Spagnolo": {
        "welcome": "Bienvenido al Padel Performance Hub",
        "select_area": "Selecciona tu área de acceso para continuar:",
        "player_area": "Área de Jugador",
        "player_desc": "Accede a tu ficha personal protegida por contraseña para ver y actualizar tus valoraciones.",
        "player_btn": "Acceder como Jugador",
        "coach_area": "Área de Entrenador",
        "coach_desc": "Acceso restringido al cuerpo técnico para la gestión de datos, planificación y partidos.",
        "coach_btn": "Acceder como Entrenador",
        "login_player_title": "Acceso Área de Jugador",
        "login_player_sub": "Selecciona tu nombre e introduce tu contraseña (tu nombre de pila).",
        "profile_select": "Selecciona tu perfil:",
        "pwd_label": "Contraseña (Tu nombre de pila)",
        "enter_card": "Entrar a mi ficha",
        "back_home": "Volver al Inicio",
        "wrong_pwd": "¡Contraseña incorrecta! Recuerda que es tu nombre de pila.",
        "coach_login_title": "Autenticación Área Entrenador",
        "coach_login_sub": "Introduce la contraseña de seguridad para acceder a las funciones de gestión.",
        "coach_pwd_label": "Contraseña Entrenador",
        "verify_pwd": "Verificar Contraseña",
        "logout": "Salir",
        "tech_skills": "Habilidades Técnicas",
        "mental_skills": "Actitud y Táctica",
        "self_eval": "Mis Valoraciones (Autoevaluación)",
        "coach_eval": "Evaluación del Entrenador y Comparativa",
        "diff_table": "Tabla de Diferencias (Tú vs Entrenador)",
        "partners_tab": "Ranking de Compañeros",
        "history_tab": "Historial y Mejoras",
        "comments_tab": "Comentarios de Compañeros",
        "matches_dash": "Gestión de Partidos (Entrenador)",
        "all_comments": "Todos los Comentarios (Entrenador)"
    },
    "Danese": {
        "welcome": "Velkommen til Padel Performance Hub",
        "select_area": "Vælg dit adgangsområde for at fortsætte:",
        "player_area": "Spillerområde",
        "player_desc": "Få adgang til dit personlige kodeordsbeskyttede kort for at se og opdatere dine bedømmelser.",
        "player_btn": "Log ind som spiller",
        "coach_area": "Trænerområde",
        "coach_desc": "Begrænset adgang for trænerstaben til datahåndtering, planlægning og kampe.",
        "coach_btn": "Log ind som træner",
        "login_player_title": "Login til Spillerområde",
        "login_player_sub": "Vælg dit navn og indtast din adgangskode (dit fornavn).",
        "profile_select": "Vælg din profil:",
        "pwd_label": "Adgangskode (Dit fornavn)",
        "enter_card": "Gå til mit kort",
        "back_home": "Tilbage til start",
        "wrong_pwd": "Forkert adgangskode! Husk at adgangskoden er dit fornavn.",
        "coach_login_title": "Godkendelse af Trænerområde",
        "coach_login_sub": "Indtast sikkerhedsadgangskoden for at få adgang til administrationsfunktioner.",
        "coach_pwd_label": "Træner-adgangskode",
        "verify_pwd": "Bekræft adgangskode",
        "logout": "Log ud",
        "tech_skills": "Tekniske færdigheder",
        "mental_skills": "Attitude & Taktik",
        "self_eval": "Mine bedømmelser (Selvvurdering)",
        "coach_eval": "Trænerbedømmelse & Sammenligning",
        "diff_table": "Differenstabel (Du vs Træner)",
        "partners_tab": "Makker-ranking",
        "history_tab": "Historik & Forbedringer",
        "comments_tab": "Kommentarer fra spillere",
        "matches_dash": "Kampadministration (Træner)",
        "all_comments": "Alle kommentarer (Træner)"
    },
    "Svedese": {
        "welcome": "Välkommen till Padel Performance Hub",
        "select_area": "Välj ditt åtkomstområde för att fortsätta:",
        "player_area": "Spelarområde",
        "player_desc": "Få tillgång till ditt personliga lösenordsskyddade kort för att visa och uppdatera dina betyg.",
        "player_btn": "Logga in som spelare",
        "coach_area": "Tränarområde",
        "coach_desc": "Begränsad åtkomst för tränarstaben för datahantering, planering och matcher.",
        "coach_btn": "Logga in som tränare",
        "login_player_title": "Inloggning Spelarområde",
        "login_player_sub": "Välj ditt namn och ange ditt lösenord (ditt förnamn).",
        "profile_select": "Välj din profil:",
        "pwd_label": "Lösenord (Ditt förnamn)",
        "enter_card": "Gå till mitt kort",
        "back_home": "Tillbaka till start",
        "wrong_pwd": "Fel lösenord! Kom ihåg att lösenordet är ditt förnamn.",
        "coach_login_title": "Autentisering Tränarområde",
        "coach_login_sub": "Ange säkerhetslösenordet för att komma åt hanteringsfunktioner.",
        "coach_pwd_label": "Tränarlösenord",
        "verify_pwd": "Verifiera lösenord",
        "logout": "Logga ut",
        "tech_skills": "Tekniska färdigheter",
        "mental_skills": "Attityd & Taktik",
        "self_eval": "Mina betyg (Självutvärdering)",
        "coach_eval": "Tränarbedömning & Jämförelse",
        "diff_table": "Differenstabell (Du vs Tränare)",
        "partners_tab": "Partner-ranking",
        "history_tab": "Historik & Förbättringar",
        "comments_tab": "Kommentarer från spelare",
        "matches_dash": "Matchhantering (Tränare)",
        "all_comments": "Alla kommentarer (Tränare)"
    },
    "Olandese": {
        "welcome": "Welkom bij de Padel Performance Hub",
        "select_area": "Selecteer je toegangsgebied om door te gaan:",
        "player_area": "Spelersgebied",
        "player_desc": "Toegang tot je persoonlijke met een wachtwoord beveiligde kaart om je beoordelingen te bekijken en bij te werken.",
        "player_btn": "Inloggen als Speler",
        "coach_area": "Coachgebied",
        "coach_desc": "Beperkte toegang voor de technische staf voor gegevensbeheer, planning en wedstrijden.",
        "coach_btn": "Inloggen als Coach",
        "login_player_title": "Inloggen Spelersgebied",
        "login_player_sub": "Selecteer je naam en voer je wachtwoord in (je voornaam).",
        "profile_select": "Selecteer je profiel:",
        "pwd_label": "Wachtwoord (Je voornaam)",
        "enter_card": "Naar mijn kaart",
        "back_home": "Terug naar Start",
        "wrong_pwd": "Onjuist wachtwoord! Onthoud dat het wachtwoord je voornaam is.",
        "coach_login_title": "Authenticatie Coachgebied",
        "coach_login_sub": "Voer het beveiligingswachtwoord in om toegang te krijgen tot de beheerfuncties.",
        "coach_pwd_label": "Coachwachtwoord",
        "verify_pwd": "Wachtwoord verifiëren",
        "logout": "Uitloggen",
        "tech_skills": "Technische Vaardigheden",
        "mental_skills": "Attitude & Tactiek",
        "self_eval": "Mijn Beoordelingen (Zelfevaluatie)",
        "coach_eval": "Coach Beoordeling & Vergelijking",
        "diff_table": "Verschillentabel (Jij vs Coach)",
        "partners_tab": "Partner Ranking",
        "history_tab": "Geschiedenis & Verbeteringen",
        "comments_tab": "Opmerkingen van spelers",
        "matches_dash": "Wedstrijdbeheer (Coach)",
        "all_comments": "Alle opmerkingen (Coach)"
    }
}

# --- INIZIALIZZAZIONE STATO ---
if "language" not in st.session_state:
    st.session_state.language = "Italiano"

if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "Home"

if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

if "authenticated_player" not in st.session_state:
    st.session_state.authenticated_player = None

# Struttura dati estesa per gestire: storico valutazioni, partner matchati, commenti e partite coach
if "squad_data" not in st.session_state:
    st.session_state.squad_data = [
        {"fname": "Álvaro", "lname": "Gomez", "side": "Left", "tech": [7, 7, 7, 6, 8, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 6, 5, 7, 5], "c_mental": [7, 6, 6, 6, 7, 6], "history": [], "partners": {"Yannik Langeslag": 12, "Josu Usabiaga": 8, "Andrea Lonoce": 5}, "comments": []},
        {"fname": "Yannik", "lname": "Langeslag", "side": "Left", "tech": [8, 6, 7, 7, 7, 5], "mental": [7, 6, 8, 6, 7, 6], "c_tech": [7, 5, 6, 6, 6, 4], "c_mental": [6, 5, 7, 5, 6, 5], "history": [], "partners": {"Álvaro Gomez": 12, "Benjamin Thyrell": 10, "Pedro Rios": 4}, "comments": []},
        {"fname": "Josu", "lname": "Usabiaga", "side": "Right", "tech": [6, 8, 7, 7, 6, 7], "mental": [6, 8, 6, 8, 7, 7], "c_tech": [5, 7, 6, 6, 5, 6], "c_mental": [5, 7, 5, 7, 6, 6], "history": [], "partners": {"Álvaro Gomez": 8, "Alexander Wennstam": 11, "Andrea Lonoce": 9}, "comments": []},
        {"fname": "Benjamin", "lname": "Thyrell", "side": "Left", "tech": [7, 7, 8, 6, 7, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 7, 5, 6, 5], "c_mental": [7, 6, 6, 6, 7, 6], "history": [], "partners": {"Yannik Langeslag": 10, "Mikkel Hoff": 6}, "comments": []},
        {"fname": "Alexander", "lname": "Wennstam", "side": "Left", "tech": [8, 8, 7, 7, 8, 6], "mental": [7, 7, 8, 8, 7, 7], "c_tech": [7, 7, 6, 6, 7, 5], "c_mental": [6, 6, 7, 7, 6, 6], "history": [], "partners": {"Josu Usabiaga": 11, "Andrea Lonoce": 14}, "comments": []},
        {"fname": "Andrea", "lname": "Lonoce", "side": "Right", "tech": [8, 7, 8, 7, 9, 6], "mental": [9, 7, 8, 8, 9, 7], "c_tech": [8, 7, 8, 7, 9, 6], "c_mental": [9, 7, 8, 8, 9, 7], "history": [], "partners": {"Alexander Wennstam": 14, "Josu Usabiaga": 9, "Pedro Rios": 10}, "comments": []},
        {"fname": "Mikkel", "lname": "Hoff", "side": "Right", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5], "history": [], "partners": {"Benjamin Thyrell": 6, "Lars Mikkelsen": 7}, "comments": []},
        {"fname": "Pedro", "lname": "Rios", "side": "Right", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7], "history": [], "partners": {"Andrea Lonoce": 10, "Yannik Langeslag": 4}, "comments": []},
        {"fname": "Hector", "lname": "Guerrero", "side": "Right", "tech": [7, 7, 7, 7, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 6, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6], "history": [], "partners": {"Gonzalo Diez de Onate": 8}, "comments": []},
        {"fname": "Gonzalo", "lname": "Diez de Onate", "side": "Left", "tech": [8, 7, 8, 7, 8, 6], "mental": [8, 7, 8, 8, 8, 7], "c_tech": [7, 6, 7, 6, 7, 5], "c_mental": [7, 6, 7, 7, 7, 6], "history": [], "partners": {"Hector Guerrero": 8, "Julio Morales": 5}, "comments": []},
        {"fname": "Julio", "lname": "Morales", "side": "Right", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5], "history": [], "partners": {"Gonzalo Diez de Onate": 5}, "comments": []},
        {"fname": "Lars", "lname": "Mikkelsen", "side": "Left", "tech": [7, 7, 7, 6, 8, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 6, 5, 7, 5], "c_mental": [7, 6, 6, 6, 7, 6], "history": [], "partners": {"Mikkel Hoff": 7, "Joahn Lohman": 9}, "comments": []},
        {"fname": "Joahn", "lname": "Lohman", "side": "Left", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5], "history": [], "partners": {"Lars Mikkelsen": 9}, "comments": []},
        {"fname": "Nacho", "lname": "Saracho", "side": "Right", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7], "history": [], "partners": {"Juanjo Lopez Benitez": 11}, "comments": []},
        {"fname": "Peter", "lname": "Gustafsson", "side": "Left", "tech": [7, 7, 7, 6, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6], "history": [], "partners": {"Sascha Van De Bilt": 7}, "comments": []},
        {"fname": "Juanjo", "lname": "Lopez Benitez", "side": "Left", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7], "history": [], "partners": {"Nacho Saracho": 11}, "comments": []},
        {"fname": "Sascha", "lname": "Van De Bilt", "side": "Right", "tech": [7, 7, 7, 6, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6], "history": [], "partners": {"Peter Gustafsson": 7, "Fernando Oribe": 8}, "comments": []},
        {"fname": "Fernando", "lname": "Oribe", "side": "Right", "tech": [8, 7, 8, 7, 8, 6], "mental": [8, 7, 8, 8, 8, 7], "c_tech": [7, 6, 7, 6, 7, 5], "c_mental": [7, 6, 7, 7, 7, 6], "history": [], "partners": {"Sascha Van De Bilt": 8, "Doug Ramsay": 6}, "comments": []},
        {"fname": "Doug", "lname": "Ramsay", "side": "Left", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5], "history": [], "partners": {"Fernando Oribe": 6}, "comments": []}
    ]

if "match_results" not in st.session_state:
    st.session_state.match_results = []

squad_players = st.session_state.squad_data
lang_dict = translations[st.session_state.language]

# --- SIDEBAR (SELETTORE LINGUA) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/padel.png", width=64)
    st.title("Padel Hub")
    selected_lang = st.selectbox(
        "🌐 Lingua / Language / Idioma / Sprog / Språk / Taal",
        ["Italiano", "Inglese", "Spagnolo", "Danese", "Svedese", "Olandese"],
        index=["Italiano", "Inglese", "Spagnolo", "Danese", "Svedese", "Olandese"].index(st.session_state.language)
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
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
        if st.button(lang_dict['coach_btn'], use_container_width=True):
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

# --- DASHBOARD GIOCATORE (CON TABS AGGIUNTI) ---
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
    
    # Tabs della Dashboard Giocatore
    tab_eval, tab_partners, tab_history, tab_comments = st.tabs([
        "📊 Autovalutazione & Coach", 
        f"🏆 {lang_dict['partners_tab']}", 
        f"📈 {lang_dict['history_tab']}", 
        f"💬 {lang_dict['comments_tab']}"
    ])
    
    with tab_eval:
        st.subheader("Confronto Valutazioni & Discrepanze")
        skills_names = ["Volley", "Smash", "Bandeja", "Serve", "Defense", "Chiquita", 
                        "Chemistry", "Error Mgmt", "Positioning", "Focus", "Stamina", "Intensity"]
        
        player_all_vals = current_player['tech'] + current_player['mental']
        coach_all_vals = current_player['c_tech'] + current_player['c_mental']
        
        diff_data = []
        for i, skill in enumerate(skills_names):
            p_val = player_all_vals[i]
            c_val = coach_all_vals[i]
            diff = p_val - c_val
            # Richiesta 3: Evidenzia in rosso se ci sono discrepanze
            diff_display = f"<span style='color:red; font-weight:bold;'>{diff} (Discrepanza)</span>" if diff != 0 else f"<span style='color:green;'>{diff}</span>"
            diff_data.append({
                "Skill": skill,
                "Tuo Valore": p_val,
                "Valore Coach": c_val,
                "Delta": diff_display
            })
        
        df_diff = pd.DataFrame(diff_data)
        st.markdown(df_diff.to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab_partners:
        st.subheader("🏆 Ranking dei giocatori con cui ti trovi di più a giocare")
        partners_dict = current_player.get("partners", {})
        if partners_dict:
            df_partners = pd.DataFrame(list(partners_dict.items()), columns=["Compagno", "Match Giocati Insieme"])
            df_partners = df_partners.sort_values(by="Match Giocati Insieme", ascending=False).reset_index(drop=True)
            st.table(df_partners)
        else:
            st.info("Nessun dato registrato sui partner.")

    with tab_history:
        st.subheader("📈 Grafico a tela di ragno (Evoluzione Storica)")
        st.markdown("Mostra i miglioramenti storici registrati ogni volta che il coach aggiorna la valutazione.")
        history_records = current_player.get("history", [])
        if history_records:
            for idx, hist in enumerate(history_records):
                st.markdown(f"**Aggiornamento #{idx+1} ({hist.get('date', 'Data non specificata')})**")
                st.json(hist.get('values'))
        else:
            st.info("Nessuna modifica precedente registrata dal coach. Verranno mostrate qui man mano che il coach aggiorna i valori.")

    with tab_comments:
        st.subheader("💬 Commenti e Feedback da parte dei compagni di squadra")
        # Inserimento nuovo commento su altri giocatori o visualizzazione
        target_colleagues = [f"{p['fname']} {p['lname']}" for p in squad_players if p['fname'] != current_player['fname']]
        selected_target = st.selectbox("Seleziona un compagno a cui lasciare un commento o nota:", target_colleagues)
        comment_text = st.text_area("Scrivi un commento sul compagno:")
        
        if st.button("Invia Commento"):
            if comment_text.strip():
                target_player_obj = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_target), None)
                if target_player_obj:
                    if "comments" not in target_player_obj:
                        target_player_obj["comments"] = []
                    target_player_obj["comments"].append({
                        "from": f"{current_player['fname']} {current_player['lname']}",
                        "text": comment_text,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.success("Commento inviato con successo!")
            else:
                st.warning("Il commento non può essere vuoto.")
                
        st.markdown("---")
        st.markdown("### Commenti ricevuti su di te:")
        my_comments = current_player.get("comments", [])
        if my_comments:
            for c in my_comments:
                st.info(f"**Da {c['from']}** ({c['date']}): {c['text']}")
        else:
            st.write("Non ci sono ancora commenti per te.")

# --- AREA ALLENATORE (CON GESTIONE MODIFICHE, MATCH E VISUALIZZAZIONE COMMENTI) ---
elif st.session_state.nav_mode == "Coach" and st.session_state.authenticated_coach:
    st.title("📋 Dashboard Allenatore - Gestione Squadra e Match")
    
    if st.button("🚪 Esci da Area Allenatore"):
        st.session_state.authenticated_coach = False
        st.session_state.nav_mode = "Home"
        st.rerun()
        
    coach_tab1, coach_tab2, coach_tab3 = st.tabs([
        "👥 Gestione Giocatori & Valutazioni", 
        f"📅 {lang_dict['matches_dash']}", 
        f"💬 {lang_dict['all_comments']}"
    ])
    
    with coach_tab1:
        st.subheader("Modifica Valutazioni Giocatore (Riservato al Coach)")
        selected_player_name = st.selectbox("Seleziona giocatore da aggiornare:", [f"{p['fname']} {p['lname']}" for p in squad_players])
        p_obj = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_player_name), None)
        
        if p_obj:
            st.markdown(f"Modifica dei valori tecnici e mentali assegnati da coach per **{selected_player_name}**:")
            
            c_tech_new = []
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.markdown("**Tecnica (Coach)**")
                tech_labels_list = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita']
                for idx, t_label in enumerate(tech_labels_list):
                    val = st.slider(f"{t_label}", 1, 10, int(p_obj['c_tech'][idx]), key=f"scoach_tech_{idx}")
                    c_tech_new.append(val)
            
            c_mental_new = []
            with col_c2:
                st.markdown("**Tattica & Mentale (Coach)**")
                mental_labels_list = ['Chemistry', 'Errors', 'Positioning', 'Focus', 'Stamina', 'Intensity']
                for idx, m_label in enumerate(mental_labels_list):
                    val = st.slider(f"{m_label}", 1, 10, int(p_obj['c_mental'][idx]), key=f"scoach_mental_{idx}")
                    c_mental_new.append(val)
                    
            if st.button("Salva Modifiche e Registra Storico"):
                # Registra storico per grafico evolutivo (Richiesta 7)
                if "history" not in p_obj:
                    p_obj["history"] = []
                p_obj["history"].append({
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "values": c_tech_new + c_mental_new
                })
                p_obj['c_tech'] = c_tech_new
                p_obj['c_mental'] = c_mental_new
                st.success(f"Valutazioni aggiornate per {selected_player_name}! Storico registrato.")

    with coach_tab2:
        st.subheader("📅 Inserimento e Tracciamento Partite")
        st.markdown("Inserisci qui i match disputati e i relativi risultati per tenerne traccia.")
        
        with st.form("match_form"):
            match_date = st.date_input("Data Partita", datetime.now())
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                team_a = st.text_input("Coppia Team A (es. Alvaro / Yannik)")
            with col_m2:
                team_b = st.text_input("Coppia Team B (es. Josu / Andrea)")
            
            result_score = st.text_input("Risultato (es. 6-4, 3-6, 7-6)")
            submit_match = st.form_submit_button("Registra Partita")
            
            if submit_match:
                if team_a and team_b and result_score:
                    st.session_state.match_results.append({
                        "date": str(match_date),
                        "team_a": team_a,
                        "team_b": team_b,
                        "score": result_score
                    })
                    st.success("Partita registrata con successo!")
                else:
                    st.error("Compila tutti i campi della partita.")
                    
        st.markdown("### Storico Partite Registrate:")
        if st.session_state.match_results:
            df_matches = pd.DataFrame(st.session_state.match_results)
            st.table(df_matches)
        else:
            st.info("Nessuna partita registrata.")

    with coach_tab3:
        st.subheader("💬 Vista Globale di Tutti i Commenti dei Giocatori")
        all_comments_found = False
        for p in squad_players:
            if p.get("comments"):
                all_comments_found = True
                st.markdown(f"#### 👤 {p['fname']} {p['lname']}")
                for c in p["comments"]:
                    st.markdown(f"- *Da {c['from']}* ({c['date']}): {c['text']}")
                st.markdown("---")
        if not all_comments_found:
            st.info("Nessun commento inserito dai giocatori al momento.")
