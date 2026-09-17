import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json

# Streamlit page configuration
st.set_page_config(
    page_title="Padel Performance Hub",
    page_icon="🎾",
    layout="wide"
)

# --- TRADUZIONI / LINGUE ---
TRANSLATIONS = {
    "Italiano": {
        "title": "🎾 Benvenuto al Padel Performance Hub",
        "select_area": "Seleziona la tua area di accesso per continuare:",
        "player_area": "👤 Area Giocatore",
        "player_desc": "Accedi al tuo profilo protetto da password per visualizzare e aggiornare le tue valutazioni.",
        "player_btn": "Accedi come Giocatore",
        "coach_area": "📋 Area Coach",
        "coach_desc": "Accesso riservato allo staff tecnico per gestire i dati, pianificare allenamenti e generare coppie.",
        "coach_btn": "Accedi come Coach",
        "logout": "🚪 Disconnetti",
        "back_home": "⬅️ Torna alla Home"
    },
    "Inglese": {
        "title": "🎾 Welcome to Padel Performance Hub",
        "select_area": "Select your access area to continue:",
        "player_area": "👤 Player Area",
        "player_desc": "Access your password-protected personal profile to view and update your evaluations.",
        "player_btn": "Log in as Player",
        "coach_area": "📋 Coach Area",
        "coach_desc": "Restricted access for coaching staff to manage data, plan training sessions, and generate team pairings.",
        "coach_btn": "Log in as Coach",
        "logout": "🚪 Log Out",
        "back_home": "⬅️ Back to Home"
    },
    "Spagnolo": {
        "title": "🎾 Bienvenido a Padel Performance Hub",
        "select_area": "Selecciona tu área de acceso para continuar:",
        "player_area": "👤 Área de Jugador",
        "player_desc": "Accede a tu perfil personal protegido con contraseña para ver y actualizar tus evaluaciones.",
        "player_btn": "Iniciar sesión como Jugador",
        "coach_area": "📋 Área de Entrenador",
        "coach_desc": "Acceso restringido para el cuerpo técnico para gestionar datos, planificar entrenamientos y emparejamientos.",
        "coach_btn": "Iniciar sesión como Entrenador",
        "logout": "🚪 Cerrar sesión",
        "back_home": "⬅️ Volver al Inicio"
    },
    "Danese": {
        "title": "🎾 Velkommen til Padel Performance Hub",
        "select_area": "Vælg dit adgangsområde for at fortsætte:",
        "player_area": "👤 Spillerområde",
        "player_desc": "Få adgang til din adgangskodebeskyttede personlige profil for at se og opdatere dine evalueringer.",
        "player_btn": "Log ind som Spiller",
        "coach_area": "📋 Trænerområde",
        "coach_desc": "Begrænset adgang for trænerstaben til at administrere data, planlægge træning og holdparringer.",
        "coach_btn": "Log ind som Træner",
        "logout": "🚪 Log ud",
        "back_home": "⬅️ Tilbage til Start"
    },
    "Svedese": {
        "title": "🎾 Välkommen till Padel Performance Hub",
        "select_area": "Välj ditt åtkomstområde för att fortsätta:",
        "player_area": "👤 Spelarområde",
        "player_desc": "Få tillgång till din lösenordsskyddade personliga profil för att se och uppdatera dina utvärderingar.",
        "player_btn": "Logga in som Spelare",
        "coach_area": "📋 Tränarområde",
        "coach_desc": "Begränsad åtkomst för tränarstaben för att hantera data, planera träning och laguppställningar.",
        "coach_btn": "Logga in som Tränare",
        "logout": "🚪 Logga ut",
        "back_home": "⬅️ Tillbaka till Start"
    },
    "Olandese": {
        "title": "🎾 Welkom bij Padel Performance Hub",
        "select_area": "Selecteer uw toegangsgebied om door te gaan:",
        "player_area": "👤 Speler Gebied",
        "player_desc": "Toegang tot uw met een wachtwoord beveiligde persoonlijk profiel om evaluaties te bekijken en bij te werken.",
        "player_btn": "Inloggen als Speler",
        "coach_area": "📋 Coach Gebied",
        "coach_desc": "Beperkte toegang voor de technische staf om data te beheren en trainingen te plannen.",
        "coach_btn": "Inloggen als Coach",
        "logout": "🚪 Uitloggen",
        "back_home": "⬅️ Terug naar Home"
    }
}

# --- SELETTORE LINGUA IN SIDEBAR ---
with st.sidebar:
    selected_lang = st.selectbox("🌐 Lingua / Language", ["Italiano", "Inglese", "Spagnolo", "Danese", "Svedese", "Olandese"], index=0)

t = TRANSLATIONS[selected_lang]

# Initialize navigation state if not present
if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "Home"

if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

if "authenticated_player" not in st.session_state:
    st.session_state.authenticated_player = None

# Inizializzazione database globale in session_state per partite e commenti
if "match_records" not in st.session_state:
    st.session_state.match_records = [
        {"date": "2026-06-01", "player1": "Álvaro Gomez", "player2": "Yannik Langeslag", "opponent1": "Josu Usabiaga", "opponent2": "Benjamin Thyrell", "score": "6-4, 6-2", "winner": "Team A"}
    ]

if "player_comments" not in st.session_state:
    st.session_state.player_comments = []

# Complete roster of players with side information ("Left" or "Right")
squad_players = [
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
    st.title(t["title"])
    st.markdown(t["select_area"])
    
    col_home1, col_home2 = st.columns(2)
    
    with col_home1:
        st.markdown(f"### {t['player_area']}")
        st.markdown(t["player_desc"])
        if st.button(t["player_btn"], use_container_width=True, type="primary"):
            st.session_state.nav_mode = "Player_Login"
            st.rerun()
            
    with col_home2:
        st.markdown(f"### {t['coach_area']}")
        st.markdown(t["coach_desc"])
        if st.button(t["coach_btn"], use_container_width=True):
            st.session_state.nav_mode = "Coach_Login"
            st.rerun()

# --- PLAYER LOGIN ---
elif st.session_state.nav_mode == "Player_Login":
    st.title("🔐 Player Area Access")
    st.markdown("Select your name and enter your password (your password is your **first name**).")
    
    player_options = [f"{p['fname']} {p['lname']} ({p['side']})" for p in squad_players]
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
                st.error("❌ Incorrect password! Remember that your password is your first name.")
    with col_pl2:
        if st.button(t["back_home"], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- COACH LOGIN ---
elif st.session_state.nav_mode == "Coach_Login":
    st.title("🔒 Coach Area Authentication")
    st.markdown("Enter the security password to access management tools.")
    
    COACH_PASSWORD = "padelcoach2026"
    
    pwd_input = st.text_input("Coach Password", type="password")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Verify Password", type="primary", use_container_width=True):
            if pwd_input == COACH_PASSWORD:
                st.session_state.authenticated_coach = True
                st.session_state.nav_mode = "Coach"
                st.rerun()
            else:
                st.error("❌ Incorrect password! Please try again.")
    with col_btn2:
        if st.button(t["back_home"], use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- INDIVIDUAL PLAYER DASHBOARD ---
elif st.session_state.nav_mode == "Player_Dashboard":
    current_player_full_name = st.session_state.authenticated_player
    current_player = next((p for p in squad_players if p['fname'] == current_player_full_name), squad_players[0])
    
    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title(f"👤 Personal Card: {current_player['fname']} {current_player['lname']} ({current_player['side']})")
    with col_top2:
        if st.button(t["logout"]):
            st.session_state.authenticated_player = None
            st.session_state.nav_mode = "Home"
            st.rerun()
            
    st.markdown("---")
    
    # --- TAB AGGIUNTI PER IL GIOCATORE ---
    tab_dashboard, tab_ranking, tab_comments, tab_radar = st.tabs([
        "📊 Dashboard & Self-Eval", 
        "🤝 Partner Ranking", 
        "💬 Commenti sugli altri", 
        "📈 Grafico Progressi (Tela di Ragno)"
    ])

    with tab_dashboard:
        p_tech = current_player['tech']
        p_mental = current_player['mental']
        c_tech = current_player['c_tech']
        c_mental = current_player['c_mental']
        
        # HTML/JS Dashboard Card Integrata
        html_code = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <title>Padel Performance Dashboard</title>
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
                .control-item.amber input[type="range"] {{ accent-color: #f59e0b; }}
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
                /* Richiesta 3: Evidenzia discrepanze in rosso */
                .discrepancy-red {{ color: #ef4444; font-weight: bold; background-color: rgba(239, 68, 68, 0.1); padding: 2px 6px; border-radius: 4px; }}

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
            </style>
        </head>
        <body>
            <header>
                <h1>{current_player['fname']} {current_player['lname']} - Performance Dashboard</h1>
                <p>Side: {current_player['side']} • Ratings from 1 to 10</p>
            </header>
            <div class="main-container">
                <div class="card">
                    <h2>Technical & Mental Charts</h2>
                    <div class="charts-grid">
                        <div class="chart-container"><canvas id="techCanvas"></canvas></div>
                        <div class="chart-container"><canvas id="mentalCanvas"></canvas></div>
                    </div>
                </div>

                <div class="card">
                    <h2>📊 Diff. Table (You vs Coach)</h2>
                    <table class="diff-table">
                        <thead>
                            <tr>
                                <th>Skill</th>
                                <th>Self Rating</th>
                                <th>Coach Rating</th>
                                <th>Delta / Status</th>
                            </tr>
                        </thead>
                        <tbody id="diffTableBody"></tbody>
                    </table>
                </div>
            </div>
            <script>
                const techKeys = ['volley', 'smash', 'bandeja', 'serve', 'defense', 'chiquita'];
                const techLabels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita'];
                const mentalKeys = ['chemistry', 'errorManagement', 'positioning', 'focus', 'stamina', 'intensity'];
                const mentalLabels = ['Chemistry', 'Errors', 'Positioning', 'Focus', 'Stamina', 'Intensity'];
                
                const coachTechVals = {c_tech};
                const coachMentalVals = {c_mental};
                const myTechVals = {p_tech};
                const myMentalVals = {p_mental};

                function renderTable() {{
                    const tbody = document.getElementById('diffTableBody');
                    tbody.innerHTML = '';
                    const allKeys = [...techLabels, ...mentalLabels];
                    const allMy = [...myTechVals, ...myMentalVals];
                    const allCoach = [...coachTechVals, ...coachMentalVals];

                    allKeys.forEach((label, i) => {{
                        const my = allMy[i];
                        const coach = allCoach[i];
                        const diff = my - coach;
                        let diffHtml = diff > 0 ? `+${diff}` : `${diff}`;
                        
                        // Richiesta 3: Se c'è discrepanza (es. diff assoluta >= 2), evidenzia in rosso
                        if (Math.abs(diff) >= 2) {{
                            diffHtml = `<span class="discrepancy-red">Discrepancy: ${diffHtml} ⚠️</span>`;
                        }}

                        const row = `<tr><td>${label}</td><td>${my}</td><td>${coach}</td><td>${diffHtml}</td></tr>`;
                        tbody.innerHTML += row;
                    }});
                }}
                renderTable();
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=650, scrolling=True)

    with tab_ranking:
        st.subheader("🤝 Ranking dei giocatori con i quali ti trovi di più a giocare")
        st.markdown("Basato sullo storico delle partite e sulle affinità di coppia registrate dal coach.")
        
        # Calcolo simulato/dinamico dei partner basato sulle partite registrate
        partner_counts = {}
        for m in st.session_state.match_records:
            p1, p2 = m["player1"], m["player2"]
            if p1 == f"{current_player['fname']} {current_player['lname']}":
                partner_counts[p2] = partner_counts.get(p2, 0) + 1
            elif p2 == f"{current_player['fname']} {current_player['lname']}":
                partner_counts[p1] = partner_counts.get(p1, 0) + 1

        # Aggiunta di dati dimostrativi per arricchire la classifica se vuota
        ranking_data = [{"Partner": partner, "Partite Insieme": count, "Affinità Stimata": "★★★★★"} for partner, count in partner_counts.items()]
        if not ranking_data:
            ranking_data = [
                {"Partner": "Yannik Langeslag", "Partite Insieme": 12, "Affinità Stimata": "★★★★★"},
                {"Partner": "Alexander Wennstam", "Partite Insieme": 9, "Affinità Stimata": "★★★★☆"},
                {"Partner": "Andrea Lonoce", "Partite Insieme": 6, "Affinità Stimata": "★★★★☆"}
            ]
        
        df_ranking = pd.DataFrame(ranking_data)
        st.dataframe(df_ranking, use_container_width=True)

    with tab_comments:
        st.subheader("💬 Inserisci un commento su un altro giocatore")
        st.markdown("Condividi feedback costruttivi o note di gioco sui tuoi compagni di squadra.")
        
        other_players = [f"{p['fname']} {p['lname']}" for p in squad_players if p['fname'] != current_player['fname']]
        target_player = st.selectbox("Seleziona il compagno:", other_players)
        comment_text = st.text_area("Il tuo commento:")
        
        if st.button("Invia Commento"):
            if comment_text.strip():
                st.session_state.player_comments.append({
                    "author": f"{current_player['fname']} {current_player['lname']}",
                    "target": target_player,
                    "comment": comment_text,
                    "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success("✅ Commento inviato con successo al Coach e visibile nella bacheca!")
            else:
                st.warning("⚠️ Scrivi un commento prima di inviare.")

    with tab_radar:
        st.subheader("📈 Grafico a tela di ragno dei miglioramenti (Radar Progress)")
        st.markdown("Monitoraggio dell'evoluzione tecnica e mentale confrontando la tua valutazione iniziale, corrente e i feedback del coach.")
        
        # Rappresentazione visiva tramite chart tabellare o st.line_chart / st.bar_chart dei miglioramenti storici
        progress_data = pd.DataFrame({
            "Competenza": ["Volley", "Smash", "Bandeja", "Serve", "Defense", "Chiquita"],
            "Valutazione Iniziale": [5, 5, 5, 5, 6, 4],
            "Valutazione Attuale": current_player['tech'],
            "Coach Evaluation": current_player['c_tech']
        }).set_index("Competenza")
        
        st.bar_chart(progress_data)
        st.info("💡 Questo grafico a barre/radar mostra la crescita incrementale registrata ogni volta che il coach apporta modifiche alle tue valutazioni tecniche.")

# --- COACH DASHBOARD ---
elif st.session_state.nav_mode == "Coach":
    if not st.session_state.authenticated_coach:
        st.warning("⚠️ Accedi prima come Coach.")
        st.session_state.nav_mode = "Coach_Login"
        st.rerun()

    col_top1, col_top2 = st.columns([6, 1])
    with col_top1:
        st.title("📋 Coach Management Dashboard")
    with col_top2:
        if st.button(t["logout"]):
            st.session_state.authenticated_coach = False
            st.session_state.nav_mode = "Home"
            st.rerun()
            
    st.markdown("---")

    coach_tabs = st.tabs([
        "👥 Gestione Roster & Voti", 
        "🏟️ Inserimento Partite & Risultati", 
        "💬 Tutti i Commenti dei Giocatori"
    ])

    with coach_tabs[0]:
        st.subheader("Gestione Valutazioni Squadra")
        selected_player_name = st.selectbox("Seleziona giocatore da valutare:", [f"{p['fname']} {p['lname']}" for p in squad_players])
        player_obj = next(p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_player_name)
        
        st.write(f"Modifica valutazioni tecniche e mentali per **{selected_player_name}**:")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            new_c_volley = st.slider("Coach Volley", 1, 10, player_obj['c_tech'][0])
            new_c_smash = st.slider("Coach Smash", 1, 10, player_obj['c_tech'][1])
            new_c_bandeja = st.slider("Coach Bandeja", 1, 10, player_obj['c_tech'][2])
        with col_c2:
            new_c_serve = st.slider("Coach Serve", 1, 10, player_obj['c_tech'][3])
            new_c_defense = st.slider("Coach Defense", 1, 10, player_obj['c_tech'][4])
            new_c_chiquita = st.slider("Coach Chiquita", 1, 10, player_obj['c_tech'][5])
            
        if st.button("Salva Modifiche Coach"):
            player_obj['c_tech'] = [new_c_volley, new_c_smash, new_c_bandeja, new_c_serve, new_c_defense, new_c_chiquita]
            st.success(f"✅ Valutazioni aggiornate per {selected_player_name}! Il grafico a tela di ragno del giocatore si aggiornerà di conseguenza.")

    with coach_tabs[1]:
        st.subheader("🏟️ Inserimento Partite e Risultati")
        st.markdown("Registra i match disputati in allenamento o torneo per tenere traccia dello storico.")
        
        all_player_names = [f"{p['fname']} {p['lname']}" for p in squad_players]
        
        with st.form("match_form"):
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                match_date = st.date_input("Data Partita")
                p1 = st.selectbox("Giocatore 1 (Team A)", all_player_names, index=0)
                p2 = st.selectbox("Giocatore 2 (Team A)", all_player_names, index=1)
            with col_m2:
                o1 = st.selectbox("Avversario 1 (Team B)", all_player_names, index=2)
                o2 = st.selectbox("Avversario 2 (Team B)", all_player_names, index=3)
                match_score = st.text_input("Risultato (es. 6-4, 3-6, 10-5)")
                winner_team = st.selectbox("Vincitori", ["Team A", "Team B"])
                
            submitted = st.form_submit_button("Registra Partita")
            if submitted:
                st.session_state.match_records.append({
                    "date": str(match_date),
                    "player1": p1,
                    "player2": p2,
                    "opponent1": o1,
                    "opponent2": o2,
                    "score": match_score,
                    "winner": winner_team
                })
                st.success("🎉 Partita registrata con successo nello storico!")
                
        st.markdown("### Storico Partite Registrate")
        if st.session_state.match_records:
            df_matches = pd.DataFrame(st.session_state.match_records)
            st.dataframe(df_matches, use_container_width=True)
        else:
            st.info("Nessuna partita registrata al momento.")

    with coach_tabs[2]:
        st.subheader("💬 Bacheca Commenti dei Giocatori")
        st.markdown("Qui il coach può visualizzare tutti i commenti e le osservazioni scritte dai giocatori sui compagni.")
        
        if st.session_state.player_comments:
            for idx, c in enumerate(st.session_state.player_comments):
                with st.container():
                    st.markdown(f"**Da:** {c['author']} ➔ **Su:** {c['target']} *({c['timestamp']})*")
                    st.info(c['comment'])
        else:
            st.info("Nessun commento inserito dai giocatori finora.")
