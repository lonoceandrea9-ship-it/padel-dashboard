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
    page_title="Padel AI",
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
    _ld = translations.get(st.session_state.get("language", "English"), translations["English"])
    st.error(_ld.get('save_failed_error', '⚠️ Save FAILED: unable to write to the database ({error}). Your changes were NOT saved — try again in a few seconds before leaving this page.').format(error=last_error))
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
        "welcome": "Padel AI",
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
        "welcome": "Padel AI",
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
        "welcome": "Padel AI",
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
        "welcome": "Padel AI",
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
        "welcome": "Padel AI",
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
        "welcome": "Padel AI",
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


CALENDAR_TRANSLATIONS = {
    "Italiano": {"calendar_tab": "Calendario Partite", "cal_next": "Prossima partita", "cal_in_days": "tra {n} giorni", "cal_today": "oggi", "cal_tomorrow": "domani", "cal_home": "casa", "cal_away": "trasferta", "cal_you_play": "Giochi in pista {pista} con {partner}", "cal_you_play_alone": "Giochi in pista {pista}", "cal_not_called": "Non sei convocato per questa partita", "cal_lineup_pending": "Formazione non ancora pubblicata", "cal_date": "Data", "cal_match": "Partita", "cal_you": "Tu", "cal_court": "Pista", "cal_result": "Risultato", "cal_details": "Dettagli partite (piste, coppie e risultati)", "cal_notes": "Note", "cal_season_over": "Stagione terminata: nessuna partita in programma.", "cal_player1": "Giocatore 1", "cal_player2": "Giocatore 2"},
    "English": {"calendar_tab": "Match Calendar", "cal_next": "Next match", "cal_in_days": "in {n} days", "cal_today": "today", "cal_tomorrow": "tomorrow", "cal_home": "home", "cal_away": "away", "cal_you_play": "You're playing on court {pista} with {partner}", "cal_you_play_alone": "You're playing on court {pista}", "cal_not_called": "You're not in the lineup for this match", "cal_lineup_pending": "Lineup not out yet", "cal_date": "Date", "cal_match": "Match", "cal_you": "You", "cal_court": "Court", "cal_result": "Result", "cal_details": "Match details (courts, pairs and results)", "cal_notes": "Notes", "cal_season_over": "Season finished: no upcoming matches.", "cal_player1": "Player 1", "cal_player2": "Player 2"},
    "Español": {"calendar_tab": "Calendario de Partidos", "cal_next": "Próximo partido", "cal_in_days": "en {n} días", "cal_today": "hoy", "cal_tomorrow": "mañana", "cal_home": "local", "cal_away": "visitante", "cal_you_play": "Juegas en la pista {pista} con {partner}", "cal_you_play_alone": "Juegas en la pista {pista}", "cal_not_called": "No estás convocado para este partido", "cal_lineup_pending": "Alineación aún no publicada", "cal_date": "Fecha", "cal_match": "Partido", "cal_you": "Tú", "cal_court": "Pista", "cal_result": "Resultado", "cal_details": "Detalles de los partidos (pistas, parejas y resultados)", "cal_notes": "Notas", "cal_season_over": "Temporada terminada: no hay partidos programados.", "cal_player1": "Jugador 1", "cal_player2": "Jugador 2"},
    "Svenska": {"calendar_tab": "Matchkalender", "cal_next": "Nästa match", "cal_in_days": "om {n} dagar", "cal_today": "idag", "cal_tomorrow": "imorgon", "cal_home": "hemma", "cal_away": "borta", "cal_you_play": "Du spelar på bana {pista} med {partner}", "cal_you_play_alone": "Du spelar på bana {pista}", "cal_not_called": "Du är inte uttagen till denna match", "cal_lineup_pending": "Laguppställning ej publicerad", "cal_date": "Datum", "cal_match": "Match", "cal_you": "Du", "cal_court": "Bana", "cal_result": "Resultat", "cal_details": "Matchdetaljer (banor, par och resultat)", "cal_notes": "Anteckningar", "cal_season_over": "Säsongen är slut: inga kommande matcher.", "cal_player1": "Spelare 1", "cal_player2": "Spelare 2"},
    "Nederlands": {"calendar_tab": "Wedstrijdkalender", "cal_next": "Volgende wedstrijd", "cal_in_days": "over {n} dagen", "cal_today": "vandaag", "cal_tomorrow": "morgen", "cal_home": "thuis", "cal_away": "uit", "cal_you_play": "Je speelt op baan {pista} met {partner}", "cal_you_play_alone": "Je speelt op baan {pista}", "cal_not_called": "Je staat niet in de opstelling voor deze wedstrijd", "cal_lineup_pending": "Opstelling nog niet bekend", "cal_date": "Datum", "cal_match": "Wedstrijd", "cal_you": "Jij", "cal_court": "Baan", "cal_result": "Uitslag", "cal_details": "Wedstrijddetails (banen, koppels en uitslagen)", "cal_notes": "Notities", "cal_season_over": "Seizoen afgelopen: geen komende wedstrijden.", "cal_player1": "Speler 1", "cal_player2": "Speler 2"},
    "Dansk": {"calendar_tab": "Kampkalender", "cal_next": "Næste kamp", "cal_in_days": "om {n} dage", "cal_today": "i dag", "cal_tomorrow": "i morgen", "cal_home": "hjemme", "cal_away": "ude", "cal_you_play": "Du spiller på bane {pista} med {partner}", "cal_you_play_alone": "Du spiller på bane {pista}", "cal_not_called": "Du er ikke udtaget til denne kamp", "cal_lineup_pending": "Holdopstilling ikke offentliggjort endnu", "cal_date": "Dato", "cal_match": "Kamp", "cal_you": "Dig", "cal_court": "Bane", "cal_result": "Resultat", "cal_details": "Kampdetaljer (baner, par og resultater)", "cal_notes": "Noter", "cal_season_over": "Sæsonen er slut: ingen kommende kampe.", "cal_player1": "Spiller 1", "cal_player2": "Spiller 2"},
}
for _lang, _vals in CALENDAR_TRANSLATIONS.items():
    translations.setdefault(_lang, {}).update(_vals)

# --- RECUPERO PASSWORD CON DOMANDA DI SICUREZZA ---
SECURITY_QUESTION_KEYS = ["sq_pet", "sq_city", "sq_school", "sq_friend", "sq_custom"]

SECURITY_TRANSLATIONS = {
    "Italiano": {
        "forgot_pwd_btn": "Password dimenticata?", "forgot_title": "Recupero password",
        "forgot_sub": "Rispondi alla tua domanda di sicurezza per impostare una nuova password.",
        "forgot_first_login": "Non hai ancora fatto il primo accesso: la tua password è il tuo nome di battesimo.",
        "forgot_no_question": "Non hai impostato una domanda di sicurezza, quindi non puoi recuperare la password da solo. Chiedi al coach o all'admin.",
        "forgot_answer_lbl": "La tua risposta", "forgot_new_pwd": "Nuova password", "forgot_confirm_pwd": "Conferma nuova password",
        "forgot_submit": "Imposta nuova password", "forgot_cancel": "Annulla",
        "forgot_wrong_answer": "Risposta errata. Tentativi rimasti: {n}",
        "forgot_too_many": "Troppi tentativi errati. Chiedi al coach o all'admin di aiutarti.",
        "forgot_success": "Password aggiornata! Ora puoi accedere con la nuova password.",
        "pwd_empty": "La password non può essere vuota.", "pwd_mismatch": "Le password non coincidono. Riprova.",
        "sec_section_title": "Domanda di sicurezza (recupero password)",
        "sec_section_desc": "Serve per recuperare la password se la dimentichi. La risposta non viene mostrata a nessuno.",
        "sec_not_set_warn": "Non hai ancora impostato una domanda di sicurezza: se dimentichi la password non potrai recuperarla da solo.",
        "sec_current_lbl": "Domanda attuale:", "sec_question_lbl": "Domanda di sicurezza",
        "sec_custom_lbl": "Se hai scelto 'Altra domanda', scrivila qui", "sec_answer_lbl": "Risposta",
        "sec_save_btn": "Salva domanda di sicurezza", "sec_saved": "Domanda di sicurezza salvata!",
        "sec_answer_empty": "La risposta non può essere vuota.", "sec_custom_empty": "Scrivi la tua domanda personalizzata.",
        "sq_pet": "Come si chiamava il tuo primo animale domestico?", "sq_city": "In che città sei nato/a?",
        "sq_school": "Come si chiamava la tua scuola elementare?", "sq_friend": "Come si chiama il tuo migliore amico d'infanzia?",
        "sq_custom": "Altra domanda (scrivila tu)",
    },
    "English": {
        "forgot_pwd_btn": "Forgot password?", "forgot_title": "Password recovery",
        "forgot_sub": "Answer your security question to set a new password.",
        "forgot_first_login": "You haven't logged in for the first time yet: your password is your first name.",
        "forgot_no_question": "You haven't set a security question, so you can't recover your password yourself. Ask the coach or the admin.",
        "forgot_answer_lbl": "Your answer", "forgot_new_pwd": "New password", "forgot_confirm_pwd": "Confirm new password",
        "forgot_submit": "Set new password", "forgot_cancel": "Cancel",
        "forgot_wrong_answer": "Wrong answer. Attempts left: {n}",
        "forgot_too_many": "Too many wrong attempts. Ask the coach or the admin for help.",
        "forgot_success": "Password updated! You can now log in with your new password.",
        "pwd_empty": "The password can't be empty.", "pwd_mismatch": "The passwords don't match. Try again.",
        "sec_section_title": "Security question (password recovery)",
        "sec_section_desc": "Used to recover your password if you forget it. The answer is never shown to anyone.",
        "sec_not_set_warn": "You haven't set a security question yet: if you forget your password you won't be able to recover it yourself.",
        "sec_current_lbl": "Current question:", "sec_question_lbl": "Security question",
        "sec_custom_lbl": "If you chose 'Other question', write it here", "sec_answer_lbl": "Answer",
        "sec_save_btn": "Save security question", "sec_saved": "Security question saved!",
        "sec_answer_empty": "The answer can't be empty.", "sec_custom_empty": "Write your custom question.",
        "sq_pet": "What was the name of your first pet?", "sq_city": "In which city were you born?",
        "sq_school": "What was the name of your primary school?", "sq_friend": "What is the name of your best childhood friend?",
        "sq_custom": "Other question (write your own)",
    },
    "Español": {
        "forgot_pwd_btn": "¿Has olvidado la contraseña?", "forgot_title": "Recuperar contraseña",
        "forgot_sub": "Responde a tu pregunta de seguridad para establecer una nueva contraseña.",
        "forgot_first_login": "Aún no has hecho el primer acceso: tu contraseña es tu nombre de pila.",
        "forgot_no_question": "No has configurado una pregunta de seguridad, así que no puedes recuperar la contraseña tú solo. Pide ayuda al entrenador o al admin.",
        "forgot_answer_lbl": "Tu respuesta", "forgot_new_pwd": "Nueva contraseña", "forgot_confirm_pwd": "Confirmar nueva contraseña",
        "forgot_submit": "Establecer nueva contraseña", "forgot_cancel": "Cancelar",
        "forgot_wrong_answer": "Respuesta incorrecta. Intentos restantes: {n}",
        "forgot_too_many": "Demasiados intentos fallidos. Pide ayuda al entrenador o al admin.",
        "forgot_success": "¡Contraseña actualizada! Ya puedes acceder con la nueva contraseña.",
        "pwd_empty": "La contraseña no puede estar vacía.", "pwd_mismatch": "Las contraseñas no coinciden. Inténtalo de nuevo.",
        "sec_section_title": "Pregunta de seguridad (recuperar contraseña)",
        "sec_section_desc": "Sirve para recuperar la contraseña si la olvidas. La respuesta no se muestra a nadie.",
        "sec_not_set_warn": "Aún no has configurado una pregunta de seguridad: si olvidas la contraseña no podrás recuperarla tú solo.",
        "sec_current_lbl": "Pregunta actual:", "sec_question_lbl": "Pregunta de seguridad",
        "sec_custom_lbl": "Si elegiste 'Otra pregunta', escríbela aquí", "sec_answer_lbl": "Respuesta",
        "sec_save_btn": "Guardar pregunta de seguridad", "sec_saved": "¡Pregunta de seguridad guardada!",
        "sec_answer_empty": "La respuesta no puede estar vacía.", "sec_custom_empty": "Escribe tu pregunta personalizada.",
        "sq_pet": "¿Cómo se llamaba tu primera mascota?", "sq_city": "¿En qué ciudad naciste?",
        "sq_school": "¿Cómo se llamaba tu colegio de primaria?", "sq_friend": "¿Cómo se llama tu mejor amigo de la infancia?",
        "sq_custom": "Otra pregunta (escríbela tú)",
    },
    "Svenska": {
        "forgot_pwd_btn": "Glömt lösenordet?", "forgot_title": "Återställ lösenord",
        "forgot_sub": "Svara på din säkerhetsfråga för att välja ett nytt lösenord.",
        "forgot_first_login": "Du har inte loggat in första gången än: ditt lösenord är ditt förnamn.",
        "forgot_no_question": "Du har inte angett någon säkerhetsfråga, så du kan inte återställa lösenordet själv. Fråga tränaren eller admin.",
        "forgot_answer_lbl": "Ditt svar", "forgot_new_pwd": "Nytt lösenord", "forgot_confirm_pwd": "Bekräfta nytt lösenord",
        "forgot_submit": "Spara nytt lösenord", "forgot_cancel": "Avbryt",
        "forgot_wrong_answer": "Fel svar. Försök kvar: {n}",
        "forgot_too_many": "För många felaktiga försök. Be tränaren eller admin om hjälp.",
        "forgot_success": "Lösenordet är uppdaterat! Nu kan du logga in med det nya lösenordet.",
        "pwd_empty": "Lösenordet får inte vara tomt.", "pwd_mismatch": "Lösenorden matchar inte. Försök igen.",
        "sec_section_title": "Säkerhetsfråga (återställ lösenord)",
        "sec_section_desc": "Används för att återställa lösenordet om du glömmer det. Svaret visas aldrig för någon.",
        "sec_not_set_warn": "Du har inte angett någon säkerhetsfråga: om du glömmer lösenordet kan du inte återställa det själv.",
        "sec_current_lbl": "Nuvarande fråga:", "sec_question_lbl": "Säkerhetsfråga",
        "sec_custom_lbl": "Om du valde 'Annan fråga', skriv den här", "sec_answer_lbl": "Svar",
        "sec_save_btn": "Spara säkerhetsfråga", "sec_saved": "Säkerhetsfrågan är sparad!",
        "sec_answer_empty": "Svaret får inte vara tomt.", "sec_custom_empty": "Skriv din egen fråga.",
        "sq_pet": "Vad hette ditt första husdjur?", "sq_city": "I vilken stad föddes du?",
        "sq_school": "Vad hette din lågstadieskola?", "sq_friend": "Vad heter din bästa barndomsvän?",
        "sq_custom": "Annan fråga (skriv själv)",
    },
    "Nederlands": {
        "forgot_pwd_btn": "Wachtwoord vergeten?", "forgot_title": "Wachtwoord herstellen",
        "forgot_sub": "Beantwoord je beveiligingsvraag om een nieuw wachtwoord in te stellen.",
        "forgot_first_login": "Je hebt nog niet voor het eerst ingelogd: je wachtwoord is je voornaam.",
        "forgot_no_question": "Je hebt geen beveiligingsvraag ingesteld, dus je kunt je wachtwoord niet zelf herstellen. Vraag het aan de coach of de admin.",
        "forgot_answer_lbl": "Jouw antwoord", "forgot_new_pwd": "Nieuw wachtwoord", "forgot_confirm_pwd": "Bevestig nieuw wachtwoord",
        "forgot_submit": "Nieuw wachtwoord instellen", "forgot_cancel": "Annuleren",
        "forgot_wrong_answer": "Verkeerd antwoord. Resterende pogingen: {n}",
        "forgot_too_many": "Te veel verkeerde pogingen. Vraag de coach of de admin om hulp.",
        "forgot_success": "Wachtwoord bijgewerkt! Je kunt nu inloggen met je nieuwe wachtwoord.",
        "pwd_empty": "Het wachtwoord mag niet leeg zijn.", "pwd_mismatch": "De wachtwoorden komen niet overeen. Probeer het opnieuw.",
        "sec_section_title": "Beveiligingsvraag (wachtwoord herstellen)",
        "sec_section_desc": "Wordt gebruikt om je wachtwoord te herstellen als je het vergeet. Het antwoord wordt aan niemand getoond.",
        "sec_not_set_warn": "Je hebt nog geen beveiligingsvraag ingesteld: als je je wachtwoord vergeet, kun je het niet zelf herstellen.",
        "sec_current_lbl": "Huidige vraag:", "sec_question_lbl": "Beveiligingsvraag",
        "sec_custom_lbl": "Als je 'Andere vraag' koos, schrijf hem hier", "sec_answer_lbl": "Antwoord",
        "sec_save_btn": "Beveiligingsvraag opslaan", "sec_saved": "Beveiligingsvraag opgeslagen!",
        "sec_answer_empty": "Het antwoord mag niet leeg zijn.", "sec_custom_empty": "Schrijf je eigen vraag.",
        "sq_pet": "Hoe heette je eerste huisdier?", "sq_city": "In welke stad ben je geboren?",
        "sq_school": "Hoe heette je basisschool?", "sq_friend": "Hoe heet je beste jeugdvriend?",
        "sq_custom": "Andere vraag (schrijf zelf)",
    },
    "Dansk": {
        "forgot_pwd_btn": "Glemt adgangskode?", "forgot_title": "Gendan adgangskode",
        "forgot_sub": "Svar på dit sikkerhedsspørgsmål for at vælge en ny adgangskode.",
        "forgot_first_login": "Du har ikke logget ind første gang endnu: din adgangskode er dit fornavn.",
        "forgot_no_question": "Du har ikke valgt et sikkerhedsspørgsmål, så du kan ikke gendanne adgangskoden selv. Spørg træneren eller admin.",
        "forgot_answer_lbl": "Dit svar", "forgot_new_pwd": "Ny adgangskode", "forgot_confirm_pwd": "Bekræft ny adgangskode",
        "forgot_submit": "Gem ny adgangskode", "forgot_cancel": "Annuller",
        "forgot_wrong_answer": "Forkert svar. Forsøg tilbage: {n}",
        "forgot_too_many": "For mange forkerte forsøg. Bed træneren eller admin om hjælp.",
        "forgot_success": "Adgangskoden er opdateret! Nu kan du logge ind med den nye adgangskode.",
        "pwd_empty": "Adgangskoden må ikke være tom.", "pwd_mismatch": "Adgangskoderne matcher ikke. Prøv igen.",
        "sec_section_title": "Sikkerhedsspørgsmål (gendan adgangskode)",
        "sec_section_desc": "Bruges til at gendanne adgangskoden, hvis du glemmer den. Svaret vises aldrig for nogen.",
        "sec_not_set_warn": "Du har endnu ikke valgt et sikkerhedsspørgsmål: hvis du glemmer adgangskoden, kan du ikke gendanne den selv.",
        "sec_current_lbl": "Nuværende spørgsmål:", "sec_question_lbl": "Sikkerhedsspørgsmål",
        "sec_custom_lbl": "Hvis du valgte 'Andet spørgsmål', skriv det her", "sec_answer_lbl": "Svar",
        "sec_save_btn": "Gem sikkerhedsspørgsmål", "sec_saved": "Sikkerhedsspørgsmålet er gemt!",
        "sec_answer_empty": "Svaret må ikke være tomt.", "sec_custom_empty": "Skriv dit eget spørgsmål.",
        "sq_pet": "Hvad hed dit første kæledyr?", "sq_city": "I hvilken by er du født?",
        "sq_school": "Hvad hed din folkeskole?", "sq_friend": "Hvad hedder din bedste barndomsven?",
        "sq_custom": "Andet spørgsmål (skriv selv)",
    },
}
for _lang, _vals in SECURITY_TRANSLATIONS.items():
    translations.setdefault(_lang, {}).update(_vals)

COACH_TRANSLATIONS = {
    "Italiano": {
        'first_login_title': '🔒 Primo Accesso: Imposta la tua Nuova Password',
        'first_login_welcome': 'Benvenuto **{name}**! Per motivi di sicurezza, essendo il tuo primo accesso, devi impostare una password personale che solo tu conoscerai.',
        'first_login_save_btn': 'Salva Password e Accedi',
        'first_login_success': '✅ Password impostata e salvata correttamente!',
        'first_login_hint_error': '❌ Primo accesso: inserisci il tuo nome di battesimo come password.',
        'coach_wrong_pwd': '❌ Password errata! Riprova.',
        'admin_pwd_label': 'Password Admin',
        'admin_wrong_pwd': '❌ Password admin errata.',
        'admin_pwd_mgmt_title': '🔑 Gestione Password Giocatori',
        'admin_pwd_mgmt_desc': 'Visualizza e modifica la password di ciascun giocatore. Le password sono salvate in chiaro: usa questa funzione con cautela.',
        'admin_pwd_mgmt_expander': 'Mostra / modifica tutte le password',
        'admin_pwd_of': 'Password di {name}',
        'admin_pwd_save_btn': '💾 Salva Tutte le Password',
        'admin_pwd_updated': '✅ Password aggiornate per: {names}',
        'no_changes_to_save': 'Nessuna modifica da salvare.',
        'roster_modal_title': '👥 Pannello Gestione Rosa Giocatori (Aggiungi o Rimuovi)',
        'roster_add_title': 'Aggiungi Nuovo Giocatore',
        'roster_fname_lbl': 'Nome',
        'roster_lname_lbl': 'Cognome',
        'roster_dup_error': 'Un giocatore con questo nome e cognome esiste già nella rosa!',
        'roster_add_success': 'Giocatore {name} aggiunto con successo!',
        'roster_name_required': 'Nome e Cognome non possono essere vuoti.',
        'roster_delete_title': 'Elimina Giocatore Esistente',
        'roster_select_remove': 'Seleziona giocatore da rimuovere',
        'roster_remove_success': 'Giocatore {name} rimosso con successo!',
        'squad_save_btn': '💾 Salva Modifiche Rosa e Ruoli',
        'squad_save_success': 'Tutte le modifiche alla rosa, ruoli e destri/mancini sono state salvate permanentemente!',
        'roster_role_lbl': 'Posizione / Ruolo',
        'roster_hand_lbl': 'Mano',
        'roster_style_lbl': 'Stile di Gioco',
        'roster_add_btn': '➕ Aggiungi Giocatore',
        'roster_remove_btn': '🗑️ Rimuovi Giocatore',
        'partner_prefs_title': '🏆 Preferenze Partner di **{name}**',
        'total_players_present': 'Totale giocatori presenti: **{n}**',
        'improvement_area': '📌 Area di miglioramento: **{skill}** ({n} giocatori)',
        'grade_label': 'Voto: {val}',
        'partner_prefs_desc': 'Ranking dei compagni con cui il giocatore preferisce giocare (impostato da lui nella sua area) e chi, tra gli altri, ha indicato lui come partner preferito. Utile per capire le affinità prima di valutare.',
        'partner_prefs_own': '**{name}** preferisce giocare con:',
        'partner_prefs_none': 'Nessuna preferenza impostata da questo giocatore.',
        'partner_prefs_reverse_title': 'Chi ha indicato **{name}** come partner preferito:',
        'partner_prefs_reverse_none': 'Nessun altro giocatore lo ha indicato come partner preferito.',
        'col_partner': 'Compagno',
        'col_score': 'Punteggio',
        'col_player': 'Giocatore',
        'training_system_analysis': 'Il sistema ha analizzato i voti del gruppo presente e suggerisce le seguenti 3 priorità:',
        'training_priority_1': '🔥 1° Priorità Consigliata',
        'training_priority_2': '⚡ 2° Priorità Consigliata',
        'training_priority_3': '💡 3° Priorità Consigliata',
        'avg_label': 'Media: {v}/10',
        'training_customize_title': '✏️ Personalizzazione e Conferma del Coach',
        'training_customize_desc': "Il coach può modificare le priorità dal menu a tendina e scegliere in quale data salvare l'allenamento nel calendario:",
        'priority1_coach_lbl': '1° Priorità (Coach)',
        'priority2_coach_lbl': '2° Priorità (Coach)',
        'priority3_coach_lbl': '3° Priorità (Coach)',
        'training_date_question': '📅 In quale data vuoi salvare questo allenamento?',
        'training_confirm_btn': '✅ Conferma e Salva nel Calendario',
        'training_saved_success': '🎉 Allenamento salvato con successo per il giorno {date}!',
        'group_split_title': '👥 Suddivisione in Gruppi da 4 (in base alla debolezza)',
        'group_split_desc': "I giocatori selezionati vengono raggruppati in **gruppi da 4** in base alla loro **debolezza principale**, così ogni gruppo può lavorare su un obiettivo specifico e mirato invece di un'unica priorità per tutti.",
        'group_min_players': 'Servono almeno {n} giocatori disponibili per formare un gruppo. Al momento ce ne sono {m}.',
        'group_label': 'Gruppo {i}',
        'group_incomplete_suffix': ' (gruppo incompleto)',
        'group_main_weakness': '🎯 Debolezza principale',
        'group_focus_lbl': 'Focus allenamento — Gruppo {i}',
        'group_date_question': '📅 In quale data vuoi salvare questi allenamenti di gruppo?',
        'group_save_btn': '✅ Salva Allenamenti per Gruppo',
        'group_saved_success': '🎉 {n} allenamenti di gruppo salvati per il giorno {date}!',
        'training_history_title': '📅 Storico Calendario Allenamenti Pianificati',
        'training_edit_title': '✏️ Modifica Allenamento',
        'training_select_edit': 'Seleziona allenamento da modificare',
        'priority1_lbl': '1° Priorità',
        'priority2_lbl': '2° Priorità',
        'priority3_lbl': '3° Priorità',
        'training_date_lbl': '📅 Data allenamento',
        'participants_lbl': 'Partecipanti',
        'training_save_edit_btn': '💾 Salva Modifiche Allenamento',
        'select_at_least_one_participant': 'Seleziona almeno un partecipante.',
        'training_edit_success': 'Allenamento modificato con successo!',
        'training_delete_title': '🗑️ Cancella Allenamento dal Calendario',
        'training_select_delete': 'Seleziona allenamento da rimuovere',
        'training_delete_btn': '🗑️ Elimina Allenamento Selezionato',
        'training_delete_success': 'Allenamento del {date} eliminato con successo dal calendario!',
        'no_trainings_saved': 'Nessun allenamento ancora confermato e salvato nel calendario.',
        'snp_mgmt_title': '📅 Calendario & Registrazione Partite SNP',
        'snp_mgmt_desc': 'Gestione delle **7 giornate SNP**. Per ogni incontro assegna i giocatori NAC e il **risultato di ogni pista**.',
        'snp_select_day': '📆 Seleziona la giornata SNP',
        'snp_formation_title': '1️⃣ Formazione',
        'snp_formation_desc': 'Scegli 2 giocatori NAC per ogni pista. Potrai inserire il risultato in un secondo momento, quando la partita sarà giocata.',
        'snp_notes_lbl': '📝 Note / Commenti giornata (opzionale)',
        'snp_notes_placeholder': 'Osservazioni, infortuni, ecc.',
        'snp_save_formation_btn': '💾 Salva Formazione',
        'snp_formation_saved': '✅ Formazione salvata per **{label}**! Potrai inserire i risultati quando la partita sarà stata giocata.',
        'snp_results_title': '2️⃣ Risultati',
        'snp_no_lineup_info': 'ℹ️ Assegna prima i giocatori nella Formazione qui sopra: potrai poi inserire qui i risultati.',
        'snp_results_desc': 'Inserisci il risultato di ogni pista quando disponibile. I giocatori restano quelli assegnati nella Formazione.',
        'snp_save_results_btn': '🏆 Salva Risultati',
        'snp_results_saved': '✅ Risultati salvati per **{label}**!',
        'snp_summary_title': '📋 Riepilogo Completo Calendario SNP',
        'snp_courts_filled': '{n}/5 piste compilate',
        'snp_not_filled': 'Non compilata',
        'snp_no_lineup_yet': 'Nessuna formazione ancora inserita per questa giornata.',
        'snp_reset_expander': '🗑️ Reset dati SNP',
        'snp_reset_btn': 'Cancella TUTTE le formazioni e risultati SNP',
        'snp_reset_success': 'Dati SNP resettati.',
        'pairing_confirm_btn': '✅ Conferma Selezione Pairing',
        'pairing_confirm_success': 'Pairing confermato e salvato con successo!',
        'save_failed_error': '⚠️ Salvataggio NON riuscito: impossibile scrivere sul database ({error}). Le modifiche NON sono state salvate — riprova tra qualche secondo prima di uscire da questa pagina.',
        'db_unreachable_error': "⚠️ Impossibile connettersi al database. I tuoi dati salvati potrebbero non essere visibili in questo momento. Per proteggerli, l'app non prosegue con dati vuoti: ricarica la pagina tra qualche secondo. Se il problema persiste, contatta l'amministratore.",
    },
    "English": {
        'first_login_title': '🔒 First Login: Set Your New Password',
        'first_login_welcome': 'Welcome **{name}**! For security reasons, since this is your first login, you need to set a personal password that only you will know.',
        'first_login_save_btn': 'Save Password and Login',
        'first_login_success': '✅ Password set and saved successfully!',
        'first_login_hint_error': '❌ First login: enter your first name as the password.',
        'coach_wrong_pwd': '❌ Wrong password! Try again.',
        'admin_pwd_label': 'Admin Password',
        'admin_wrong_pwd': '❌ Wrong admin password.',
        'admin_pwd_mgmt_title': '🔑 Player Password Management',
        'admin_pwd_mgmt_desc': "View and edit each player's password. Passwords are stored in plain text: use this feature with caution.",
        'admin_pwd_mgmt_expander': 'Show / edit all passwords',
        'admin_pwd_of': 'Password for {name}',
        'admin_pwd_save_btn': '💾 Save All Passwords',
        'admin_pwd_updated': '✅ Passwords updated for: {names}',
        'no_changes_to_save': 'No changes to save.',
        'roster_modal_title': '👥 Squad Management Panel (Add or Remove)',
        'roster_add_title': 'Add New Player',
        'roster_fname_lbl': 'First Name',
        'roster_lname_lbl': 'Last Name',
        'roster_dup_error': 'A player with this first and last name already exists in the squad!',
        'roster_add_success': 'Player {name} added successfully!',
        'roster_name_required': 'First name and last name cannot be empty.',
        'roster_delete_title': 'Remove Existing Player',
        'roster_select_remove': 'Select player to remove',
        'roster_remove_success': 'Player {name} removed successfully!',
        'squad_save_btn': '💾 Save Squad and Role Changes',
        'squad_save_success': 'All changes to the squad, roles and dominant hand have been saved permanently!',
        'roster_role_lbl': 'Position / Role',
        'roster_hand_lbl': 'Hand',
        'roster_style_lbl': 'Play Style',
        'roster_add_btn': '➕ Add Player',
        'roster_remove_btn': '🗑️ Remove Player',
        'partner_prefs_title': '🏆 Partner Preferences of **{name}**',
        'total_players_present': 'Total players present: **{n}**',
        'improvement_area': '📌 Improvement area: **{skill}** ({n} players)',
        'grade_label': 'Grade: {val}',
        'partner_prefs_desc': 'Ranking of the partners the player prefers to play with (set by them in their own area), and who among the others has ranked them as a preferred partner. Useful to understand affinities before grading.',
        'partner_prefs_own': '**{name}** prefers to play with:',
        'partner_prefs_none': "This player hasn't set any preferences.",
        'partner_prefs_reverse_title': 'Who has ranked **{name}** as a preferred partner:',
        'partner_prefs_reverse_none': 'No other player has ranked them as a preferred partner.',
        'col_partner': 'Partner',
        'col_score': 'Score',
        'col_player': 'Player',
        'training_system_analysis': 'The system analyzed the grades of the present group and suggests the following 3 priorities:',
        'training_priority_1': '🔥 1st Recommended Priority',
        'training_priority_2': '⚡ 2nd Recommended Priority',
        'training_priority_3': '💡 3rd Recommended Priority',
        'avg_label': 'Avg: {v}/10',
        'training_customize_title': '✏️ Coach Customization & Confirmation',
        'training_customize_desc': 'The coach can change the priorities from the dropdown menu and choose the date to save the training in the calendar:',
        'priority1_coach_lbl': '1st Priority (Coach)',
        'priority2_coach_lbl': '2nd Priority (Coach)',
        'priority3_coach_lbl': '3rd Priority (Coach)',
        'training_date_question': '📅 On which date do you want to save this training?',
        'training_confirm_btn': '✅ Confirm and Save to Calendar',
        'training_saved_success': '🎉 Training successfully saved for {date}!',
        'group_split_title': '👥 Split into Groups of 4 (by weakness)',
        'group_split_desc': 'The selected players are grouped into **groups of 4** based on their **main weakness**, so each group can work on a specific, targeted goal instead of a single priority for everyone.',
        'group_min_players': 'At least {n} available players are needed to form a group. Currently there are {m}.',
        'group_label': 'Group {i}',
        'group_incomplete_suffix': ' (incomplete group)',
        'group_main_weakness': '🎯 Main weakness',
        'group_focus_lbl': 'Training focus — Group {i}',
        'group_date_question': '📅 On which date do you want to save these group trainings?',
        'group_save_btn': '✅ Save Trainings per Group',
        'group_saved_success': '🎉 {n} group trainings saved for {date}!',
        'training_history_title': '📅 Planned Training Calendar History',
        'training_edit_title': '✏️ Edit Training',
        'training_select_edit': 'Select training to edit',
        'priority1_lbl': '1st Priority',
        'priority2_lbl': '2nd Priority',
        'priority3_lbl': '3rd Priority',
        'training_date_lbl': '📅 Training date',
        'participants_lbl': 'Participants',
        'training_save_edit_btn': '💾 Save Training Changes',
        'select_at_least_one_participant': 'Select at least one participant.',
        'training_edit_success': 'Training edited successfully!',
        'training_delete_title': '🗑️ Delete Training from Calendar',
        'training_select_delete': 'Select training to remove',
        'training_delete_btn': '🗑️ Delete Selected Training',
        'training_delete_success': 'Training on {date} deleted successfully from the calendar!',
        'no_trainings_saved': 'No training sessions confirmed and saved in the calendar yet.',
        'snp_mgmt_title': '📅 SNP Match Calendar & Registration',
        'snp_mgmt_desc': 'Manage the **7 SNP matchdays**. For each match, assign the NAC players and the **result of each court**.',
        'snp_select_day': '📆 Select the SNP matchday',
        'snp_formation_title': '1️⃣ Lineup',
        'snp_formation_desc': "Choose 2 NAC players for each court. You'll be able to enter the result later, once the match has been played.",
        'snp_notes_lbl': '📝 Matchday notes / comments (optional)',
        'snp_notes_placeholder': 'Observations, injuries, etc.',
        'snp_save_formation_btn': '💾 Save Lineup',
        'snp_formation_saved': "✅ Lineup saved for **{label}**! You'll be able to enter the results once the match has been played.",
        'snp_results_title': '2️⃣ Results',
        'snp_no_lineup_info': "ℹ️ First assign the players in the Lineup above: you'll then be able to enter the results here.",
        'snp_results_desc': 'Enter the result of each court when available. The players remain those assigned in the Lineup.',
        'snp_save_results_btn': '🏆 Save Results',
        'snp_results_saved': '✅ Results saved for **{label}**!',
        'snp_summary_title': '📋 Full SNP Calendar Summary',
        'snp_courts_filled': '{n}/5 courts filled',
        'snp_not_filled': 'Not filled in',
        'snp_no_lineup_yet': 'No lineup entered yet for this matchday.',
        'snp_reset_expander': '🗑️ Reset SNP data',
        'snp_reset_btn': 'Delete ALL SNP lineups and results',
        'snp_reset_success': 'SNP data reset.',
        'pairing_confirm_btn': '✅ Confirm Pairing Selection',
        'pairing_confirm_success': 'Pairing confirmed and saved successfully!',
        'save_failed_error': '⚠️ Save FAILED: unable to write to the database ({error}). Your changes were NOT saved — try again in a few seconds before leaving this page.',
        'db_unreachable_error': '⚠️ Unable to connect to the database. Your saved data might not be visible right now. To protect it, the app will not proceed with empty data: reload the page in a few seconds. If the problem persists, contact the administrator.',
    },
    "Español": {
        'first_login_title': '🔒 Primer Acceso: Establece tu Nueva Contraseña',
        'first_login_welcome': '¡Bienvenido **{name}**! Por motivos de seguridad, al ser tu primer acceso, debes establecer una contraseña personal que solo tú conocerás.',
        'first_login_save_btn': 'Guardar Contraseña y Acceder',
        'first_login_success': '¡✅ Contraseña establecida y guardada correctamente!',
        'first_login_hint_error': '❌ Primer acceso: introduce tu nombre de pila como contraseña.',
        'coach_wrong_pwd': '❌ ¡Contraseña incorrecta! Inténtalo de nuevo.',
        'admin_pwd_label': 'Contraseña de Admin',
        'admin_wrong_pwd': '❌ Contraseña de admin incorrecta.',
        'admin_pwd_mgmt_title': '🔑 Gestión de Contraseñas de Jugadores',
        'admin_pwd_mgmt_desc': 'Consulta y edita la contraseña de cada jugador. Las contraseñas se guardan en texto sin cifrar: usa esta función con precaución.',
        'admin_pwd_mgmt_expander': 'Mostrar / editar todas las contraseñas',
        'admin_pwd_of': 'Contraseña de {name}',
        'admin_pwd_save_btn': '💾 Guardar Todas las Contraseñas',
        'admin_pwd_updated': '✅ Contraseñas actualizadas para: {names}',
        'no_changes_to_save': 'No hay cambios que guardar.',
        'roster_modal_title': '👥 Panel de Gestión de Plantilla (Añadir o Eliminar)',
        'roster_add_title': 'Añadir Nuevo Jugador',
        'roster_fname_lbl': 'Nombre',
        'roster_lname_lbl': 'Apellido',
        'roster_dup_error': '¡Ya existe un jugador con este nombre y apellido en la plantilla!',
        'roster_add_success': '¡Jugador {name} añadido con éxito!',
        'roster_name_required': 'El nombre y el apellido no pueden estar vacíos.',
        'roster_delete_title': 'Eliminar Jugador Existente',
        'roster_select_remove': 'Selecciona jugador a eliminar',
        'roster_remove_success': '¡Jugador {name} eliminado con éxito!',
        'squad_save_btn': '💾 Guardar Cambios de Plantilla y Roles',
        'squad_save_success': '¡Todos los cambios en la plantilla, roles y mano dominante se han guardado permanentemente!',
        'roster_role_lbl': 'Posición / Rol',
        'roster_hand_lbl': 'Mano',
        'roster_style_lbl': 'Estilo de Juego',
        'roster_add_btn': '➕ Añadir Jugador',
        'roster_remove_btn': '🗑️ Eliminar Jugador',
        'partner_prefs_title': '🏆 Preferencias de Compañero de **{name}**',
        'total_players_present': 'Total de jugadores presentes: **{n}**',
        'improvement_area': '📌 Área de mejora: **{skill}** ({n} jugadores)',
        'grade_label': 'Nota: {val}',
        'partner_prefs_desc': 'Ranking de los compañeros con los que el jugador prefiere jugar (establecido por él en su propia área), y quién entre los demás lo ha clasificado como compañero preferido. Útil para entender las afinidades antes de evaluar.',
        'partner_prefs_own': '**{name}** prefiere jugar con:',
        'partner_prefs_none': 'Este jugador no ha establecido ninguna preferencia.',
        'partner_prefs_reverse_title': 'Quién ha indicado a **{name}** como compañero preferido:',
        'partner_prefs_reverse_none': 'Ningún otro jugador lo ha indicado como compañero preferido.',
        'col_partner': 'Compañero',
        'col_score': 'Puntuación',
        'col_player': 'Jugador',
        'training_system_analysis': 'El sistema ha analizado las notas del grupo presente y sugiere las siguientes 3 prioridades:',
        'training_priority_1': '🔥 1ª Prioridad Recomendada',
        'training_priority_2': '⚡ 2ª Prioridad Recomendada',
        'training_priority_3': '💡 3ª Prioridad Recomendada',
        'avg_label': 'Media: {v}/10',
        'training_customize_title': '✏️ Personalización y Confirmación del Entrenador',
        'training_customize_desc': 'El entrenador puede modificar las prioridades desde el menú desplegable y elegir la fecha para guardar el entrenamiento en el calendario:',
        'priority1_coach_lbl': '1ª Prioridad (Entrenador)',
        'priority2_coach_lbl': '2ª Prioridad (Entrenador)',
        'priority3_coach_lbl': '3ª Prioridad (Entrenador)',
        'training_date_question': '📅 ¿En qué fecha quieres guardar este entrenamiento?',
        'training_confirm_btn': '✅ Confirmar y Guardar en el Calendario',
        'training_saved_success': '🎉 ¡Entrenamiento guardado con éxito para el {date}!',
        'group_split_title': '👥 División en Grupos de 4 (según la debilidad)',
        'group_split_desc': 'Los jugadores seleccionados se agrupan en **grupos de 4** según su **debilidad principal**, para que cada grupo pueda trabajar en un objetivo específico en lugar de una única prioridad para todos.',
        'group_min_players': 'Se necesitan al menos {n} jugadores disponibles para formar un grupo. Actualmente hay {m}.',
        'group_label': 'Grupo {i}',
        'group_incomplete_suffix': ' (grupo incompleto)',
        'group_main_weakness': '🎯 Debilidad principal',
        'group_focus_lbl': 'Enfoque de entrenamiento — Grupo {i}',
        'group_date_question': '📅 ¿En qué fecha quieres guardar estos entrenamientos de grupo?',
        'group_save_btn': '✅ Guardar Entrenamientos por Grupo',
        'group_saved_success': '🎉 ¡{n} entrenamientos de grupo guardados para el {date}!',
        'training_history_title': '📅 Historial del Calendario de Entrenamientos Planificados',
        'training_edit_title': '✏️ Editar Entrenamiento',
        'training_select_edit': 'Selecciona entrenamiento a editar',
        'priority1_lbl': '1ª Prioridad',
        'priority2_lbl': '2ª Prioridad',
        'priority3_lbl': '3ª Prioridad',
        'training_date_lbl': '📅 Fecha de entrenamiento',
        'participants_lbl': 'Participantes',
        'training_save_edit_btn': '💾 Guardar Cambios del Entrenamiento',
        'select_at_least_one_participant': 'Selecciona al menos un participante.',
        'training_edit_success': '¡Entrenamiento editado con éxito!',
        'training_delete_title': '🗑️ Eliminar Entrenamiento del Calendario',
        'training_select_delete': 'Selecciona entrenamiento a eliminar',
        'training_delete_btn': '🗑️ Eliminar Entrenamiento Seleccionado',
        'training_delete_success': '¡Entrenamiento del {date} eliminado con éxito del calendario!',
        'no_trainings_saved': 'Aún no hay entrenamientos confirmados y guardados en el calendario.',
        'snp_mgmt_title': '📅 Calendario y Registro de Partidos SNP',
        'snp_mgmt_desc': 'Gestión de las **7 jornadas SNP**. Para cada partido, asigna los jugadores de NAC y el **resultado de cada pista**.',
        'snp_select_day': '📆 Selecciona la jornada SNP',
        'snp_formation_title': '1️⃣ Alineación',
        'snp_formation_desc': 'Elige 2 jugadores de NAC para cada pista. Podrás introducir el resultado más adelante, una vez jugado el partido.',
        'snp_notes_lbl': '📝 Notas / Comentarios de la jornada (opcional)',
        'snp_notes_placeholder': 'Observaciones, lesiones, etc.',
        'snp_save_formation_btn': '💾 Guardar Alineación',
        'snp_formation_saved': '✅ ¡Alineación guardada para **{label}**! Podrás introducir los resultados una vez jugado el partido.',
        'snp_results_title': '2️⃣ Resultados',
        'snp_no_lineup_info': 'ℹ️ Primero asigna los jugadores en la Alineación de arriba: después podrás introducir aquí los resultados.',
        'snp_results_desc': 'Introduce el resultado de cada pista cuando esté disponible. Los jugadores siguen siendo los asignados en la Alineación.',
        'snp_save_results_btn': '🏆 Guardar Resultados',
        'snp_results_saved': '✅ ¡Resultados guardados para **{label}**!',
        'snp_summary_title': '📋 Resumen Completo del Calendario SNP',
        'snp_courts_filled': '{n}/5 pistas completadas',
        'snp_not_filled': 'No completada',
        'snp_no_lineup_yet': 'Aún no se ha introducido ninguna alineación para esta jornada.',
        'snp_reset_expander': '🗑️ Restablecer datos SNP',
        'snp_reset_btn': 'Eliminar TODAS las alineaciones y resultados SNP',
        'snp_reset_success': 'Datos SNP restablecidos.',
        'pairing_confirm_btn': '✅ Confirmar Selección de Emparejamiento',
        'pairing_confirm_success': '¡Emparejamiento confirmado y guardado con éxito!',
        'save_failed_error': '⚠️ El guardado FALLÓ: no se pudo escribir en la base de datos ({error}). Tus cambios NO se guardaron — inténtalo de nuevo en unos segundos antes de salir de esta página.',
        'db_unreachable_error': '⚠️ No se puede conectar con la base de datos. Es posible que tus datos guardados no sean visibles en este momento. Para protegerlos, la aplicación no continuará con datos vacíos: recarga la página en unos segundos. Si el problema persiste, contacta con el administrador.',
    },
    "Svenska": {
        'first_login_title': '🔒 Första Inloggning: Ange ditt Nya Lösenord',
        'first_login_welcome': 'Välkommen **{name}**! Av säkerhetsskäl, eftersom detta är din första inloggning, måste du ange ett personligt lösenord som bara du känner till.',
        'first_login_save_btn': 'Spara Lösenord och Logga in',
        'first_login_success': '✅ Lösenordet har angetts och sparats!',
        'first_login_hint_error': '❌ Första inloggning: ange ditt förnamn som lösenord.',
        'coach_wrong_pwd': '❌ Fel lösenord! Försök igen.',
        'admin_pwd_label': 'Admin-lösenord',
        'admin_wrong_pwd': '❌ Fel admin-lösenord.',
        'admin_pwd_mgmt_title': '🔑 Hantering av Spelarlösenord',
        'admin_pwd_mgmt_desc': 'Visa och redigera varje spelares lösenord. Lösenorden lagras i klartext: använd denna funktion med försiktighet.',
        'admin_pwd_mgmt_expander': 'Visa / redigera alla lösenord',
        'admin_pwd_of': 'Lösenord för {name}',
        'admin_pwd_save_btn': '💾 Spara Alla Lösenord',
        'admin_pwd_updated': '✅ Lösenord uppdaterade för: {names}',
        'no_changes_to_save': 'Inga ändringar att spara.',
        'roster_modal_title': '👥 Trupphanteringspanel (Lägg till eller Ta bort)',
        'roster_add_title': 'Lägg till Ny Spelare',
        'roster_fname_lbl': 'Förnamn',
        'roster_lname_lbl': 'Efternamn',
        'roster_dup_error': 'En spelare med detta för- och efternamn finns redan i truppen!',
        'roster_add_success': 'Spelaren {name} har lagts till!',
        'roster_name_required': 'För- och efternamn får inte vara tomma.',
        'roster_delete_title': 'Ta bort Befintlig Spelare',
        'roster_select_remove': 'Välj spelare att ta bort',
        'roster_remove_success': 'Spelaren {name} har tagits bort!',
        'squad_save_btn': '💾 Spara Trupp- och Rolländringar',
        'squad_save_success': 'Alla ändringar av truppen, roller och dominant hand har sparats permanent!',
        'roster_role_lbl': 'Position / Roll',
        'roster_hand_lbl': 'Hand',
        'roster_style_lbl': 'Spelstil',
        'roster_add_btn': '➕ Lägg till Spelare',
        'roster_remove_btn': '🗑️ Ta bort Spelare',
        'partner_prefs_title': '🏆 Partnerpreferenser för **{name}**',
        'total_players_present': 'Totalt antal närvarande spelare: **{n}**',
        'improvement_area': '📌 Förbättringsområde: **{skill}** ({n} spelare)',
        'grade_label': 'Betyg: {val}',
        'partner_prefs_desc': 'Ranking av de partner spelaren föredrar att spela med (angett av spelaren själv), och vem bland de andra som har rankat honom/henne som en föredragen partner. Användbart för att förstå affiniteter innan betygsättning.',
        'partner_prefs_own': '**{name}** föredrar att spela med:',
        'partner_prefs_none': 'Denna spelare har inte angett några preferenser.',
        'partner_prefs_reverse_title': 'Vem har rankat **{name}** som en föredragen partner:',
        'partner_prefs_reverse_none': 'Ingen annan spelare har rankat honom/henne som en föredragen partner.',
        'col_partner': 'Partner',
        'col_score': 'Poäng',
        'col_player': 'Spelare',
        'training_system_analysis': 'Systemet har analyserat betygen för den närvarande gruppen och föreslår följande 3 prioriteringar:',
        'training_priority_1': '🔥 1:a Rekommenderade Prioritet',
        'training_priority_2': '⚡ 2:a Rekommenderade Prioritet',
        'training_priority_3': '💡 3:e Rekommenderade Prioritet',
        'avg_label': 'Snitt: {v}/10',
        'training_customize_title': '✏️ Anpassning och Bekräftelse av Tränaren',
        'training_customize_desc': 'Tränaren kan ändra prioriteringarna från rullgardinsmenyn och välja vilket datum träningen ska sparas i kalendern:',
        'priority1_coach_lbl': '1:a Prioritet (Tränare)',
        'priority2_coach_lbl': '2:a Prioritet (Tränare)',
        'priority3_coach_lbl': '3:e Prioritet (Tränare)',
        'training_date_question': '📅 Vilket datum vill du spara denna träning på?',
        'training_confirm_btn': '✅ Bekräfta och Spara i Kalendern',
        'training_saved_success': '🎉 Träningen har sparats för {date}!',
        'group_split_title': '👥 Uppdelning i Grupper om 4 (efter svaghet)',
        'group_split_desc': 'De valda spelarna grupperas i **grupper om 4** baserat på deras **huvudsvaghet**, så att varje grupp kan arbeta mot ett specifikt, riktat mål istället för en enda prioritet för alla.',
        'group_min_players': 'Minst {n} tillgängliga spelare behövs för att bilda en grupp. För närvarande finns det {m}.',
        'group_label': 'Grupp {i}',
        'group_incomplete_suffix': ' (ofullständig grupp)',
        'group_main_weakness': '🎯 Huvudsvaghet',
        'group_focus_lbl': 'Träningsfokus — Grupp {i}',
        'group_date_question': '📅 Vilket datum vill du spara dessa gruppträningar på?',
        'group_save_btn': '✅ Spara Träningar per Grupp',
        'group_saved_success': '🎉 {n} gruppträningar sparade för {date}!',
        'training_history_title': '📅 Historik för Planerad Träningskalender',
        'training_edit_title': '✏️ Redigera Träning',
        'training_select_edit': 'Välj träning att redigera',
        'priority1_lbl': '1:a Prioritet',
        'priority2_lbl': '2:a Prioritet',
        'priority3_lbl': '3:e Prioritet',
        'training_date_lbl': '📅 Träningsdatum',
        'participants_lbl': 'Deltagare',
        'training_save_edit_btn': '💾 Spara Träningsändringar',
        'select_at_least_one_participant': 'Välj minst en deltagare.',
        'training_edit_success': 'Träningen har redigerats!',
        'training_delete_title': '🗑️ Ta bort Träning från Kalendern',
        'training_select_delete': 'Välj träning att ta bort',
        'training_delete_btn': '🗑️ Ta bort Vald Träning',
        'training_delete_success': 'Träningen den {date} har tagits bort från kalendern!',
        'no_trainings_saved': 'Inga träningspass har ännu bekräftats och sparats i kalendern.',
        'snp_mgmt_title': '📅 SNP-matchkalender & Registrering',
        'snp_mgmt_desc': 'Hantering av de **7 SNP-matchdagarna**. För varje match, tilldela NAC-spelarna och **resultatet för varje bana**.',
        'snp_select_day': '📆 Välj SNP-matchdag',
        'snp_formation_title': '1️⃣ Laguppställning',
        'snp_formation_desc': 'Välj 2 NAC-spelare för varje bana. Du kan ange resultatet senare, när matchen har spelats.',
        'snp_notes_lbl': '📝 Anteckningar / Kommentarer för matchdagen (valfritt)',
        'snp_notes_placeholder': 'Observationer, skador, etc.',
        'snp_save_formation_btn': '💾 Spara Laguppställning',
        'snp_formation_saved': '✅ Laguppställning sparad för **{label}**! Du kan ange resultaten när matchen har spelats.',
        'snp_results_title': '2️⃣ Resultat',
        'snp_no_lineup_info': 'ℹ️ Tilldela först spelarna i Laguppställningen ovan: du kan sedan ange resultaten här.',
        'snp_results_desc': 'Ange resultatet för varje bana när det är tillgängligt. Spelarna förblir de som tilldelats i Laguppställningen.',
        'snp_save_results_btn': '🏆 Spara Resultat',
        'snp_results_saved': '✅ Resultat sparade för **{label}**!',
        'snp_summary_title': '📋 Fullständig Sammanfattning av SNP-kalendern',
        'snp_courts_filled': '{n}/5 banor ifyllda',
        'snp_not_filled': 'Ej ifylld',
        'snp_no_lineup_yet': 'Ingen laguppställning har angetts för denna matchdag ännu.',
        'snp_reset_expander': '🗑️ Återställ SNP-data',
        'snp_reset_btn': 'Ta bort ALLA SNP-laguppställningar och resultat',
        'snp_reset_success': 'SNP-data har återställts.',
        'pairing_confirm_btn': '✅ Bekräfta Parval',
        'pairing_confirm_success': 'Parningen har bekräftats och sparats!',
        'save_failed_error': '⚠️ Sparning MISSLYCKADES: kunde inte skriva till databasen ({error}). Dina ändringar sparades INTE — försök igen om några sekunder innan du lämnar denna sida.',
        'db_unreachable_error': '⚠️ Det går inte att ansluta till databasen. Dina sparade data kanske inte är synliga just nu. För att skydda dem fortsätter appen inte med tomma data: ladda om sidan om några sekunder. Om problemet kvarstår, kontakta administratören.',
    },
    "Nederlands": {
        'first_login_title': '🔒 Eerste Keer Inloggen: Stel je Nieuwe Wachtwoord in',
        'first_login_welcome': 'Welkom **{name}**! Om veiligheidsredenen moet je, omdat dit je eerste keer inloggen is, een persoonlijk wachtwoord instellen dat alleen jij kent.',
        'first_login_save_btn': 'Wachtwoord Opslaan en Inloggen',
        'first_login_success': '✅ Wachtwoord ingesteld en succesvol opgeslagen!',
        'first_login_hint_error': '❌ Eerste keer inloggen: voer je voornaam in als wachtwoord.',
        'coach_wrong_pwd': '❌ Verkeerd wachtwoord! Probeer het opnieuw.',
        'admin_pwd_label': 'Adminwachtwoord',
        'admin_wrong_pwd': '❌ Verkeerd adminwachtwoord.',
        'admin_pwd_mgmt_title': '🔑 Beheer van Spelerswachtwoorden',
        'admin_pwd_mgmt_desc': 'Bekijk en bewerk het wachtwoord van elke speler. Wachtwoorden worden onversleuteld opgeslagen: gebruik deze functie met voorzichtigheid.',
        'admin_pwd_mgmt_expander': 'Toon / bewerk alle wachtwoorden',
        'admin_pwd_of': 'Wachtwoord van {name}',
        'admin_pwd_save_btn': '💾 Alle Wachtwoorden Opslaan',
        'admin_pwd_updated': '✅ Wachtwoorden bijgewerkt voor: {names}',
        'no_changes_to_save': 'Geen wijzigingen om op te slaan.',
        'roster_modal_title': '👥 Selectiebeheerpaneel (Toevoegen of Verwijderen)',
        'roster_add_title': 'Nieuwe Speler Toevoegen',
        'roster_fname_lbl': 'Voornaam',
        'roster_lname_lbl': 'Achternaam',
        'roster_dup_error': 'Er bestaat al een speler met deze voor- en achternaam in de selectie!',
        'roster_add_success': 'Speler {name} succesvol toegevoegd!',
        'roster_name_required': 'Voor- en achternaam mogen niet leeg zijn.',
        'roster_delete_title': 'Bestaande Speler Verwijderen',
        'roster_select_remove': 'Selecteer speler om te verwijderen',
        'roster_remove_success': 'Speler {name} succesvol verwijderd!',
        'squad_save_btn': '💾 Selectie- en Rolwijzigingen Opslaan',
        'squad_save_success': 'Alle wijzigingen aan de selectie, rollen en dominante hand zijn permanent opgeslagen!',
        'roster_role_lbl': 'Positie / Rol',
        'roster_hand_lbl': 'Hand',
        'roster_style_lbl': 'Speelstijl',
        'roster_add_btn': '➕ Speler Toevoegen',
        'roster_remove_btn': '🗑️ Speler Verwijderen',
        'partner_prefs_title': '🏆 Partnervoorkeuren van **{name}**',
        'total_players_present': 'Totaal aantal aanwezige spelers: **{n}**',
        'improvement_area': '📌 Verbeterpunt: **{skill}** ({n} spelers)',
        'grade_label': 'Cijfer: {val}',
        'partner_prefs_desc': 'Ranglijst van de partners met wie de speler het liefst speelt (door hemzelf ingesteld in zijn eigen omgeving), en wie van de anderen hem/haar als voorkeurspartner heeft aangegeven. Handig om affiniteiten te begrijpen vóór het beoordelen.',
        'partner_prefs_own': '**{name}** speelt het liefst met:',
        'partner_prefs_none': 'Deze speler heeft geen voorkeuren ingesteld.',
        'partner_prefs_reverse_title': 'Wie heeft **{name}** als voorkeurspartner aangegeven:',
        'partner_prefs_reverse_none': 'Geen enkele andere speler heeft hem/haar als voorkeurspartner aangegeven.',
        'col_partner': 'Partner',
        'col_score': 'Score',
        'col_player': 'Speler',
        'training_system_analysis': 'Het systeem heeft de cijfers van de aanwezige groep geanalyseerd en stelt de volgende 3 prioriteiten voor:',
        'training_priority_1': '🔥 1e Aanbevolen Prioriteit',
        'training_priority_2': '⚡ 2e Aanbevolen Prioriteit',
        'training_priority_3': '💡 3e Aanbevolen Prioriteit',
        'avg_label': 'Gem: {v}/10',
        'training_customize_title': '✏️ Aanpassing en Bevestiging door de Coach',
        'training_customize_desc': 'De coach kan de prioriteiten wijzigen via het dropdownmenu en de datum kiezen om de training in de kalender op te slaan:',
        'priority1_coach_lbl': '1e Prioriteit (Coach)',
        'priority2_coach_lbl': '2e Prioriteit (Coach)',
        'priority3_coach_lbl': '3e Prioriteit (Coach)',
        'training_date_question': '📅 Op welke datum wil je deze training opslaan?',
        'training_confirm_btn': '✅ Bevestigen en Opslaan in de Kalender',
        'training_saved_success': '🎉 Training succesvol opgeslagen voor {date}!',
        'group_split_title': '👥 Verdeling in Groepen van 4 (op basis van zwakte)',
        'group_split_desc': 'De geselecteerde spelers worden ingedeeld in **groepen van 4** op basis van hun **belangrijkste zwakte**, zodat elke groep aan een specifiek, gericht doel kan werken in plaats van één prioriteit voor iedereen.',
        'group_min_players': 'Er zijn minstens {n} beschikbare spelers nodig om een groep te vormen. Momenteel zijn er {m}.',
        'group_label': 'Groep {i}',
        'group_incomplete_suffix': ' (onvolledige groep)',
        'group_main_weakness': '🎯 Belangrijkste zwakte',
        'group_focus_lbl': 'Trainingsfocus — Groep {i}',
        'group_date_question': '📅 Op welke datum wil je deze groepstrainingen opslaan?',
        'group_save_btn': '✅ Trainingen per Groep Opslaan',
        'group_saved_success': '🎉 {n} groepstrainingen opgeslagen voor {date}!',
        'training_history_title': '📅 Geschiedenis van Geplande Trainingskalender',
        'training_edit_title': '✏️ Training Bewerken',
        'training_select_edit': 'Selecteer training om te bewerken',
        'priority1_lbl': '1e Prioriteit',
        'priority2_lbl': '2e Prioriteit',
        'priority3_lbl': '3e Prioriteit',
        'training_date_lbl': '📅 Trainingsdatum',
        'participants_lbl': 'Deelnemers',
        'training_save_edit_btn': '💾 Trainingswijzigingen Opslaan',
        'select_at_least_one_participant': 'Selecteer minstens één deelnemer.',
        'training_edit_success': 'Training succesvol bewerkt!',
        'training_delete_title': '🗑️ Training uit Kalender Verwijderen',
        'training_select_delete': 'Selecteer training om te verwijderen',
        'training_delete_btn': '🗑️ Geselecteerde Training Verwijderen',
        'training_delete_success': 'Training van {date} succesvol uit de kalender verwijderd!',
        'no_trainings_saved': 'Er zijn nog geen trainingen bevestigd en opgeslagen in de kalender.',
        'snp_mgmt_title': '📅 SNP-wedstrijdkalender & Registratie',
        'snp_mgmt_desc': 'Beheer van de **7 SNP-wedstrijddagen**. Wijs voor elke wedstrijd de NAC-spelers en de **uitslag van elke baan** toe.',
        'snp_select_day': '📆 Selecteer de SNP-wedstrijddag',
        'snp_formation_title': '1️⃣ Opstelling',
        'snp_formation_desc': 'Kies 2 NAC-spelers voor elke baan. Je kunt de uitslag later invoeren, zodra de wedstrijd is gespeeld.',
        'snp_notes_lbl': '📝 Notities / opmerkingen wedstrijddag (optioneel)',
        'snp_notes_placeholder': 'Opmerkingen, blessures, enz.',
        'snp_save_formation_btn': '💾 Opstelling Opslaan',
        'snp_formation_saved': '✅ Opstelling opgeslagen voor **{label}**! Je kunt de resultaten invoeren zodra de wedstrijd is gespeeld.',
        'snp_results_title': '2️⃣ Resultaten',
        'snp_no_lineup_info': 'ℹ️ Wijs eerst de spelers toe in de Opstelling hierboven: daarna kun je hier de resultaten invoeren.',
        'snp_results_desc': 'Voer de uitslag van elke baan in zodra deze beschikbaar is. De spelers blijven degenen die in de Opstelling zijn toegewezen.',
        'snp_save_results_btn': '🏆 Resultaten Opslaan',
        'snp_results_saved': '✅ Resultaten opgeslagen voor **{label}**!',
        'snp_summary_title': '📋 Volledig Overzicht SNP-kalender',
        'snp_courts_filled': '{n}/5 banen ingevuld',
        'snp_not_filled': 'Niet ingevuld',
        'snp_no_lineup_yet': 'Er is nog geen opstelling ingevoerd voor deze wedstrijddag.',
        'snp_reset_expander': '🗑️ SNP-gegevens Resetten',
        'snp_reset_btn': 'Verwijder ALLE SNP-opstellingen en resultaten',
        'snp_reset_success': 'SNP-gegevens gereset.',
        'pairing_confirm_btn': '✅ Koppelselectie Bevestigen',
        'pairing_confirm_success': 'Koppeling bevestigd en succesvol opgeslagen!',
        'save_failed_error': '⚠️ Opslaan MISLUKT: kan niet naar de database schrijven ({error}). Je wijzigingen zijn NIET opgeslagen — probeer het over een paar seconden opnieuw voordat je deze pagina verlaat.',
        'db_unreachable_error': '⚠️ Kan geen verbinding maken met de database. Je opgeslagen gegevens zijn mogelijk nu niet zichtbaar. Om ze te beschermen gaat de app niet verder met lege gegevens: herlaad de pagina over een paar seconden. Als het probleem aanhoudt, neem contact op met de beheerder.',
    },
    "Dansk": {
        'first_login_title': '🔒 Første Login: Angiv din Nye Adgangskode',
        'first_login_welcome': 'Velkommen **{name}**! Af sikkerhedsmæssige årsager skal du, da dette er din første login, angive en personlig adgangskode, som kun du kender.',
        'first_login_save_btn': 'Gem Adgangskode og Log ind',
        'first_login_success': '✅ Adgangskode angivet og gemt!',
        'first_login_hint_error': '❌ Første login: indtast dit fornavn som adgangskode.',
        'coach_wrong_pwd': '❌ Forkert adgangskode! Prøv igen.',
        'admin_pwd_label': 'Adminadgangskode',
        'admin_wrong_pwd': '❌ Forkert adminadgangskode.',
        'admin_pwd_mgmt_title': '🔑 Håndtering af Spilleradgangskoder',
        'admin_pwd_mgmt_desc': 'Se og rediger hver spillers adgangskode. Adgangskoderne gemmes i klartekst: brug denne funktion med forsigtighed.',
        'admin_pwd_mgmt_expander': 'Vis / rediger alle adgangskoder',
        'admin_pwd_of': 'Adgangskode for {name}',
        'admin_pwd_save_btn': '💾 Gem Alle Adgangskoder',
        'admin_pwd_updated': '✅ Adgangskoder opdateret for: {names}',
        'no_changes_to_save': 'Ingen ændringer at gemme.',
        'roster_modal_title': '👥 Trupstyringspanel (Tilføj eller Fjern)',
        'roster_add_title': 'Tilføj Ny Spiller',
        'roster_fname_lbl': 'Fornavn',
        'roster_lname_lbl': 'Efternavn',
        'roster_dup_error': 'Der findes allerede en spiller med dette for- og efternavn i truppen!',
        'roster_add_success': 'Spilleren {name} er tilføjet!',
        'roster_name_required': 'For- og efternavn må ikke være tomme.',
        'roster_delete_title': 'Fjern Eksisterende Spiller',
        'roster_select_remove': 'Vælg spiller, der skal fjernes',
        'roster_remove_success': 'Spilleren {name} er fjernet!',
        'squad_save_btn': '💾 Gem Trup- og Rolleændringer',
        'squad_save_success': 'Alle ændringer af truppen, roller og dominerende hånd er gemt permanent!',
        'roster_role_lbl': 'Position / Rolle',
        'roster_hand_lbl': 'Hånd',
        'roster_style_lbl': 'Spillestil',
        'roster_add_btn': '➕ Tilføj Spiller',
        'roster_remove_btn': '🗑️ Fjern Spiller',
        'partner_prefs_title': '🏆 Partnerpræferencer for **{name}**',
        'total_players_present': 'Samlet antal tilstedeværende spillere: **{n}**',
        'improvement_area': '📌 Forbedringsområde: **{skill}** ({n} spillere)',
        'grade_label': 'Karakter: {val}',
        'partner_prefs_desc': 'Rangering af de partnere, spilleren foretrækker at spille med (angivet af spilleren selv), og hvem blandt de andre der har rangeret vedkommende som foretrukken partner. Nyttigt til at forstå affiniteter før bedømmelse.',
        'partner_prefs_own': '**{name}** foretrækker at spille med:',
        'partner_prefs_none': 'Denne spiller har ikke angivet nogen præferencer.',
        'partner_prefs_reverse_title': 'Hvem har angivet **{name}** som foretrukken partner:',
        'partner_prefs_reverse_none': 'Ingen anden spiller har angivet vedkommende som foretrukken partner.',
        'col_partner': 'Partner',
        'col_score': 'Point',
        'col_player': 'Spiller',
        'training_system_analysis': 'Systemet har analyseret karaktererne for den tilstedeværende gruppe og foreslår følgende 3 prioriteter:',
        'training_priority_1': '🔥 1. Anbefalede Prioritet',
        'training_priority_2': '⚡ 2. Anbefalede Prioritet',
        'training_priority_3': '💡 3. Anbefalede Prioritet',
        'avg_label': 'Gns: {v}/10',
        'training_customize_title': '✏️ Tilpasning og Bekræftelse fra Træneren',
        'training_customize_desc': 'Træneren kan ændre prioriteterne fra rullemenuen og vælge, hvilken dato træningen skal gemmes i kalenderen:',
        'priority1_coach_lbl': '1. Prioritet (Træner)',
        'priority2_coach_lbl': '2. Prioritet (Træner)',
        'priority3_coach_lbl': '3. Prioritet (Træner)',
        'training_date_question': '📅 På hvilken dato vil du gemme denne træning?',
        'training_confirm_btn': '✅ Bekræft og Gem i Kalenderen',
        'training_saved_success': '🎉 Træningen er gemt for {date}!',
        'group_split_title': '👥 Opdeling i Grupper á 4 (efter svaghed)',
        'group_split_desc': 'De valgte spillere grupperes i **grupper á 4** baseret på deres **primære svaghed**, så hver gruppe kan arbejde mod et specifikt, målrettet mål i stedet for én prioritet for alle.',
        'group_min_players': 'Der kræves mindst {n} tilgængelige spillere for at danne en gruppe. Der er i øjeblikket {m}.',
        'group_label': 'Gruppe {i}',
        'group_incomplete_suffix': ' (ufuldstændig gruppe)',
        'group_main_weakness': '🎯 Primær svaghed',
        'group_focus_lbl': 'Træningsfokus — Gruppe {i}',
        'group_date_question': '📅 På hvilken dato vil du gemme disse gruppetræninger?',
        'group_save_btn': '✅ Gem Træninger pr. Gruppe',
        'group_saved_success': '🎉 {n} gruppetræninger gemt for {date}!',
        'training_history_title': '📅 Historik for Planlagt Træningskalender',
        'training_edit_title': '✏️ Rediger Træning',
        'training_select_edit': 'Vælg træning, der skal redigeres',
        'priority1_lbl': '1. Prioritet',
        'priority2_lbl': '2. Prioritet',
        'priority3_lbl': '3. Prioritet',
        'training_date_lbl': '📅 Træningsdato',
        'participants_lbl': 'Deltagere',
        'training_save_edit_btn': '💾 Gem Træningsændringer',
        'select_at_least_one_participant': 'Vælg mindst én deltager.',
        'training_edit_success': 'Træningen er redigeret!',
        'training_delete_title': '🗑️ Slet Træning fra Kalenderen',
        'training_select_delete': 'Vælg træning, der skal fjernes',
        'training_delete_btn': '🗑️ Slet Valgt Træning',
        'training_delete_success': 'Træningen den {date} er slettet fra kalenderen!',
        'no_trainings_saved': 'Ingen træningspas er endnu bekræftet og gemt i kalenderen.',
        'snp_mgmt_title': '📅 SNP-kampkalender & Registrering',
        'snp_mgmt_desc': 'Håndtering af de **7 SNP-kampdage**. Tildel for hver kamp NAC-spillerne og **resultatet for hver bane**.',
        'snp_select_day': '📆 Vælg SNP-kampdag',
        'snp_formation_title': '1️⃣ Holdopstilling',
        'snp_formation_desc': 'Vælg 2 NAC-spillere til hver bane. Du kan indtaste resultatet senere, når kampen er spillet.',
        'snp_notes_lbl': '📝 Noter / kommentarer til kampdagen (valgfrit)',
        'snp_notes_placeholder': 'Observationer, skader, osv.',
        'snp_save_formation_btn': '💾 Gem Holdopstilling',
        'snp_formation_saved': '✅ Holdopstilling gemt for **{label}**! Du kan indtaste resultaterne, når kampen er spillet.',
        'snp_results_title': '2️⃣ Resultater',
        'snp_no_lineup_info': 'ℹ️ Tildel først spillerne i Holdopstillingen ovenfor: derefter kan du indtaste resultaterne her.',
        'snp_results_desc': 'Indtast resultatet for hver bane, når det er tilgængeligt. Spillerne forbliver dem, der er tildelt i Holdopstillingen.',
        'snp_save_results_btn': '🏆 Gem Resultater',
        'snp_results_saved': '✅ Resultater gemt for **{label}**!',
        'snp_summary_title': '📋 Fuldstændigt Resumé af SNP-kalenderen',
        'snp_courts_filled': '{n}/5 baner udfyldt',
        'snp_not_filled': 'Ikke udfyldt',
        'snp_no_lineup_yet': 'Der er endnu ikke angivet nogen holdopstilling for denne kampdag.',
        'snp_reset_expander': '🗑️ Nulstil SNP-data',
        'snp_reset_btn': 'Slet ALLE SNP-holdopstillinger og resultater',
        'snp_reset_success': 'SNP-data nulstillet.',
        'pairing_confirm_btn': '✅ Bekræft Parvalg',
        'pairing_confirm_success': 'Parring bekræftet og gemt!',
        'save_failed_error': '⚠️ Gemning MISLYKKEDES: kunne ikke skrive til databasen ({error}). Dine ændringer blev IKKE gemt — prøv igen om et par sekunder, før du forlader denne side.',
        'db_unreachable_error': '⚠️ Kan ikke oprette forbindelse til databasen. Dine gemte data er muligvis ikke synlige lige nu. For at beskytte dem fortsætter appen ikke med tomme data: genindlæs siden om et par sekunder. Hvis problemet fortsætter, skal du kontakte administratoren.',
    },
}
for _lang, _vals in COACH_TRANSLATIONS.items():
    translations.setdefault(_lang, {}).update(_vals)

TRAINING_SNP_TRANSLATIONS = {
    "Italiano": {
        'training_system_intro': 'Il sistema ha analizzato i voti del gruppo presente e suggerisce le seguenti 3 priorità:',
        'training_priority_1_label': '🔥 1° Priorità Consigliata',
        'training_priority_2_label': '⚡ 2° Priorità Consigliata',
        'training_priority_3_label': '💡 3° Priorità Consigliata',
        'training_avg_label': 'Media: {val}/10',
        'training_custom_title': '✏️ Personalizzazione e Conferma del Coach',
        'training_custom_desc': 'Il coach può modificare le priorità dal menu a tendina e scegliere in quale data salvare l\'allenamento nel calendario:',
        'training_coach_p1_label': '1° Priorità (Coach)',
        'training_coach_p2_label': '2° Priorità (Coach)',
        'training_coach_p3_label': '3° Priorità (Coach)',
        'training_date_question': '📅 In quale data vuoi salvare questo allenamento?',
        'training_confirm_btn': '✅ Conferma e Salva nel Calendario',
        'training_saved_success': '🎉 Allenamento salvato con successo per il giorno {date}!',
        'groups_split_title': '👥 Suddivisione in Gruppi da 4 (in base alla debolezza)',
        'groups_split_desc': 'I giocatori selezionati vengono raggruppati in **gruppi da 4** in base alla loro **debolezza principale**, così ogni gruppo può lavorare su un obiettivo specifico e mirato invece di un\'unica priorità per tutti.',
        'groups_min_players_warning': 'Servono almeno {n} giocatori disponibili per formare un gruppo. Al momento ce ne sono {count}.',
        'group_label_prefix': 'Gruppo {n}',
        'group_incomplete_suffix': ' (gruppo incompleto)',
        'group_weak_metric_label': '🎯 Debolezza principale',
        'group_focus_label': 'Focus allenamento — Gruppo {n}',
        'group_date_question': '📅 In quale data vuoi salvare questi allenamenti di gruppo?',
        'group_save_btn': '✅ Salva Allenamenti per Gruppo',
        'group_saved_success': '🎉 {n} allenamenti di gruppo salvati per il giorno {date}!',
        'training_history_title': '📅 Storico Calendario Allenamenti Pianificati',
        'training_edit_title': '✏️ Modifica Allenamento',
        'training_select_edit': 'Seleziona allenamento da modificare',
        'training_edit_date_label': '📅 Data allenamento',
        'training_participants_label': 'Partecipanti',
        'training_edit_save_btn': '💾 Salva Modifiche Allenamento',
        'training_select_participant_warning': 'Seleziona almeno un partecipante.',
        'training_edit_success': 'Allenamento modificato con successo!',
        'training_delete_title': '🗑️ Cancella Allenamento dal Calendario',
        'training_select_delete': 'Seleziona allenamento da rimuovere',
        'training_delete_btn': '🗑️ Elimina Allenamento Selezionato',
        'training_delete_success': 'Allenamento del {date} eliminato con successo dal calendario!',
        'training_none_saved': 'Nessun allenamento ancora confermato e salvato nel calendario.',
        'priority1_label': '1° Priorità',
        'priority2_label': '2° Priorità',
        'priority3_label': '3° Priorità',
        'snp_title': '📅 Calendario & Registrazione Partite SNP',
        'snp_desc': 'Gestione delle **7 giornate SNP**. Per ogni incontro assegna i giocatori NAC e il **risultato di ogni pista**.',
        'snp_select_day': '📆 Seleziona la giornata SNP',
        'snp_formation_title': '1️⃣ Formazione',
        'snp_formation_desc': 'Scegli 2 giocatori NAC per ogni pista. Potrai inserire il risultato in un secondo momento, quando la partita sarà giocata.',
        'snp_court_label': 'Pista {n}',
        'snp_player1_court': 'Giocatore 1 - Pista {n}',
        'snp_player2_court': 'Giocatore 2 - Pista {n}',
        'snp_notes_label': '📝 Note / Commenti giornata (opzionale)',
        'snp_notes_placeholder': 'Osservazioni, infortuni, ecc.',
        'snp_save_formation_btn': '💾 Salva Formazione',
        'snp_formation_saved': '✅ Formazione salvata per **{day}**! Potrai inserire i risultati quando la partita sarà stata giocata.',
        'snp_results_title': '2️⃣ Risultati',
        'snp_results_no_lineup': 'ℹ️ Assegna prima i giocatori nella Formazione qui sopra: potrai poi inserire qui i risultati.',
        'snp_results_desc': 'Inserisci il risultato di ogni pista quando disponibile. I giocatori restano quelli assegnati nella Formazione.',
        'snp_result_court_label': 'Risultato Pista {n}',
        'snp_result_placeholder': 'es. 6-4, 6-2',
        'snp_save_results_btn': '🏆 Salva Risultati',
        'snp_results_saved': '✅ Risultati salvati per **{day}**!',
        'snp_summary_title': '📋 Riepilogo Completo Calendario SNP',
        'snp_courts_filled': '{n}/5 piste compilate',
        'snp_not_filled': 'Non compilata',
        'snp_col_court': 'Pista',
        'snp_col_player1': 'Giocatore 1',
        'snp_col_player2': 'Giocatore 2',
        'snp_col_result': 'Risultato',
        'snp_notes_display': '**Note:** {notes}',
        'snp_no_lineup_yet': 'Nessuna formazione ancora inserita per questa giornata.',
        'snp_reset_expander': '🗑️ Reset dati SNP',
        'snp_reset_btn': 'Cancella TUTTE le formazioni e risultati SNP',
        'snp_reset_success': 'Dati SNP resettati.',
    },
    "English": {
        'training_system_intro': 'The system has analyzed the grades of the group present and suggests the following 3 priorities:',
        'training_priority_1_label': '🔥 1st Recommended Priority',
        'training_priority_2_label': '⚡ 2nd Recommended Priority',
        'training_priority_3_label': '💡 3rd Recommended Priority',
        'training_avg_label': 'Average: {val}/10',
        'training_custom_title': '✏️ Coach Customization and Confirmation',
        'training_custom_desc': 'The coach can change the priorities from the dropdown menu and choose which date to save the training in the calendar:',
        'training_coach_p1_label': '1st Priority (Coach)',
        'training_coach_p2_label': '2nd Priority (Coach)',
        'training_coach_p3_label': '3rd Priority (Coach)',
        'training_date_question': '📅 On which date do you want to save this training?',
        'training_confirm_btn': '✅ Confirm and Save to Calendar',
        'training_saved_success': '🎉 Training saved successfully for {date}!',
        'groups_split_title': '👥 Split into Groups of 4 (based on weakness)',
        'groups_split_desc': 'The selected players are grouped into **groups of 4** based on their **main weakness**, so each group can work on a specific and targeted goal instead of a single priority for everyone.',
        'groups_min_players_warning': 'At least {n} available players are needed to form a group. There are currently {count}.',
        'group_label_prefix': 'Group {n}',
        'group_incomplete_suffix': ' (incomplete group)',
        'group_weak_metric_label': '🎯 Main weakness',
        'group_focus_label': 'Training focus — Group {n}',
        'group_date_question': '📅 On which date do you want to save these group trainings?',
        'group_save_btn': '✅ Save Group Trainings',
        'group_saved_success': '🎉 {n} group trainings saved for {date}!',
        'training_history_title': '📅 Planned Trainings Calendar History',
        'training_edit_title': '✏️ Edit Training',
        'training_select_edit': 'Select training to edit',
        'training_edit_date_label': '📅 Training date',
        'training_participants_label': 'Participants',
        'training_edit_save_btn': '💾 Save Training Changes',
        'training_select_participant_warning': 'Select at least one participant.',
        'training_edit_success': 'Training edited successfully!',
        'training_delete_title': '🗑️ Delete Training from Calendar',
        'training_select_delete': 'Select training to remove',
        'training_delete_btn': '🗑️ Delete Selected Training',
        'training_delete_success': 'Training on {date} removed successfully from the calendar!',
        'training_none_saved': 'No training confirmed and saved to the calendar yet.',
        'priority1_label': '1st Priority',
        'priority2_label': '2nd Priority',
        'priority3_label': '3rd Priority',
        'snp_title': '📅 Calendar & SNP Match Registration',
        'snp_desc': 'Management of the **7 SNP matchdays**. For each fixture, assign the NAC players and the **result of each court**.',
        'snp_select_day': '📆 Select the SNP matchday',
        'snp_formation_title': '1️⃣ Lineup',
        'snp_formation_desc': 'Choose 2 NAC players for each court. You can enter the result later, once the match has been played.',
        'snp_court_label': 'Court {n}',
        'snp_player1_court': 'Player 1 - Court {n}',
        'snp_player2_court': 'Player 2 - Court {n}',
        'snp_notes_label': '📝 Matchday notes / comments (optional)',
        'snp_notes_placeholder': 'Observations, injuries, etc.',
        'snp_save_formation_btn': '💾 Save Lineup',
        'snp_formation_saved': '✅ Lineup saved for **{day}**! You can enter results once the match has been played.',
        'snp_results_title': '2️⃣ Results',
        'snp_results_no_lineup': 'ℹ️ First assign the players in the Lineup above: you can then enter the results here.',
        'snp_results_desc': 'Enter the result of each court when available. The players remain those assigned in the Lineup.',
        'snp_result_court_label': 'Result Court {n}',
        'snp_result_placeholder': 'e.g. 6-4, 6-2',
        'snp_save_results_btn': '🏆 Save Results',
        'snp_results_saved': '✅ Results saved for **{day}**!',
        'snp_summary_title': '📋 Complete SNP Calendar Summary',
        'snp_courts_filled': '{n}/5 courts filled',
        'snp_not_filled': 'Not filled in',
        'snp_col_court': 'Court',
        'snp_col_player1': 'Player 1',
        'snp_col_player2': 'Player 2',
        'snp_col_result': 'Result',
        'snp_notes_display': '**Notes:** {notes}',
        'snp_no_lineup_yet': 'No lineup entered yet for this matchday.',
        'snp_reset_expander': '🗑️ Reset SNP data',
        'snp_reset_btn': 'Delete ALL SNP lineups and results',
        'snp_reset_success': 'SNP data reset.',
    },
    "Español": {
        'training_system_intro': 'El sistema ha analizado las calificaciones del grupo presente y sugiere las siguientes 3 prioridades:',
        'training_priority_1_label': '🔥 1ª Prioridad Recomendada',
        'training_priority_2_label': '⚡ 2ª Prioridad Recomendada',
        'training_priority_3_label': '💡 3ª Prioridad Recomendada',
        'training_avg_label': 'Media: {val}/10',
        'training_custom_title': '✏️ Personalización y Confirmación del Entrenador',
        'training_custom_desc': 'El entrenador puede modificar las prioridades desde el menú desplegable y elegir en qué fecha guardar el entrenamiento en el calendario:',
        'training_coach_p1_label': '1ª Prioridad (Entrenador)',
        'training_coach_p2_label': '2ª Prioridad (Entrenador)',
        'training_coach_p3_label': '3ª Prioridad (Entrenador)',
        'training_date_question': '📅 ¿En qué fecha quieres guardar este entrenamiento?',
        'training_confirm_btn': '✅ Confirmar y Guardar en el Calendario',
        'training_saved_success': '🎉 ¡Entrenamiento guardado con éxito para el día {date}!',
        'groups_split_title': '👥 División en Grupos de 4 (según debilidad)',
        'groups_split_desc': 'Los jugadores seleccionados se agrupan en **grupos de 4** según su **debilidad principal**, para que cada grupo pueda trabajar en un objetivo específico en lugar de una única prioridad para todos.',
        'groups_min_players_warning': 'Se necesitan al menos {n} jugadores disponibles para formar un grupo. Actualmente hay {count}.',
        'group_label_prefix': 'Grupo {n}',
        'group_incomplete_suffix': ' (grupo incompleto)',
        'group_weak_metric_label': '🎯 Debilidad principal',
        'group_focus_label': 'Enfoque de entrenamiento — Grupo {n}',
        'group_date_question': '📅 ¿En qué fecha quieres guardar estos entrenamientos de grupo?',
        'group_save_btn': '✅ Guardar Entrenamientos por Grupo',
        'group_saved_success': '🎉 ¡{n} entrenamientos de grupo guardados para el día {date}!',
        'training_history_title': '📅 Historial del Calendario de Entrenamientos Planificados',
        'training_edit_title': '✏️ Editar Entrenamiento',
        'training_select_edit': 'Selecciona entrenamiento a editar',
        'training_edit_date_label': '📅 Fecha de entrenamiento',
        'training_participants_label': 'Participantes',
        'training_edit_save_btn': '💾 Guardar Cambios de Entrenamiento',
        'training_select_participant_warning': 'Selecciona al menos un participante.',
        'training_edit_success': '¡Entrenamiento editado con éxito!',
        'training_delete_title': '🗑️ Eliminar Entrenamiento del Calendario',
        'training_select_delete': 'Selecciona entrenamiento a eliminar',
        'training_delete_btn': '🗑️ Eliminar Entrenamiento Seleccionado',
        'training_delete_success': '¡Entrenamiento del {date} eliminado con éxito del calendario!',
        'training_none_saved': 'Aún no hay ningún entrenamiento confirmado y guardado en el calendario.',
        'priority1_label': '1ª Prioridad',
        'priority2_label': '2ª Prioridad',
        'priority3_label': '3ª Prioridad',
        'snp_title': '📅 Calendario y Registro de Partidos SNP',
        'snp_desc': 'Gestión de las **7 jornadas SNP**. Para cada encuentro asigna los jugadores NAC y el **resultado de cada pista**.',
        'snp_select_day': '📆 Selecciona la jornada SNP',
        'snp_formation_title': '1️⃣ Alineación',
        'snp_formation_desc': 'Elige 2 jugadores NAC para cada pista. Podrás introducir el resultado más adelante, cuando se haya jugado el partido.',
        'snp_court_label': 'Pista {n}',
        'snp_player1_court': 'Jugador 1 - Pista {n}',
        'snp_player2_court': 'Jugador 2 - Pista {n}',
        'snp_notes_label': '📝 Notas / Comentarios de la jornada (opcional)',
        'snp_notes_placeholder': 'Observaciones, lesiones, etc.',
        'snp_save_formation_btn': '💾 Guardar Alineación',
        'snp_formation_saved': '✅ ¡Alineación guardada para **{day}**! Podrás introducir los resultados cuando se haya jugado el partido.',
        'snp_results_title': '2️⃣ Resultados',
        'snp_results_no_lineup': 'ℹ️ Primero asigna a los jugadores en la Alineación de arriba: luego podrás introducir aquí los resultados.',
        'snp_results_desc': 'Introduce el resultado de cada pista cuando esté disponible. Los jugadores siguen siendo los asignados en la Alineación.',
        'snp_result_court_label': 'Resultado Pista {n}',
        'snp_result_placeholder': 'ej. 6-4, 6-2',
        'snp_save_results_btn': '🏆 Guardar Resultados',
        'snp_results_saved': '✅ ¡Resultados guardados para **{day}**!',
        'snp_summary_title': '📋 Resumen Completo del Calendario SNP',
        'snp_courts_filled': '{n}/5 pistas completadas',
        'snp_not_filled': 'No completada',
        'snp_col_court': 'Pista',
        'snp_col_player1': 'Jugador 1',
        'snp_col_player2': 'Jugador 2',
        'snp_col_result': 'Resultado',
        'snp_notes_display': '**Notas:** {notes}',
        'snp_no_lineup_yet': 'Aún no se ha introducido ninguna alineación para esta jornada.',
        'snp_reset_expander': '🗑️ Restablecer datos SNP',
        'snp_reset_btn': 'Eliminar TODAS las alineaciones y resultados SNP',
        'snp_reset_success': 'Datos SNP restablecidos.',
    },
    "Svenska": {
        'training_system_intro': 'Systemet har analyserat betygen för den närvarande gruppen och föreslår följande 3 prioriteringar:',
        'training_priority_1_label': '🔥 1:a Rekommenderad Prioritet',
        'training_priority_2_label': '⚡ 2:a Rekommenderad Prioritet',
        'training_priority_3_label': '💡 3:e Rekommenderad Prioritet',
        'training_avg_label': 'Snitt: {val}/10',
        'training_custom_title': '✏️ Coachens Anpassning och Bekräftelse',
        'training_custom_desc': 'Coachen kan ändra prioriteringarna från rullgardinsmenyn och välja vilket datum träningen ska sparas i kalendern:',
        'training_coach_p1_label': '1:a Prioritet (Coach)',
        'training_coach_p2_label': '2:a Prioritet (Coach)',
        'training_coach_p3_label': '3:e Prioritet (Coach)',
        'training_date_question': '📅 Vilket datum vill du spara denna träning på?',
        'training_confirm_btn': '✅ Bekräfta och Spara i Kalendern',
        'training_saved_success': '🎉 Träningen sparades framgångsrikt för {date}!',
        'groups_split_title': '👥 Uppdelning i Grupper om 4 (baserat på svaghet)',
        'groups_split_desc': 'De valda spelarna grupperas i **grupper om 4** baserat på deras **huvudsakliga svaghet**, så att varje grupp kan arbeta mot ett specifikt mål istället för en enda prioritet för alla.',
        'groups_min_players_warning': 'Minst {n} tillgängliga spelare krävs för att bilda en grupp. Just nu finns det {count}.',
        'group_label_prefix': 'Grupp {n}',
        'group_incomplete_suffix': ' (ofullständig grupp)',
        'group_weak_metric_label': '🎯 Huvudsaklig svaghet',
        'group_focus_label': 'Träningsfokus — Grupp {n}',
        'group_date_question': '📅 Vilket datum vill du spara dessa gruppträningar på?',
        'group_save_btn': '✅ Spara Gruppträningar',
        'group_saved_success': '🎉 {n} gruppträningar sparade för {date}!',
        'training_history_title': '📅 Historik för Planerade Träningar',
        'training_edit_title': '✏️ Redigera Träning',
        'training_select_edit': 'Välj träning att redigera',
        'training_edit_date_label': '📅 Träningsdatum',
        'training_participants_label': 'Deltagare',
        'training_edit_save_btn': '💾 Spara Träningsändringar',
        'training_select_participant_warning': 'Välj minst en deltagare.',
        'training_edit_success': 'Träningen redigerades!',
        'training_delete_title': '🗑️ Ta bort Träning från Kalendern',
        'training_select_delete': 'Välj träning att ta bort',
        'training_delete_btn': '🗑️ Ta bort Vald Träning',
        'training_delete_success': 'Träningen den {date} togs bort från kalendern!',
        'training_none_saved': 'Ingen träning har ännu bekräftats och sparats i kalendern.',
        'priority1_label': '1:a Prioritet',
        'priority2_label': '2:a Prioritet',
        'priority3_label': '3:e Prioritet',
        'snp_title': '📅 Kalender & SNP-matchregistrering',
        'snp_desc': 'Hantering av de **7 SNP-omgångarna**. Tilldela NAC-spelarna och **resultatet för varje bana** för varje match.',
        'snp_select_day': '📆 Välj SNP-omgången',
        'snp_formation_title': '1️⃣ Uppställning',
        'snp_formation_desc': 'Välj 2 NAC-spelare för varje bana. Du kan ange resultatet senare, när matchen har spelats.',
        'snp_court_label': 'Bana {n}',
        'snp_player1_court': 'Spelare 1 - Bana {n}',
        'snp_player2_court': 'Spelare 2 - Bana {n}',
        'snp_notes_label': '📝 Anteckningar/kommentarer för omgången (valfritt)',
        'snp_notes_placeholder': 'Observationer, skador, etc.',
        'snp_save_formation_btn': '💾 Spara Uppställning',
        'snp_formation_saved': '✅ Uppställning sparad för **{day}**! Du kan ange resultat när matchen har spelats.',
        'snp_results_title': '2️⃣ Resultat',
        'snp_results_no_lineup': 'ℹ️ Tilldela först spelarna i Uppställningen ovan: du kan sedan ange resultaten här.',
        'snp_results_desc': 'Ange resultatet för varje bana när det är tillgängligt. Spelarna förblir de som tilldelats i Uppställningen.',
        'snp_result_court_label': 'Resultat Bana {n}',
        'snp_result_placeholder': 't.ex. 6-4, 6-2',
        'snp_save_results_btn': '🏆 Spara Resultat',
        'snp_results_saved': '✅ Resultat sparade för **{day}**!',
        'snp_summary_title': '📋 Fullständig Sammanfattning av SNP-kalendern',
        'snp_courts_filled': '{n}/5 banor ifyllda',
        'snp_not_filled': 'Ej ifylld',
        'snp_col_court': 'Bana',
        'snp_col_player1': 'Spelare 1',
        'snp_col_player2': 'Spelare 2',
        'snp_col_result': 'Resultat',
        'snp_notes_display': '**Anteckningar:** {notes}',
        'snp_no_lineup_yet': 'Ingen uppställning har ännu angetts för denna omgång.',
        'snp_reset_expander': '🗑️ Återställ SNP-data',
        'snp_reset_btn': 'Ta bort ALLA SNP-uppställningar och resultat',
        'snp_reset_success': 'SNP-data återställd.',
    },
    "Nederlands": {
        'training_system_intro': 'Het systeem heeft de cijfers van de aanwezige groep geanalyseerd en stelt de volgende 3 prioriteiten voor:',
        'training_priority_1_label': '🔥 1e Aanbevolen Prioriteit',
        'training_priority_2_label': '⚡ 2e Aanbevolen Prioriteit',
        'training_priority_3_label': '💡 3e Aanbevolen Prioriteit',
        'training_avg_label': 'Gemiddeld: {val}/10',
        'training_custom_title': '✏️ Aanpassing en Bevestiging door Coach',
        'training_custom_desc': 'De coach kan de prioriteiten wijzigen via het vervolgkeuzemenu en kiezen op welke datum de training in de kalender wordt opgeslagen:',
        'training_coach_p1_label': '1e Prioriteit (Coach)',
        'training_coach_p2_label': '2e Prioriteit (Coach)',
        'training_coach_p3_label': '3e Prioriteit (Coach)',
        'training_date_question': '📅 Op welke datum wil je deze training opslaan?',
        'training_confirm_btn': '✅ Bevestigen en Opslaan in Kalender',
        'training_saved_success': '🎉 Training succesvol opgeslagen voor {date}!',
        'groups_split_title': '👥 Verdeling in Groepen van 4 (op basis van zwakte)',
        'groups_split_desc': 'De geselecteerde spelers worden ingedeeld in **groepen van 4** op basis van hun **belangrijkste zwakte**, zodat elke groep aan een specifiek doel kan werken in plaats van één prioriteit voor iedereen.',
        'groups_min_players_warning': 'Er zijn minstens {n} beschikbare spelers nodig om een groep te vormen. Er zijn er momenteel {count}.',
        'group_label_prefix': 'Groep {n}',
        'group_incomplete_suffix': ' (onvolledige groep)',
        'group_weak_metric_label': '🎯 Belangrijkste zwakte',
        'group_focus_label': 'Trainingsfocus — Groep {n}',
        'group_date_question': '📅 Op welke datum wil je deze groepstrainingen opslaan?',
        'group_save_btn': '✅ Groepstrainingen Opslaan',
        'group_saved_success': '🎉 {n} groepstrainingen opgeslagen voor {date}!',
        'training_history_title': '📅 Geschiedenis Geplande Trainingen',
        'training_edit_title': '✏️ Training Bewerken',
        'training_select_edit': 'Selecteer training om te bewerken',
        'training_edit_date_label': '📅 Trainingsdatum',
        'training_participants_label': 'Deelnemers',
        'training_edit_save_btn': '💾 Trainingswijzigingen Opslaan',
        'training_select_participant_warning': 'Selecteer minstens één deelnemer.',
        'training_edit_success': 'Training succesvol bewerkt!',
        'training_delete_title': '🗑️ Training uit Kalender Verwijderen',
        'training_select_delete': 'Selecteer training om te verwijderen',
        'training_delete_btn': '🗑️ Geselecteerde Training Verwijderen',
        'training_delete_success': 'Training van {date} succesvol verwijderd uit de kalender!',
        'training_none_saved': 'Nog geen training bevestigd en opgeslagen in de kalender.',
        'priority1_label': '1e Prioriteit',
        'priority2_label': '2e Prioriteit',
        'priority3_label': '3e Prioriteit',
        'snp_title': '📅 Kalender & SNP-wedstrijdregistratie',
        'snp_desc': 'Beheer van de **7 SNP-speeldagen**. Wijs voor elke wedstrijd de NAC-spelers en het **resultaat van elke baan** toe.',
        'snp_select_day': '📆 Selecteer de SNP-speeldag',
        'snp_formation_title': '1️⃣ Opstelling',
        'snp_formation_desc': 'Kies 2 NAC-spelers voor elke baan. Je kunt het resultaat later invoeren, zodra de wedstrijd is gespeeld.',
        'snp_court_label': 'Baan {n}',
        'snp_player1_court': 'Speler 1 - Baan {n}',
        'snp_player2_court': 'Speler 2 - Baan {n}',
        'snp_notes_label': '📝 Notities/opmerkingen speeldag (optioneel)',
        'snp_notes_placeholder': 'Opmerkingen, blessures, enz.',
        'snp_save_formation_btn': '💾 Opstelling Opslaan',
        'snp_formation_saved': '✅ Opstelling opgeslagen voor **{day}**! Je kunt de resultaten invoeren zodra de wedstrijd is gespeeld.',
        'snp_results_title': '2️⃣ Resultaten',
        'snp_results_no_lineup': 'ℹ️ Wijs eerst de spelers toe in de Opstelling hierboven: je kunt hier daarna de resultaten invoeren.',
        'snp_results_desc': 'Voer het resultaat van elke baan in wanneer beschikbaar. De spelers blijven degenen die zijn toegewezen in de Opstelling.',
        'snp_result_court_label': 'Resultaat Baan {n}',
        'snp_result_placeholder': 'bijv. 6-4, 6-2',
        'snp_save_results_btn': '🏆 Resultaten Opslaan',
        'snp_results_saved': '✅ Resultaten opgeslagen voor **{day}**!',
        'snp_summary_title': '📋 Volledig Overzicht SNP-kalender',
        'snp_courts_filled': '{n}/5 banen ingevuld',
        'snp_not_filled': 'Niet ingevuld',
        'snp_col_court': 'Baan',
        'snp_col_player1': 'Speler 1',
        'snp_col_player2': 'Speler 2',
        'snp_col_result': 'Resultaat',
        'snp_notes_display': '**Notities:** {notes}',
        'snp_no_lineup_yet': 'Nog geen opstelling ingevoerd voor deze speeldag.',
        'snp_reset_expander': '🗑️ SNP-gegevens resetten',
        'snp_reset_btn': 'ALLE SNP-opstellingen en resultaten verwijderen',
        'snp_reset_success': 'SNP-gegevens gereset.',
    },
    "Dansk": {
        'training_system_intro': 'Systemet har analyseret karaktererne for den tilstedeværende gruppe og foreslår følgende 3 prioriteter:',
        'training_priority_1_label': '🔥 1. Anbefalede Prioritet',
        'training_priority_2_label': '⚡ 2. Anbefalede Prioritet',
        'training_priority_3_label': '💡 3. Anbefalede Prioritet',
        'training_avg_label': 'Gennemsnit: {val}/10',
        'training_custom_title': '✏️ Trænerens Tilpasning og Bekræftelse',
        'training_custom_desc': 'Træneren kan ændre prioriteterne fra rullemenuen og vælge, hvilken dato træningen skal gemmes i kalenderen:',
        'training_coach_p1_label': '1. Prioritet (Træner)',
        'training_coach_p2_label': '2. Prioritet (Træner)',
        'training_coach_p3_label': '3. Prioritet (Træner)',
        'training_date_question': '📅 Hvilken dato vil du gemme denne træning på?',
        'training_confirm_btn': '✅ Bekræft og Gem i Kalenderen',
        'training_saved_success': '🎉 Træning gemt for {date}!',
        'groups_split_title': '👥 Opdeling i Grupper på 4 (baseret på svaghed)',
        'groups_split_desc': 'De valgte spillere grupperes i **grupper på 4** baseret på deres **primære svaghed**, så hver gruppe kan arbejde med et specifikt mål i stedet for én prioritet for alle.',
        'groups_min_players_warning': 'Der kræves mindst {n} tilgængelige spillere for at danne en gruppe. Der er i øjeblikket {count}.',
        'group_label_prefix': 'Gruppe {n}',
        'group_incomplete_suffix': ' (ufuldstændig gruppe)',
        'group_weak_metric_label': '🎯 Primær svaghed',
        'group_focus_label': 'Træningsfokus — Gruppe {n}',
        'group_date_question': '📅 Hvilken dato vil du gemme disse gruppetræninger på?',
        'group_save_btn': '✅ Gem Gruppetræninger',
        'group_saved_success': '🎉 {n} gruppetræninger gemt for {date}!',
        'training_history_title': '📅 Historik for Planlagte Træninger',
        'training_edit_title': '✏️ Rediger Træning',
        'training_select_edit': 'Vælg træning der skal redigeres',
        'training_edit_date_label': '📅 Træningsdato',
        'training_participants_label': 'Deltagere',
        'training_edit_save_btn': '💾 Gem Træningsændringer',
        'training_select_participant_warning': 'Vælg mindst én deltager.',
        'training_edit_success': 'Træning redigeret!',
        'training_delete_title': '🗑️ Slet Træning fra Kalenderen',
        'training_select_delete': 'Vælg træning der skal fjernes',
        'training_delete_btn': '🗑️ Slet Valgt Træning',
        'training_delete_success': 'Træningen den {date} blev fjernet fra kalenderen!',
        'training_none_saved': 'Ingen træning er endnu bekræftet og gemt i kalenderen.',
        'priority1_label': '1. Prioritet',
        'priority2_label': '2. Prioritet',
        'priority3_label': '3. Prioritet',
        'snp_title': '📅 Kalender & SNP-kampregistrering',
        'snp_desc': 'Håndtering af de **7 SNP-spilledage**. Tildel NAC-spillerne og **resultatet for hver bane** for hver kamp.',
        'snp_select_day': '📆 Vælg SNP-spilledagen',
        'snp_formation_title': '1️⃣ Opstilling',
        'snp_formation_desc': 'Vælg 2 NAC-spillere til hver bane. Du kan indtaste resultatet senere, når kampen er spillet.',
        'snp_court_label': 'Bane {n}',
        'snp_player1_court': 'Spiller 1 - Bane {n}',
        'snp_player2_court': 'Spiller 2 - Bane {n}',
        'snp_notes_label': '📝 Noter/kommentarer til spilledagen (valgfrit)',
        'snp_notes_placeholder': 'Observationer, skader osv.',
        'snp_save_formation_btn': '💾 Gem Opstilling',
        'snp_formation_saved': '✅ Opstilling gemt for **{day}**! Du kan indtaste resultater, når kampen er spillet.',
        'snp_results_title': '2️⃣ Resultater',
        'snp_results_no_lineup': 'ℹ️ Tildel først spillerne i Opstillingen ovenfor: du kan derefter indtaste resultaterne her.',
        'snp_results_desc': 'Indtast resultatet for hver bane, når det er tilgængeligt. Spillerne forbliver dem, der er tildelt i Opstillingen.',
        'snp_result_court_label': 'Resultat Bane {n}',
        'snp_result_placeholder': 'f.eks. 6-4, 6-2',
        'snp_save_results_btn': '🏆 Gem Resultater',
        'snp_results_saved': '✅ Resultater gemt for **{day}**!',
        'snp_summary_title': '📋 Komplet Oversigt over SNP-kalenderen',
        'snp_courts_filled': '{n}/5 baner udfyldt',
        'snp_not_filled': 'Ikke udfyldt',
        'snp_col_court': 'Bane',
        'snp_col_player1': 'Spiller 1',
        'snp_col_player2': 'Spiller 2',
        'snp_col_result': 'Resultat',
        'snp_notes_display': '**Noter:** {notes}',
        'snp_no_lineup_yet': 'Ingen opstilling er endnu indtastet for denne spilledag.',
        'snp_reset_expander': '🗑️ Nulstil SNP-data',
        'snp_reset_btn': 'Slet ALLE SNP-opstillinger og resultater',
        'snp_reset_success': 'SNP-data nulstillet.',
    },
}

for _lang, _vals in TRAINING_SNP_TRANSLATIONS.items():
    translations.setdefault(_lang, {}).update(_vals)

MAX_RECOVERY_ATTEMPTS = 5


def hash_security_answer(answer):
    """Store only a hash of the answer; ignore case and extra spaces when comparing."""
    normalized = " ".join((answer or "").strip().lower().split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def security_question_text(player, lang_dict):
    key = player.get("security_question_key", "")
    if key == "sq_custom":
        return player.get("security_question_custom", "")
    return lang_dict.get(key, "") if key else ""


def has_security_question(player, lang_dict):
    return bool(player.get("security_answer_hash")) and bool(security_question_text(player, lang_dict))


def security_question_inputs(lang_dict, key_prefix, player=None):
    """Widgets to choose a question and answer. Returns (key, custom_text, answer)."""
    current_key = (player or {}).get("security_question_key", SECURITY_QUESTION_KEYS[0])
    if current_key not in SECURITY_QUESTION_KEYS:
        current_key = SECURITY_QUESTION_KEYS[0]
    q_key = st.selectbox(
        lang_dict.get('sec_question_lbl', 'Security question'),
        options=SECURITY_QUESTION_KEYS,
        index=SECURITY_QUESTION_KEYS.index(current_key),
        format_func=lambda k: lang_dict.get(k, k),
        key=f"{key_prefix}_q"
    )
    custom = st.text_input(
        lang_dict.get('sec_custom_lbl', 'Custom question'),
        value=(player or {}).get("security_question_custom", ""),
        key=f"{key_prefix}_custom"
    )
    answer = st.text_input(lang_dict.get('sec_answer_lbl', 'Answer'), type="password", key=f"{key_prefix}_answer")
    return q_key, custom, answer


def validate_security_inputs(q_key, custom, answer, lang_dict):
    if q_key == "sq_custom" and not custom.strip():
        return lang_dict.get('sec_custom_empty', 'Write your question.')
    if not answer.strip():
        return lang_dict.get('sec_answer_empty', 'Answer required.')
    return None


def apply_security_question(player, q_key, custom, answer):
    player["security_question_key"] = q_key
    player["security_question_custom"] = custom.strip() if q_key == "sq_custom" else ""
    player["security_answer_hash"] = hash_security_answer(answer)

# --- LISTA DELLE SKILLS ---
TECH_SKILLS = ["Volley", "Bandeja", "Vibora", "Smash", "Bajada", "Chiquita", "Lob"]

# --- INIZIALIZZAZIONE LINGUA & SKILLS ---
if "language" not in st.session_state:
    st.session_state.language = "English"

lang_dict = translations.get(st.session_state.language, translations["English"])
MENTAL_SKILLS = lang_dict.get("mental_list", translations["English"]["mental_list"])
ALL_SKILLS = TECH_SKILLS + MENTAL_SKILLS

if "nav_mode" not in st.session_state:
    st.session_state.nav_mode = "Home"

if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

if "authenticated_admin" not in st.session_state:
    st.session_state.authenticated_admin = False

if "authenticated_player" not in st.session_state:
    st.session_state.authenticated_player = None

if "show_roster_modal" not in st.session_state:
    st.session_state.show_roster_modal = False

if "force_password_change" not in st.session_state:
    st.session_state.force_password_change = False

# Caricamento dati salvati in precedenza sul server se esistono
print(f"[DB] DATABASE_URL present at startup: {bool(DATABASE_URL)}", flush=True)
init_db()
db_reachable, saved_server_data = load_data_from_server()
print(f"[DB] Startup load: reachable={db_reachable}", flush=True)

if not db_reachable and "squad_data" not in st.session_state:
    # The database could not be reached even after retries. Do NOT fall back to
    # the hardcoded default roster here: that would silently discard real saved
    # data, and a later "Save" click would overwrite it permanently. Stop and
    # tell the user instead, so nothing is lost.
    st.error(lang_dict.get('db_unreachable_error', "⚠️ Unable to connect to the database. Your saved data might not be visible right now. To protect it, the app will not proceed with empty data: reload the page in a few seconds. If the problem persists, contact the administrator."))
    st.stop()

if saved_server_data:
    if "squad_data" not in st.session_state:
        st.session_state.squad_data = saved_server_data.get("squad_data", [])
    if "planned_trainings" not in st.session_state:
        st.session_state.planned_trainings = saved_server_data.get("planned_trainings", [])
    if "match_results" not in st.session_state:
        st.session_state.match_results = saved_server_data.get("match_results", [])
    if "snp_lineups" not in st.session_state:
        st.session_state.snp_lineups = normalize_snp_lineups(saved_server_data.get("snp_lineups", {}))
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = saved_server_data.get("activity_log", [])
else:
    if "planned_trainings" not in st.session_state:
        st.session_state.planned_trainings = []
    if "match_results" not in st.session_state:
        st.session_state.match_results = []
    if "snp_lineups" not in st.session_state:
        st.session_state.snp_lineups = {}
    if "activity_log" not in st.session_state:
        st.session_state.activity_log = []
    if "squad_data" not in st.session_state:
        st.session_state.squad_data = [
            {"fname": "Alexander", "lname": "Wennstam", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1, "tech": [8, 8, 7, 7, 8, 6, 7], "mental": [7, 7, 8, 8, 7, 7, 8], "c_tech": [7, 7, 6, 6, 7, 5, 6], "c_mental": [6, 6, 7, 7, 6, 6, 7], "play_style": "Equilibrated", "player_play_style": "Equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Alexander", "first_login_done": False},
            {"fname": "Alvaro", "lname": "Gomez", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1, "tech": [7, 7, 6, 7, 6, 6, 7], "mental": [8, 7, 7, 7, 8, 7, 8], "c_tech": [6, 6, 5, 6, 5, 5, 6], "c_mental": [7, 6, 6, 6, 7, 6, 7], "play_style": "Equilibrated", "player_play_style": "Equilibrated", "history": [], "coach_note": "", "partners": {"Yannik Langeslag": 12, "Josu Usabiaga": 8}, "comments": [], "password": "Alvaro", "first_login_done": False},
            {"fname": "Andrea", "lname": "Lonoce", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1, "tech": [8, 7, 8, 7, 9, 6, 8], "mental": [9, 7, 8, 8, 9, 7, 9], "c_tech": [8, 7, 8, 7, 9, 6, 8], "c_mental": [9, 7, 8, 8, 9, 7, 9], "play_style": "Offensive", "player_play_style": "Offensive", "history": [], "coach_note": "", "partners": {"Alexander Wennstam": 14}, "comments": [], "password": "Andrea", "first_login_done": False},
            {"fname": "Benjamin", "lname": "Thyrell", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1, "tech": [7, 7, 8, 6, 7, 6, 7], "mental": [8, 7, 7, 7, 8, 7, 8], "c_tech": [6, 6, 7, 5, 6, 5, 6], "c_mental": [7, 6, 6, 6, 7, 6, 7], "play_style": "Counterattack", "player_play_style": "Counterattack", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Benjamin", "first_login_done": False},
            {"fname": "Doug", "lname": "Ramsay", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0, "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "Equilibrated", "player_play_style": "Equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Doug", "first_login_done": False},
            {"fname": "Fernando", "lname": "Oribe", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 0, "tech": [8, 7, 8, 7, 8, 6, 7], "mental": [8, 7, 8, 8, 8, 7, 8], "c_tech": [7, 6, 7, 6, 7, 5, 6], "c_mental": [7, 6, 7, 7, 7, 6, 7], "play_style": "Counterattack", "player_play_style": "Counterattack", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Fernando", "first_login_done": False},
            {"fname": "Gonzalo", "lname": "Diez de Onate", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1, "tech": [8, 7, 8, 7, 8, 6, 7], "mental": [8, 7, 8, 8, 8, 7, 8], "c_tech": [7, 6, 7, 6, 7, 5, 6], "c_mental": [7, 6, 7, 7, 7, 6, 7], "play_style": "Equilibrated", "player_play_style": "Equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Gonzalo", "first_login_done": False},
            {"fname": "Hector", "lname": "Guerrero", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1, "tech": [7, 7, 7, 7, 7, 6, 7], "mental": [7, 7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 6, 6, 5, 6], "c_mental": [6, 6, 6, 6, 6, 6, 6], "play_style": "Counterattack", "player_play_style": "Counterattack", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Hector", "first_login_done": False},
            {"fname": "Jairo", "lname": "Lopez", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0, "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "Defensive", "player_play_style": "Defensive", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Jairo", "first_login_done": False},
            {"fname": "Josu", "lname": "Usabiaga", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1, "tech": [6, 8, 7, 7, 6, 7, 7], "mental": [6, 8, 6, 8, 7, 7, 8], "c_tech": [5, 7, 6, 6, 5, 6, 6], "c_mental": [5, 7, 5, 7, 6, 6, 7], "play_style": "Defensive", "player_play_style": "Defensive", "history": [], "coach_note": "", "partners": {"Alvaro Gomez": 8}, "comments": [], "password": "Josu", "first_login_done": False},
            {"fname": "Juanjo", "lname": "Lopez Benitez", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0, "tech": [8, 8, 8, 7, 8, 7, 7], "mental": [8, 8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6, 6], "c_mental": [7, 7, 7, 7, 7, 7, 7], "play_style": "Offensive", "player_play_style": "Offensive", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Juanjo", "first_login_done": False},
            {"fname": "Julio", "lname": "Morales", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1, "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "Offensive", "player_play_style": "Offensive", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Julio", "first_login_done": False},
            {"fname": "Lars", "lname": "Mikkelsen", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0, "tech": [7, 7, 7, 6, 8, 6, 7], "mental": [8, 7, 7, 7, 8, 7, 8], "c_tech": [6, 6, 6, 5, 7, 5, 6], "c_mental": [7, 6, 6, 6, 7, 6, 7], "play_style": "Equilibrated", "player_play_style": "Equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Lars", "first_login_done": False},
            {"fname": "Mikkel", "lname": "Hoff", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1, "tech": [7, 6, 7, 6, 7, 5, 6], "mental": [7, 6, 7, 7, 7, 6, 7], "c_tech": [6, 5, 6, 5, 6, 4, 5], "c_mental": [6, 5, 6, 6, 6, 5, 6], "play_style": "Defensive", "player_play_style": "Defensive", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Mikkel", "first_login_done": False},
            {"fname": "Nacho", "lname": "Saracho", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 0, "tech": [8, 8, 8, 7, 8, 7, 7], "mental": [8, 8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6, 6], "c_mental": [7, 7, 7, 7, 7, 7, 7], "play_style": "Counterattack", "player_play_style": "Counterattack", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Nacho", "first_login_done": False},
            {"fname": "Pedro", "lname": "Rios", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 1, "tech": [8, 8, 8, 7, 8, 7, 7], "mental": [8, 8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6, 6], "c_mental": [7, 7, 7, 7, 7, 7, 7], "play_style": "Equilibrated", "player_play_style": "Equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Pedro", "first_login_done": False},
            {"fname": "Peter", "lname": "Gustafsson", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 0, "tech": [7, 7, 7, 6, 7, 6, 7], "mental": [7, 7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5, 6], "c_mental": [6, 6, 6, 6, 6, 6, 6], "play_style": "Equilibrated", "player_play_style": "Equilibrated", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Peter", "first_login_done": False},
            {"fname": "Sascha", "lname": "Van De Bilt", "side": "Right", "hand": "Destro", "trainings": 1, "participated": 0, "tech": [7, 7, 7, 6, 7, 6, 7], "mental": [7, 7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5, 6], "c_mental": [6, 6, 6, 6, 6, 6, 6], "play_style": "Defensive", "player_play_style": "Defensive", "history": [], "coach_note": "", "partners": {}, "comments": [], "password": "Sascha", "first_login_done": False},
            {"fname": "Yannik", "lname": "Langeslag", "side": "Left", "hand": "Mancino", "trainings": 1, "participated": 1, "tech": [8, 6, 7, 7, 7, 5, 6], "mental": [7, 6, 8, 6, 7, 6, 7], "c_tech": [7, 5, 6, 6, 6, 4, 5], "c_mental": [6, 5, 7, 5, 6, 5, 6], "play_style": "Offensive", "player_play_style": "Offensive", "history": [], "coach_note": "", "partners": {"Alvaro Gomez": 12}, "comments": [], "password": "Yannik", "first_login_done": False}
        ]

st.session_state.squad_data = sorted(st.session_state.squad_data, key=lambda x: x['fname'])

for p in st.session_state.squad_data:
    if "hand" not in p: p["hand"] = "Mancino" if p.get("side") == "Left" else "Destro"
    if "coach_note" not in p: p["coach_note"] = ""
    if "play_style" not in p: p["play_style"] = "Equilibrated"
    if "player_play_style" not in p: p["player_play_style"] = p.get("play_style", "Equilibrated")
    if "trainings" not in p: p["trainings"] = 1
    if "participated" not in p: p["participated"] = 1
    if "password" not in p: p["password"] = p["fname"]
    if "first_login_done" not in p: p["first_login_done"] = False
    
    if len(p["tech"]) != len(TECH_SKILLS): p["tech"] = [7] * len(TECH_SKILLS)
    if len(p["mental"]) != len(MENTAL_SKILLS): p["mental"] = [7] * len(MENTAL_SKILLS)
    if len(p["c_tech"]) != len(TECH_SKILLS): p["c_tech"] = [6] * len(TECH_SKILLS)
    if len(p["c_mental"]) != len(MENTAL_SKILLS): p["c_mental"] = [6] * len(MENTAL_SKILLS)

squad_players = st.session_state.squad_data
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []
save_data_to_server()


# --- SIDEBAR & LINGUA ---
with st.sidebar:
    st.title("Padel Hub")
    
    available_languages = ["Italiano", "English", "Español", "Svenska", "Nederlands", "Dansk"]
    current_lang_index = available_languages.index(st.session_state.language) if st.session_state.language in available_languages else 0
    selected_lang = st.selectbox("🌐 Lingua / Language", available_languages, index=current_lang_index)
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
        
    lang_dict = translations.get(st.session_state.language, translations["English"])
    
    st.markdown("---")
    if st.session_state.get("authenticated_admin"):
        st.success("🛡️ Admin Logged In")
        if st.button(lang_dict.get("logout", "Logout"), key="sidebar_logout_admin"):
            st.session_state.authenticated_admin = False
            st.session_state.authenticated_coach = False
            st.session_state.nav_mode = "Home"
            st.rerun()
    elif st.session_state.authenticated_coach:
        st.success("🔒 Coach Logged In")
        if st.button(lang_dict.get("logout", "Logout"), key="sidebar_logout_coach"):
            st.session_state.authenticated_coach = False
            st.session_state.nav_mode = "Home"
            st.rerun()
    elif st.session_state.authenticated_player:
        st.success(f"👤 Player: {st.session_state.authenticated_player}")
        if st.button(lang_dict.get("logout", "Logout"), key="sidebar_logout_player"):
            st.session_state.authenticated_player = None
            st.session_state.force_password_change = False
            st.session_state.nav_mode = "Home"
            st.rerun()

lang_dict = translations.get(st.session_state.language, translations["English"])
MENTAL_SKILLS = lang_dict.get("mental_list", translations["English"]["mental_list"])
ALL_SKILLS = TECH_SKILLS + MENTAL_SKILLS

# --- CONTROLLO FORZATURA CAMBIO PASSWORD (PRIMO ACCESSO) ---
if st.session_state.get("force_password_change", False):
    current_player = next((p for p in squad_players if p['fname'] == st.session_state.authenticated_player), None)
    st.title(lang_dict.get('first_login_title', '🔒 First Login: Set Your New Password'))
    st.markdown(lang_dict.get('first_login_welcome', "Welcome **{name}**! For security reasons, since this is your first login, you need to set a personal password that only you will know.").format(name=current_player['fname']))

    with st.form("change_pwd_form"):
        new_pwd1 = st.text_input(lang_dict.get('forgot_new_pwd', 'New password'), type="password")
        new_pwd2 = st.text_input(lang_dict.get('forgot_confirm_pwd', 'Confirm new password'), type="password")

        st.markdown("---")
        st.markdown(f"**🔐 {lang_dict.get('sec_section_title', 'Security question')}**")
        st.caption(lang_dict.get('sec_section_desc', ''))
        fl_q_key, fl_custom, fl_answer = security_question_inputs(lang_dict, "first_login_sec", current_player)

        if st.form_submit_button(lang_dict.get('first_login_save_btn', 'Save Password and Login'), type="primary"):
            sec_error = validate_security_inputs(fl_q_key, fl_custom, fl_answer, lang_dict)
            if not new_pwd1.strip():
                st.warning(lang_dict.get('pwd_empty', "The password can't be empty."))
            elif new_pwd1 != new_pwd2:
                st.error(lang_dict.get('pwd_mismatch', "The passwords don't match. Try again."))
            elif sec_error:
                st.warning(sec_error)
            else:
                current_player["password"] = new_pwd1
                current_player["first_login_done"] = True
                apply_security_question(current_player, fl_q_key, fl_custom, fl_answer)
                if save_data_to_server():
                    st.session_state.force_password_change = False
                    st.session_state.nav_mode = "Player_Dashboard"
                    st.success(lang_dict.get('first_login_success', '✅ Password set and saved successfully!'))
                    st.rerun()

# --- HOME SELECTION ---
elif st.session_state.nav_mode == "Home":
    st.title(f"🎾 {lang_dict.get('welcome', 'Padel AI')}")
    st.markdown(lang_dict.get('select_area', 'Select area:'))
    
    col_home1, col_home2 = st.columns(2)
    with col_home1:
        st.markdown(f"### 👤 {lang_dict.get('player_area', 'Player Area')}")
        st.markdown(lang_dict.get('player_desc', ''))
        if st.button(lang_dict.get('player_btn', 'Player Login'), use_container_width=True, type="primary"):
            st.session_state.nav_mode = "Player_Login"
            st.rerun()
            
    with col_home2:
        st.markdown(f"### 📋 {lang_dict.get('coach_area', 'Coach Area')}")
        st.markdown(lang_dict.get('coach_desc', ''))
        if st.button(lang_dict.get('coach_btn', 'Coach Login'), use_container_width=True, type="primary"):
            st.session_state.nav_mode = "Coach_Login"
            st.rerun()
    
    # Admin access - small, bottom
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    col_adm1, col_adm2, col_adm3 = st.columns([2, 1, 2])
    with col_adm2:
        if st.button("🛡️ Admin", use_container_width=True, type="secondary"):
            st.session_state.nav_mode = "Admin_Login"
            st.rerun()

# --- LOGIN GIOCATORE ---
elif st.session_state.nav_mode == "Player_Login":
    st.title(f"🔐 {lang_dict.get('login_player_title', 'Player Login')}")
    st.markdown(lang_dict.get('login_player_sub', ''))
    
    player_options = [f"{p['fname']} {p['lname']} ({p['side']})" for p in squad_players]
    selected_player_str = st.selectbox(lang_dict.get('profile_select', 'Select profile:'), player_options)
    selected_fname = selected_player_str.split(" ")[0]
    
    player_obj = next((p for p in squad_players if p['fname'] == selected_fname), None)
    
    player_pwd_input = st.text_input(lang_dict.get('pwd_label', 'Password'), type="password")
    
    col_pl1, col_pl2 = st.columns(2)
    with col_pl1:
        if st.button(lang_dict.get('enter_card', 'Enter'), type="primary", use_container_width=True):
            if player_obj:
                is_first_login = not player_obj.get("first_login_done", False)
                current_saved_pwd = player_obj.get("password", player_obj["fname"])
                
                if is_first_login:
                    if player_pwd_input.strip().lower() == player_obj["fname"].lower():
                        st.session_state.authenticated_player = selected_fname
                        st.session_state.force_password_change = True
                        log_activity("Player login (first access)", f"{player_obj['fname']} {player_obj['lname']}")
                        st.rerun()
                    else:
                        st.error(lang_dict.get('first_login_hint_error', '❌ First login: enter your first name as the password.'))
                else:
                    if player_pwd_input == current_saved_pwd:
                        st.session_state.authenticated_player = selected_fname
                        st.session_state.force_password_change = False
                        st.session_state.nav_mode = "Player_Dashboard"
                        log_activity("Player login", f"{player_obj['fname']} {player_obj['lname']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {lang_dict.get('wrong_pwd', 'Wrong password')}")
    with col_pl2:
        if st.button(lang_dict.get('back_home', 'Back'), use_container_width=True):
            st.session_state.forgot_pwd_mode = False
            st.session_state.nav_mode = "Home"
            st.rerun()

    # --- Recupero password con domanda di sicurezza ---
    if st.button(f"🔑 {lang_dict.get('forgot_pwd_btn', 'Forgot password?')}", key="forgot_pwd_toggle"):
        st.session_state.forgot_pwd_mode = not st.session_state.get("forgot_pwd_mode", False)
        st.rerun()

    if st.session_state.get("forgot_pwd_mode", False) and player_obj:
        st.markdown("---")
        st.subheader(f"🔑 {lang_dict.get('forgot_title', 'Password recovery')}")
        attempts = st.session_state.setdefault("recovery_attempts", {})
        used = attempts.get(player_obj["fname"], 0)

        if not player_obj.get("first_login_done", False):
            st.info(lang_dict.get('forgot_first_login', 'Your password is your first name.'))
        elif not has_security_question(player_obj, lang_dict):
            st.warning(lang_dict.get('forgot_no_question', 'No security question set.'))
        elif used >= MAX_RECOVERY_ATTEMPTS:
            st.error(lang_dict.get('forgot_too_many', 'Too many attempts.'))
        else:
            st.markdown(lang_dict.get('forgot_sub', ''))
            st.markdown(f"**{security_question_text(player_obj, lang_dict)}**")
            with st.form(f"forgot_pwd_form_{player_obj['fname']}"):
                rec_answer = st.text_input(lang_dict.get('forgot_answer_lbl', 'Your answer'), type="password")
                rec_pwd1 = st.text_input(lang_dict.get('forgot_new_pwd', 'New password'), type="password")
                rec_pwd2 = st.text_input(lang_dict.get('forgot_confirm_pwd', 'Confirm new password'), type="password")
                if st.form_submit_button(lang_dict.get('forgot_submit', 'Set new password'), type="primary"):
                    if hash_security_answer(rec_answer) != player_obj.get("security_answer_hash"):
                        attempts[player_obj["fname"]] = used + 1
                        left = MAX_RECOVERY_ATTEMPTS - attempts[player_obj["fname"]]
                        log_activity("Password recovery failed", f"{player_obj['fname']} {player_obj['lname']}")
                        if left > 0:
                            st.error(lang_dict.get('forgot_wrong_answer', 'Wrong answer. Attempts left: {n}').format(n=left))
                        else:
                            st.error(lang_dict.get('forgot_too_many', 'Too many attempts.'))
                    elif not rec_pwd1.strip():
                        st.warning(lang_dict.get('pwd_empty', 'Password cannot be empty.'))
                    elif rec_pwd1 != rec_pwd2:
                        st.error(lang_dict.get('pwd_mismatch', 'Passwords do not match.'))
                    else:
                        player_obj["password"] = rec_pwd1
                        player_obj["first_login_done"] = True
                        attempts[player_obj["fname"]] = 0
                        log_activity("Password recovered", f"{player_obj['fname']} {player_obj['lname']}")
                        if save_data_to_server():
                            st.session_state.forgot_pwd_mode = False
                            st.success(f"✅ {lang_dict.get('forgot_success', 'Password updated!')}")

# --- LOGIN ALLENATORE ---
elif st.session_state.nav_mode == "Coach_Login":
    st.title(f"🔒 {lang_dict.get('coach_login_title', 'Coach Login')}")
    st.markdown(lang_dict.get('coach_login_sub', ''))
    
    COACH_PASSWORD = "padelcoach2026"
    pwd_input = st.text_input(lang_dict.get('coach_pwd_label', 'Password'), type="password")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button(lang_dict.get('verify_pwd', 'Verify'), type="primary", use_container_width=True):
            if pwd_input == COACH_PASSWORD:
                st.session_state.authenticated_coach = True
                log_activity("Coach login", "Coach accessed the system")
                if save_data_to_server():
                    st.session_state.nav_mode = "Coach"
                    st.rerun()
            else:
                st.error(lang_dict.get('coach_wrong_pwd', '❌ Wrong password! Try again.'))
    with col_btn2:
        if st.button(lang_dict.get('back_home', 'Back'), use_container_width=True, key="coach_login_back"):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- LOGIN ADMIN ---
elif st.session_state.nav_mode == "Admin_Login":
    st.title("🛡️ Admin Access")
    st.markdown("Full access to all app features (squad, evaluations, matches, players).")
    
    ADMIN_PASSWORD = "nacadmin2026"
    admin_pwd = st.text_input(lang_dict.get('admin_pwd_label', 'Admin Password'), type="password", key="admin_pwd_input")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("Verify Admin", type="primary", use_container_width=True, key="admin_verify_btn"):
            if admin_pwd == ADMIN_PASSWORD:
                st.session_state.authenticated_admin = True
                st.session_state.authenticated_coach = True  # full coach privileges
                log_activity("Admin login", "Admin accessed the system")
                if save_data_to_server():
                    st.session_state.nav_mode = "Coach"
                    st.rerun()
            else:
                st.error(lang_dict.get('admin_wrong_pwd', '❌ Wrong admin password.'))
    with col_a2:
        if st.button(lang_dict.get('back_home', 'Back'), use_container_width=True, key="admin_login_back"):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- DASHBOARD GIOCATORE ---
elif st.session_state.nav_mode == "Player_Dashboard":
    current_player = next((p for p in squad_players if p['fname'] == st.session_state.authenticated_player), None)
    admin_viewing = st.session_state.get("admin_viewing_player", False) and st.session_state.get("authenticated_admin", False)
    
    col_top1, col_top2 = st.columns([5, 2])
    with col_top1:
        if admin_viewing:
            st.title(f"🛡️ Admin → 👤 {current_player['fname']} {current_player['lname']} ({current_player['side']})")
            st.caption("You are viewing this player profile as Admin. You can edit all fields.")
        else:
            st.title(f"👤 {current_player['fname']} {current_player['lname']} ({current_player['side']})")
    with col_top2:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if admin_viewing:
            if st.button("← Back to Admin", use_container_width=True, type="primary", key="back_to_admin_btn"):
                st.session_state.authenticated_player = None
                st.session_state.admin_viewing_player = False
                st.session_state.force_password_change = False
                st.session_state.nav_mode = "Coach"
                st.rerun()
        else:
            if st.button(lang_dict.get('logout', 'Logout'), use_container_width=False):
                st.session_state.authenticated_player = None
                st.session_state.force_password_change = False
                st.session_state.nav_mode = "Home"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("---")

    # --- Domanda di sicurezza per il recupero password ---
    sec_is_set = has_security_question(current_player, lang_dict)
    if not sec_is_set:
        st.warning(f"🔐 {lang_dict.get('sec_not_set_warn', 'No security question set.')}")
    with st.expander(f"🔐 {lang_dict.get('sec_section_title', 'Security question')}", expanded=not sec_is_set):
        st.caption(lang_dict.get('sec_section_desc', ''))
        if sec_is_set:
            st.markdown(f"{lang_dict.get('sec_current_lbl', 'Current question:')} **{security_question_text(current_player, lang_dict)}**")
        with st.form("security_question_form"):
            dq_key, dq_custom, dq_answer = security_question_inputs(lang_dict, "dash_sec", current_player)
            if st.form_submit_button(lang_dict.get('sec_save_btn', 'Save'), type="primary"):
                sec_error = validate_security_inputs(dq_key, dq_custom, dq_answer, lang_dict)
                if sec_error:
                    st.warning(sec_error)
                else:
                    apply_security_question(current_player, dq_key, dq_custom, dq_answer)
                    log_activity("Security question set", f"{current_player['fname']} {current_player['lname']}")
                    if save_data_to_server():
                        st.success(lang_dict.get('sec_saved', 'Saved!'))
                        st.rerun()
    
    tab_eval, tab_partners, tab_history, tab_comments, tab_calendar = st.tabs([
        f"📊 {lang_dict.get('eval_coach_tab', 'Evaluation')}", 
        f"🏆 {lang_dict.get('partners_tab', 'Partners')}", 
        f"📈 {lang_dict.get('history_tab', 'History')}", 
        f"💬 {lang_dict.get('comments_tab', 'Comments')}",
        f"📅 {lang_dict.get('calendar_tab', 'Match Calendar')}"
    ])
    
    with tab_eval:
        st.subheader(f"📊 {lang_dict.get('eval_coach_tab', 'Evaluation')}")
        st.markdown(lang_dict.get('eval_desc', ''))
        
        style_options = ["Offensive", "Defensive", "Equilibrated", "Counterattack"]
        
        col_eval_left, col_eval_right = st.columns(2)
        
        new_tech_vals = []
        new_mental_vals = []
        
        with col_eval_left:
            st.markdown(f"**{lang_dict.get('tech_skills', 'Technical Skills')}**")
            for i, skill in enumerate(TECH_SKILLS):
                c1, c2 = st.columns(2)
                with c1:
                    val = st.slider(f"Tu - {skill}", 1, 10, int(current_player['tech'][i]), key=f"p_tech_{i}")
                    new_tech_vals.append(val)
                with c2:
                    st.slider(f"Coach - {skill}", 1, 10, int(current_player['c_tech'][i]), disabled=True, key=f"c_tech_view_{i}")

        with col_eval_right:
            st.markdown(f"**{lang_dict.get('mental_skills', 'Mental Skills')}**")
            for i, skill in enumerate(MENTAL_SKILLS):
                c1, c2 = st.columns(2)
                with c1:
                    val = st.slider(f"Tu - {skill}", 1, 10, int(current_player['mental'][i]), key=f"p_mental_{i}")
                    new_mental_vals.append(val)
                with c2:
                    st.slider(f"Coach - {skill}", 1, 10, int(current_player['c_mental'][i]), disabled=True, key=f"c_mental_view_{i}")
                
        st.markdown("---")
        current_p_style = current_player.get("player_play_style", "Equilibrated")
        if current_p_style not in style_options: current_p_style = "Equilibrated"
        new_player_style = st.selectbox(lang_dict.get('style_select_lbl', 'Play Style:'), options=style_options, index=style_options.index(current_p_style))
                
        if st.button(lang_dict.get('save_eval', 'Save'), type="primary"):
            current_player['tech'] = new_tech_vals
            current_player['mental'] = new_mental_vals
            current_player['player_play_style'] = new_player_style
            log_activity("Self-evaluation saved", f"{current_player['fname']} {current_player['lname']} – style: {new_player_style}")
            if save_data_to_server():
                st.success(lang_dict.get('eval_saved', 'Saved!'))
                st.rerun()

        st.markdown("---")
        st.subheader(f"🕸️ {lang_dict.get('radar_title', 'Radar Charts')}")
        
        all_skills_labels = TECH_SKILLS + MENTAL_SKILLS
        player_full_vals = current_player['tech'] + current_player['mental']
        coach_full_vals = current_player['c_tech'] + current_player['c_mental']
        
        categories = all_skills_labels + [all_skills_labels[0]]
        p_vals_radar = player_full_vals + [player_full_vals[0]]
        c_vals_radar = coach_full_vals + [coach_full_vals[0]]
        
        radar_col1, radar_col2 = st.columns(2)
        
        with radar_col1:
            st.markdown(f"### {lang_dict.get('player_radar_title', 'Player Radar')}")
            p_style_display = current_player.get("player_play_style", "Equilibrated")
            st.markdown(f"**{lang_dict.get('play_style_lbl', 'Play Style:')}** {p_style_display}")
            
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
                height=400,
                margin=dict(l=20, r=20, t=10, b=10)
            )
            st.plotly_chart(fig_player, use_container_width=True)
            
        with radar_col2:
            st.markdown(f"### {lang_dict.get('coach_radar_title', 'Coach Radar')}")
            play_style_display = current_player.get("play_style", "Equilibrated")
            st.markdown(f"**{lang_dict.get('play_style_lbl', 'Play Style:')}** {play_style_display}")
            
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
                height=400,
                margin=dict(l=20, r=20, t=10, b=10)
            )
            st.plotly_chart(fig_coach, use_container_width=True)

        st.markdown("---")
        st.subheader(f"📋 {lang_dict.get('diff_tables', 'Difference Tables')}")
        
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
            st.markdown(f"#### 🎾 {lang_dict.get('tech_feat', 'Technical Features')}")
            st.markdown(f"<div class='table-container'>{pd.DataFrame(diff_tech_rows).to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
            
        with t_col2:
            st.markdown(f"#### 🧠 {lang_dict.get('mental_feat', 'Mental Features')}")
            st.markdown(f"<div class='table-container'>{pd.DataFrame(diff_mental_rows).to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)

    with tab_partners:
        st.subheader(f"🏆 {lang_dict.get('partner_mgmt', 'Partner Management')}")
        all_colleagues = [f"{p['fname']} {p['lname']}" for p in squad_players if p['fname'] != current_player['fname']]
        current_partners = current_player.get("partners", {})
        
        with st.form("partners_form"):
            new_partners_dict = {}
            for i in range(5):
                existing_keys = list(current_partners.keys())
                default_partner = existing_keys[i] if i < len(existing_keys) else (all_colleagues[0] if all_colleagues else "")
                default_val = int(current_partners.get(default_partner, 5 - i))
                
                p_sel = st.selectbox(f"Partner #{i+1}", all_colleagues, index=all_colleagues.index(default_partner) if default_partner in all_colleagues else 0, key=f"partner_sel_{i}")
                
                if p_sel:
                    new_partners_dict[p_sel] = default_val
                    
            if st.form_submit_button(lang_dict.get('save_partners', 'Save Partners'), type="primary"):
                current_player["partners"] = new_partners_dict
                log_activity("Partner ranking updated", f"{current_player['fname']} {current_player['lname']}")
                if save_data_to_server():
                    st.success(lang_dict.get('partners_saved', 'Saved!'))
                    st.rerun()
                
        st.markdown(f"### {lang_dict.get('current_ranking', 'Current Ranking:')}")
        if current_player.get("partners"):
            df_part = pd.DataFrame(list(current_player["partners"].keys()), columns=[lang_dict.get('col_partner', 'Partner')]).reset_index(drop=True)
            df_part.index = df_part.index + 1
            st.markdown(f"<div class='table-container'>{df_part.to_html(escape=False, index=True, classes='custom-table')}</div>", unsafe_allow_html=True)
        else:
            st.info(lang_dict.get('no_partners', 'No partners.'))

    with tab_history:
        st.subheader(f"📈 {lang_dict.get('history_title', 'History')}")
        history_records = current_player.get("history", [])
        if history_records:
            for idx, hist in enumerate(history_records):
                st.markdown(f"**Aggiornamento #{idx+1} ({hist.get('date', '')})**")
                st.json(hist.get('values'))
        else:
            st.info(lang_dict.get('no_history', 'No history.'))

    with tab_comments:
        st.subheader(f"💬 {lang_dict.get('comments_tab', 'Comments')}")
        
        st.markdown(f"### 📋 {lang_dict.get('official_note', 'Official Note')}")
        coach_note_val = current_player.get("coach_note", "")
        if coach_note_val.strip():
            st.markdown(
                f"<div class='coach-note-box'>{coach_note_val}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"*{lang_dict.get('no_coach_note', 'No note.')}*")
            
        st.markdown("---")
        st.subheader(f"💬 {lang_dict.get('peer_feedback', 'Peer Feedback')}")
        target_colleagues = [f"{p['fname']} {p['lname']}" for p in squad_players if p['fname'] != current_player['fname']]
        selected_target = st.selectbox(lang_dict.get('select_partner_lbl', 'Select partner:'), target_colleagues)
        comment_text = st.text_area(lang_dict.get('note_on_partner', 'Note:'))
        if st.button(lang_dict.get('send_note', 'Send')):
            if comment_text.strip():
                target_p = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_target), None)
                if target_p:
                    target_p.setdefault("comments", []).append({
                        "from": f"{current_player['fname']} {current_player['lname']}",
                        "text": comment_text,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    log_activity("Peer feedback sent", f"From {current_player['fname']} to {selected_target}")
                    if save_data_to_server():
                        st.success(lang_dict.get('note_sent', 'Sent!'))
            else:
                st.warning(lang_dict.get('empty_note_warn', 'Cannot be empty.'))
        
        st.markdown(f"### {lang_dict.get('received_lbl', 'Received:')}")
        for c in current_player.get("comments", []):
            st.markdown(
                f"<div class='feedback-box'>"
                f"<strong>From {c['from']}</strong> <span class='feedback-date'>({c['date']})</span><br>"
                f"{c['text']}</div>",
                unsafe_allow_html=True
            )

    with tab_calendar:
        st.subheader(f"📅 {lang_dict.get('calendar_tab', 'Match Calendar')}")

        my_name = f"{current_player['fname']} {current_player['lname']}"
        lineups = normalize_snp_lineups(st.session_state.get("snp_lineups", {}))
        today = datetime.now().date()

        def cal_my_slot(day_lineup):
            """Return (pista, partner, result) if the player is in this lineup, else None."""
            for pista in range(1, 6):
                p1 = day_lineup.get(f"pista_{pista}_p1", "")
                p2 = day_lineup.get(f"pista_{pista}_p2", "")
                if my_name in (p1, p2):
                    partner = p2 if p1 == my_name else p1
                    return pista, partner, day_lineup.get(f"pista_{pista}_risultato", "").strip()
            return None

        def cal_lineup_published(day_lineup):
            return any(day_lineup.get(f"pista_{p}_{k}", "") for p in range(1, 6) for k in ("p1", "p2"))

        def cal_you_text(day_lineup):
            if not day_lineup or not cal_lineup_published(day_lineup):
                return lang_dict.get('cal_lineup_pending', 'Lineup not out yet'), "#8fa3bf"
            slot = cal_my_slot(day_lineup)
            if not slot:
                return lang_dict.get('cal_not_called', 'Not in the lineup'), "#8fa3bf"
            pista, partner, result = slot
            txt = f"{lang_dict.get('cal_court', 'Court')} {pista}" + (f" · {partner}" if partner else "")
            if result:
                txt += f" · {result}"
            return txt, "#7ee2a8"

        # --- Prossima partita ---
        next_day = next((d for d in SNP_CALENDAR if datetime.strptime(d["iso"], "%Y-%m-%d").date() >= today), None)
        if next_day:
            match_date = datetime.strptime(next_day["iso"], "%Y-%m-%d").date()
            days_left = (match_date - today).days
            if days_left == 0:
                when = lang_dict.get('cal_today', 'today')
            elif days_left == 1:
                when = lang_dict.get('cal_tomorrow', 'tomorrow')
            else:
                when = lang_dict.get('cal_in_days', 'in {n} days').format(n=days_left)
            is_home = next_day["home"] == "NAC"
            venue = lang_dict.get('cal_home', 'home') if is_home else lang_dict.get('cal_away', 'away')

            day_lineup = lineups.get(next_day["id"], {})
            if day_lineup and cal_lineup_published(day_lineup):
                slot = cal_my_slot(day_lineup)
                if slot:
                    pista, partner, _ = slot
                    if partner:
                        status = lang_dict.get('cal_you_play', 'Court {pista} with {partner}').format(pista=pista, partner=partner)
                    else:
                        status = lang_dict.get('cal_you_play_alone', 'Court {pista}').format(pista=pista)
                    status_bg, status_fg = "rgba(46, 204, 113, 0.18)", "#7ee2a8"
                else:
                    status = lang_dict.get('cal_not_called', 'Not in the lineup')
                    status_bg, status_fg = "rgba(255, 255, 255, 0.08)", "#c9d6e8"
            else:
                status = lang_dict.get('cal_lineup_pending', 'Lineup not out yet')
                status_bg, status_fg = "rgba(255, 255, 255, 0.08)", "#c9d6e8"

            card_html = (
                f"<div style='border: 2px solid #4da3ff; border-radius: 12px; padding: 16px 20px; margin-bottom: 18px; background: #1b263b;'>"
                f"<div style='font-size: 13px;'><span style='color:#4da3ff !important;'>{lang_dict.get('cal_next', 'Next match')} · {when}</span></div>"
                f"<div style='font-size: 22px; font-weight: 600; margin: 4px 0 2px 0;'><span>{match_date.strftime('%d %b %Y')} — {next_day['home']} vs {next_day['away']}</span></div>"
                f"<div style='font-size: 14px; margin-bottom: 12px;'><span style='color:#8fa3bf !important;'>{venue.capitalize()}</span></div>"
                f"<div style='background: {status_bg}; border-radius: 8px; padding: 10px 14px; font-size: 15px;'><span style='color:{status_fg} !important;'>{status}</span></div>"
                f"</div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info(lang_dict.get('cal_season_over', 'Season finished.'))

        # --- Calendario completo ---
        rows_html = ""
        for d in SNP_CALENDAR:
            match_date = datetime.strptime(d["iso"], "%Y-%m-%d").date()
            venue = lang_dict.get('cal_home', 'home') if d["home"] == "NAC" else lang_dict.get('cal_away', 'away')
            you_txt, you_color = cal_you_text(lineups.get(d["id"], {}))
            is_next = next_day is not None and d["id"] == next_day["id"]
            is_past = match_date < today
            row_style = "background: rgba(77, 163, 255, 0.15);" if is_next else ("opacity: 0.6;" if is_past else "")
            rows_html += (
                f"<tr style='{row_style}'>"
                f"<td><strong>{match_date.strftime('%d %b')}</strong></td>"
                f"<td>{d['home']} vs {d['away']} <span style='color:#8fa3bf !important;'>· {venue}</span></td>"
                f"<td><span style='color:{you_color} !important;'>{you_txt}</span></td>"
                f"</tr>"
            )
        st.markdown(
            f"<div class='table-container'><table class='custom-table'>"
            f"<thead><tr><th>{lang_dict.get('cal_date', 'Date')}</th><th>{lang_dict.get('cal_match', 'Match')}</th><th>{lang_dict.get('cal_you', 'You')}</th></tr></thead>"
            f"<tbody>{rows_html}</tbody></table></div>",
            unsafe_allow_html=True
        )

        # --- Dettagli per giornata ---
        st.markdown(f"#### {lang_dict.get('cal_details', 'Match details')}")
        for d in SNP_CALENDAR:
            match_date = datetime.strptime(d["iso"], "%Y-%m-%d").date()
            day_lineup = lineups.get(d["id"], {})
            with st.expander(f"{match_date.strftime('%d %b')} — {d['home']} vs {d['away']}", expanded=False):
                if day_lineup and cal_lineup_published(day_lineup):
                    detail_rows = []
                    for pista in range(1, 6):
                        p1 = day_lineup.get(f"pista_{pista}_p1", "") or "—"
                        p2 = day_lineup.get(f"pista_{pista}_p2", "") or "—"
                        res = day_lineup.get(f"pista_{pista}_risultato", "") or "—"
                        if my_name in (p1, p2):
                            p1 = f"<strong>{p1}</strong>" if p1 == my_name else p1
                            p2 = f"<strong>{p2}</strong>" if p2 == my_name else p2
                        detail_rows.append({
                            lang_dict.get('cal_court', 'Court'): f"{lang_dict.get('cal_court', 'Court')} {pista}",
                            lang_dict.get('cal_player1', 'Player 1'): p1,
                            lang_dict.get('cal_player2', 'Player 2'): p2,
                            lang_dict.get('cal_result', 'Result'): res,
                        })
                    df_detail = pd.DataFrame(detail_rows)
                    st.markdown(f"<div class='table-container'>{df_detail.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
                    if day_lineup.get("note"):
                        st.markdown(f"**{lang_dict.get('cal_notes', 'Notes')}:** {day_lineup['note']}")
                else:
                    st.info(lang_dict.get('cal_lineup_pending', 'Lineup not out yet'))


# --- AREA ALLENATORE / ADMIN ---
elif st.session_state.nav_mode == "Coach" and st.session_state.authenticated_coach:
    is_admin = st.session_state.get("authenticated_admin", False)
    col_title, col_btn_roster, col_btn_exit = st.columns([4, 1.8, 1.8])
    with col_title:
        if is_admin:
            st.title("🛡️ Admin Dashboard – Full Access")
        else:
            st.title(f"📋 {lang_dict.get('coach_dash_title', 'Coach Dashboard')}")
    with col_btn_roster:
        st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
        if st.button(lang_dict.get('manage_roster_btn', 'Manage Squad'), use_container_width=True):
            st.session_state.show_roster_modal = not st.session_state.show_roster_modal
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_btn_exit:
        st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
        if st.button(lang_dict.get('exit_coach', 'Exit'), use_container_width=True):
            st.session_state.authenticated_coach = False
            st.session_state.authenticated_admin = False
            st.session_state.show_roster_modal = False
            st.session_state.nav_mode = "Home"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Admin: open any player profile
    if is_admin:
        st.markdown("---")
        st.markdown("### 🛡️ Open Player Profile")
        st.caption("Enter any player's personal card to view and edit their data as admin.")
        admin_player_opts = [f"{p['fname']} {p['lname']} ({p['side']})" for p in squad_players]
        col_ap1, col_ap2 = st.columns([3, 1])
        with col_ap1:
            selected_admin_player = st.selectbox(
                "Select player",
                options=admin_player_opts,
                key="admin_open_player_select",
                label_visibility="collapsed"
            )
        with col_ap2:
            if st.button("🔓 Open Profile", type="primary", use_container_width=True, key="admin_open_player_btn"):
                selected_fname = selected_admin_player.split(" ")[0]
                st.session_state.authenticated_player = selected_fname
                st.session_state.admin_viewing_player = True
                st.session_state.force_password_change = False
                log_activity("Admin opened player profile", selected_admin_player)
                if save_data_to_server():
                    st.session_state.nav_mode = "Player_Dashboard"
                    st.rerun()

        st.markdown("---")
        st.markdown(f"### {lang_dict.get('admin_pwd_mgmt_title', '🔑 Player Password Management')}")
        st.caption(lang_dict.get('admin_pwd_mgmt_desc', "View and edit each player's password. Passwords are stored in plain text: use this feature with caution."))
        with st.expander(lang_dict.get('admin_pwd_mgmt_expander', 'Show / edit all passwords'), expanded=False):
            with st.form("admin_manage_passwords_form"):
                new_pwd_values = {}
                for p in squad_players:
                    col_pw1, col_pw2 = st.columns([2, 2])
                    with col_pw1:
                        st.markdown(f"**{p['fname']} {p['lname']}**")
                    with col_pw2:
                        new_pwd_values[p['fname']] = st.text_input(
                            lang_dict.get('admin_pwd_of', 'Password for {name}').format(name=p['fname']),
                            value=p.get("password", p["fname"]),
                            key=f"admin_pwd_{p['fname']}_{p['lname']}",
                            label_visibility="collapsed"
                        )
                if st.form_submit_button(lang_dict.get('admin_pwd_save_btn', '💾 Save All Passwords'), type="primary"):
                    changed = []
                    for p in squad_players:
                        new_val = new_pwd_values.get(p['fname'], "").strip()
                        if new_val and new_val != p.get("password", p["fname"]):
                            p["password"] = new_val
                            p["first_login_done"] = True
                            changed.append(f"{p['fname']} {p['lname']}")
                    if changed:
                        log_activity("Admin updated player password(s)", ", ".join(changed))
                        if save_data_to_server():
                            st.success(lang_dict.get('admin_pwd_updated', '✅ Passwords updated for: {names}').format(names=', '.join(changed)))
                            st.rerun()
                    else:
                        st.info(lang_dict.get('no_changes_to_save', 'No changes to save.'))

    if st.session_state.show_roster_modal:
        st.markdown("---")
        st.markdown(f"### {lang_dict.get('roster_modal_title', '👥 Squad Management Panel (Add or Remove)')}")
        with st.container():
            col_add_m, col_del_m = st.columns(2)

            with col_add_m:
                st.markdown(f"#### {lang_dict.get('roster_add_title', 'Add New Player')}")
                with st.form("modal_add_player_form"):
                    new_fname = st.text_input(lang_dict.get('roster_fname_lbl', 'First Name'))
                    new_lname = st.text_input(lang_dict.get('roster_lname_lbl', 'Last Name'))
                    new_side = st.selectbox(lang_dict.get('roster_role_lbl', 'Position / Role'), ["Left", "Right"])
                    new_hand = st.selectbox(lang_dict.get('roster_hand_lbl', 'Hand'), ["Destro", "Mancino"])
                    new_style = st.selectbox(lang_dict.get('roster_style_lbl', 'Play Style'), ["Offensive", "Defensive", "Equilibrated", "Counterattack"])

                    if st.form_submit_button(lang_dict.get('roster_add_btn', '➕ Add Player'), type="primary"):
                        if new_fname.strip() and new_lname.strip():
                            exists = any(p['fname'].lower() == new_fname.strip().lower() and p['lname'].lower() == new_lname.strip().lower() for p in st.session_state.squad_data)
                            if exists:
                                st.error(lang_dict.get('roster_dup_error', 'A player with this first and last name already exists in the squad!'))
                            else:
                                st.session_state.squad_data.append({
                                    "fname": new_fname.strip(),
                                    "lname": new_lname.strip(),
                                    "side": new_side,
                                    "hand": new_hand,
                                    "trainings": 1,
                                    "participated": 1,
                                    "tech": [7] * len(TECH_SKILLS),
                                    "mental": [7] * len(MENTAL_SKILLS),
                                    "c_tech": [6] * len(TECH_SKILLS),
                                    "c_mental": [6] * len(MENTAL_SKILLS),
                                    "play_style": new_style,
                                    "player_play_style": new_style,
                                    "history": [],
                                    "coach_note": "",
                                    "partners": {},
                                    "comments": [],
                                    "password": new_fname.strip(),
                                    "first_login_done": False
                                })
                                log_activity("Player added", f"{new_fname.strip()} {new_lname.strip()} ({new_side})")
                                if save_data_to_server():
                                    st.success(lang_dict.get('roster_add_success', 'Player {name} added successfully!').format(name=f"{new_fname} {new_lname}"))
                                    st.rerun()
                        else:
                            st.warning(lang_dict.get('roster_name_required', "First and last name can't be empty."))

            with col_del_m:
                st.markdown(f"#### {lang_dict.get('roster_delete_title', 'Remove Existing Player')}")
                with st.form("modal_delete_player_form"):
                    player_to_delete = st.selectbox(lang_dict.get('roster_select_remove', 'Select player to remove'), [f"{p['fname']} {p['lname']}" for p in st.session_state.squad_data])

                    if st.form_submit_button(lang_dict.get('roster_remove_btn', '🗑️ Remove Player'), type="secondary"):
                        st.session_state.squad_data = [p for p in st.session_state.squad_data if f"{p['fname']} {p['lname']}" != player_to_delete]
                        log_activity("Player removed", player_to_delete)
                        if save_data_to_server():
                            st.success(lang_dict.get('roster_remove_success', 'Player {name} removed successfully!').format(name=player_to_delete))
                            st.rerun()
        st.markdown("---")
        
    if is_admin:
        coach_tab1, coach_tab_evals, coach_tab_stats, coach_tab_training, coach_tab3, coach_tab_pairing, coach_tab2, coach_tab_log = st.tabs([
            f"👥 {lang_dict.get('coach_tab_squad', 'Squad')}", 
            f"✏️ {lang_dict.get('coach_tab_evals', 'Grades')}",
            f"📊 Players Stats",
            f"🎾 {lang_dict.get('coach_tab_training', 'Training')}",
            f"💬 {lang_dict.get('coach_tab_comments', 'Comments')}",
            f"🤖 {lang_dict.get('coach_tab_pairing', 'Pairing')}",
            f"📅 {lang_dict.get('coach_tab_matches', 'Matches')}",
            "📋 Activity Log"
        ])
    else:
        coach_tab1, coach_tab_evals, coach_tab_stats, coach_tab_training, coach_tab3, coach_tab_pairing, coach_tab2 = st.tabs([
            f"👥 {lang_dict.get('coach_tab_squad', 'Squad')}", 
            f"✏️ {lang_dict.get('coach_tab_evals', 'Grades')}",
            f"📊 Players Stats",
            f"🎾 {lang_dict.get('coach_tab_training', 'Training')}",
            f"💬 {lang_dict.get('coach_tab_comments', 'Comments')}",
            f"🤖 {lang_dict.get('coach_tab_pairing', 'Pairing')}",
            f"📅 {lang_dict.get('coach_tab_matches', 'Matches')}"
        ])
        coach_tab_log = None
    
    with coach_tab1:
        st.subheader(f"👥 {lang_dict.get('coach_tab_squad', 'Squad Management & Attendance')}")
        st.markdown(lang_dict.get('total_players_present', 'Total players present: **{n}**').format(n=len(squad_players)))
        st.markdown(lang_dict.get('squad_desc', ''))
        
        st.session_state.squad_data = sorted(st.session_state.squad_data, key=lambda x: x['fname'])
        squad_players = st.session_state.squad_data
        
        total_scheduled_trainings = len(st.session_state.planned_trainings)
        
        th_cols = st.columns([1.8, 1.2, 1.2, 1.4, 0.9, 0.9, 0.9])
        with th_cols[0]: st.markdown(lang_dict.get('col_name', 'Name'))
        with th_cols[1]: st.markdown(lang_dict.get('col_role', 'Role'))
        with th_cols[2]: st.markdown(lang_dict.get('col_hand', 'Hand'))
        with th_cols[3]: st.markdown(lang_dict.get('col_style', 'Style'))
        with th_cols[4]: st.markdown(lang_dict.get('col_trainings', 'Trainings'))
        with th_cols[5]: st.markdown(lang_dict.get('col_participated', 'Participated'))
        with th_cols[6]: st.markdown(f"<div style='text-align: center;'>{lang_dict.get('col_commitment', 'Commitment (%)')}</div>", unsafe_allow_html=True)
        st.markdown("---")

        with st.form("squad_update_form"):
            for idx, p in enumerate(squad_players):
                col_n, col_r, col_h, col_s, col_t, col_p, col_c = st.columns([1.8, 1.2, 1.2, 1.4, 0.9, 0.9, 0.9])
                
                player_first_name = p['fname']
                participated_count = 0
                for session in st.session_state.planned_trainings:
                    attendees_str = session.get("Partecipanti", "")
                    if player_first_name in attendees_str:
                        participated_count += 1
                
                if total_scheduled_trainings > 0:
                    calc_trainings = total_scheduled_trainings
                    calc_participated = participated_count
                else:
                    calc_trainings = int(p.get("trainings", 1))
                    calc_participated = int(p.get("participated", 1))

                with col_n:
                    st.markdown(f"**{p['fname']} {p['lname']}**")
                with col_r:
                    new_side = st.selectbox("Role", ["Left", "Right"], index=0 if p["side"]=="Left" else 1, key=f"side_{idx}", label_visibility="collapsed")
                with col_h:
                    new_hand = st.selectbox("Mano", ["Destro", "Mancino"], index=0 if p.get("hand","Destro")=="Destro" else 1, key=f"hand_{idx}", label_visibility="collapsed")
                with col_s:
                    styles_list = ["Offensive", "Defensive", "Equilibrated", "Counterattack"]
                    curr_st = p.get("play_style", "Equilibrated")
                    idx_st = styles_list.index(curr_st) if curr_st in styles_list else 2
                    new_st = st.selectbox("Style", styles_list, index=idx_st, key=f"style_{idx}", label_visibility="collapsed")
                with col_t:
                    st.markdown(f"<div style='padding-top: 8px; text-align: center; font-weight: bold;'>{calc_trainings}</div>", unsafe_allow_html=True)
                with col_p:
                    st.markdown(f"<div style='padding-top: 8px; text-align: center; font-weight: bold;'>{calc_participated}</div>", unsafe_allow_html=True)
                with col_c:
                    pct_calc = int(round((calc_participated / calc_trainings) * 100)) if calc_trainings > 0 else 0
                    st.markdown(f"<div style='padding-top: 8px; font-weight: bold; text-align: center; color: {'#2ecc71' if pct_calc >= 70 else '#e74c3c'};'>{pct_calc}%</div>", unsafe_allow_html=True)
                
                p["side"] = new_side
                p["hand"] = new_hand
                p["play_style"] = new_st
                p["trainings"] = calc_trainings
                p["participated"] = calc_participated

            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button(lang_dict.get('squad_save_btn', '💾 Save Squad and Role Changes'), type="primary"):
                log_activity("Squad roles/styles updated", f"{len(squad_players)} players")
                if save_data_to_server():
                    st.success(lang_dict.get('squad_save_success', 'All changes to the squad, roles and dominant hand have been saved permanently!'))
                    st.rerun()

        st.markdown("---")
        st.subheader(f"🎯 {lang_dict.get('work_groups', 'Work Groups')}")
        st.markdown(lang_dict.get('work_groups_desc', ''))
        
        skill_groups = {skill: [] for skill in ALL_SKILLS}
        for p in squad_players:
            p_coach_vals = p['c_tech'] + p['c_mental']
            for i, skill in enumerate(ALL_SKILLS):
                if p_coach_vals[i] <= 6:
                    skill_groups[skill].append(f"{p['fname']} {p['lname']} ({lang_dict.get('grade_label', 'Grade: {val}').format(val=p_coach_vals[i])})")
                    
        active_groups = {k: v for k, v in skill_groups.items() if len(v) > 0}
        
        if active_groups:
            cols = st.columns(2)
            col_idx = 0
            for skill, members in active_groups.items():
                with cols[col_idx % 2]:
                    with st.expander(lang_dict.get('improvement_area', '📌 Improvement area: **{skill}** ({n} players)').format(skill=skill, n=len(members))):
                        for m in members:
                            st.markdown(f"- {m}")
                col_idx += 1
        else:
            st.info(lang_dict.get('no_critics', 'No criticalities.'))

    with coach_tab_evals:
        st.subheader(f"✏️ {lang_dict.get('coach_eval_title', 'Coach Grades')}")
        st.markdown(lang_dict.get('coach_eval_desc', ''))
        
        selected_player_name = st.selectbox(lang_dict.get('select_player_eval', 'Select player:'), [f"{p['fname']} {p['lname']}" for p in squad_players], key="coach_eval_select")
        p_obj = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_player_name), None)

        if p_obj:
            st.markdown(f"### {lang_dict.get('partner_prefs_title', '🏆 Partner Preferences of **{name}**').format(name=selected_player_name)}")
            st.caption(lang_dict.get('partner_prefs_desc', 'Ranking of the partners the player prefers to play with (set by them in their own area), and who among the others has ranked them as a preferred partner. Useful to understand affinities before grading.'))
            col_pref1, col_pref2 = st.columns(2)

            with col_pref1:
                st.markdown(lang_dict.get('partner_prefs_own', '**{name}** prefers to play with:').format(name=selected_player_name))
                own_partners = p_obj.get("partners", {})
                if own_partners:
                    sorted_own = sorted(own_partners.items(), key=lambda x: x[1], reverse=True)
                    df_own_partners = pd.DataFrame(sorted_own, columns=[lang_dict.get('col_partner', 'Partner'), lang_dict.get('col_score', 'Score')])
                    st.markdown(f"<div class='table-container'>{df_own_partners.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
                else:
                    st.info(lang_dict.get('partner_prefs_none', "This player hasn't set any preferences."))

            with col_pref2:
                st.markdown(lang_dict.get('partner_prefs_reverse_title', 'Who has ranked **{name}** as a preferred partner:').format(name=selected_player_name))
                reverse_prefs = []
                for other in squad_players:
                    if other['fname'] == p_obj['fname'] and other['lname'] == p_obj['lname']:
                        continue
                    score = other.get("partners", {}).get(selected_player_name)
                    if score is not None:
                        reverse_prefs.append((f"{other['fname']} {other['lname']}", score))
                if reverse_prefs:
                    reverse_prefs.sort(key=lambda x: x[1], reverse=True)
                    df_reverse_prefs = pd.DataFrame(reverse_prefs, columns=[lang_dict.get('col_player', 'Player'), lang_dict.get('col_score', 'Score')])
                    st.markdown(f"<div class='table-container'>{df_reverse_prefs.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
                else:
                    st.info(lang_dict.get('partner_prefs_reverse_none', 'No other player has ranked them as a preferred partner.'))

            st.markdown("---")

            with st.form("coach_eval_form"):
                style_options = ["Offensive", "Defensive", "Equilibrated", "Counterattack"]
                current_style = p_obj.get("play_style", "Equilibrated")
                if current_style not in style_options:
                    current_style = "Equilibrated"
                
                st.markdown(f"### {lang_dict.get('coach_eval_sub_title', 'Coach Evaluation')}")
                selected_style = st.selectbox(
                    lang_dict.get('play_style_lbl', 'Play Style:'),
                    options=style_options,
                    index=style_options.index(current_style)
                )
                
                st.markdown("---")
                st.markdown(f"📝 **{lang_dict.get('coach_note_lbl', 'Coach Note')}**")
                new_coach_note = st.text_area(lang_dict.get('coach_note_placeholder', 'Write note...'), value=p_obj.get("coach_note", ""), key="coach_note_input")
                
                st.markdown("---")
                col_c_left, col_c_right = st.columns(2)
                
                c_tech_new = []
                c_mental_new = []
                
                with col_c_left:
                    st.markdown(f"🎾 *{lang_dict.get('tech_skills_coach', 'Technical Skills')}*")
                    for idx, t_label in enumerate(TECH_SKILLS):
                        val = st.slider(f"Coach - {t_label}", 1, 10, int(p_obj['c_tech'][idx]), key=f"scoach_tech_{idx}")
                        c_tech_new.append(val)
                
                with col_c_right:
                    st.markdown(f"🧠 *{lang_dict.get('mental_skills_coach', 'Mental Skills')}*")
                    for idx, m_label in enumerate(MENTAL_SKILLS):
                        val = st.slider(f"Coach - {m_label}", 1, 10, int(p_obj['c_mental'][idx]), key=f"scoach_mental_{idx}")
                        c_mental_new.append(val)
                        
                if st.form_submit_button(lang_dict.get('save_coach_eval', 'Save Grades'), type="primary"):
                    p_obj.setdefault("history", []).append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "values": c_tech_new + c_mental_new
                    })
                    p_obj['c_tech'] = c_tech_new
                    p_obj['c_mental'] = c_mental_new
                    p_obj['play_style'] = selected_style
                    p_obj['coach_note'] = new_coach_note
                    log_activity("Coach grades updated", f"{selected_player_name} – style: {selected_style}")
                    if save_data_to_server():
                        st.success(f"✅ {selected_player_name} updated and saved successfully!")

    with coach_tab_stats:
        st.subheader("📊 Players Stats – Self-Evaluation vs Coach Evaluation")
        st.markdown("Overview of every player's self-evaluation (left) and **editable** coach evaluation (right), with radar charts.")
        
        all_skills_labels = TECH_SKILLS + MENTAL_SKILLS
        style_options = ["Offensive", "Defensive", "Equilibrated", "Counterattack"]
        
        for p in squad_players:
            player_name = f"{p['fname']} {p['lname']}"
            player_style = p.get("player_play_style", "Equilibrated")
            coach_style = p.get("play_style", "Equilibrated")
            if coach_style not in style_options:
                coach_style = "Equilibrated"
            
            with st.expander(f"👤 **{player_name}**  |  Side: {p['side']}  |  Self style: {player_style}  |  Coach style: {coach_style}", expanded=False):
                
                player_full = list(p.get("tech", [7]*len(TECH_SKILLS))) + list(p.get("mental", [7]*len(MENTAL_SKILLS)))
                coach_full = list(p.get("c_tech", [6]*len(TECH_SKILLS))) + list(p.get("c_mental", [6]*len(MENTAL_SKILLS)))
                
                while len(player_full) < len(all_skills_labels):
                    player_full.append(7)
                while len(coach_full) < len(all_skills_labels):
                    coach_full.append(6)
                player_full = player_full[:len(all_skills_labels)]
                coach_full = coach_full[:len(all_skills_labels)]
                
                categories = all_skills_labels + [all_skills_labels[0]]
                p_vals_radar = player_full + [player_full[0]]
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("#### 🟦 Player Self-Evaluation *(read-only)*")
                    st.markdown(f"**Play Style:** {player_style}")
                    
                    rows_p = [{"Skill": skill, "Value": player_full[i]} for i, skill in enumerate(all_skills_labels)]
                    df_p = pd.DataFrame(rows_p)
                    st.markdown(f"<div class='table-container'>{df_p.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
                    
                    fig_p = go.Figure()
                    fig_p.add_trace(go.Scatterpolar(
                        r=p_vals_radar,
                        theta=categories,
                        fill='toself',
                        name='Self-Evaluation',
                        line_color='#3b82f6'
                    ))
                    fig_p.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        polar=dict(
                            bgcolor='rgba(0,0,0,0)',
                            radialaxis=dict(visible=True, range=[0, 10], color='white', gridcolor='#334155'),
                            angularaxis=dict(gridcolor='#334155')
                        ),
                        showlegend=False,
                        height=380,
                        margin=dict(l=30, r=30, t=20, b=20)
                    )
                    st.plotly_chart(fig_p, use_container_width=True, key=f"radar_player_{p['fname']}_{p['lname']}")
                
                with col_right:
                    st.markdown("#### 🟧 Coach Evaluation *(editable)*")
                    
                    with st.form(key=f"coach_edit_form_{p['fname']}_{p['lname']}"):
                        new_coach_style = st.selectbox(
                            "Coach Play Style",
                            options=style_options,
                            index=style_options.index(coach_style),
                            key=f"stats_style_{p['fname']}_{p['lname']}"
                        )
                        
                        st.markdown("**Technical Skills**")
                        new_c_tech = []
                        for i, skill in enumerate(TECH_SKILLS):
                            val = st.slider(
                                f"Coach – {skill}",
                                1, 10,
                                int(coach_full[i]),
                                key=f"stats_ctech_{p['fname']}_{p['lname']}_{i}"
                            )
                            new_c_tech.append(val)
                        
                        st.markdown("**Mental Skills**")
                        new_c_mental = []
                        for i, skill in enumerate(MENTAL_SKILLS):
                            val = st.slider(
                                f"Coach – {skill}",
                                1, 10,
                                int(coach_full[len(TECH_SKILLS) + i]),
                                key=f"stats_cmental_{p['fname']}_{p['lname']}_{i}"
                            )
                            new_c_mental.append(val)
                        
                        saved = st.form_submit_button("💾 Save Coach Evaluation", type="primary")
                        
                        if saved:
                            p.setdefault("history", []).append({
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "values": new_c_tech + new_c_mental
                            })
                            p["c_tech"] = new_c_tech
                            p["c_mental"] = new_c_mental
                            p["play_style"] = new_coach_style
                            log_activity("Coach evaluation saved (Players Stats)", f"{player_name} – style: {new_coach_style}")
                            if save_data_to_server():
                                st.success(f"✅ Coach evaluation for **{player_name}** saved!")
                                st.rerun()
                    
                    # Radar with current (possibly just-saved) values
                    current_coach = list(p.get("c_tech", [6]*len(TECH_SKILLS))) + list(p.get("c_mental", [6]*len(MENTAL_SKILLS)))
                    while len(current_coach) < len(all_skills_labels):
                        current_coach.append(6)
                    current_coach = current_coach[:len(all_skills_labels)]
                    c_vals_radar = current_coach + [current_coach[0]]
                    
                    fig_c = go.Figure()
                    fig_c.add_trace(go.Scatterpolar(
                        r=c_vals_radar,
                        theta=categories,
                        fill='toself',
                        name='Coach Evaluation',
                        line_color='#f97316'
                    ))
                    fig_c.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        polar=dict(
                            bgcolor='rgba(0,0,0,0)',
                            radialaxis=dict(visible=True, range=[0, 10], color='white', gridcolor='#334155'),
                            angularaxis=dict(gridcolor='#334155')
                        ),
                        showlegend=False,
                        height=380,
                        margin=dict(l=30, r=30, t=20, b=20)
                    )
                    st.plotly_chart(fig_c, use_container_width=True, key=f"radar_coach_{p['fname']}_{p['lname']}")
                
                # Difference summary (using latest coach values)
                current_coach = list(p.get("c_tech", [6]*len(TECH_SKILLS))) + list(p.get("c_mental", [6]*len(MENTAL_SKILLS)))
                while len(current_coach) < len(all_skills_labels):
                    current_coach.append(6)
                current_coach = current_coach[:len(all_skills_labels)]
                
                st.markdown("---")
                st.markdown("##### 📉 Differences (Self − Coach)")
                diff_rows = []
                for i, skill in enumerate(all_skills_labels):
                    diff = player_full[i] - current_coach[i]
                    if diff > 0:
                        diff_display = f"<span style='color:#2ecc71; font-weight:bold;'>+{diff}</span>"
                    elif diff < 0:
                        diff_display = f"<span style='color:#e74c3c; font-weight:bold;'>{diff}</span>"
                    else:
                        diff_display = "<span style='color:#bdc3c7;'>0</span>"
                    diff_rows.append({
                        "Skill": skill,
                        "Self": player_full[i],
                        "Coach": current_coach[i],
                        "Diff": diff_display
                    })
                df_diff = pd.DataFrame(diff_rows)
                st.markdown(f"<div class='table-container'>{df_diff.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)

    with coach_tab_training:
        st.subheader(f"🎾 {lang_dict.get('training_title', 'Training Planning & Focus')}")
        st.markdown(lang_dict.get('training_desc', ''))
        
        all_player_names = [f"{p['fname']} {p['lname']}" for p in squad_players]
        selected_attendees_names = st.multiselect(
            lang_dict.get('select_attendees', 'Select attendees:'),
            options=all_player_names,
            default=all_player_names,
            key="captain_attendees_select"
        )
        
        if selected_attendees_names:
            attending_players = [p for p in squad_players if f"{p['fname']} {p['lname']}" in selected_attendees_names]
            
            skill_averages = {}
            for idx, skill in enumerate(ALL_SKILLS):
                vals = []
                for p in attending_players:
                    p_vals = p['c_tech'] + p['c_mental']
                    vals.append(p_vals[idx])
                skill_averages[skill] = sum(vals) / len(vals) if vals else 0.0
                
            sorted_skills = sorted(skill_averages.items(), key=lambda x: x[1])
            top_priorities_system = [s[0] for s in sorted_skills[:3]]
            
            st.markdown("---")
            st.markdown(f"### {lang_dict.get('training_priorities', 'System Recommended Priority Areas')}")
            st.markdown(lang_dict.get('training_system_intro', 'The system has analyzed the grades of the group present and suggests the following 3 priorities:'))

            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                if len(sorted_skills) > 0:
                    st.metric(label=lang_dict.get('training_priority_1_label', '🔥 1st Recommended Priority'), value=sorted_skills[0][0], delta=lang_dict.get('training_avg_label', 'Average: {val}/10').format(val=round(sorted_skills[0][1], 1)), delta_color="inverse")
            with col_p2:
                if len(sorted_skills) > 1:
                    st.metric(label=lang_dict.get('training_priority_2_label', '⚡ 2nd Recommended Priority'), value=sorted_skills[1][0], delta=lang_dict.get('training_avg_label', 'Average: {val}/10').format(val=round(sorted_skills[1][1], 1)), delta_color="inverse")
            with col_p3:
                if len(sorted_skills) > 2:
                    st.metric(label=lang_dict.get('training_priority_3_label', '💡 3rd Recommended Priority'), value=sorted_skills[2][0], delta=lang_dict.get('training_avg_label', 'Average: {val}/10').format(val=round(sorted_skills[2][1], 1)), delta_color="inverse")

            st.markdown("---")
            st.markdown(f"### {lang_dict.get('training_custom_title', '✏️ Coach Customization and Confirmation')}")
            st.markdown(lang_dict.get('training_custom_desc', 'The coach can change the priorities from the dropdown menu and choose which date to save the training in the calendar:'))

            with st.form("coach_training_confirmation_form"):
                col_m1, col_m2, col_m3 = st.columns(3)

                default_p1_idx = ALL_SKILLS.index(top_priorities_system[0]) if top_priorities_system[0] in ALL_SKILLS else 0
                default_p2_idx = ALL_SKILLS.index(top_priorities_system[1]) if len(top_priorities_system) > 1 and top_priorities_system[1] in ALL_SKILLS else 1
                default_p3_idx = ALL_SKILLS.index(top_priorities_system[2]) if len(top_priorities_system) > 2 and top_priorities_system[2] in ALL_SKILLS else 2

                with col_m1:
                    coach_choice_p1 = st.selectbox(lang_dict.get('training_coach_p1_label', '1st Priority (Coach)'), options=ALL_SKILLS, index=default_p1_idx)
                with col_m2:
                    coach_choice_p2 = st.selectbox(lang_dict.get('training_coach_p2_label', '2nd Priority (Coach)'), options=ALL_SKILLS, index=default_p2_idx)
                with col_m3:
                    coach_choice_p3 = st.selectbox(lang_dict.get('training_coach_p3_label', '3rd Priority (Coach)'), options=ALL_SKILLS, index=default_p3_idx)

                st.markdown("<br>", unsafe_allow_html=True)
                training_date = st.date_input(lang_dict.get('training_date_question', '📅 On which date do you want to save this training?'), datetime.now() + timedelta(days=2))

                submit_training = st.form_submit_button(lang_dict.get('training_confirm_btn', '✅ Confirm and Save to Calendar'), type="primary")

                if submit_training:
                    st.session_state.planned_trainings.append({
                        "Data": str(training_date),
                        "Partecipanti": ", ".join([p.split(" ")[0] for p in selected_attendees_names]),
                        "1° Priorità": coach_choice_p1,
                        "2° Priorità": coach_choice_p2,
                        "3° Priorità": coach_choice_p3
                    })
                    log_activity("Training planned", f"{training_date} – {coach_choice_p1}, {coach_choice_p2}, {coach_choice_p3}")
                    if save_data_to_server():
                        st.success(lang_dict.get('training_saved_success', '🎉 Training saved successfully for {date}!').format(date=training_date))
                        st.rerun()

            st.markdown("---")
            st.markdown(f"### {lang_dict.get('groups_split_title', '👥 Split into Groups of 4 (based on weakness)')}")
            st.markdown(lang_dict.get('groups_split_desc', "The selected players are grouped into **groups of 4** based on their **main weakness**, so each group can work on a specific and targeted goal instead of a single priority for everyone."))

            def _player_weakest_skill(p):
                p_vals = p['c_tech'] + p['c_mental']
                min_idx = min(range(len(p_vals)), key=lambda i: p_vals[i])
                return ALL_SKILLS[min_idx], p_vals[min_idx]

            def _group_skill_averages(group_players):
                averages = {}
                for idx, skill in enumerate(ALL_SKILLS):
                    vals = [(gp['c_tech'] + gp['c_mental'])[idx] for gp in group_players]
                    averages[skill] = sum(vals) / len(vals) if vals else 0.0
                return averages

            players_with_weakness = []
            for p in attending_players:
                skill_name, skill_val = _player_weakest_skill(p)
                players_with_weakness.append({"player": p, "weak_skill": skill_name, "weak_val": skill_val})

            # Raggruppa vicino chi condivide la stessa debolezza principale, poi divide in blocchi da 4
            players_with_weakness.sort(key=lambda x: (x["weak_skill"], x["weak_val"]))

            GROUP_SIZE = 4
            training_groups = [
                players_with_weakness[i:i + GROUP_SIZE]
                for i in range(0, len(players_with_weakness), GROUP_SIZE)
            ]

            if len(attending_players) < GROUP_SIZE:
                st.info(lang_dict.get('groups_min_players_warning', 'At least {n} available players are needed to form a group. There are currently {count}.').format(n=GROUP_SIZE, count=len(attending_players)))
            else:
                with st.form("group_training_form"):
                    group_focus_selections = []

                    for gi, group in enumerate(training_groups):
                        group_players = [g["player"] for g in group]
                        names = ", ".join(f"{gp['fname']} {gp['lname']}" for gp in group_players)
                        is_partial = len(group_players) < GROUP_SIZE

                        group_avgs = _group_skill_averages(group_players)
                        sorted_group_skills = sorted(group_avgs.items(), key=lambda x: x[1])
                        top_skill, top_val = sorted_group_skills[0]

                        title_suffix = lang_dict.get('group_incomplete_suffix', ' (incomplete group)') if is_partial else ""
                        st.markdown(f"**{lang_dict.get('group_label_prefix', 'Group {n}').format(n=gi + 1)}{title_suffix}** — {names}")

                        col_g1, col_g2 = st.columns([1, 1.6])
                        with col_g1:
                            st.metric(label=lang_dict.get('group_weak_metric_label', '🎯 Main weakness'), value=top_skill, delta=lang_dict.get('training_avg_label', 'Average: {val}/10').format(val=round(top_val, 1)), delta_color="inverse")
                        with col_g2:
                            default_idx = ALL_SKILLS.index(top_skill) if top_skill in ALL_SKILLS else 0
                            chosen_focus = st.selectbox(
                                lang_dict.get('group_focus_label', 'Training focus — Group {n}').format(n=gi + 1),
                                options=ALL_SKILLS,
                                index=default_idx,
                                key=f"group_focus_{gi}"
                            )
                        group_focus_selections.append((group_players, chosen_focus))
                        st.markdown("---")

                    group_training_date = st.date_input(
                        lang_dict.get('group_date_question', '📅 On which date do you want to save these group trainings?'),
                        datetime.now() + timedelta(days=2),
                        key="group_training_date"
                    )

                    submit_groups = st.form_submit_button(lang_dict.get('group_save_btn', '✅ Save Group Trainings'), type="primary")

                    if submit_groups:
                        for gi, (group_players, chosen_focus) in enumerate(group_focus_selections):
                            st.session_state.planned_trainings.append({
                                "Data": str(group_training_date),
                                "Partecipanti": ", ".join(gp['fname'] for gp in group_players),
                                "1° Priorità": chosen_focus,
                                "2° Priorità": "-",
                                "3° Priorità": "-",
                                "Gruppo": f"Gruppo {gi + 1}"
                            })
                        log_activity("Group trainings planned", f"{group_training_date} – {len(group_focus_selections)} gruppi")
                        if save_data_to_server():
                            st.success(lang_dict.get('group_saved_success', '🎉 {n} group trainings saved for {date}!').format(n=len(group_focus_selections), date=group_training_date))
                            st.rerun()

            st.markdown("---")
            st.markdown(f"### {lang_dict.get('training_history_title', '📅 Planned Trainings Calendar History')}")
            if st.session_state.planned_trainings:
                df_planned = pd.DataFrame(st.session_state.planned_trainings).sort_values(by="Data").reset_index(drop=True)
                st.markdown(f"<div class='table-container'>{df_planned.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)

                st.markdown(f"#### {lang_dict.get('training_edit_title', '✏️ Edit Training')}")
                training_options_edit = [f"{t['Data']} - {t['1° Priorità']} ({t['Partecipanti'][:25]}...)" for t in st.session_state.planned_trainings]
                selected_training_to_edit_label = st.selectbox(
                    lang_dict.get('training_select_edit', 'Select training to edit'),
                    training_options_edit,
                    key="edit_training_select"
                )
                edit_index = training_options_edit.index(selected_training_to_edit_label)
                training_to_edit = st.session_state.planned_trainings[edit_index]

                with st.form("edit_training_form"):
                    try:
                        default_edit_date = datetime.strptime(training_to_edit["Data"], "%Y-%m-%d").date()
                    except (ValueError, TypeError):
                        default_edit_date = datetime.now().date()
                    edit_date = st.date_input(lang_dict.get('training_edit_date_label', '📅 Training date'), default_edit_date, key="edit_training_date")

                    all_player_names_edit = [f"{p['fname']} {p['lname']}" for p in squad_players]
                    current_participant_fnames = [x.strip() for x in training_to_edit.get("Partecipanti", "").split(",") if x.strip()]
                    default_selected_full = [name for name in all_player_names_edit if name.split(" ")[0] in current_participant_fnames]
                    edit_attendees = st.multiselect(
                        lang_dict.get('training_participants_label', 'Participants'),
                        options=all_player_names_edit,
                        default=default_selected_full,
                        key="edit_training_attendees"
                    )

                    edit_p1_default = training_to_edit.get("1° Priorità")
                    edit_p2_default = training_to_edit.get("2° Priorità")
                    edit_p3_default = training_to_edit.get("3° Priorità")
                    edit_p1 = st.selectbox(lang_dict.get('priority1_label', '1st Priority'), options=ALL_SKILLS, index=ALL_SKILLS.index(edit_p1_default) if edit_p1_default in ALL_SKILLS else 0, key="edit_training_p1")
                    edit_p2 = st.selectbox(lang_dict.get('priority2_label', '2nd Priority'), options=ALL_SKILLS, index=ALL_SKILLS.index(edit_p2_default) if edit_p2_default in ALL_SKILLS else 1, key="edit_training_p2")
                    edit_p3 = st.selectbox(lang_dict.get('priority3_label', '3rd Priority'), options=ALL_SKILLS, index=ALL_SKILLS.index(edit_p3_default) if edit_p3_default in ALL_SKILLS else 2, key="edit_training_p3")

                    if st.form_submit_button(lang_dict.get('training_edit_save_btn', '💾 Save Training Changes'), type="primary"):
                        if not edit_attendees:
                            st.warning(lang_dict.get('training_select_participant_warning', 'Select at least one participant.'))
                        else:
                            st.session_state.planned_trainings[edit_index] = {
                                "Data": str(edit_date),
                                "Partecipanti": ", ".join([p.split(" ")[0] for p in edit_attendees]),
                                "1° Priorità": edit_p1,
                                "2° Priorità": edit_p2,
                                "3° Priorità": edit_p3
                            }
                            log_activity("Training edited", f"{edit_date} – {edit_p1}, {edit_p2}, {edit_p3}")
                            if save_data_to_server():
                                st.success(lang_dict.get('training_edit_success', 'Training edited successfully!'))
                                st.rerun()

                st.markdown(f"#### {lang_dict.get('training_delete_title', '🗑️ Delete Training from Calendar')}")
                with st.form("delete_training_form"):
                    training_options = [f"{t['Data']} - {t['1° Priorità']} ({t['Partecipanti'][:25]}...)" for t in st.session_state.planned_trainings]
                    selected_training_to_delete = st.selectbox(lang_dict.get('training_select_delete', 'Select training to remove'), training_options, key="delete_training_select")

                    if st.form_submit_button(lang_dict.get('training_delete_btn', '🗑️ Delete Selected Training'), type="secondary"):
                        selected_index = training_options.index(selected_training_to_delete)
                        removed_training = st.session_state.planned_trainings.pop(selected_index)
                        if save_data_to_server():
                            st.success(lang_dict.get('training_delete_success', 'Training on {date} removed successfully from the calendar!').format(date=removed_training['Data']))
                            st.rerun()
            else:
                st.info(lang_dict.get('training_none_saved', 'No training confirmed and saved to the calendar yet.'))
            
        else:
            st.info(lang_dict.get('training_no_attendees', 'Select at least one player.'))

    with coach_tab2:
        st.subheader(lang_dict.get('snp_title', '📅 Calendar & SNP Match Registration'))
        st.markdown(lang_dict.get('snp_desc', 'Management of the **7 SNP matchdays**. For each fixture, assign the NAC players and the **result of each court**.'))

        all_players_list = [f"{p['fname']} {p['lname']}" for p in squad_players]


        # Inizializza storage delle formazioni SNP se non esiste
        if "snp_lineups" not in st.session_state:
            st.session_state.snp_lineups = {}
        st.session_state.snp_lineups = normalize_snp_lineups(st.session_state.snp_lineups)

        # Selettore giornata
        day_labels = [d["label"] for d in SNP_CALENDAR]
        selected_label = st.selectbox(lang_dict.get('snp_select_day', '📆 Select the SNP matchday'), day_labels)
        selected_day = next(d for d in SNP_CALENDAR if d["label"] == selected_label)
        day_id = selected_day["id"]

        st.markdown(f"### {selected_day['label']}")

        # Carica lineup esistente se presente
        existing = st.session_state.snp_lineups.get(day_id, {})

        def _sync_snp_match_results(day_id, selected_day, lineup_data):
            """Ricostruisce le righe di match_results per questa giornata SNP a partire dal lineup corrente."""
            st.session_state.match_results = [
                m for m in st.session_state.match_results
                if not (m.get("Tipo") == "SNP" and m.get("Giornata_ID") == day_id)
            ]
            for pista in range(1, 6):
                p1 = lineup_data.get(f"pista_{pista}_p1", "")
                p2 = lineup_data.get(f"pista_{pista}_p2", "")
                res = lineup_data.get(f"pista_{pista}_risultato", "")
                if p1 or p2 or res:
                    st.session_state.match_results.append({
                        "Data": selected_day["date"],
                        "Tipo": "SNP",
                        "Giornata_ID": day_id,
                        "Incontro": selected_day["label"],
                        "Casa": selected_day["home"],
                        "Trasferta": selected_day["away"],
                        "Pista": f"Pista {pista}",
                        "Giocatori_NAC": f"{p1} / {p2}" if p1 and p2 else (p1 or p2 or "—"),
                        "Risultato_Pista": res or "—"
                    })

        # --- STEP 1: Formazione — assegna i giocatori alle piste ---
        st.markdown(f"#### {lang_dict.get('snp_formation_title', '1️⃣ Lineup')}")
        st.caption(lang_dict.get('snp_formation_desc', 'Choose 2 NAC players for each court. You can enter the result later, once the match has been played.'))

        with st.form(f"snp_lineup_form_{day_id}"):
            lineup_inputs = {}

            for pista in range(1, 6):
                st.markdown(f"**{lang_dict.get('snp_court_label', 'Court {n}').format(n=pista)}**")
                c1, c2 = st.columns([2, 2])

                default_p1 = existing.get(f"pista_{pista}_p1", "")
                default_p2 = existing.get(f"pista_{pista}_p2", "")

                with c1:
                    opts1 = [""] + all_players_list
                    idx1 = opts1.index(default_p1) if default_p1 in opts1 else 0
                    p1 = st.selectbox(
                        lang_dict.get('snp_player1_court', 'Player 1 - Court {n}').format(n=pista),
                        options=opts1,
                        index=idx1,
                        key=f"lineup_day{day_id}_pista{pista}_p1",
                        label_visibility="collapsed"
                    )
                with c2:
                    opts2 = [""] + all_players_list
                    idx2 = opts2.index(default_p2) if default_p2 in opts2 else 0
                    p2 = st.selectbox(
                        lang_dict.get('snp_player2_court', 'Player 2 - Court {n}').format(n=pista),
                        options=opts2,
                        index=idx2,
                        key=f"lineup_day{day_id}_pista{pista}_p2",
                        label_visibility="collapsed"
                    )

                lineup_inputs[pista] = {"p1": p1, "p2": p2}

            st.markdown("---")
            note_giornata = st.text_area(
                lang_dict.get('snp_notes_label', '📝 Matchday notes / comments (optional)'),
                value=existing.get("note", ""),
                placeholder=lang_dict.get('snp_notes_placeholder', 'Observations, injuries, etc.'),
                key=f"lineup_note_{day_id}"
            )

            lineup_submitted = st.form_submit_button(lang_dict.get('snp_save_formation_btn', '💾 Save Lineup'), type="primary")

            if lineup_submitted:
                lineup_data = {
                    "date": selected_day["date"],
                    "home": selected_day["home"],
                    "away": selected_day["away"],
                    "label": selected_day["label"],
                    "note": note_giornata.strip()
                }

                for pista, info in lineup_inputs.items():
                    lineup_data[f"pista_{pista}_p1"] = info["p1"]
                    lineup_data[f"pista_{pista}_p2"] = info["p2"]
                    # Il risultato non si tocca qui: si inserisce nello step 2, più avanti
                    lineup_data[f"pista_{pista}_risultato"] = existing.get(f"pista_{pista}_risultato", "")

                st.session_state.snp_lineups[day_id] = lineup_data
                _sync_snp_match_results(day_id, selected_day, lineup_data)

                log_activity("SNP lineup saved", selected_day["label"])
                if save_data_to_server():
                    st.success(lang_dict.get('snp_formation_saved', '✅ Lineup saved for **{day}**! You can enter results once the match has been played.').format(day=selected_day['label']))
                    st.rerun()

        st.markdown("---")

        # --- STEP 2: Risultati — solo per le piste già assegnate ---
        st.markdown(f"#### {lang_dict.get('snp_results_title', '2️⃣ Results')}")

        existing = st.session_state.snp_lineups.get(day_id, {})
        pistas_con_giocatori = [p for p in range(1, 6) if existing.get(f"pista_{p}_p1") or existing.get(f"pista_{p}_p2")]

        if not pistas_con_giocatori:
            st.info(lang_dict.get('snp_results_no_lineup', 'ℹ️ First assign the players in the Lineup above: you can then enter the results here.'))
        else:
            st.caption(lang_dict.get('snp_results_desc', 'Enter the result of each court when available. The players remain those assigned in the Lineup.'))
            with st.form(f"snp_results_form_{day_id}"):
                result_inputs = {}

                for pista in pistas_con_giocatori:
                    p1_label = existing.get(f"pista_{pista}_p1", "") or "—"
                    p2_label = existing.get(f"pista_{pista}_p2", "") or "—"
                    default_res = existing.get(f"pista_{pista}_risultato", "")

                    c1, c2 = st.columns([2, 1.5])
                    with c1:
                        st.markdown(f"**{lang_dict.get('snp_court_label', 'Court {n}').format(n=pista)}** — {p1_label} / {p2_label}")
                    with c2:
                        res = st.text_input(
                            lang_dict.get('snp_result_court_label', 'Result Court {n}').format(n=pista),
                            value=default_res,
                            placeholder=lang_dict.get('snp_result_placeholder', 'e.g. 6-4, 6-2'),
                            key=f"results_day{day_id}_pista{pista}_res",
                            label_visibility="collapsed"
                        )
                    result_inputs[pista] = res

                results_submitted = st.form_submit_button(lang_dict.get('snp_save_results_btn', '🏆 Save Results'), type="primary")

                if results_submitted:
                    lineup_data = dict(existing)
                    for pista, res in result_inputs.items():
                        lineup_data[f"pista_{pista}_risultato"] = res.strip()

                    st.session_state.snp_lineups[day_id] = lineup_data
                    _sync_snp_match_results(day_id, selected_day, lineup_data)

                    log_activity("SNP results saved", selected_day["label"])
                    if save_data_to_server():
                        st.success(lang_dict.get('snp_results_saved', '✅ Results saved for **{day}**!').format(day=selected_day['label']))
                        st.rerun()

        # --- Riepilogo completo delle 7 giornate ---
        st.markdown("---")
        st.markdown(f"### {lang_dict.get('snp_summary_title', '📋 Complete SNP Calendar Summary')}")

        for day in SNP_CALENDAR:
            did = day["id"]
            data = st.session_state.snp_lineups.get(did, {})

            # Conta quante piste hanno risultato
            piste_con_risultato = sum(1 for p in range(1, 6) if data.get(f"pista_{p}_risultato", "").strip())
            summary = lang_dict.get('snp_courts_filled', '{n}/5 courts filled').format(n=piste_con_risultato) if data else lang_dict.get('snp_not_filled', 'Not filled in')

            with st.expander(f"**{day['label']}**   →   {summary}", expanded=False):
                if data:
                    rows = []
                    for pista in range(1, 6):
                        p1 = data.get(f"pista_{pista}_p1", "")
                        p2 = data.get(f"pista_{pista}_p2", "")
                        res = data.get(f"pista_{pista}_risultato", "")
                        rows.append({
                            lang_dict.get('snp_col_court', 'Court'): lang_dict.get('snp_court_label', 'Court {n}').format(n=pista),
                            lang_dict.get('snp_col_player1', 'Player 1'): p1 or "—",
                            lang_dict.get('snp_col_player2', 'Player 2'): p2 or "—",
                            lang_dict.get('snp_col_result', 'Result'): res or "—"
                        })
                    df_day = pd.DataFrame(rows)
                    st.markdown(f"<div class='table-container'>{df_day.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)

                    if data.get("note"):
                        st.markdown(lang_dict.get('snp_notes_display', '**Notes:** {notes}').format(notes=data['note']))
                else:
                    st.info(lang_dict.get('snp_no_lineup_yet', 'No lineup entered yet for this matchday.'))

        # Pulsante reset
        with st.expander(lang_dict.get('snp_reset_expander', '🗑️ Reset SNP data')):
            if st.button(lang_dict.get('snp_reset_btn', 'Delete ALL SNP lineups and results'), type="secondary"):
                st.session_state.snp_lineups = {}
                st.session_state.match_results = [m for m in st.session_state.match_results if m.get("Tipo") != "SNP"]
                if save_data_to_server():
                    st.success(lang_dict.get('snp_reset_success', 'SNP data reset.'))
                    st.rerun()

    with coach_tab3:
        st.subheader(f"💬 {lang_dict.get('global_comments', 'Global Comments')}")
        for p in squad_players:
            st.markdown(f"#### 👤 {p['fname']} {p['lname']} (Coach Style: {p.get('play_style', 'Equilibrated')} | Player Style: {p.get('player_play_style', 'Equilibrated')})")
            if p.get("coach_note"):
                st.markdown(f"**Coach Note:** {p['coach_note']}")
            else:
                st.markdown("*No coach note.*")
            
            if p.get("comments"):
                st.markdown("**Peer notes:**")
                for c in p["comments"]:
                    st.markdown(f"- *From {c['from']}*: {c['text']}")
            st.markdown("---")

    with coach_tab_pairing:
        st.subheader(f"🤖 {lang_dict.get('pairing_title', 'Pairing Algorithm')}")
        st.markdown(lang_dict.get('pairing_desc', ''))
        st.markdown(f"- {lang_dict.get('pairing_p1', '')}")
        st.markdown(f"- {lang_dict.get('pairing_p2', '')}")
        
        all_player_names = [f"{p['fname']} {p['lname']} ({p['side']})" for p in squad_players]
        selected_available_str = st.multiselect(
            lang_dict.get('select_available_players', 'Select available players:'),
            options=all_player_names,
            default=all_player_names
        )
        
        selected_names_only = [s.split(" (")[0] for s in selected_available_str]
        available_players = [p for p in squad_players if f"{p['fname']} {p['lname']}" in selected_names_only]
        
        left_players = [p for p in available_players if p["side"] == "Left"]
        right_players = [p for p in available_players if p["side"] == "Right"]
        
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"⬅️ **Left available: {len(left_players)}**\n" + ("\n".join([f"- {p['fname']} {p['lname']}" for p in left_players]) if left_players else "None"))
        with col_info2:
            st.info(f"➡️ **Right available: {len(right_players)}**\n" + ("\n".join([f"- {p['fname']} {p['lname']}" for p in right_players]) if right_players else "None"))
        
        if st.button(lang_dict.get('run_pairing', 'Run Pairing'), type="primary"):
            if not left_players or not right_players:
                st.error(f"⚠️ {lang_dict.get('pairing_err', 'Error')}")
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
                
                final_pairs = final_pairs[:5]
                
                unmatched_l = [l for l in left_players if f"{l['fname']} {l['lname']}" not in matched_left]
                unmatched_r = [r for r in right_players if f"{r['fname']} {r['lname']}" not in matched_right]
                
                st.session_state.final_pairs_cache = final_pairs
                st.session_state.unmatched_cache = unmatched_l + unmatched_r

        if "final_pairs_cache" in st.session_state and st.session_state.final_pairs_cache:
            st.markdown(f"### 🏆 {lang_dict.get('recommended_pairing', 'Recommended Pairing')}")
            
            available_left_names = [f"{p['fname']} {p['lname']}" for p in left_players]
            available_right_names = [f"{p['fname']} {p['lname']}" for p in right_players]
            
            selected_lefts = []
            selected_rights = []
            
            st.markdown("""
                <div class="table-container">
                    <table class="custom-table">
                        <tr>
                            <th style="width: 10%;">Pair #</th>
                            <th style="width: 30%;">Left Player</th>
                            <th style="width: 30%;">Right Player</th>
                            <th style="width: 10%;">Coach Score</th>
                            <th style="width: 10%;">Mutual Willingness</th>
                            <th style="width: 10%;">Total Score</th>
                        </tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
            
            new_confirmed_pairs = []
            
            for idx, fp in enumerate(st.session_state.final_pairs_cache):
                c_pair, c_left, c_right, c_cs, c_mw, c_ts = st.columns([1, 3, 3, 1, 1, 1])
                
                with c_pair:
                    st.markdown(f"<div style='padding-top: 10px; font-weight: bold;'>#{idx + 1}</div>", unsafe_allow_html=True)
                
                with c_left:
                    current_l = fp["left"]
                    options_l = [current_l] + [name for name in available_left_names if name not in selected_lefts and name != current_l]
                    idx_l = options_l.index(current_l) if current_l in options_l else 0
                    chosen_l = st.selectbox(f"Left {idx+1}", options=options_l, index=idx_l, key=f"edit_left_{idx}", label_visibility="collapsed")
                    selected_lefts.append(chosen_l)
                
                with c_right:
                    current_r = fp["right"]
                    options_r = [current_r] + [name for name in available_right_names if name not in selected_rights and name != current_r]
                    idx_r = options_r.index(current_r) if current_r in options_r else 0
                    chosen_r = st.selectbox(f"Right {idx+1}", options=options_r, index=idx_r, key=f"edit_right_{idx}", label_visibility="collapsed")
                    selected_rights.append(chosen_r)
                
                with c_cs:
                    st.markdown(f"<div style='padding-top: 10px;'>{fp['coach_avg']}</div>", unsafe_allow_html=True)
                with c_mw:
                    st.markdown(f"<div style='padding-top: 10px;'>{fp['willingness']}</div>", unsafe_allow_html=True)
                with c_ts:
                    st.markdown(f"<div style='padding-top: 10px; font-weight: bold;'>{round(fp['score'], 2)}</div>", unsafe_allow_html=True)
                
                new_confirmed_pairs.append({
                    "Pair #": idx + 1,
                    "Left Player": chosen_l,
                    "Right Player": chosen_r,
                    "Coach Score": fp["coach_avg"],
                    "Mutual Willingness": fp["willingness"],
                    "Total Score": round(fp["score"], 2)
                })
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button(lang_dict.get('pairing_confirm_btn', '✅ Confirm Pairing Selection'), type="primary"):
                st.session_state.confirmed_pairing = pd.DataFrame(new_confirmed_pairs)
                st.success(lang_dict.get('pairing_confirm_success', 'Pairing confirmed and saved successfully!'))
                
            if "unmatched_cache" in st.session_state and st.session_state.unmatched_cache:
                st.warning(f"⚠️ {lang_dict.get('unmatched_warn', 'Unmatched warning')}")
                un_names = [f"{p['fname']} {p['lname']}" for p in st.session_state.unmatched_cache]
                st.markdown("- " + "\n- ".join(un_names))


    # --- ACTIVITY LOG (Admin only) ---
    if is_admin and coach_tab_log is not None:
        with coach_tab_log:
            st.subheader("📋 Activity Log")
            st.markdown("History of recent changes in the app. Visible only to Admin.")
            
            logs = st.session_state.get("activity_log", [])
            if not logs:
                st.info("No activity recorded yet.")
            else:
                df_log = pd.DataFrame(logs)
                # Ensure columns order
                cols = [c for c in ["timestamp", "actor", "action", "detail"] if c in df_log.columns]
                df_log = df_log[cols]
                df_log.columns = ["Timestamp", "User", "Action", "Detail"]
                st.markdown(
                    f"<div class='table-container'>{df_log.to_html(escape=False, index=False, classes='custom-table')}</div>",
                    unsafe_allow_html=True
                )
                st.caption(f"Showing last {len(logs)} entries (max 500).")
            
            st.markdown("---")
            col_clear1, col_clear2 = st.columns([1, 3])
            with col_clear1:
                if st.button("🗑️ Clear Activity Log", type="secondary"):
                    st.session_state.activity_log = []
                    if save_data_to_server():
                        st.success("Activity log cleared.")
                        st.rerun()
