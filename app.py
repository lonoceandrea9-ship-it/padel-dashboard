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
