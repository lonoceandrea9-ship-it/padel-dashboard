import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# Streamlit page configuration
st.set_page_config(
    page_title="Nac Padel Team Performance Hub",
    page_icon="🎾",
    layout="wide"
)

# Initialize navigation state if not present
if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "Home"

if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

if "authenticated_player" not in st.session_state:
    st.session_state.authenticated_player = None

if "language" not in st.session_state:
    st.session_state.language = "English"

# Dizionario delle traduzioni per la schermata Home e di Login
translations = {
    "English": {
        "welcome": "🎾 Welcome to Nac Padel Team Performance Hub",
        "select_lang": "Select your language / Seleziona la lingua:",
        "select_area": "Select your access area to continue:",
        "player_title": "👤 Player Area",
        "player_desc": "Access your password-protected personal profile to view and update your evaluations.",
        "player_btn": "Log in as Player",
        "coach_title": "📋 Coach Area",
        "coach_desc": "Restricted access for coaching staff to manage data, plan training sessions, and generate team pairings.",
        "coach_btn": "Log in as Coach",
        "player_login_title": "🔐 Player Area Access",
        "player_login_desc": "Select your name and enter your password (your password is your **first name**).",
        "select_profile": "Select your profile:",
        "pwd_label": "Password (Enter your first name)",
        "enter_profile": "Enter My Profile",
        "back_home": "⬅️ Back to Home",
        "wrong_pwd": "❌ Incorrect password! Remember that your password is your first name.",
        "coach_login_title": "🔒 Coach Area Authentication",
        "coach_login_desc": "Enter the security password to access management tools.",
        "coach_pwd_label": "Coach Password",
        "verify_pwd": "Verify Password",
        "wrong_coach_pwd": "❌ Incorrect password! Please try again."
    },
    "Italiano": {
        "welcome": "🎾 Benvenuto in Nac Padel Team Performance Hub",
        "select_lang": "Seleziona la lingua:",
        "select_area": "Seleziona l'area di accesso per continuare:",
        "player_title": "👤 Area Giocatore",
        "player_desc": "Accedi al tuo profilo personale protetto da password per visualizzare e aggiornare le tue valutazioni.",
        "player_btn": "Accedi come Giocatore",
        "coach_title": "📋 Area Allenatore",
        "coach_desc": "Accesso riservato allo staff tecnico per gestire i dati, pianificare gli allenamenti e generare le coppie.",
        "coach_btn": "Accedi come Allenatore",
        "player_login_title": "🔐 Accesso Area Giocatore",
        "player_login_desc": "Seleziona il tuo nome e inserisci la password (la password è il tuo **nome**).",
        "select_profile": "Seleziona il tuo profilo:",
        "pwd_label": "Password (Inserisci il tuo nome)",
        "enter_profile": "Entra nel mio profilo",
        "back_home": "⬅️ Torna alla Home",
        "wrong_pwd": "❌ Password errata! Ricorda che la tua password è il tuo nome.",
        "coach_login_title": "🔒 Autenticazione Area Allenatore",
        "coach_login_desc": "Inserisci la password di sicurezza per accedere agli strumenti di gestione.",
        "coach_pwd_label": "Password Allenatore",
        "verify_pwd": "Verifica Password",
        "wrong_coach_pwd": "❌ Password errata! Riprova."
    },
    "Español": {
        "welcome": "🎾 Bienvenido a Nac Padel Team Performance Hub",
        "select_lang": "Selecciona tu idioma:",
        "select_area": "Selecciona tu área de acceso para continuar:",
        "player_title": "👤 Área de Jugador",
        "player_desc": "Accede a tu perfil personal protegido por contraseña para ver y actualizar tus evaluaciones.",
        "player_btn": "Iniciar sesión como Jugador",
        "coach_title": "📋 Área de Entrenador",
        "coach_desc": "Acceso restringido para el cuerpo técnico para gestionar datos, planificar entrenamientos y generar parejas.",
        "coach_btn": "Iniciar sesión como Entrenador",
        "player_login_title": "🔐 Acceso al Área de Jugador",
        "player_login_desc": "Selecciona tu nombre e introduce tu contraseña (tu contraseña es tu **nombre**).",
        "select_profile": "Selecciona tu perfil:",
        "pwd_label": "Contraseña (Introduce tu nombre)",
        "enter_profile": "Entrar a mi perfil",
        "back_home": "⬅️ Volver al Inicio",
        "wrong_pwd": "❌ ¡Contraseña incorrecta! Recuerda que tu contraseña es tu nombre.",
        "coach_login_title": "🔒 Autenticación del Área de Entrenador",
        "coach_login_desc": "Introduce la contraseña de seguridad para acceder a las herramientas de gestión.",
        "coach_pwd_label": "Contraseña de Entrenador",
        "verify_pwd": "Verificar Contraseña",
        "wrong_coach_pwd": "❌ ¡Contraseña incorrecta! Inténtalo de nuevo."
    },
    "Svenska": {
        "welcome": "🎾 Välkommen till Nac Padel Team Performance Hub",
        "select_lang": "Välj ditt språk:",
        "select_area": "Välj ditt åtkomstområde för att fortsätta:",
        "player_title": "👤 Spelarområde",
        "player_desc": "Få tillgång till din lösenordsskyddade personliga profil för att visa och uppdatera dina utvärderingar.",
        "player_btn": "Logga in som spelare",
        "coach_title": "📋 Tränarområde",
        "coach_desc": "Begränsad åtkomst för tränarstab för att hantera data, planera träningspass och generera lag.",
        "coach_btn": "Logga in som tränare",
        "player_login_title": "🔐 Åtkomst till spelarområde",
        "player_login_desc": "Välj ditt namn och ange ditt lösenord (ditt lösenord är ditt **förnamn**).",
        "select_profile": "Välj din profil:",
        "pwd_label": "Lösenord (Ange ditt förnamn)",
        "enter_profile": "Gå till min profil",
        "back_home": "⬅️ Tillbaka till start",
        "wrong_pwd": "❌ Felaktigt lösenord! Kom ihåg att ditt lösenord är ditt förnamn.",
        "coach_login_title": "🔒 Autentisering för tränarområde",
        "coach_login_desc": "Ange säkerhetslösenordet för att komma åt hanteringsverktyg.",
        "coach_pwd_label": "Tränarlösenord",
        "verify_pwd": "Verifiera lösenord",
        "wrong_coach_pwd": "❌ Felaktigt lösenord! Försök igen."
    },
    "Nederlands": {
        "welcome": "🎾 Welkom bij Nac Padel Team Performance Hub",
        "select_lang": "Selecteer uw taal:",
        "select_area": "Selecteer uw toegangsgebied om door te gaan:",
        "player_title": "👤 Spelersgebied",
        "player_desc": "Toegang tot uw met een wachtwoord beveiligde persoonlijke profiel om uw evaluaties te bekijken en bij te werken.",
        "player_btn": "Inloggen als speler",
        "coach_title": "📋 Coachgebied",
        "coach_desc": "Beperkte toegang voor de technische staf om data te beheren, trainingen te plannen en koppels te genereren.",
        "coach_btn": "Inloggen als coach",
        "player_login_title": "🔐 Toegang Spelersgebied",
        "player_login_desc": "Selecteer uw naam en voer uw wachtwoord in (uw wachtwoord is uw **voornaam**).",
        "select_profile": "Selecteer uw profiel:",
        "pwd_label": "Wachtwoord (Voer uw voornaam in)",
        "enter_profile": "Naar mijn profiel",
        "back_home": "⬅️ Terug naar Home",
        "wrong_pwd": "❌ Onjuist wachtwoord! Vergeet niet dat uw wachtwoord uw voornaam is.",
        "coach_login_title": "🔒 Authenticatie Coachgebied",
        "coach_login_desc": "Voer het beveiligingswachtwoord in om toegang te krijgen tot de beheertools.",
        "coach_pwd_label": "Coach Wachtwoord",
        "verify_pwd": "Verifieer Wachtwoord",
        "wrong_coach_pwd": "❌ Onjuist wachtwoord! Probeer het opnieuw."
    },
    "Dansk": {
        "welcome": "🎾 Velkommen til Nac Padel Team Performance Hub",
        "select_lang": "Vælg dit sprog:",
        "select_area": "Vælg dit adgangsområde for at fortsætte:",
        "player_title": "👤 Spillerområde",
        "player_desc": "Få adgang til din adgangskodebeskyttede personlige profil for at se og opdatere dine evalueringer.",
        "player_btn": "Log ind som spiller",
        "coach_title": "📋 Trænerområde",
        "coach_desc": "Begrænset adgang for trænerstaben til at administrere data, planlægge træningspas og generere holdparringer.",
        "coach_btn": "Log ind som træner",
        "player_login_title": "🔐 Adgang til spillerområde",
        "player_login_desc": "Vælg dit navn og indtast din adgangskode (din adgangskode er dit **fornavn**).",
        "select_profile": "Vælg din profil:",
        "pwd_label": "Adgangskode (Indtast dit fornavn)",
        "enter_profile": "Gå til min profil",
        "back_home": "⬅️ Tilbage til Start",
        "wrong_pwd": "❌ Forkert adgangskode! Husk at din adgangskode er dit fornavn.",
        "coach_login_title": "🔒 Godkendelse af trænerområde",
        "coach_login_desc": "Indtast sikkerhedsadgangskoden for at få adgang til administrationsværktøjer.",
        "coach_pwd_label": "Træneradgangskode",
        "verify_pwd": "Bekræft adgangskode",
        "wrong_coach_pwd": "❌ Forkert adgangskode! Prøv igen."
    }
}

t = translations[st.session_state.language]

# Complete roster of players with side information ("Left" or "Right")
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

# --- HOME SELECTION SCREEN ---
if st.session_state.nav_mode == "Home":
    # Selettore della lingua in alto a destra o in evidenza
    lang_col1, lang_col2 = st.columns([4, 1])
    with lang_col2:
        selected_lang = st.selectbox(
            t["select_lang"], 
            ["English", "Italiano", "Español", "Svenska", "Nederlands", "Dansk"],
            index=["English", "Italiano", "Español", "Svenska", "Nederlands", "Dansk"].index(st.session_state.language)
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

    st.title(t["welcome"])
    st.markdown(t["select_area"])
    
    col_home1, col_home2 = st.columns(2)
    
    with col_home1:
        st.markdown(f"### {t['player_title']}")
        st.markdown(t["player_desc"])
        if st.button(t["player_btn"], use_container_width=True, type="primary"):
            st.session_state.nav_mode = "Player_Login"
            st.rerun()
            
    with col_home2:
        st.markdown(f"### {t['coach_title']}")
        st.markdown(t["coach_desc"])
        if st.button(t["coach_btn"], use_container_width=True):
            st.session_state.nav_mode = "Coach_Login"
            st.rerun()

# --- PLAYER LOGIN ---
elif st.session_state.nav_mode == "Player_Login":
    st.title(t["player_login_title"])
    st.markdown(t["player_login_desc"])
    
    player_options = [f"{p['fname']} {p['lname']} ({p['side']})" for p in st.session_state.squad_players]
    selected_player_str = st.selectbox(t["select_profile"], player_options)
    
    selected_fname = selected_player_str.split(" ")[0]
    
    player_pwd_input = st.text_input(t["pwd_label"], type="password")
    
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        if st.button(t["enter_profile"], type="primary", use_container_width=True):
            if player_pwd_input.strip().lower() == selected_fname.lower():
                st.session_state.authenticated_player = selected_fname
                st.session_state.nav_mode = "Player_Dashboard"
                st.rerun()
            else:
                st.error(t["wrong_pwd"])
    with col_pl2:
        if st.button(t["back_home"], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- COACH LOGIN ---
elif st.session_state.nav_mode == "Coach_Login":
    st.title(t["coach_login_title"])
    st.markdown(t["coach_login_desc"])
    
    COACH_PASSWORD = "padelcoach2026"
    
    pwd_input = st.text_input(t["coach_pwd_label"], type="password")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(t["verify_pwd"], type="primary", use_container_width=True):
            if pwd_input == COACH_PASSWORD:
                st.session_state.authenticated_coach = True
                st.session_state.nav_mode = "Coach_Dashboard"
                st.rerun()
            else:
                st.error(t["wrong_coach_pwd"])
    with col_btn2:
        if st.button(t["back_home"], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- COACH MANAGEMENT DASHBOARD ---
elif st.session_state.nav_mode == "Coach_Dashboard":
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title("📋 Coach Dashboard - Squad Management & Evaluations")
        st.markdown("As a coach, you can view all players and modify their **Coach Evaluations & Comparisons**.")
    with col_top2:
        if st.button("🚪 Log Out"):
            st.session_state.authenticated_coach = False
            st.session_state.nav_mode = "Home"
            st.rerun()
            
    st.markdown("---")
    
    player_options = [f"{p['fname']} {p['lname']} ({p['side']})" for p in st.session_state.squad_players]
    selected_player_str = st.selectbox("Select player to review/edit coach evaluations:", player_options)
    
    selected_idx = player_options.index(selected_player_str)
    current_player = st.session_state.squad_players[selected_idx]
    
    st.subheader(f"Editing Coach Ratings for: {current_player['fname']} {current_player['lname']}")
    st.info("💡 As coach, you can modify the values below and save them. The player will see these updates in read-only mode.")
    
    with st.form("coach_edit_form"):
        st.markdown("#### Technical Skills (Coach Evaluation)")
        c_tech_inputs = []
        tech_labels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita']
        
        cols = st.columns(3)
        for i, label in enumerate(tech_labels):
            with cols[i % 3]:
                val = st.slider(f"{label} (Coach)", 1, 10, int(current_player['c_tech'][i]), key=f"coach_tech_{i}")
                c_tech_inputs.append(val)
                
        st.markdown("#### Tactics & Mental Skills (Coach Evaluation)")
        c_mental_inputs = []
        mental_labels = ['Chemistry', 'Error Management', 'Positioning', 'Focus', 'Stamina', 'Intensity']
        
        cols2 = st.columns(3)
        for i, label in enumerate(mental_labels):
            with cols2[i % 3]:
                val = st.slider(f"{label} (Coach)", 1, 10, int(current_player['c_mental'][i]), key=f"coach_mental_{i}")
                c_mental_inputs.append(val)
                
        submitted_coach = st.form_submit_button("💾 Save Coach Evaluations", type="primary")
        if submitted_coach:
            st.session_state.squad_players[selected_idx]['c_tech'] = c_tech_inputs
            st.session_state.squad_players[selected_idx]['c_mental'] = c_mental_inputs
            st.success(f"Successfully updated coach evaluations for {current_player['fname']} {current_player['lname']}!")

    if st.button("⬅️ Back to Home"):
        st.session_state.nav_mode = "Home"
        st.rerun()

# --- INDIVIDUAL PLAYER DASHBOARD ---
elif st.session_state.nav_mode == "Player_Dashboard":
    current_player = next((p for p in st.session_state.squad_players if p['fname'] == st.session_state.authenticated_player), None)
    
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title(f"👤 Personal Card: {current_player['fname']} {current_player['lname']} ({current_player['side']})")
    with col_top2:
        if st.button("🚪 Log Out"):
            st.session_state.authenticated_player = None
            st.session_state.nav_mode = "Home"
            st.rerun()
            
    st.markdown("---")
    
    p_tech = current_player['tech']
    p_mental = current_player['mental']
    c_tech = current_player['c_tech']
    c_mental = current_player['c_mental']
    
    html_code = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Nac Padel Team Performance Dashboard</title>
        <style>
            * {{ box-sizing: border-box; touch-action: manipulation; }}
            :root {{
                --bg-primary: #0f172a;
                --bg-card: #1e293b;
                --accent-blue: #38bdf8;
                --accent-purple: #a855f7;
                --accent-green: #22c55e;
                --accent-whatsapp: #25d366;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: var(--bg-primary);
                color: var(--text-main);
                margin: 0;
                padding: 12px;
                -webkit-tap-highlight-color: transparent;
            }}
            header {{ text-align: center; margin-bottom: 16px; }}
            header h1 {{ color: var(--accent-blue); margin: 0 0 4px 0; font-size: 1.4rem; }}
            header p {{ color: var(--text-muted); margin: 0; font-size: 0.8rem; }}
            
            .main-container {{
                max-width: 1000px;
                margin: 0 auto;
                display: flex;
                flex-direction: column;
                gap: 16px;
            }}
            .card {{
                background-color: var(--bg-card);
                border-radius: 14px;
                padding: 16px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.05);
                width: 100%;
            }}
            .card h2 {{ margin-top: 0; text-align: center; font-size: 1.05rem; }}
            
            .actions-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
                gap: 10px;
            }}
            
            .btn {{
                border: none;
                padding: 12px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 0.85rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 6px;
                transition: opacity 0.2s, transform 0.1s;
                text-decoration: none;
                color: #fff;
            }}
            .btn:active {{ transform: scale(0.98); }}
            .btn-whatsapp {{ background-color: #25d366; color: #fff; }}
            .btn-save-img {{ background-color: var(--accent-purple); color: #fff; }}
            .btn-share-link {{ background-color: var(--accent-blue); color: #0f172a; }}
            .btn-export {{ background-color: #f59e0b; color: #0f172a; }}

            .charts-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 16px;
            }}
            .tech-title {{ color: var(--accent-blue); }}
            .mental-title {{ color: var(--accent-purple); }}
            .coach-title {{ color: #f59e0b; }}
            
            .chart-container {{
                position: relative;
                width: 100%;
                height: 260px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            canvas {{
                width: 100% !important;
                height: 100% !important;
            }}

            .controls-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 16px;
            }}
            .control-group {{ display: flex; flex-direction: column; gap: 8px; }}
            .control-item {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 8px;
                background: rgba(255, 255, 255, 0.03);
                padding: 8px 12px;
                border-radius: 8px;
            }}
            .control-item label {{ font-size: 0.85rem; flex: 1; }}
            .control-item input[type="range"] {{
                flex: 1.2;
                height: 24px;
                accent-color: var(--accent-blue);
            }}
            .control-item.purple input[type="range"] {{ accent-color: var(--accent-purple); }}
            .control-item.amber input[type="range"] {{ accent-color: #f59e0b; opacity: 0.8; cursor: not-allowed; }}
            .control-item .val-badge {{ font-weight: bold; min-width: 20px; text-align: right; }}

            .diff-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 0.85rem;
            }}
            .diff-table th, .diff-table td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid rgba(255,255,255,0.08);
            }}
            .diff-table th {{ color: var(--text-muted); }}
            .badge-pos {{ color: #22c55e; font-weight: bold; }}
            .badge-neg {{ color: #ef4444; font-weight: bold; }}
            .badge-eq {{ color: var(--text-muted); }}

            .insights-box {{
                background: rgba(245, 158, 11, 0.08);
                border: 1px solid rgba(245, 158, 11, 0.2);
                border-radius: 10px;
                padding: 14px;
                margin-top: 16px;
            }}
            .insights-box h3 {{
                color: #f59e0b;
                margin-top: 0;
                font-size: 0.95rem;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .insights-list {{
                margin: 0;
                padding-left: 20px;
                font-size: 0.85rem;
                color: var(--text-main);
                display: flex;
                flex-direction: column;
                gap: 6px;
            }}

            .modal-overlay {{
                display: none;
                position: fixed;
                top:0; left:0; right:0; bottom:0;
                background: rgba(0,0,0,0.85);
                z-index: 1000;
                align-items: center;
                justify-content: center;
                padding: 16px;
                overflow-y: auto;
            }}
            .modal {{
                background: var(--bg-card);
                border-radius: 14px;
                padding: 20px;
                width: 100%;
                max-width: 460px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.1);
            }}
            .modal img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                margin: 12px 0;
                border: 1px solid rgba(255,255,255,0.2);
            }}
            .modal input[type="text"] {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.2);
                color: #fff;
                border-radius: 6px;
            }}
            .modal-btn {{
                background: var(--accent-blue);
                color: #0f172a;
                border: none;
                padding: 10px 18px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 8px;
            }}
            
            .toast {{
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: var(--accent-green);
                color: #fff;
                padding: 10px 20px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: bold;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                display: none;
                z-index: 2000;
            }}
        </style>
    </head>
    <body>

        <header>
            <h1>{current_player['fname']} {current_player['lname']} - Performance Dashboard</h1>
            <p>Side: {current_player['side']} • Ratings from 1 to 10</p>
        </header>

        <div class="main-container">
            <div class="card">
                <h2>Actions & Sharing</h2>
                <div class="actions-grid">
                    <button class="btn btn-whatsapp" onclick="shareOnWhatsApp()">💬 WhatsApp</button>
                    <button class="btn btn-save-img" onclick="saveResultAsImage()">💾 Save PNG</button>
                    <button class="btn btn-share-link" onclick="shareOrCopyLink()">🔗 Copy Link</button>
                    <button class="btn btn-export" onclick="exportJsonFile()">📥 Export JSON</button>
                </div>
            </div>

            <div class="charts-grid">
                <div class="card">
                    <h2 class="tech-title">Technical Skills</h2>
                    <div class="chart-container"><canvas id="techCanvas"></canvas></div>
                </div>
                <div class="card">
                    <h2 class="mental-title">Attitude & Tactics</h2>
                    <div class="chart-container"><canvas id="mentalCanvas"></canvas></div>
                </div>
            </div>

            <div class="card">
                <h2>My Ratings (Self-Evaluation)</h2>
                <div class="controls-grid">
                    <div class="control-group">
                        <h3 class="tech-title" style="margin:0 0 4px 0; font-size:0.95rem;">Technique</h3>
                        <div class="control-item"><label>Volley</label><input type="range" id="volley" min="1" max="10" value="{p_tech[0]}" oninput="onDataChange()"><span id="volley-val" class="val-badge">{p_tech[0]}</span></div>
                        <div class="control-item"><label>Smash</label><input type="range" id="smash" min="1" max="10" value="{p_tech[1]}" oninput="onDataChange()"><span id="smash-val" class="val-badge">{p_tech[1]}</span></div>
                        <div class="control-item"><label>Bandeja</label><input type="range" id="bandeja" min="1" max="10" value="{p_tech[2]}" oninput="onDataChange()"><span id="bandeja-val" class="val-badge">{p_tech[2]}</span></div>
                        <div class="control-item"><label>Serve</label><input type="range" id="serve" min="1" max="10" value="{p_tech[3]}" oninput="onDataChange()"><span id="serve-val" class="val-badge">{p_tech[3]}</span></div>
                        <div class="control-item"><label>Defense</label><input type="range" id="defense" min="1" max="10" value="{p_tech[4]}" oninput="onDataChange()"><span id="defense-val" class="val-badge">{p_tech[4]}</span></div>
                        <div class="control-item"><label>Chiquita</label><input type="range" id="chiquita" min="1" max="10" value="{p_tech[5]}" oninput="onDataChange()"><span id="chiquita-val" class="val-badge">{p_tech[5]}</span></div>
                    </div>
                    <div class="control-group">
                        <h3 class="mental-title" style="margin:0 0 4px 0; font-size:0.95rem;">Tactics & Mental</h3>
                        <div class="control-item purple"><label>Pair Chemistry</label><input type="range" id="chemistry" min="1" max="10" value="{p_mental[0]}" oninput="onDataChange()"><span id="chemistry-val" class="val-badge">{p_mental[0]}</span></div>
                        <div class="control-item purple"><label>Error Management</label><input type="range" id="errorManagement" min="1" max="10" value="{p_mental[1]}" oninput="onDataChange()"><span id="errorManagement-val" class="val-badge">{p_mental[1]}</span></div>
                        <div class="control-item purple"><label>Positioning</label><input type="range" id="positioning" min="1" max="10" value="{p_mental[2]}" oninput="onDataChange()"><span id="positioning-val" class="val-badge">{p_mental[2]}</span></div>
                        <div class="control-item purple"><label>Focus</label><input type="range" id="focus" min="1" max="10" value="{p_mental[3]}" oninput="onDataChange()"><span id="focus-val" class="val-badge">{p_mental[3]}</span></div>
                        <div class="control-item purple"><label>Stamina</label><input type="range" id="stamina" min="1" max="10" value="{p_mental[4]}" oninput="onDataChange()"><span id="stamina-val" class="val-badge">{p_mental[4]}</span></div>
                        <div class="control-item purple"><label>Intensity</label><input type="range" id="intensity" min="1" max="10" value="{p_mental[5]}" oninput="onDataChange()"><span id="intensity-val" class="val-badge">{p_mental[5]}</span></div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2 class="coach-title">📋 Coach Evaluation & Comparison</h2>
                <p style="font-size:0.85rem; color:var(--text-muted); text-align:center; margin-top:0;">Evaluations assigned by your coach (Read-only for players).</p>
                
                <div class="controls-grid">
                    <div class="control-group">
                        <h3 class="coach-title" style="margin:0 0 4px 0; font-size:0.95rem;">Technique (Coach)</h3>
                        <div class="control-item amber"><label>Volley (Coach)</label><input type="range" id="c_volley" min="1" max="10" value="{c_tech[0]}" disabled><span class="val-badge">{c_tech[0]}</span></div>
                        <div class="control-item amber"><label>Smash (Coach)</label><input type="range" id="c_smash" min="1" max="10" value="{c_tech[1]}" disabled><span class="val-badge">{c_tech[1]}</span></div>
                        <div class="control-item amber"><label>Bandeja (Coach)</label><input type="range" id="c_bandeja" min="1" max="10" value="{c_tech[2]}" disabled><span class="val-badge">{c_tech[2]}</span></div>
                        <div class="control-item amber"><label>Serve (Coach)</label><input type="range" id="c_serve" min="1" max="10" value="{c_tech[3]}" disabled><span class="val-badge">{c_tech[3]}</span></div>
                        <div class="control-item amber"><label>Defense (Coach)</label><input type="range" id="c_defense" min="1" max="10" value="{c_tech[4]}" disabled><span class="val-badge">{c_tech[4]}</span></div>
                        <div class="control-item amber"><label>Chiquita (Coach)</label><input type="range" id="c_chiquita" min="1" max="10" value="{c_tech[5]}" disabled><span class="val-badge">{c_tech[5]}</span></div>
                    </div>
                    <div class="control-group">
                        <h3 class="coach-title" style="margin:0 0 4px 0; font-size:0.95rem;">Tactics & Mental (Coach)</h3>
                        <div class="control-item amber"><label>Chemistry (Coach)</label><input type="range" id="c_chemistry" min="1" max="10" value="{c_mental[0]}" disabled><span class="val-badge">{c_mental[0]}</span></div>
                        <div class="control-item amber"><label>Errors (Coach)</label><input type="range" id="c_errorManagement" min="1" max="10" value="{c_mental[1]}" disabled><span class="val-badge">{c_mental[1]}</span></div>
                        <div class="control-item amber"><label>Positioning (Coach)</label><input type="range" id="c_positioning" min="1" max="10" value="{c_mental[2]}" disabled><span class="val-badge">{c_mental[2]}</span></div>
                        <div class="control-item amber"><label>Focus (Coach)</label><input type="range" id="c_focus" min="1" max="10" value="{c_mental[3]}" disabled><span class="val-badge">{c_mental[3]}</span></div>
                        <div class="control-item amber"><label>Stamina (Coach)</label><input type="range" id="c_stamina" min="1" max="10" value="{c_mental[4]}" disabled><span class="val-badge">{c_mental[4]}</span></div>
                        <div class="control-item amber"><label>Intensity (Coach)</label><input type="range" id="c_intensity" min="1" max="10" value="{c_mental[5]}" disabled><span class="val-badge">{c_mental[5]}</span></div>
                    </div>
                </div>

                <h3 style="font-size:0.95rem; margin-top:20px; text-align:center; color:var(--text-main);">📊 Differences Table (You vs Coach)</h3>
                <div style="overflow-x:auto;">
                    <table class="diff-table">
                        <thead>
                            <tr>
                                <th>Skill</th>
                                <th>Your Rating</th>
                                <th>Coach Rating</th>
                                <th>Delta (Diff.)</th>
                            </tr>
                        </thead>
                        <tbody id="diffTableBody"></tbody>
                    </table>
                </div>

                <div class="insights-box">
                    <h3>🎯 Focus on Areas for Improvement (Coach Feedback)</h3>
                    <ul class="insights-list" id="insightsList"></ul>
                </div>
            </div>
        </div>

        <div class="modal-overlay" id="mainModal">
            <div class="modal">
                <h3 id="modalTitle" style="margin-top:0">Generated Card</h3>
                <div id="modalContent"></div>
                <button class="modal-btn" onclick="closeModal()">Close</button>
            </div>
        </div>

        <div class="toast" id="toastMsg">✓ Action completed!</div>

        <script>
            const techKeys = ['volley', 'smash', 'bandeja', 'serve', 'defense', 'chiquita'];
            const techLabels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita'];
            
            const mentalKeys = ['chemistry', 'errorManagement', 'positioning', 'focus', 'stamina', 'intensity'];
            const mentalLabels = ['Chemistry', 'Errors', 'Positioning', 'Focus', 'Stamina', 'Intensity'];

            const coachTechVals = {c_tech};
            const coachMentalVals = {c_mental};

            function drawRadarChart(canvasId, labels, dataValues, lineColor, fillColor) {{
                const canvas = document.getElementById(canvasId);
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                
                const rect = canvas.getBoundingClientRect();
                const dpr = window.devicePixelRatio || 1;
                
                canvas.width = rect.width * dpr;
                canvas.height = rect.height * dpr;
                ctx.scale(dpr, dpr);

                const width = rect.width;
                const height = rect.height;
                const centerX = width / 2;
                const centerY = height / 2;
                const radius = Math.min(centerX, centerY) - 32;

                ctx.clearRect(0, 0, width, height);

                const numAxes = labels.length;
                const levels = 5;

                for (let l = 1; l <= levels; l++) {{
                    const r = (radius / levels) * l;
                    ctx.beginPath();
                    for (let i = 0; i < numAxes; i++) {{
                        const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                        const x = centerX + r * Math.cos(angle);
                        const y = centerY + r * Math.sin(angle);
                        if (i === 0) ctx.moveTo(x, y);
                        else ctx.lineTo(x, y);
                    }}
                    ctx.closePath();
                    ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }}

                ctx.font = 'bold 10px -apple-system, sans-serif';
                ctx.fillStyle = '#94a3b8';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';

                for (let i = 0; i < numAxes; i++) {{
                    const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                    const x = centerX + radius * Math.cos(angle);
                    const y = centerY + radius * Math.sin(angle);

                    ctx.beginPath();
                    ctx.moveTo(centerX, centerY);
                    ctx.lineTo(x, y);
                    ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
                    ctx.stroke();

                    const labelR = radius + 18;
                    const lx = centerX + labelR * Math.cos(angle);
                    const ly = centerY + labelR * Math.sin(angle);
                    ctx.fillText(labels[i], lx, ly);
                }}

                ctx.beginPath();
                for (let i = 0; i < numAxes; i++) {{
                    const val = Math.max(1, Math.min(10, dataValues[i]));
                    const r = (radius / 10) * val;
                    const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                    const x = centerX + r * Math.cos(angle);
                    const y = centerY + r * Math.sin(angle);
                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                }}
                ctx.closePath();
                ctx.fillStyle = fillColor;
                ctx.fill();
                ctx.strokeStyle = lineColor;
                ctx.lineWidth = 2.5;
                ctx.stroke();

                for (let i = 0; i < numAxes; i++) {{
                    const val = Math.max(1, Math.min(10, dataValues[i]));
                    const r = (radius / 10) * val;
                    const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                    const x = centerX + r * Math.cos(angle);
                    const y = centerY + r * Math.sin(angle);
                    ctx.beginPath();
                    ctx.arc(x, y, 4, 0, Math.PI * 2);
                    ctx.fillStyle = lineColor;
                    ctx.fill();
                }}
            }}

            function updateAnalysisAndTable() {{
                const tbody = document.getElementById('diffTableBody');
                const insightsList = document.getElementById('insightsList');
                tbody.innerHTML = '';
                insightsList.innerHTML = '';
                
                const allKeys = [...techKeys, ...mentalKeys];
                const allLabels = [...techLabels, ...mentalLabels];
                const allCoachVals = [...coachTechVals, ...coachMentalVals];

                let gaps = [];

                allKeys.forEach((key, index) => {{
                    const myVal = parseInt(document.getElementById(key).value);
                    const coachVal = allCoachVals[index];
                    const diff = myVal - coachVal;
                    
                    let diffHtml = '';
                    if (diff > 0) {{
                        diffHtml = `<span class="badge-pos">+${{diff}} (You > Coach)</span>`;
                    }} else if (diff < 0) {{
                        diffHtml = `<span class="badge-neg">${{diff}} (You < Coach)</span>`;
                        gaps.push({{ label: allLabels[index], myVal, coachVal, diff }});
                    }} else {{
                        diffHtml = `<span class="badge-eq">= (Perfect)</span>`;
                    }}

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${{allLabels[index]}}</td>
                        <td><b>${{myVal}}</b></td>
                        <td><b>${{coachVal}}</b></td>
                        <td>${{diffHtml}}</td>
                    `;
                    tbody.appendChild(row);
                }});

                if (gaps.length === 0) {{
                    const li = document.createElement('li');
                    li.innerHTML = `<b>Great job!</b> There are no areas where the coach rates you below your self-evaluation. Keep up the high standard!`;
                    insightsList.appendChild(li);
                }} else {{
                    gaps.sort((a, b) => a.diff - b.diff);
                    gaps.forEach(gap => {{
                        const li = document.createElement('li');
                        li.innerHTML = `<b>${{gap.label}}</b>: Your rating is ${{gap.myVal}}, but your coach rated you ${{gap.coachVal}} (Diff: ${{gap.diff}}). Focus on instructor feedback here.`;
                        insightsList.appendChild(li);
                    }});
                }}
            }}

            function getTechValues() {{
                return techKeys.map(k => parseInt(document.getElementById(k).value));
            }}

            function getMentalValues() {{
                return mentalKeys.map(k => parseInt(document.getElementById(k).value));
            }}

            function onDataChange() {{
                techKeys.forEach(k => {{
                    document.getElementById(k + '-val').innerText = document.getElementById(k).value;
                }});
                mentalKeys.forEach(k => {{
                    document.getElementById(k + '-val').innerText = document.getElementById(k).value;
                }});

                drawRadarChart('techCanvas', techLabels, getTechValues(), '#38bdf8', 'rgba(56, 189, 248, 0.2)');
                drawRadarChart('mentalCanvas', mentalLabels, getMentalValues(), '#a855f7', 'rgba(168, 85, 247, 0.2)');
                updateAnalysisAndTable();
            }}

            window.onload = function() {{
                onDataChange();
            }};

            function showToast(msg) {{
                const t = document.getElementById('toastMsg');
                t.innerText = msg;
                t.style.display = 'block';
                setTimeout(() => {{ t.style.display = 'none'; }}, 3000);
            }}

            function shareOnWhatsApp() {{
                const tech = getTechValues();
                const mental = getMentalValues();
                const text = encodeURIComponent("🎾 Nac Padel Team Performance Hub - {current_player['fname']} {current_player['lname']}\\nTechnical avg: " + (tech.reduce((a,b)=>a+b,0)/6).toFixed(1) + "\\nMental avg: " + (mental.reduce((a,b)=>a+b,0)/6).toFixed(1));
                window.open("https://api.whatsapp.com/send?text=" + text, "_blank");
            }}

            function saveResultAsImage() {{
                showToast("Generating image preview...");
                document.getElementById('modalTitle').innerText = "Card Snapshot Ready";
                document.getElementById('modalContent').innerHTML = "<p style='font-size:0.85rem; color:#94a3b8;'>Long-press or right-click the charts above to save them directly, or take a screenshot.</p>";
                document.getElementById('mainModal').style.display = 'flex';
            }}

            function shareOrCopyLink() {{
                navigator.clipboard.writeText(window.location.href);
                showToast("✓ Link copied to clipboard!");
            }}

            function exportJsonFile() {{
                const data = {{
                    player: "{current_player['fname']} {current_player['lname']}",
                    side: "{current_player['side']}",
                    tech: getTechValues(),
                    mental: getMentalValues(),
                    coach_tech: coachTechVals,
                    coach_mental: coachMentalVals
                }};
                const blob = new Blob([JSON.stringify(data, null, 2)], {{type: 'application/json'}});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "{current_player['fname']}_{current_player['lname']}_performance.json";
                a.click();
            }}

            function closeModal() {{
                document.getElementById('mainModal').style.display = 'none';
            }}
        </script>
    </body>
    </html>
    """

    components.html(html_code, height=1350, scrolling=True)

    if st.button("⬅️ Back to Home"):
        st.session_state.authenticated_player = None
        st.session_state.nav_mode = "Home"
        st.rerun()
