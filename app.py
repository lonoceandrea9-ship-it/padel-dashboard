import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

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
    </style>
""", unsafe_allow_html=True)

# --- GESTIONE PERSISTENZA AUTOMATICA SU SERVER ---
DATA_FILE = "squad_data_persistence.json"

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

def save_data_to_server():
    data_to_save = {
        "squad_data": st.session_state.squad_data,
        "planned_trainings": st.session_state.planned_trainings,
        "match_results": st.session_state.match_results,
        "snp_lineups": st.session_state.get("snp_lineups", {}),
        "activity_log": st.session_state.get("activity_log", [])
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    except Exception as e:
        pass

def load_data_from_server():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return None
    return None

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
saved_server_data = load_data_from_server()

if saved_server_data:
    if "squad_data" not in st.session_state:
        st.session_state.squad_data = saved_server_data.get("squad_data", [])
    if "planned_trainings" not in st.session_state:
        st.session_state.planned_trainings = saved_server_data.get("planned_trainings", [])
    if "match_results" not in st.session_state:
        st.session_state.match_results = saved_server_data.get("match_results", [])
    if "snp_lineups" not in st.session_state:
        st.session_state.snp_lineups = saved_server_data.get("snp_lineups", {})
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
    st.title("🔒 Primo Accesso: Imposta la tua Nuova Password")
    st.markdown(f"Benvenuto **{current_player['fname']}**! Per motivi di sicurezza, essendo il tuo primo accesso, devi impostare una password personale che solo tu conoscerai.")
    
    with st.form("change_pwd_form"):
        new_pwd1 = st.text_input("Nuova Password Personale", type="password")
        new_pwd2 = st.text_input("Conferma Nuova Password", type="password")
        
        if st.form_submit_button("Salva Password e Accedi", type="primary"):
            if not new_pwd1.strip():
                st.warning("La password non può essere vuota.")
            elif new_pwd1 != new_pwd2:
                st.error("Le password non coincidono. Riprova.")
            else:
                current_player["password"] = new_pwd1
                current_player["first_login_done"] = True
                save_data_to_server()
                st.session_state.force_password_change = False
                st.session_state.nav_mode = "Player_Dashboard"
                st.success("Password impostata con successo!")
                st.rerun()

# --- HOME SELECTION ---
elif st.session_state.nav_mode == "Home":
    st.title(f"🎾 {lang_dict.get('welcome', 'Nac Team Performance App')}")
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
                        st.rerun()
                    else:
                        st.error("❌ Primo accesso: inserisci il tuo nome di battesimo come password.")
                else:
                    if player_pwd_input == current_saved_pwd:
                        st.session_state.authenticated_player = selected_fname
                        st.session_state.force_password_change = False
                        st.session_state.nav_mode = "Player_Dashboard"
                        st.rerun()
                    else:
                        st.error(f"❌ {lang_dict.get('wrong_pwd', 'Wrong password')}")
    with col_pl2:
        if st.button(lang_dict.get('back_home', 'Back'), use_container_width=True):
            st.session_state.nav_mode = "Home"
            st.rerun()

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
                save_data_to_server()
                st.session_state.nav_mode = "Coach"
                st.rerun()
            else:
                st.error("❌ Password errata! Riprova.")
    with col_btn2:
        if st.button(lang_dict.get('back_home', 'Back'), use_container_width=True, key="coach_login_back"):
            st.session_state.nav_mode = "Home"
            st.rerun()

# --- LOGIN ADMIN ---
elif st.session_state.nav_mode == "Admin_Login":
    st.title("🛡️ Admin Access")
    st.markdown("Full access to all app features (squad, evaluations, matches, players).")
    
    ADMIN_PASSWORD = "nacadmin2026"
    admin_pwd = st.text_input("Admin Password", type="password", key="admin_pwd_input")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if st.button("Verify Admin", type="primary", use_container_width=True, key="admin_verify_btn"):
            if admin_pwd == ADMIN_PASSWORD:
                st.session_state.authenticated_admin = True
                st.session_state.authenticated_coach = True  # full coach privileges
                log_activity("Admin login", "Admin accessed the system")
                save_data_to_server()
                st.session_state.nav_mode = "Coach"
                st.rerun()
            else:
                st.error("❌ Wrong admin password.")
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
    
    tab_eval, tab_partners, tab_history, tab_comments = st.tabs([
        f"📊 {lang_dict.get('eval_coach_tab', 'Evaluation')}", 
        f"🏆 {lang_dict.get('partners_tab', 'Partners')}", 
        f"📈 {lang_dict.get('history_tab', 'History')}", 
        f"💬 {lang_dict.get('comments_tab', 'Comments')}"
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
            save_data_to_server()
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
                save_data_to_server()
                st.success(lang_dict.get('partners_saved', 'Saved!'))
                st.rerun()
                
        st.markdown(f"### {lang_dict.get('current_ranking', 'Current Ranking:')}")
        if current_player.get("partners"):
            df_part = pd.DataFrame(list(current_player["partners"].keys()), columns=["Compagno"]).reset_index(drop=True)
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
                    save_data_to_server()
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
                save_data_to_server()
                st.session_state.nav_mode = "Player_Dashboard"
                st.rerun()
            
    if st.session_state.show_roster_modal:
        st.markdown("---")
        st.markdown("### 👥 Pannello Gestione Rosa Giocatori (Aggiungi o Rimuovi)")
        with st.container():
            col_add_m, col_del_m = st.columns(2)
            
            with col_add_m:
                st.markdown("#### Aggiungi Nuovo Giocatore")
                with st.form("modal_add_player_form"):
                    new_fname = st.text_input("Nome")
                    new_lname = st.text_input("Cognome")
                    new_side = st.selectbox("Posizione / Ruolo", ["Left", "Right"])
                    new_hand = st.selectbox("Mano", ["Destro", "Mancino"])
                    new_style = st.selectbox("Stile di Gioco", ["Offensive", "Defensive", "Equilibrated", "Counterattack"])
                    
                    if st.form_submit_button("➕ Aggiungi Giocatore", type="primary"):
                        if new_fname.strip() and new_lname.strip():
                            exists = any(p['fname'].lower() == new_fname.strip().lower() and p['lname'].lower() == new_lname.strip().lower() for p in st.session_state.squad_data)
                            if exists:
                                st.error("Un giocatore con questo nome e cognome esiste già nella rosa!")
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
                                save_data_to_server()
                                st.success(f"Giocatore {new_fname} {new_lname} aggiunto con successo!")
                                st.rerun()
                        else:
                            st.warning("Nome e Cognome non possono essere vuoti.")
            
            with col_del_m:
                st.markdown("#### Elimina Giocatore Esistente")
                with st.form("modal_delete_player_form"):
                    player_to_delete = st.selectbox("Seleziona giocatore da rimuovere", [f"{p['fname']} {p['lname']}" for p in st.session_state.squad_data])
                    
                    if st.form_submit_button("🗑️ Rimuovi Giocatore", type="secondary"):
                        st.session_state.squad_data = [p for p in st.session_state.squad_data if f"{p['fname']} {p['lname']}" != player_to_delete]
                        log_activity("Player removed", player_to_delete)
                        save_data_to_server()
                        st.success(f"Giocatore {player_to_delete} rimosso con successo!")
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
        st.markdown(f"Totale giocatori presenti: **{len(squad_players)}**")
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
            if st.form_submit_button("💾 Salva Modifiche Rosa e Ruoli", type="primary"):
                log_activity("Squad roles/styles updated", f"{len(squad_players)} players")
                save_data_to_server()
                st.success("Tutte le modifiche alla rosa, ruoli e destri/mancini sono state salvate permanentemente!")
                st.rerun()

        st.markdown("---")
        st.subheader(f"🎯 {lang_dict.get('work_groups', 'Work Groups')}")
        st.markdown(lang_dict.get('work_groups_desc', ''))
        
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
            st.info(lang_dict.get('no_critics', 'No criticalities.'))

    with coach_tab_evals:
        st.subheader(f"✏️ {lang_dict.get('coach_eval_title', 'Coach Grades')}")
        st.markdown(lang_dict.get('coach_eval_desc', ''))
        
        selected_player_name = st.selectbox(lang_dict.get('select_player_eval', 'Select player:'), [f"{p['fname']} {p['lname']}" for p in squad_players], key="coach_eval_select")
        p_obj = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_player_name), None)
        
        if p_obj:
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
                    save_data_to_server()
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
                            save_data_to_server()
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
            st.markdown("Il sistema ha analizzato i voti del gruppo presente e suggerisce le seguenti 3 priorità:")
            
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                if len(sorted_skills) > 0:
                    st.metric(label="🔥 1° Priorità Consigliata", value=sorted_skills[0][0], delta=f"Media: {round(sorted_skills[0][1], 1)}/10", delta_color="inverse")
            with col_p2:
                if len(sorted_skills) > 1:
                    st.metric(label="⚡ 2° Priorità Consigliata", value=sorted_skills[1][0], delta=f"Media: {round(sorted_skills[1][1], 1)}/10", delta_color="inverse")
            with col_p3:
                if len(sorted_skills) > 2:
                    st.metric(label="💡 3° Priorità Consigliata", value=sorted_skills[2][0], delta=f"Media: {round(sorted_skills[2][1], 1)}/10", delta_color="inverse")
            
            st.markdown("---")
            st.markdown("### ✏️ Personalizzazione e Conferma del Coach")
            st.markdown("Il coach può modificare le priorità dal menu a tendina e scegliere in quale data salvare l'allenamento nel calendario:")
            
            with st.form("coach_training_confirmation_form"):
                col_m1, col_m2, col_m3 = st.columns(3)
                
                default_p1_idx = ALL_SKILLS.index(top_priorities_system[0]) if top_priorities_system[0] in ALL_SKILLS else 0
                default_p2_idx = ALL_SKILLS.index(top_priorities_system[1]) if len(top_priorities_system) > 1 and top_priorities_system[1] in ALL_SKILLS else 1
                default_p3_idx = ALL_SKILLS.index(top_priorities_system[2]) if len(top_priorities_system) > 2 and top_priorities_system[2] in ALL_SKILLS else 2
                
                with col_m1:
                    coach_choice_p1 = st.selectbox("1° Priorità (Coach)", options=ALL_SKILLS, index=default_p1_idx)
                with col_m2:
                    coach_choice_p2 = st.selectbox("2° Priorità (Coach)", options=ALL_SKILLS, index=default_p2_idx)
                with col_m3:
                    coach_choice_p3 = st.selectbox("3° Priorità (Coach)", options=ALL_SKILLS, index=default_p3_idx)
                
                st.markdown("<br>", unsafe_allow_html=True)
                training_date = st.date_input("📅 In quale data vuoi salvare questo allenamento?", datetime.now() + timedelta(days=2))
                
                submit_training = st.form_submit_button("✅ Conferma e Salva nel Calendario", type="primary")
                
                if submit_training:
                    st.session_state.planned_trainings.append({
                        "Data": str(training_date),
                        "Partecipanti": ", ".join([p.split(" ")[0] for p in selected_attendees_names]),
                        "1° Priorità": coach_choice_p1,
                        "2° Priorità": coach_choice_p2,
                        "3° Priorità": coach_choice_p3
                    })
                    log_activity("Training planned", f"{training_date} – {coach_choice_p1}, {coach_choice_p2}, {coach_choice_p3}")
                    save_data_to_server()
                    st.success(f"🎉 Allenamento salvato con successo per il giorno {training_date}!")
                    st.rerun()

            st.markdown("---")
            st.markdown("### 📅 Storico Calendario Allenamenti Pianificati")
            if st.session_state.planned_trainings:
                df_planned = pd.DataFrame(st.session_state.planned_trainings).sort_values(by="Data").reset_index(drop=True)
                st.markdown(f"<div class='table-container'>{df_planned.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
                
                st.markdown("#### 🗑️ Cancella Allenamento dal Calendario")
                with st.form("delete_training_form"):
                    training_options = [f"{t['Data']} - {t['1° Priorità']} ({t['Partecipanti'][:25]}...)" for t in st.session_state.planned_trainings]
                    selected_training_to_delete = st.selectbox("Seleziona allenamento da rimuovere", training_options)
                    
                    if st.form_submit_button("🗑️ Elimina Allenamento Selezionato", type="secondary"):
                        selected_index = training_options.index(selected_training_to_delete)
                        removed_training = st.session_state.planned_trainings.pop(selected_index)
                        save_data_to_server()
                        st.success(f"Allenamento del {removed_training['Data']} eliminato con successo dal calendario!")
                        st.rerun()
            else:
                st.info("Nessun allenamento ancora confermato e salvato nel calendario.")
            
        else:
            st.info(lang_dict.get('training_no_attendees', 'Select at least one player.'))

    with coach_tab2:
        st.subheader("📅 Calendario & Registrazione Partite SNP")
        st.markdown("Gestione delle **7 giornate SNP**. Per ogni incontro assegna i giocatori NAC e il **risultato di ogni pista**.")
        
        all_players_list = [f"{p['fname']} {p['lname']}" for p in squad_players]
        
        # Calendario fisso delle 7 giornate SNP
        SNP_CALENDAR = [
            {"id": 1, "date": "27-Sep", "home": "NAC", "away": "Padelmadena", "label": "27-Sep  NAC  vs  Padelmadena"},
            {"id": 2, "date": "03-Oct", "home": "La Ultima Ronda", "away": "NAC", "label": "03-Oct  La Ultima Ronda  vs  NAC"},
            {"id": 3, "date": "25-Oct", "home": "NAC", "away": "Awa Pool Club", "label": "25-Oct  NAC  vs  Awa Pool Club"},
            {"id": 4, "date": "07-Nov", "home": "Gomez Hoyos Padel", "away": "NAC", "label": "07-Nov  Gomez Hoyos Padel  vs  NAC"},
            {"id": 5, "date": "28-Nov", "home": "Padelmadena", "away": "NAC", "label": "28-Nov  Padelmadena  vs  NAC"},
            {"id": 6, "date": "13-Dec", "home": "NAC", "away": "La Ultima Ronda", "label": "13-Dec  NAC  vs  La Ultima Ronda"},
            {"id": 7, "date": "10-Jan", "home": "NAC", "away": "Awa Pool Club", "label": "10-Jan  NAC  vs  Awa Pool Club"},
        ]
        
        # Inizializza storage delle formazioni SNP se non esiste
        if "snp_lineups" not in st.session_state:
            st.session_state.snp_lineups = {}
        
        # Selettore giornata
        day_labels = [d["label"] for d in SNP_CALENDAR]
        selected_label = st.selectbox("📆 Seleziona la giornata SNP", day_labels)
        selected_day = next(d for d in SNP_CALENDAR if d["label"] == selected_label)
        day_id = selected_day["id"]
        
        st.markdown(f"### {selected_day['label']}")
        st.caption("Per ogni pista: scegli 2 giocatori NAC + inserisci il risultato della pista")
        
        # Carica lineup esistente se presente
        existing = st.session_state.snp_lineups.get(day_id, {})
        
        with st.form(f"snp_day_form_{day_id}"):
            piste_data = {}
            
            for pista in range(1, 6):
                st.markdown(f"**Pista {pista}**")
                c1, c2, c3 = st.columns([2, 2, 1.5])
                
                default_p1 = existing.get(f"pista_{pista}_p1", "")
                default_p2 = existing.get(f"pista_{pista}_p2", "")
                default_res = existing.get(f"pista_{pista}_risultato", "")
                
                with c1:
                    opts1 = [""] + all_players_list
                    idx1 = opts1.index(default_p1) if default_p1 in opts1 else 0
                    p1 = st.selectbox(
                        f"Giocatore 1 - Pista {pista}",
                        options=opts1,
                        index=idx1,
                        key=f"day{day_id}_pista{pista}_p1",
                        label_visibility="collapsed"
                    )
                with c2:
                    opts2 = [""] + all_players_list
                    idx2 = opts2.index(default_p2) if default_p2 in opts2 else 0
                    p2 = st.selectbox(
                        f"Giocatore 2 - Pista {pista}",
                        options=opts2,
                        index=idx2,
                        key=f"day{day_id}_pista{pista}_p2",
                        label_visibility="collapsed"
                    )
                with c3:
                    res = st.text_input(
                        f"Risultato Pista {pista}",
                        value=default_res,
                        placeholder="es. 6-4, 6-2",
                        key=f"day{day_id}_pista{pista}_res",
                        label_visibility="collapsed"
                    )
                
                piste_data[pista] = {"p1": p1, "p2": p2, "risultato": res}
            
            st.markdown("---")
            note_giornata = st.text_area(
                "📝 Note / Commenti giornata (opzionale)",
                value=existing.get("note", ""),
                placeholder="Osservazioni, infortuni, ecc."
            )
            
            submitted = st.form_submit_button("💾 Salva Formazioni e Risultati di tutte le Piste", type="primary")
            
            if submitted:
                # Calcola risultato complessivo della giornata (vittorie piste)
                vittorie_nac = 0
                sconfitte_nac = 0
                for pista, info in piste_data.items():
                    r = info["risultato"].strip().lower()
                    if r:
                        # Heuristica semplice: se inizia con 6 o 7 e contiene "-" conta come possibile vittoria
                        # L'utente inserisce il risultato dal punto di vista NAC
                        # Per semplicità lasciamo il conteggio manuale, ma mostriamo i singoli risultati
                        pass
                
                lineup_data = {
                    "date": selected_day["date"],
                    "home": selected_day["home"],
                    "away": selected_day["away"],
                    "label": selected_day["label"],
                    "note": note_giornata.strip()
                }
                
                for pista, info in piste_data.items():
                    lineup_data[f"pista_{pista}_p1"] = info["p1"]
                    lineup_data[f"pista_{pista}_p2"] = info["p2"]
                    lineup_data[f"pista_{pista}_risultato"] = info["risultato"].strip()
                
                st.session_state.snp_lineups[day_id] = lineup_data
                
                # Aggiorna match_results per lo storico
                st.session_state.match_results = [
                    m for m in st.session_state.match_results
                    if not (m.get("Tipo") == "SNP" and m.get("Giornata_ID") == day_id)
                ]
                
                for pista, info in piste_data.items():
                    if info["p1"] or info["p2"] or info["risultato"].strip():
                        st.session_state.match_results.append({
                            "Data": selected_day["date"],
                            "Tipo": "SNP",
                            "Giornata_ID": day_id,
                            "Incontro": selected_day["label"],
                            "Casa": selected_day["home"],
                            "Trasferta": selected_day["away"],
                            "Pista": f"Pista {pista}",
                            "Giocatori_NAC": f"{info['p1']} / {info['p2']}" if info["p1"] and info["p2"] else (info["p1"] or info["p2"] or "—"),
                            "Risultato_Pista": info["risultato"].strip() or "—"
                        })
                
                log_activity("SNP lineup & results saved", selected_day["label"])
                save_data_to_server()
                st.success(f"✅ Formazioni e risultati di tutte le piste salvati per **{selected_day['label']}**!")
                st.rerun()
        
        # --- Riepilogo completo delle 7 giornate ---
        st.markdown("---")
        st.markdown("### 📋 Riepilogo Completo Calendario SNP")
        
        for day in SNP_CALENDAR:
            did = day["id"]
            data = st.session_state.snp_lineups.get(did, {})
            
            # Conta quante piste hanno risultato
            piste_con_risultato = sum(1 for p in range(1, 6) if data.get(f"pista_{p}_risultato", "").strip())
            summary = f"{piste_con_risultato}/5 piste compilate" if data else "Non compilata"
            
            with st.expander(f"**{day['label']}**   →   {summary}", expanded=False):
                if data:
                    rows = []
                    for pista in range(1, 6):
                        p1 = data.get(f"pista_{pista}_p1", "")
                        p2 = data.get(f"pista_{pista}_p2", "")
                        res = data.get(f"pista_{pista}_risultato", "")
                        rows.append({
                            "Pista": f"Pista {pista}",
                            "Giocatore 1": p1 or "—",
                            "Giocatore 2": p2 or "—",
                            "Risultato": res or "—"
                        })
                    df_day = pd.DataFrame(rows)
                    st.markdown(f"<div class='table-container'>{df_day.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
                    
                    if data.get("note"):
                        st.markdown(f"**Note:** {data['note']}")
                else:
                    st.info("Nessuna formazione ancora inserita per questa giornata.")
        
        # Pulsante reset
        with st.expander("🗑️ Reset dati SNP"):
            if st.button("Cancella TUTTE le formazioni e risultati SNP", type="secondary"):
                st.session_state.snp_lineups = {}
                st.session_state.match_results = [m for m in st.session_state.match_results if m.get("Tipo") != "SNP"]
                save_data_to_server()
                st.success("Dati SNP resettati.")
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
            
            if st.button("✅ Conferma Selezione Pairing", type="primary"):
                st.session_state.confirmed_pairing = pd.DataFrame(new_confirmed_pairs)
                st.success("Pairing confermato e salvato con successo!")
                
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
                    save_data_to_server()
                    st.success("Activity log cleared.")
                    st.rerun()
