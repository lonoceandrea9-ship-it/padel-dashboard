import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
import os
import time
import psycopg2
import psycopg2.extras

# Streamlit page configuration
st.set_page_config(
    page_title="Nac Team Performance App",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- CUSTOM CSS: MOBILE FRIENDLY, SFONDO BLU SCURO, TESTO BIANCO, HEADER, BOTTONI E TABELLE STILIZZATE ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1b2a;
        color: #ffffff;
    }
    header[data-testid="stHeader"] {
        background-color: #0d1b2a !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown, div[data-baseweb="select"] span {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1b263b;
        color: #ffffff;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    @media (max-width: 768px) {
        .stColumns {
            flex-direction: column !important;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
    }
    .element-container:has(button:contains("Allenatore")) button,
    .element-container:has(button:contains("Giocatore")) button,
    .element-container:has(button:contains("Coach")) button,
    .element-container:has(button:contains("Player")) button,
    .element-container:has(button:contains("Entrenador")) button,
    .element-container:has(button:contains("Jugador")) button,
    .element-container:has(button:contains("Tränare")) button,
    .element-container:has(button:contains("Spelare")) button,
    .element-container:has(button:contains("Speler")) button,
    .element-container:has(button:contains("Træner")) button,
    .element-container:has(button:contains("Spiller")) button,
    .element-container:has(button:contains("Esci da Area Allenatore")) button,
    .element-container:has(button:contains("Exit Coach Area")) button,
    .element-container:has(button:contains("Salir del Área de Entrenador")) button,
    .element-container:has(button:contains("Logga ut från Tränarområde")) button,
    .element-container:has(button:contains("Verlaat Coachgebied")) button,
    .element-container:has(button:contains("Log ud fra Trænerområde")) button,
    .element-container:has(button:contains("Esci")) button,
    .element-container:has(button:contains("Logout")) button,
    .element-container:has(button:contains("Salir")) button,
    .element-container:has(button:contains("Logga ut")) button,
    .element-container:has(button:contains("Uitloggen")) button,
    .element-container:has(button:contains("Log ud")) button,
    .element-container:has(button:contains("Gestisci Rosa Giocatori")) button,
    .element-container:has(button:contains("Manage Squad")) button,
    .element-container:has(button:contains("Gestión de Plantilla")) button,
    .element-container:has(button:contains("Trupphantering")) button,
    .element-container:has(button:contains("Selectiebeheer")) button,
    .element-container:has(button:contains("Trupstyring")) button {
        background-color: #dc2626 !important;
        color: white !important;
        border-color: #b91c1c !important;
    }
    div.stButton > button, div.stFormSubmitButton > button, button[kind="secondary"] {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #1d4ed8 !important;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    .table-container {
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        margin-bottom: 20px;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #1b263b !important;
        color: #ffffff !important;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #334155;
        white-space: nowrap;
    }
    .custom-table th {
        background-color: #0d1b2a !important;
        color: #ffffff !important;
        padding: 12px;
        text-align: left;
        border-bottom: 2px solid #334155 !important;
        font-weight: 600;
    }
    .custom-table td {
        background-color: #1b263b !important;
        color: #ffffff !important;
        padding: 10px 12px;
        border-bottom: 1px solid #334155 !important;
    }
    .custom-table tr:hover {
        background-color: #24344d !important;
    }
    .feedback-box {
        background-color: #f1f5f9 !important;
        color: #000000 !important;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid #64748b;
        margin-bottom: 8px;
    }
    .feedback-box, .feedback-box * {
        color: #000000 !important;
    }
    .feedback-box .feedback-date {
        color: #334155 !important;
    }
    .coach-note-box {
        background-color: #e0f2fe !important;
        color: #000000 !important;
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 4px solid #0284c7;
        margin-bottom: 8px;
    }
    .coach-note-box, .coach-note-box * {
        color: #000000 !important;
    }
    /* Text inputs and text areas: black text on light background */
    textarea, 
    .stTextArea textarea,
    div[data-baseweb="textarea"] textarea,
    input[type="text"],
    .stTextInput input,
    div[data-baseweb="input"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #000000 !important;
    }
    textarea::placeholder,
    .stTextArea textarea::placeholder,
    input::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
    }
    /* Date input BOX only: black text on white background (was unreadable white-on-white).
       The widget's label ("In quale data...") stays white via the global h1-p rule above. */
    div[data-testid="stDateInput"] div[data-baseweb="input"],
    div[data-testid="stDateInput"] div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
    }
    div[data-testid="stDateInput"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
        -webkit-text-fill-color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- GESTIONE PERSISTENZA AUTOMATICA SU DATABASE (POSTGRES) ---
# All app state (squad, trainings, matches, comments, activity log) is stored
# as a single JSON document in a Postgres table, so it survives restarts and
# redeploys instead of living in a local file on ephemeral disk.
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    """Open a new connection to the Postgres database configured via DATABASE_URL.
    Returns None if no database is configured (e.g. running locally without one)."""
    if not DATABASE_URL:
        print("[DB] DATABASE_URL is not set (empty/None) in this container's environment.", flush=True)
        return None
    try:
        return psycopg2.connect(DATABASE_URL, sslmode="require")
    except Exception as e:
        # Print (not just swallow) so the real cause shows up in `railway logs` /
        # the Railway deploy-log viewer instead of being invisible.
        print(f"[DB] Connection failed: {type(e).__name__}: {e}", flush=True)
        return None


def init_db():
    """Create the app_state table if it doesn't exist yet. Safe to call every run."""
    conn = get_db_connection()
    if conn is None:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS app_state (
                        id INTEGER PRIMARY KEY,
                        data JSONB NOT NULL,
                        updated_at TIMESTAMP NOT NULL DEFAULT NOW()
                    )
                """)
    except Exception:
        pass
    finally:
        conn.close()


def log_activity(action, detail=""):
    """Append an entry to the activity log (Admin only view)."""
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    actor = "System"
    if st.session_state.get("authenticated_admin"):
        actor = "Admin"
    elif st.session_state.get("authenticated_coach"):
        actor = "Coach"
    elif st.session_state.get("authenticated_player"):
        actor = f"Player: {st.session_state.authenticated_player}"
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": actor,
        "action": action,
        "detail": detail
    }
    st.session_state.activity_log.insert(0, entry)
    # Keep last 500 entries
    st.session_state.activity_log = st.session_state.activity_log[:500]

def save_data_to_server(retries=3, delay=0.7):
    """Persist current session data to Postgres.
    Returns True on confirmed success, False on failure (and shows a visible
    error so a failed save is never mistaken for a successful one)."""
    data_to_save = {
        "squad_data": st.session_state.squad_data,
        "planned_trainings": st.session_state.planned_trainings,
        "match_results": st.session_state.match_results,
        "snp_lineups": st.session_state.get("snp_lineups", {}),
        "activity_log": st.session_state.get("activity_log", [])
    }
    last_error = None
    for attempt in range(retries):
        conn = get_db_connection()
        if conn is None:
            last_error = "connessione al database non disponibile"
            time.sleep(delay)
            continue
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO app_state (id, data, updated_at)
                        VALUES (1, %s, NOW())
                        ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data, updated_at = NOW()
                        """,
                        (psycopg2.extras.Json(data_to_save),)
                    )
            return True
        except Exception as e:
            last_error = str(e)
            print(f"[DB] Save query failed: {type(e).__name__}: {e}", flush=True)
            time.sleep(delay)
        finally:
            conn.close()
    st.error(f"⚠️ Salvataggio NON riuscito: impossibile scrivere sul database ({last_error}). "
              f"Le modifiche NON sono state salvate — riprova tra qualche secondo prima di uscire da questa pagina.")
    return False

def load_data_from_server(retries=3, delay=0.7):
    """Load persisted data from Postgres.
    Returns (True, data) where data is the saved dict, or (True, None) if the
    database is reachable but genuinely has no saved data yet.
    Returns (False, None) if the database could not be reached/read after
    retries — callers must NOT treat this the same as 'no data exists yet',
    since doing so risks overwriting real saved data with blank defaults."""
    last_error = None
    for attempt in range(retries):
        conn = get_db_connection()
        if conn is None:
            last_error = "connessione al database non disponibile"
            time.sleep(delay)
            continue
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT data FROM app_state WHERE id = 1")
                    row = cur.fetchone()
                    return True, (row[0] if row else None)
        except Exception as e:
            last_error = str(e)
            print(f"[DB] Load query failed: {type(e).__name__}: {e}", flush=True)
            time.sleep(delay)
        finally:
            conn.close()
    return False, None

# --- TRADUZIONI COMPLETE (6 LINGUE) ---
translations = {
    "Italiano": {
        "welcome": "Nac Team Performance App",
        "select_area": "Seleziona la tua area di accesso per continuare:",
        "player_area": "Area Giocatore",
        "player_desc": "Accedi alla tua scheda personale protetta da password per visualizzare e aggiornare le tue valutazioni.",
        "player_btn": "Accedi come Giocatore",
        "coach_area": "Area Allenatore",
        "coach_desc": "Accesso riservato allo staff tecnico per la gestione dei dati, la pianificazione e le partite.",
        "coach_btn": "Accedi come Allenatore",
        "login_player_title": "Accesso Area Giocatore",
        "login_player_sub": "Seleziona il tuo nome e inserisci la tua password.",
        "profile_select": "Seleziona il tuo profilo:",
        "pwd_label": "Password",
        "enter_card": "Entra nella mia scheda",
        "back_home": "Torna alla Home",
        "wrong_pwd": "Password errata!",
        "coach_login_title": "Autenticazione Area Allenatore",
        "coach_login_sub": "Inserisci la password di sicurezza per accedere alle funzioni di gestione.",
        "coach_pwd_label": "Password Allenatore",
        "verify_pwd": "Verifica Password",
        "logout": "Esci",
        "tech_skills": "Competenze Tecniche",
        "mental_skills": "Attitudine e Tattica (Mentali)",
        "mental_list": ["Attitudine positiva / Supporto partner", "Consistenza gioco", "Gestione errori", "Posizionamento", "Resistenza", "Comunicazione con compagno", "Coachability"],
        "partners_tab": "Ranking Partner",
        "history_tab": "Storico & Miglioramenti",
        "comments_tab": "Commenti & Feedback",
        "eval_coach_tab": "Autovalutazione & Coach",
        "eval_desc": "Regola i cursori e seleziona il tuo stile di gioco per la tua autovalutazione. A sinistra trovi le competenze Tecniche e a destra quelle Mentali.",
        "style_select_lbl": "Seleziona il tuo Stile di Gioco (Autovalutazione):",
        "save_eval": "Salva Autovalutazione",
        "eval_saved": "Autovalutazione salvata con successo!",
        "radar_title": "Grafici a Tela di Ragno (Confronto Separato)",
        "player_radar_title": "Autovalutazione Giocatore",
        "coach_radar_title": "Valutazione Coach",
        "play_style_lbl": "Stile di Gioco:",
        "diff_tables": "Tabelle delle Differenze (Tu vs Coach)",
        "tech_feat": "Caratteristiche Tecniche",
        "mental_feat": "Caratteristiche Mentali",
        "partner_mgmt": "Gestione Ranking Partner",
        "save_partners": "Salva Ranking Partner",
        "partners_saved": "Ranking partner aggiornato con successo!",
        "current_ranking": "Classifica Attuale:",
        "no_partners": "Nessun partner configurato.",
        "history_title": "Storico & Evoluzione Valutazioni Coach",
        "no_history": "Nessuna modifica precedente registrata dal coach.",
        "official_note": "Nota Ufficiale del Coach",
        "no_coach_note": "Nessuna nota inserita al momento dal coach.",
        "peer_feedback": "Feedback dei compagni",
        "select_partner_lbl": "Seleziona compagno:",
        "note_on_partner": "Nota sul compagno:",
        "send_note": "Invia Nota",
        "note_sent": "Nota inviata!",
        "empty_note_warn": "Il testo non può essere vuoto.",
        "received_lbl": "Ricevuti:",
        "coach_dash_title": "Dashboard Allenatore",
        "exit_coach": "Esci da Area Allenatore",
        "manage_roster_btn": "Gestisci Rosa Giocatori",
        "coach_tab_squad": "Gestione Squadra & Presenze",
        "coach_tab_evals": "Gestione Voti Coach",
        "coach_tab_training": "Allenamenti & Focus",
        "coach_tab_matches": "Gestione Partite",
        "coach_tab_comments": "Tutti i Commenti",
        "coach_tab_pairing": "Pairing Coppie Automatico",
        "squad_desc": "I campi 'Trainings' e 'Participated' sono sincronizzati automaticamente con il Calendario Allenamenti Pianificati. Il Commitment (%) viene ricalcolato in tempo reale.",
        "col_name": "Nome", "col_role": "Role", "col_hand": "Mano", "col_style": "Play Style", "col_trainings": "Trainings", "col_participated": "Participated", "col_commitment": "Commitment (%)",
        "work_groups": "Gruppi di Lavoro e Miglioramento Mirato",
        "work_groups_desc": "Raggruppamento automatico di tutti i giocatori in base alle carenze comuni rilevate nelle valutazioni del coach (valori ≤ 6).",
        "no_critics": "Nessuna criticità rilevata (tutti i giocatori hanno voti superiori a 6).",
        "coach_eval_title": "Gestione Voti Coach & Profilo di Gioco",
        "coach_eval_desc": "Seleziona un giocatore per aggiornare le sue valutazioni, il profilo tattico e la nota ufficiale.",
        "select_player_eval": "Seleziona giocatore da valutare:",
        "coach_eval_sub_title": "Valutazione Coach",
        "coach_note_lbl": "Nota / Commento Ufficiale del Coach (Visibile al giocatore)",
        "coach_note_placeholder": "Scrivi qui il commento per il giocatore...",
        "tech_skills_coach": "Competenze Tecniche (Coach)",
        "mental_skills_coach": "Competenze Mentali (Coach)",
        "save_coach_eval": "Salva Voti, Profilo e Nota Coach",
        "training_title": "Pianificazione Allenamento & Focus Consigliato",
        "training_desc": "Seleziona i partecipanti. Il sistema suggerisce le aree prioritarie. Il coach può modificarle, scegliere la data e confermare il salvataggio in calendario.",
        "select_attendees": "Seleziona i partecipanti alla sessione:",
        "training_priorities": "🎯 Aree Prioritarie Consigliate dal Sistema",
        "training_no_attendees": "Seleziona almeno un giocatore per visualizzare il focus di allenamento.",
        "match_mgmt": "Registrazione Partite",
        "match_mgmt_desc": "Seleziona i giocatori per ciascuna squadra (ciascun team richiede 1 giocatore di Sinistra e 1 di Destra).",
        "match_date": "Data Partita",
        "team_a": "Team A",
        "team_b": "Team B",
        "left_role": "Sinistra (Left)",
        "right_role": "Destra (Right)",
        "score_lbl": "Risultato (es. 6-4, 6-2)",
        "register_match": "Registra Partita",
        "same_player_err": "All'interno dello stesso team non puoi selezionare due volte lo stesso giocatore!",
        "match_saved": "Partita registrata con successo!",
        "match_history": "Storico Partite Registrate",
        "global_comments": "Vista Globale Note & Commenti",
        "pairing_title": "Algoritmo Intelligente di Pairing per Coppie",
        "pairing_desc": "Seleziona qui sotto i giocatori disponibili per questa sessione. L'algoritmo abbinerà esclusivamente tra loro i giocatori selezionati, rispettando il vincolo di ruolo (1 Sinistra + 1 Destra) e bilanciando:",
        "pairing_p1": "Peso 1.0: Valutazione complessiva del Coach.",
        "pairing_p2": "Peso 0.5: Volontà / preferenza reciproca dei giocatori.",
        "select_available_players": "Seleziona i giocatori disponibili oggi:",
        "run_pairing": "Genera Coppie Ottimali con i Disponibili",
        "pairing_err": "Per formare le coppie servono almeno un giocatore di sinistra e un giocatore di destra tra i selezionati!",
        "recommended_pairing": "Risultato Pairing Consigliato (Top 5 Team):",
        "unmatched_warn": "Giocatori selezionati ma rimasti esclusi in questo turno per sbilanciamento numerico tra Destra e Sinistra:"
    },
    "English": {
        "welcome": "Nac Team Performance App",
        "select_area": "Select your access area to continue:",
        "player_area": "Player Area",
        "player_desc": "Access your password-protected personal card to view and update your evaluations.",
        "player_btn": "Access as Player",
        "coach_area": "Coach Area",
        "coach_desc": "Restricted access for coaching staff to manage data, planning, and matches.",
        "coach_btn": "Access as Coach",
        "login_player_title": "Player Area Login",
        "login_player_sub": "Select your name and enter your password.",
        "profile_select": "Select your profile:",
        "pwd_label": "Password",
        "enter_card": "Enter my card",
        "back_home": "Back to Home",
        "wrong_pwd": "Wrong password!",
        "coach_login_title": "Coach Area Authentication",
        "coach_login_sub": "Enter the security password to access management features.",
        "coach_pwd_label": "Coach Password",
        "verify_pwd": "Verify Password",
        "logout": "Logout",
        "tech_skills": "Technical Skills",
        "mental_skills": "Attitude & Tactics (Mental)",
        "mental_list": ["Positive Attitude / Partner Support", "Game Consistency", "Error Management", "Positioning", "Stamina", "Partner Communication", "Coachability"],
        "partners_tab": "Partner Ranking",
        "history_tab": "History & Improvements",
        "comments_tab": "Comments & Feedback",
        "eval_coach_tab": "Self-Evaluation & Coach",
        "eval_desc": "Adjust the sliders and select your play style for your self-evaluation. On the left you will find Technical skills and on the right Mental skills.",
        "style_select_lbl": "Select your Play Style (Self-Evaluation):",
        "save_eval": "Save Self-Evaluation",
        "eval_saved": "Self-evaluation successfully saved!",
        "radar_title": "Spider Radar Charts (Separate Comparison)",
        "player_radar_title": "Player Self-Evaluation",
        "coach_radar_title": "Coach Evaluation",
        "play_style_lbl": "Play Style:",
        "diff_tables": "Difference Tables (You vs Coach)",
        "tech_feat": "Technical Features",
        "mental_feat": "Mental Features",
        "partner_mgmt": "Partner Ranking Management",
        "save_partners": "Save Partner Ranking",
        "partners_saved": "Partner ranking successfully updated!",
        "current_ranking": "Current Ranking:",
        "no_partners": "No partners configured.",
        "history_title": "History & Coach Evaluation Evolution",
        "no_history": "No previous modifications recorded by the coach.",
        "official_note": "Official Coach Note",
        "no_coach_note": "No note entered by the coach at the moment.",
        "peer_feedback": "Peer Feedback",
        "select_partner_lbl": "Select partner:",
        "note_on_partner": "Note on partner:",
        "send_note": "Send Note",
        "note_sent": "Note sent!",
        "empty_note_warn": "Text cannot be empty.",
        "received_lbl": "Received:",
        "coach_dash_title": "Coach Dashboard",
        "exit_coach": "Exit Coach Area",
        "manage_roster_btn": "Manage Squad",
        "coach_tab_squad": "Squad Management & Attendance",
        "coach_tab_evals": "Coach Grades Management",
        "coach_tab_training": "Training & Focus",
        "coach_tab_matches": "Match Management",
        "coach_tab_comments": "All Comments",
        "coach_tab_pairing": "Automatic Pair Pairing",
        "squad_desc": "'Trainings' and 'Participated' are automatically synced with the Planned Training Calendar. Commitment (%) is recalculated in real time.",
        "col_name": "Name", "col_role": "Role", "col_hand": "Hand", "col_style": "Play Style", "col_trainings": "Trainings", "col_participated": "Participated", "col_commitment": "Commitment (%)",
        "work_groups": "Work Groups & Targeted Improvement",
        "work_groups_desc": "Automatic grouping of all players based on common weaknesses identified in coach evaluations (values ≤ 6).",
        "no_critics": "No critical issues detected (all players have grades above 6).",
        "coach_eval_title": "Coach Grades Management & Play Profile",
        "coach_eval_desc": "Select a player to update their evaluations, tactical profile, and official note.",
        "select_player_eval": "Select player to evaluate:",
        "coach_eval_sub_title": "Coach Evaluation",
        "coach_note_lbl": "Official Coach Note / Comment (Visible to player)",
        "coach_note_placeholder": "Write the comment for the player here...",
        "tech_skills_coach": "Technical Skills (Coach)",
        "mental_skills_coach": "Mental Skills (Coach)",
        "save_coach_eval": "Save Grades, Profile and Coach Note",
        "training_title": "Training & Focus",
        "training_desc": "Select participants. The system suggests priority areas. The coach can modify them, choose the date, and confirm saving to the calendar.",
        "select_attendees": "Select session attendees:",
        "training_priorities": "🎯 System Recommended Priority Areas",
        "training_no_attendees": "Select at least one player to view training focus.",
        "match_mgmt": "Match Registration",
        "match_mgmt_desc": "Select players for each team (each team requires 1 Left player and 1 Right player).",
        "match_date": "Match Date",
        "team_a": "Team A",
        "team_b": "Team B",
        "left_role": "Left",
        "right_role": "Right",
        "score_lbl": "Result (e.g. 6-4, 6-2)",
        "register_match": "Register Match",
        "same_player_err": "Within the same team you cannot select the same player twice!",
        "match_saved": "Match successfully registered!",
        "match_history": "Registered Match History",
        "global_comments": "Global Notes & Comments View",
        "pairing_title": "Intelligent Pair Pairing Algorithm",
        "pairing_desc": "Select below the players available for this session. The algorithm will pair only the selected players with each other, respecting the role constraint (1 Left + 1 Right) and balancing:",
        "pairing_p1": "Weight 1.0: Overall Coach evaluation.",
        "pairing_p2": "Weight 0.5: Mutual willingness / preference of players.",
        "select_available_players": "Select available players today:",
        "run_pairing": "Generates Optimal Pairs with Available",
        "pairing_err": "To form pairs you need at least one left player and one right player among the selected ones!",
        "recommended_pairing": "Recommended Pairing Result (Top 5 Teams):",
        "unmatched_warn": "Selected players left out in this round due to numerical imbalance between Right and Left:"
    },
    "Español": {
        "welcome": "Nac Team Performance App",
        "select_area": "Selecciona tu área de acceso para continuar:",
        "player_area": "Área de Jugador",
        "player_desc": "Accede a tu ficha personal protegida con contraseña para ver y actualizar tus valoraciones.",
        "player_btn": "Acceder como Jugador",
        "coach_area": "Área de Entrenador",
        "coach_desc": "Acceso restringido al cuerpo técnico para la gestión de datos, planificación y partidos.",
        "coach_btn": "Acceder como Entrenador",
        "login_player_title": "Acceso Área de Jugador",
        "login_player_sub": "Selecciona tu nombre e introduce tu contraseña.",
        "profile_select": "Selecciona tu perfil:",
        "pwd_label": "Contraseña",
        "enter_card": "Entrar en mi ficha",
        "back_home": "Volver al Inicio",
        "wrong_pwd": "¡Contraseña incorrecta!",
        "coach_login_title": "Autenticación Área de Entrenador",
        "coach_login_sub": "Introduce la contraseña de seguridad para acceder a las funciones de gestión.",
        "coach_pwd_label": "Contraseña de Entrenador",
        "verify_pwd": "Verificar Contraseña",
        "logout": "Salir",
        "tech_skills": "Habilidades Técnicas",
        "mental_skills": "Actitud y Táctica (Mentales)",
        "mental_list": ["Actitud positiva / Apoyo al compañero", "Consistencia de juego", "Gestión de errores", "Posicionamiento", "Resistencia", "Comunicación con el compañero", "Coachability"],
        "partners_tab": "Ranking de Compañeros",
        "history_tab": "Historial y Mejoras",
        "comments_tab": "Comentarios y Feedback",
        "eval_coach_tab": "Autovaloración y Coach",
        "eval_desc": "Ajusta los controles deslizantes y selecciona tu estilo de juego para tu autoevaluación. A la izquierda encontrarás las habilidades Técnicas y a la derecha las Mentales.",
        "style_select_lbl": "Selecciona tu Estilo de Juego (Autoevaluación):",
        "save_eval": "Guardar Autoevaluación",
        "eval_saved": "¡Autoevaluación guardada con éxito!",
        "radar_title": "Gráficos de Radar (Comparación Separada)",
        "player_radar_title": "Autoevaluación del Jugador",
        "coach_radar_title": "Evaluación del Entrenador",
        "play_style_lbl": "Estilo de Juego:",
        "diff_tables": "Tablas de Diferencias (Tú vs Entrenador)",
        "tech_feat": "Características Técnicas",
        "mental_feat": "Características Mentales",
        "partner_mgmt": "Gestión de Ranking de Compañeros",
        "save_partners": "Guardar Ranking de Compañeros",
        "partners_saved": "¡Ranking de compañeros actualizado con éxito!",
        "current_ranking": "Clasificación Actual:",
        "no_partners": "Ningún compañero configurado.",
        "history_title": "Historial y Evolución de Valoraciones del Entrenador",
        "no_history": "Ninguna modificación previa registrada por el entrenador.",
        "official_note": "Nota Oficial del Entrenador",
        "no_coach_note": "Ninguna nota introducida por el entrenador en este momento.",
        "peer_feedback": "Feedback de Compañeros",
        "select_partner_lbl": "Selecciona compañero:",
        "note_on_partner": "Nota sobre el compañero:",
        "send_note": "Enviar Nota",
        "note_sent": "¡Nota enviada!",
        "empty_note_warn": "El texto no puede estar vacío.",
        "received_lbl": "Recibidos:",
        "coach_dash_title": "Dashboard de Entrenador",
        "exit_coach": "Salir del Área de Entrenador",
        "manage_roster_btn": "Gestión de Plantilla",
        "coach_tab_squad": "Gestión de Plantilla y Asistencia",
        "coach_tab_evals": "Gestión de Notas del Entrenador",
        "coach_tab_training": "Entrenamiento y Enfoque",
        "coach_tab_matches": "Gestión de Partidos",
        "coach_tab_comments": "Todos los Comentarios",
        "coach_tab_pairing": "Emparejamiento Automático de Parejas",
        "squad_desc": "'Trainings' y 'Participated' se sincronizan automáticamente con el Calendario de Entrenamientos. El Compromiso (%) se recalcula en tiempo real.",
        "col_name": "Nombre", "col_role": "Rol", "col_hand": "Mano", "col_style": "Estilo", "col_trainings": "Entrenamientos", "col_participated": "Participado", "col_commitment": "Compromiso (%)",
        "work_groups": "Grupos de Trabajo y Mejora Dirigida",
        "work_groups_desc": "Agrupación automática de todos los jugadores basada en carencias comunes detectadas en las evaluaciones del entrenador (valores ≤ 6).",
        "no_critics": "Ninguna criticidad detectada (todos los jugadores tienen notas superiores a 6).",
        "coach_eval_title": "Gestión de Notas del Entrenador y Perfil de Juego",
        "coach_eval_desc": "Selecciona un jugador para actualizar sus valoraciones, perfil táctico y nota oficial.",
        "select_player_eval": "Selecciona jugador a evaluar:",
        "coach_eval_sub_title": "Evaluación del Entrenador",
        "coach_note_lbl": "Nota / Comentario Oficial del Entrenador (Visible para el jugador)",
        "coach_note_placeholder": "Escribe aquí el comentario para el jugador...",
        "tech_skills_coach": "Habilidades Técnicas (Entrenador)",
        "mental_skills_coach": "Habilidades Mentales (Entrenador)",
        "save_coach_eval": "Guardar Notas, Perfil y Nota del Entrenador",
        "training_title": "Entrenamiento y Enfoque",
        "training_desc": "Selecciona los participantes. El sistema sugiere áreas prioritarias. El entrenador puede modificarlas, elegir la fecha y confirmar el guardado en el calendario.",
        "select_attendees": "Selecciona los participantes de la sesión:",
        "training_priorities": "🎯 Áreas Prioritarias Recomendadas por el Sistema",
        "training_no_attendees": "Selecciona al menos un jugador para ver el enfoque de entrenamiento.",
        "match_mgmt": "Registro de Partidos",
        "match_mgmt_desc": "Selecciona los jugadores para cada equipo (cada equipo requiere 1 jugador de Izquierda y 1 de Derecha).",
        "match_date": "Fecha del Partido",
        "team_a": "Equipo A",
        "team_b": "Equipo B",
        "left_role": "Izquierda (Left)",
        "right_role": "Derecha (Right)",
        "score_lbl": "Resultado (ej. 6-4, 6-2)",
        "register_match": "Registrar Partido",
        "same_player_err": "¡Dentro del mismo equipo no puedes seleccionar dos veces al mismo jugador!",
        "match_saved": "¡Partido registrado con éxito!",
        "match_history": "Historial de Partidos Registrados",
        "global_comments": "Vista Global de Notas y Comentarios",
        "pairing_title": "Algoritmo Inteligente de Emparejamiento de Parejas",
        "pairing_desc": "Selecciona a continuación los jugadores disponibles para esta sesión. El algoritmo emparejará exclusivamente entre sí a los jugadores seleccionados, respetando la restricción de rol (1 Izquierda + 1 Derecha) y equilibrando:",
        "pairing_p1": "Peso 1.0: Evaluación global del Entrenador.",
        "pairing_p2": "Peso 0.5: Voluntad / preferencia mutua de los jugadores.",
        "select_available_players": "Selecciona los jugadores disponibles hoy:",
        "run_pairing": "Generar Parejas Óptimas con los Disponibles",
        "pairing_err": "¡Para formar parejas se necesita al menos un jugador de izquierda y un jugador de derecha entre los seleccionados!",
        "recommended_pairing": "Resultado de Emparejamiento Recomendado (Top 5 Equipos):",
        "unmatched_warn": "Jugadores seleccionados pero excluidos en esta ronda por desequilibrio numérico entre Derecha e Izquierda:"
    },
    "Svenska": {
        "welcome": "Nac Team Performance App",
        "select_area": "Välj ditt åtkomstområde för att fortsätta:",
        "player_area": "Spelarområde",
        "player_desc": "Gå till ditt lösenordsskyddade personliga kort för att visa och uppdatera dina utvärderingar.",
        "player_btn": "Logga in som Spelare",
        "coach_area": "Tränarområde",
        "coach_desc": "Begränsad åtkomst för tränarstab för datahantering, planering och matcher.",
        "coach_btn": "Logga in som Tränare",
        "login_player_title": "Inloggning Spelarområde",
        "login_player_sub": "Välj ditt namn och ange ditt lösenord.",
        "profile_select": "Välj din profil:",
        "pwd_label": "Lösenord",
        "enter_card": "Gå till mitt kort",
        "back_home": "Tillbaka till Hem",
        "wrong_pwd": "Fel lösenord!",
        "coach_login_title": "Autentisering Tränarområde",
        "coach_login_sub": "Ange säkerhetslösenordet för att komma åt hanteringsfunktioner.",
        "coach_pwd_label": "Tränarlösenord",
        "verify_pwd": "Verifiera lösenord",
        "logout": "Logga ut",
        "tech_skills": "Tekniska färdigheter",
        "mental_skills": "Attityd & Taktik (Mentalt)",
        "mental_list": ["Positiv attityd / Partnersupport", "Spelkonsistens", "Felhantering", "Positionering", "Uthållighet", "Kommunikation med partner", "Coachability"],
        "partners_tab": "Partnerranking",
        "history_tab": "Historik & Förbättringar",
        "comments_tab": "Kommentarer & Feedback",
        "eval_coach_tab": "Självutvärdering & Coach",
        "eval_desc": "Justerreglagen och välj din spelstil för din självutvärdering. Till vänster hittar du Tekniska färdigheter och till höger Mentala.",
        "style_select_lbl": "Välj din Spelstil (Självutvärdering):",
        "save_eval": "Spara Självutvärdering",
        "eval_saved": "Självutvärdering har sparats!",
        "radar_title": "Spindeldiagram (Separat Jämförelse)",
        "player_radar_title": "Spelares Självutvärdering",
        "coach_radar_title": "Coachutvärdering",
        "play_style_lbl": "Spelstil:",
        "diff_tables": "Differenstabeller (Du vs Coach)",
        "tech_feat": "Tekniska Egenskaper",
        "mental_feat": "Mentala Egenskaper",
        "partner_mgmt": "Partnerrankinghantering",
        "save_partners": "Spara Partnerranking",
        "partners_saved": "Partnerranking uppdaterad!",
        "current_ranking": "Aktuell Ranking:",
        "no_partners": "Inga partner konfigurerade.",
        "history_title": "Historik & Coachutvärderingens Utveckling",
        "no_history": "Inga tidigare ändringar registrerade av coachen.",
        "official_note": "Officiell Coachanteckning",
        "no_coach_note": "Ingen anteckning tillagd av coachen för tillfället.",
        "peer_feedback": "Feedback från medspelare",
        "select_partner_lbl": "Välj medspelare:",
        "note_on_partner": "Anteckning om medspelare:",
        "send_note": "Skicka Anteckning",
        "note_sent": "Anteckning skickad!",
        "empty_note_warn": "Texten får inte vara tom.",
        "received_lbl": "Mottagna:",
        "coach_dash_title": "Coachdashboard",
        "exit_coach": "Logga ut från Tränarområde",
        "manage_roster_btn": "Trupphantering",
        "coach_tab_squad": "Trupphantering & Närvaro",
        "coach_tab_evals": "Coachbetygshantering",
        "coach_tab_training": "Träning & Fokus",
        "coach_tab_matches": "Matchhantering",
        "coach_tab_comments": "Alla Kommentarer",
        "coach_tab_pairing": "Automatiskt Parval",
        "squad_desc": "'Trainings' and 'Participated' synkroniseras automatiskt med träningskalendern. Engagemang (%) räknas om i realtid.",
        "col_name": "Namn", "col_role": "Roll", "col_hand": "Hand", "col_style": "Spelstil", "col_trainings": "Träningar", "col_participated": "Deltagit", "col_commitment": "Engagemang (%)",
        "work_groups": "Arbetsgrupper & Riktad Förbättring",
        "work_groups_desc": "Automatisk gruppering av alla spelare baserat på vanliga svagheter identifierade i coachbedömningar (värden ≤ 6).",
        "no_critics": "Inga kritiska punkter upptäckta (alla spelare har betyg över 6).",
        "coach_eval_title": "Coachbetyg & Spelprofil",
        "coach_eval_desc": "Välj en spelare för att uppdatera hens utvärderingar, taktiskt profil och officiell anteckning.",
        "select_player_eval": "Välj spelare att utvärdera:",
        "coach_eval_sub_title": "Coachutvärdering",
        "coach_note_lbl": "Officiell Coachanteckning / Kommentar (Synlig för spelaren)",
        "coach_note_placeholder": "Skriv kommentaren till spelaren här...",
        "tech_skills_coach": "Tekniska Färdigheter (Coach)",
        "mental_skills_coach": "Mentale Färdigheter (Coach)",
        "save_coach_eval": "Spara Betyg, Profil och Coachanteckning",
        "training_title": "Träning & Fokus",
        "training_desc": "Välj deltagare. Systemet föreslår prioriterade områden. Coachen kan ändra dem, välja datum och bekräfta sparandet i kalendern.",
        "select_attendees": "Välj mödedeltagare:",
        "training_priorities": "🎯 Systemets Rekommenderade Prioriterade Områden",
        "training_no_attendees": "Välj minst en spelare för att se träningsfokus.",
        "match_mgmt": "Matchregistrering",
        "match_mgmt_desc": "Välj spelare för varje lag (varje lag kräver 1 Vänsterspelare och 1 Högerspelare).",
        "match_date": "Matchdatum",
        "team_a": "Lag A",
        "team_b": "Lag B",
        "left_role": "Vänster (Left)",
        "right_role": "Höger (Right)",
        "score_lbl": "Resultat (t.ex. 6-4, 6-2)",
        "register_match": "Registrera Match",
        "same_player_err": "Inom samma lag kan du inte välja samma spelare två gånger!",
        "match_saved": "Match registrerad!",
        "match_history": "Registrerad Matchhistorik",
        "global_comments": "Global Översikt av Anteckningar & Kommentarer",
        "pairing_title": "Intelligent Parningalgoritm",
        "pairing_desc": "Välj nedan vilka spelare som är tillgängliga för denna session. Algoritmen parar ihop enbart de valda spelarna, respekterar rollkravet (1 Vänster + 1 Höger) och balanserar:",
        "pairing_p1": "Vikt 1.0: Övergripande Coachbedömning.",
        "pairing_p2": "Vikt 0.5: Spelares ömsesidiga vilja / preferens.",
        "select_available_players": "Välj tillgängliga spelare idag:",
        "run_pairing": "Generera Optimala Par med Tillgängliga",
        "pairing_err": "För att bilda par behöver du minst en vänsterspelare och en högerspelare bland de valda!",
        "recommended_pairing": "Rekommenderat Parresultat (Top 5 Lag):",
        "unmatched_warn": "Spelare som valdes men utelämnades denna omgång på grund av numerisk obalans mellan Höger och Vänster:"
    },
    "Nederlands": {
        "welcome": "Nac Team Performance App",
        "select_area": "Selecteer je toegangsgebied om door te gaan:",
        "player_area": "Spelersgebied",
        "player_desc": "Ga naar je met een wachtwoord beveiligde persoonlijke kaart om je evaluaties te bekijken en bij te werken.",
        "player_btn": "Toegang als Speler",
        "coach_area": "Coachgebied",
        "coach_desc": "Beperkte toegang voor de technische staf voor gegevensbeheer, planning en wedstrijden.",
        "coach_btn": "Toegang als Coach",
        "login_player_title": "Inloggen Spelersgebied",
        "login_player_sub": "Selecteer je naam en voer je wachtwoord in.",
        "profile_select": "Selecteer je profiel:",
        "pwd_label": "Wachtwoord",
        "enter_card": "Ga naar mijn kaart",
        "back_home": "Terug naar Home",
        "wrong_pwd": "Verkeerd wachtwoord!",
        "coach_login_title": "Authenticatie Coachgebied",
        "coach_login_sub": "Voer het beveiligingswachtwoord in om toegang te krijgen tot de beheerfuncties.",
        "coach_pwd_label": "Coachwachtwoord",
        "verify_pwd": "Wachtwoord verifiëren",
        "logout": "Uitloggen",
        "tech_skills": "Technische vaardigheden",
        "mental_skills": "Houding & Tactiek (Mentaal)",
        "mental_list": ["Positieve houding / Partnersupport", "Spelconsistensie", "Foutenbeheer", "Positionering", "Uithoudingsvermogen", "Communicatie met partner", "Coachability"],
        "partners_tab": "Partner Ranking",
        "history_tab": "Geschiedenis & Verbeteringen",
        "comments_tab": "Opmerkingen & Feedback",
        "eval_coach_tab": "Zelfevaluatie & Coach",
        "eval_desc": "Pas de schuifregelaars aan en selecteer je speelstijl voor je zelfevaluatie. Links vind je Technische vaardigheden en rechts Mentale.",
        "style_select_lbl": "Selecteer je Speelstijl (Zelfevaluatie):",
        "save_eval": "Zelfevaluatie Opslaan",
        "eval_saved": "Zelfevaluatie succesvol opgeslagen!",
        "radar_title": "Spindiagrammen (Afzonderlijke Vergelijking)",
        "player_radar_title": "Zelfevaluatie Speler",
        "coach_radar_title": "Coachevaluatie",
        "play_style_lbl": "Speelstijl:",
        "diff_tables": "Verschillentabellen (Jij vs Coach)",
        "tech_feat": "Technische Kenmerken",
        "mental_feat": "Mentale Kenmerken",
        "partner_mgmt": "Partner Ranking Beheer",
        "save_partners": "Partner Ranking Opslaan",
        "partners_saved": "Partner ranking succesvol bijgewerkt!",
        "current_ranking": "Huidige Ranking:",
        "no_partners": "Geen partners geconfigureerd.",
        "history_title": "Geschiedenis & Evolutie Coachevaluaties",
        "no_history": "Geen eerdere wijzigingen geregistreerd door de coach.",
        "official_note": "Officiële Coachnotitie",
        "no_coach_note": "Geen notitie ingevoerd door de coach op dit moment.",
        "peer_feedback": "Feedback van teamgenoten",
        "select_partner_lbl": "Selecteer teamgenoot:",
        "note_on_partner": "Notitie over teamgenoot:",
        "send_note": "Notitie Verzenden",
        "note_sent": "Notitie verzonden!",
        "empty_note_warn": "Tekst mag niet leeg zijn.",
        "received_lbl": "Ontvangen:",
        "coach_dash_title": "Coach Dashboard",
        "exit_coach": "Verlaat Coachgebied",
        "manage_roster_btn": "Selectiebeheer",
        "coach_tab_squad": "Selectiebeheer & Aanwezigheid",
        "coach_tab_evals": "Coach Cijfers Beheer",
        "coach_tab_training": "Training & Focus",
        "coach_tab_matches": "Wedstrijdbeheer",
        "coach_tab_comments": "Alle Opmerkingen",
        "coach_tab_pairing": "Automatische Koppelindeling",
        "squad_desc": "'Trainings' and 'Participated' worden automatisch gesynchroniseerd met de trainingskalender. Betrokkenheid (%) wordt in realtime herberekend.",
        "col_name": "Naam", "col_role": "Rol", "col_hand": "Hand", "col_style": "Stijl", "col_trainings": "Trainingen", "col_participated": "Deelgenomen", "col_commitment": "Betrokkenheid (%)",
        "work_groups": "Werkgroepen & Gerichte Verbetering",
        "work_groups_desc": "Automatische groepering van alle spelers op basis van veelvoorkomende zwakke punten gedetectererd in coachevaluaties (waarden ≤ 6).",
        "no_critics": "Geen kritieke punten gedetecteerd (alle spelers hebben cijfers boven 6).",
        "coach_eval_title": "Coach Cijfers Beheer & Speelprofiel",
        "coach_eval_desc": "Selecteer een speler om hun evaluaties, tactisch profiel en officiële notitie bij te werken.",
        "select_player_eval": "Selecteer speler om te evalueren:",
        "coach_eval_sub_title": "Coachevaluatie",
        "coach_note_lbl": "Officiële Coachnotitie / Opmerking (Zichtbaar voor speler)",
        "coach_note_placeholder": "Schrijf hier de opmerking voor de speler...",
        "tech_skills_coach": "Technische Vaardigheden (Coach)",
        "mental_skills_coach": "Mentale Vaardigheden (Coach)",
        "save_coach_eval": "Cijfers, Profiel en Coachnotitie Opslaan",
        "training_title": "Training & Focus",
        "training_desc": "Selecteer deelnemers. Het systeem suggereert prioritaire gebieden. De coach kan deze wijzigen, de datum kiezen en het opslaan in de kalender bevestigen.",
        "select_attendees": "Selecteer sessiedeelnemers:",
        "training_priorities": "🎯 Door het systeem aanbevolen prioritaire gebieden",
        "training_no_attendees": "Selecteer ten minste één speler om de trainingsfocus te bekijken.",
        "match_mgmt": "Wedstrijdregistratie",
        "match_mgmt_desc": "Selecteer spelers voor elk team (elk team vereist 1 Linkerspeler en 1 Rechterspeler).",
        "match_date": "Wedstrijddatum",
        "team_a": "Team A",
        "team_b": "Team B",
        "left_role": "Links (Left)",
        "right_role": "Rechts (Right)",
        "score_lbl": "Resultat (bijv. 6-4, 6-2)",
        "register_match": "Wedstrijd Registreren",
        "same_player_err": "Binnen hetzelfde team kun je niet twee keer dezelfde speler selecteren!",
        "match_saved": "Wedstrijd succesvol geregistreerd!",
        "match_history": "Geregistreerde Wedstrijdgeschiedenis",
        "global_comments": "Globale Weergave Notities & Opmerkingen",
        "pairing_title": "Intelligent Koppelingsalgoritme",
        "pairing_desc": "Selecteer hieronder de spelers die beschikbaar zijn voor deze sessie. Het algoritme koppelt uitsluitend de geselecteerde spelers aan elkaar, met respect voor de rolbeperking (1 Links + 1 Rechts) en balancing:",
        "pairing_p1": "Gewicht 1.0: Algemene Coachevaluatie.",
        "pairing_p2": "Gewicht 0.5: Wederzijdse wil / voorkeur van spelers.",
        "select_available_players": "Selecteer beschikbare spelers vandaag:",
        "run_pairing": "Genereer Optimale Koppels met Beschikbaren",
        "pairing_err": "Om koppels te vormen heb je minimaal één linkerspeler en één rechterspeler nodig onder de geselecteerden!",
        "recommended_pairing": "Aanbevolen Koppeling Resultaat (Top 5 Teams):",
        "unmatched_warn": "Geselecteerde spelers weggelaten in deze ronde vanwege numeriek evenwicht tussen Rechts en Links:"
    },
    "Dansk": {
        "welcome": "Nac Team Performance App",
        "select_area": "Vælg dit adgangsområde for at fortsætte:",
        "player_area": "Spillerområde",
        "player_desc": "Gå til dit adgangskodebeskyttede personlige kort for at se og opdatere dine evalueringer.",
        "player_btn": "Log ind som Spiller",
        "coach_area": "Trænerområde",
        "coach_desc": "Begrænset adgang for trænerstab til datahåndtering, planlægning og kampe.",
        "coach_btn": "Log ind som Træner",
        "login_player_title": "Login Spillerområde",
        "login_player_sub": "Vælg dit navn og indtast din adgangskode.",
        "profile_select": "Vælg din profil:",
        "pwd_label": "Adgangskode",
        "enter_card": "Gå til mit kort",
        "back_home": "Tilbage til Hjem",
        "wrong_pwd": "Forkert adgangskode!",
        "coach_login_title": "Godkendelse Trænerområde",
        "coach_login_sub": "Indtast sikkerhedsadgangskoden for at få adgang til administrationsfunktionerne.",
        "coach_pwd_label": "Træneradgangskode",
        "verify_pwd": "Bekræft adgangskode",
        "logout": "Log ud",
        "tech_skills": "Tekniske færdigheder",
        "mental_skills": "Holdning & Taktik (Mentalt)",
        "mental_list": ["Positiv holdning / Partnersupport", "Spelkonsistens", "Fejlhåndtering", "Positionering", "Utholdendhed", "Kommunikation med partner", "Coachability"],
        "partners_tab": "Partnerranking",
        "history_tab": "Historik & Forbedringer",
        "comments_tab": "Kommentarer & Feedback",
        "eval_coach_tab": "Selvevaluering & Coach",
        "eval_desc": "Juster skyderne og vælg din spillestil til din selvevaluering. Til venstre finder du Tekniske færdigheder og til højre Mentale.",
        "style_select_lbl": "Vælg din Spillestil (Selvevaluering):",
        "save_eval": "Gem Selvevaluering",
        "eval_saved": "Selvevaluering gemt successfully!",
        "radar_title": "Spindelvævsdiagrammer (Separat Sammenligning)",
        "player_radar_title": "Spillers Selvevaluering",
        "coach_radar_title": "Trænerevaluering",
        "play_style_lbl": "Spillestil:",
        "diff_tables": "Differenstabeller (Du vs Træner)",
        "tech_feat": "Tekniske Egenskaber",
        "mental_feat": "Mentale Egenskaber",
        "partner_mgmt": "Partnerranking Håndtering",
        "save_partners": "Gem Partnerranking",
        "partners_saved": "Partnerranking opdateret!",
        "current_ranking": "Aktuel Ranking:",
        "no_partners": "Ingen partnere konfigureret.",
        "history_title": "Historik & Trænerevalueringens Udvikling",
        "no_history": "Ingen tidligere ændringer registreret af træneren.",
        "official_note": "Officiel Trænernote",
        "no_coach_note": "Ingen note indtastet af træneren i øjeblikket.",
        "peer_feedback": "Medspillerfeedback",
        "select_partner_lbl": "Vælg medspiller:",
        "note_on_partner": "Note om medspiller:",
        "send_note": "Send Note",
        "note_sent": "Note sendt!",
        "empty_note_warn": "Teksten må ikke være tom.",
        "received_lbl": "Modtagne:",
        "coach_dash_title": "Træner Dashboard",
        "exit_coach": "Log ud fra Trænerområde",
        "manage_roster_btn": "Trupstyring",
        "coach_tab_squad": "Trupstyring & Fremmøde",
        "coach_tab_evals": "Trænerkarakterer Håndtering",
        "coach_tab_training": "Träning & Fokus",
        "coach_tab_matches": "Kampstyring",
        "coach_tab_comments": "Alle Kommentarer",
        "coach_tab_pairing": "Automatisk Makkerparring",
        "squad_desc": "'Trainings' and 'Participated' synkroniseres automatisk med træningskalenderen. Engagement (%) genberegnes i realtid.",
        "col_name": "Navn", "col_role": "Rolle", "col_hand": "Hånd", "col_style": "Stil", "col_trainings": "Träninger", "col_participated": "Deltaget", "col_commitment": "Engagement (%)",
        "work_groups": "Arbejdsgrupper & Målrettet Forbedring",
        "work_groups_desc": "Automatisk gruppering af alle spillere baseret på almindelige svagheder fundet i trænerevalueringer (værdier ≤ 6).",
        "no_critics": "Ingen kritiske punkter opdaget (alle spillere har karakterer over 6).",
        "coach_eval_title": "Trænerkarakterer & Spillerprofil",
        "coach_eval_desc": "Vælg en spiller for at opdatere vedkommendes evalueringer, taktiske profil og officielle note.",
        "select_player_eval": "Vælg spiller at evaluere:",
        "coach_eval_sub_title": "Trænerevaluering",
        "coach_note_lbl": "Officiel Trænernote / Kommentar (Synlig for spilleren)",
        "coach_note_placeholder": "Skriv kommentaren til spilleren her...",
        "tech_skills_coach": "Tekniske Færdigheder (Træner)",
        "mental_skills_coach": "Mentale Færdigheder (Træner)",
        "save_coach_eval": "Gem Karakterer, Profil og Trænernote",
        "training_title": "Träning & Fokus",
        "training_desc": "Vælg deltagere. Systemet foreslår prioriterede områder. Træneren kan ændre dem, vælge dato og bekræfte lagring i kalenderen.",
        "select_attendees": "Vælg mødedeltagere:",
        "training_priorities": "🎯 Systemets Anbefalede Prioriterede Områder",
        "training_no_attendees": "Vælg mindst én spiller for at se træningsfokus.",
        "match_mgmt": "Kampregistrering",
        "match_mgmt_desc": "Vælg spillere til hvert hold (hvert hold kræver 1 Venstrespiller og 1 Højrespiller).",
        "match_date": "Kampdato",
        "team_a": "Hold A",
        "team_b": "Hold B",
        "left_role": "Venstre (Left)",
        "right_role": "Højre (Right)",
        "score_lbl": "Resultat (f.eks. 6-4, 6-2)",
        "register_match": "Registrer Kamp",
        "same_player_err": "Inden for det samme hold kan du ikke vælge den samme spiller to gange!",
        "match_saved": "Kamp registreret!",
        "match_history": "Registreret Kamphistorik",
        "global_comments": "Global Oversigt over Noter & Kommentarer",
        "pairing_title": "Intelligent Parringsalgoritme",
        "pairing_desc": "Vælg nedenfor de spillere, der er tilgængelige til denne session. Algoritmen parrer udelukkende de valgte spillere med hinanden, idet den respekterer rollekravet (1 Venstre + 1 Højre) og balancerer:",
        "pairing_p1": "Vægt 1.0: Overordnede Trænerevaluering.",
        "pairing_p2": "Vikt 0.5: Spillernes gensidige vilje / præference.",
        "select_available_players": "Vælg tilgængelige spillere i dag:",
        "run_pairing": "Generer Optimal Par med Tilgængelige",
        "pairing_err": "För att bilda par behöver du minst en vänsterspelare och en högerspelare bland de valda!",
        "recommended_pairing": "Anbefalet Parringsresultat (Top 5 Hold):",
        "unmatched_warn": "Spillere valgt men udeladt i denne runde på grund af numerisk ubalance mellem Højre og Venstre:"
    }
}

# --- CALENDARIO SNP (condiviso tra area Coach e area Giocatore) ---
SNP_CALENDAR = [
    {"id": 1, "date": "27-Sep", "iso": "2026-09-27", "home": "NAC", "away": "Padelmadena", "label": "27-Sep  NAC  vs  Padelmadena"},
    {"id": 2, "date": "03-Oct", "iso": "2026-10-03", "home": "La Ultima Ronda", "away": "NAC", "label": "03-Oct  La Ultima Ronda  vs  NAC"},
    {"id": 3, "date": "25-Oct", "iso": "2026-10-25", "home": "NAC", "away": "Awa Pool Club", "label": "25-Oct  NAC  vs  Awa Pool Club"},
    {"id": 4, "date": "07-Nov", "iso": "2026-11-07", "home": "Gomez Hoyos Padel", "away": "NAC", "label": "07-Nov  Gomez Hoyos Padel  vs  NAC"},
    {"id": 5, "date": "28-Nov", "iso": "2026-11-28", "home": "Padelmadena", "away": "NAC", "label": "28-Nov  Padelmadena  vs  NAC"},
    {"id": 6, "date": "13-Dec", "iso": "2026-12-13", "home": "NAC", "away": "La Ultima Ronda", "label": "13-Dec  NAC  vs  La Ultima Ronda"},
    {"id": 7, "date": "10-Jan", "iso": "2027-01-10", "home": "NAC", "away": "Awa Pool Club", "label": "10-Jan  NAC  vs  Awa Pool Club"},
]


def normalize_snp_lineups(lineups):
    """JSON turns the integer day ids into strings when data is saved and
    reloaded. Convert them back to int so lookups by day id always work."""
    fixed = {}
    for k, v in (lineups or {}).items():
        try:
            fixed[int(k)] = v
        except (TypeError, ValueError):
            fixed[k] = v
    return fixed
