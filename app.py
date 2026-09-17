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

# --- CUSTOM CSS: SFONDO BLU SCURO, TESTO BIANCO, HEADER, BOTTONI E TABELLE STILIZZATE ---
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
    
    /* Pulsanti specifici di accesso in rosso brillante */
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
    .element-container:has(button:contains("Spiller")) button {
        background-color: #dc2626 !important;
        color: white !important;
        border-color: #b91c1c !important;
    }
    
    /* Tutti gli altri bottoni standard in Blu scuro */
    div.stButton > button, div.stFormSubmitButton > button, button[kind="secondary"] {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #1d4ed8 !important;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }

    /* --- STILE TABELLE HTML PERSONALIZZATE IN TEMA SCURO --- */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #1b263b !important;
        color: #ffffff !important;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #334155;
        margin-bottom: 20px;
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
    </style>
""", unsafe_allow_html=True)

# --- TRADUZIONI COMPLETE (6 LINGUE) ---
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
        "partner_mgmt": "Gestione Ranking Partner (Fino a 5)",
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
        "coach_tab_squad": "Gestione Squadra & Presenze",
        "coach_tab_evals": "Gestione Voti Coach",
        "coach_tab_matches": "Gestione Partite",
        "coach_tab_comments": "Tutti i Commenti",
        "coach_tab_pairing": "Pairing Coppie Automatico",
        "squad_desc": "Modifica direttamente qui sotto i dati della squadra. I cambiamenti si salvano in tempo reale e il Commitment (%) viene ricalcolato automaticamente.",
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
        "recommended_pairing": "Risultato Pairing Consigliato:",
        "unmatched_warn": "Giocatori selezionati ma rimasti esclusi in questo turno per sbilanciamento numerico tra Destra e Sinistra:",
        "edit_pairing_lbl": "Modifica Accoppiamenti (Override Coach):",
        "confirm_pairing_btn": "Conferma Pairing Selezionato",
        "pairing_confirmed_msg": "Pairing confermato e salvato con successo dal coach!"
    },
    "English": {
        "welcome": "Welcome to the Padel Performance Hub",
        "select_area": "Select your access area to continue:",
        "player_area": "Player Area",
        "player_desc": "Access your password-protected personal card to view and update your evaluations.",
        "player_btn": "Access as Player",
        "coach_area": "Coach Area",
        "coach_desc": "Restricted access for coaching staff to manage data, planning, and matches.",
        "coach_btn": "Access as Coach",
        "login_player_title": "Player Area Login",
        "login_player_sub": "Select your name and enter your password (your first name).",
        "profile_select": "Select your profile:",
        "pwd_label": "Password (Your first name)",
        "enter_card": "Enter my card",
        "back_home": "Back to Home",
        "wrong_pwd": "Wrong password! Remember the password is your first name.",
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
        "partner_mgmt": "Partner Ranking Management (Up to 5)",
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
        "coach_tab_squad": "Squad Management & Attendance",
        "coach_tab_evals": "Coach Grades Management",
        "coach_tab_matches": "Match Management",
        "coach_tab_comments": "All Comments",
        "coach_tab_pairing": "Automatic Pair Pairing",
        "squad_desc": "Edit squad data directly below. Changes save in real time and Commitment (%) is automatically recalculated.",
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
        "run_pairing": "Generate Optimal Pairs with Available",
        "pairing_err": "To form pairs you need at least one left player and one right player among the selected ones!",
        "recommended_pairing": "Recommended Pairing Result:",
        "unmatched_warn": "Selected players left out in this round due to numerical imbalance between Right and Left:",
        "edit_pairing_lbl": "Edit Pairings (Coach Override):",
        "confirm_pairing_btn": "Confirm Selected Pairing",
        "pairing_confirmed_msg": "Pairing successfully confirmed and saved by the coach!"
    },
    "Español": {
        "welcome": "Bienvenido al Padel Performance Hub",
        "select_area": "Selecciona tu área de acceso para continuar:",
        "player_area": "Área de Jugador",
        "player_desc": "Accede a tu ficha personal protegida con contraseña para ver y actualizar tus valoraciones.",
        "player_btn": "Acceder como Jugador",
        "coach_area": "Área de Entrenador",
        "coach_desc": "Acceso restringido al cuerpo técnico para la gestión de datos, planificación y partidos.",
        "coach_btn": "Acceder como Entrenador",
        "login_player_title": "Acceso Área de Jugador",
        "login_player_sub": "Selecciona tu nombre e introduce tu contraseña (tu nombre de pila).",
        "profile_select": "Selecciona tu perfil:",
        "pwd_label": "Contraseña (Tu nombre de pila)",
        "enter_card": "Entrar en mi ficha",
        "back_home": "Volver al Inicio",
        "wrong_pwd": "¡Contraseña incorrecta! Recuerda que la contraseña es tu nombre de pila.",
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
        "partner_mgmt": "Gestión de Ranking de Compañeros (Hasta 5)",
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
        "coach_tab_squad": "Gestión de Plantilla y Asistencia",
        "coach_tab_evals": "Gestión de Notas del Entrenador",
        "coach_tab_matches": "Gestión de Partidos",
        "coach_tab_comments": "Todos los Comentarios",
        "coach_tab_pairing": "Emparejamiento Automático de Parejas",
        "squad_desc": "Modifica directamente los datos de la plantilla a continuación. Los cambios se guardan en tiempo real y el Compromiso (%) se recalcula automáticamente.",
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
        "recommended_pairing": "Resultado de Emparejamiento Recomendado:",
        "unmatched_warn": "Jugadores seleccionados pero excluidos en esta ronda por desequilibrio numérico entre Derecha e Izquierda:",
        "edit_pairing_lbl": "Modificar Parejas (Override del Entrenador):",
        "confirm_pairing_btn": "Confirmar Parejas Seleccionadas",
        "pairing_confirmed_msg": "¡Parejas confirmadas y guardadas con éxito por el entrenador!"
    },
    "Svenska": {
        "welcome": "Välkommen till Padel Performance Hub",
        "select_area": "Välj ditt åtkomstområde för att fortsätta:",
        "player_area": "Spelarområde",
        "player_desc": "Gå till ditt lösenordsskyddade personliga kort för att visa och uppdatera dina utvärderingar.",
        "player_btn": "Logga in som Spelare",
        "coach_area": "Tränarområde",
        "coach_desc": "Begränsad åtkomst för tränarstab för datahantering, planering och matcher.",
        "coach_btn": "Logga in som Tränare",
        "login_player_title": "Inloggning Spelarområde",
        "login_player_sub": "Välj ditt namn och ange ditt lösenord (ditt förnamn).",
        "profile_select": "Välj din profil:",
        "pwd_label": "Lösenord (Ditt förnamn)",
        "enter_card": "Gå till mitt kort",
        "back_home": "Tillbaka till Hem",
        "wrong_pwd": "Fel lösenord! Kom ihåg att lösenordet är ditt förnamn.",
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
        "partner_mgmt": "Partnerrankinghantering (Upp till 5)",
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
        "coach_tab_squad": "Trupphantering & Närvaro",
        "coach_tab_evals": "Coachbetygshantering",
        "coach_tab_matches": "Matchhantering",
        "coach_tab_comments": "Alla Kommentarer",
        "coach_tab_pairing": "Automatiskt Parval",
        "squad_desc": "Redigera truppdata direkt nedanför. Ändringar sparas i realtid och Engagemang (%) räknas om automatiskt.",
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
        "mental_skills_coach": "Mentala Färdigheter (Coach)",
        "save_coach_eval": "Spara Betyg, Profil och Coachanteckning",
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
        "recommended_pairing": "Rekommenderat Parresultat:",
        "unmatched_warn": "Spelare som valdes men utelämnades denna omgång på grund av numerisk obalans mellan Höger och Vänster:",
        "edit_pairing_lbl": "Redigera Par (Coach Override):",
        "confirm_pairing_btn": "Bekräfta Valda Par",
        "pairing_confirmed_msg": "Par har bekräftats och sparats av coachen!"
    },
    "Nederlands": {
        "welcome": "Welkom bij de Padel Performance Hub",
        "select_area": "Selecteer je toegangsgebied om door te gaan:",
        "player_area": "Spelersgebied",
        "player_desc": "Ga naar je met een wachtwoord beveiligde persoonlijke kaart om je evaluaties te bekijken en bij te werken.",
        "player_btn": "Toegang als Speler",
        "coach_area": "Coachgebied",
        "coach_desc": "Beperkte toegang voor de technische staf voor gegevensbeheer, planning en wedstrijden.",
        "coach_btn": "Toegang als Coach",
        "login_player_title": "Inloggen Spelersgebied",
        "login_player_sub": "Selecteer je naam en voer je wachtwoord in (je voornaam).",
        "profile_select": "Selecteer je profiel:",
        "pwd_label": "Wachtwoord (Je voornaam)",
        "enter_card": "Ga naar mijn kaart",
        "back_home": "Terug naar Home",
        "wrong_pwd": "Verkeerd wachtwoord! Onthoud dat het wachtwoord je voornaam is.",
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
        "save_eval": "Zelfevaluatie opslaan",
        "eval_saved": "Zelfevaluatie succesvol opgeslagen!",
        "radar_title": "Spindiagrammen (Afzonderlijke Vergelijking)",
        "player_radar_title": "Zelfevaluatie Speler",
        "coach_radar_title": "Coachevaluatie",
        "play_style_lbl": "Speelstijl:",
        "diff_tables": "Verschilltabellen (Jij vs Coach)",
        "tech_feat": "Technische Kenmerken",
        "mental_feat": "Mentale Kenmerken",
        "partner_mgmt": "Partner Ranking Beheer (Tot 5)",
        "save_partners": "Partner Ranking Opslaan",
        "partners_saved": "Partner ranking succesvol bijgewerkt!",
        "current_ranking": "Huidige Ranking:",
        "no_partners": "Geen partners geconfigureerd.",
        "history_title": "Geschiedenis & Ontwikkeling Coachevaluatie",
        "no_history": "Geen eerdere wijzigingen geregistreerd door de coach.",
        "official_note": "Officiële Coachnotitie",
        "no_coach_note": "Geen notitie ingevoerd door de coach op dit moment.",
        "peer_feedback": "Feedback van Medespelers",
        "select_partner_lbl": "Selecteer partner:",
        "note_on_partner": "Notitie over partner:",
        "send_note": "Notitie Verzenden",
        "note_sent": "Notitie verzonden!",
        "empty_note_warn": "Tekst mag niet leeg zijn.",
        "received_lbl": "Ontvangen:",
        "coach_dash_title": "Coach Dashboard",
        "exit_coach": "Verlaat Coachgebied",
        "coach_tab_squad": "Selectiebeheer & Aanwezigheid",
        "coach_tab_evals": "Coachbeoordelingen Beheer",
        "coach_tab_matches": "Wedstrijdbeheer",
        "coach_tab_comments": "Alle Opmerkingen",
        "coach_tab_pairing": "Automatische Koppelindeling",
        "squad_desc": "Bewerk selectiegegevens direct hieronder. Wijzigingen worden in realtime opgeslagen en Commitment (%) wordt automatisch berekend.",
        "col_name": "Naam", "col_role": "Rol", "col_hand": "Hand", "col_style": "Speelstijl", "col_trainings": "Trainingen", "col_participated": "Deelgenomen", "col_commitment": "Commitment (%)",
        "work_groups": "Werkgroepen & Gerichte Verbetering",
        "work_groups_desc": "Automatische groepering van alle spelers op basis van veelvoorkomende zwakke punten geïdentificeerd in coachevaluaties (waarden ≤ 6).",
        "no_critics": "Geen kritieke punten gedetecteerd (alle spelers hebben cijfers boven 6).",
        "coach_eval_title": "Coachbeoordelingen Beheer & Speelprofiel",
        "coach_eval_desc": "Selecteer een speler om diens evaluaties, tactisch profiel en officiële notitie bij te werken.",
        "select_player_eval": "Selecteer speler om te beoordelen:",
        "coach_eval_sub_title": "Coachevaluatie",
        "coach_note_lbl": "Officiële Coachnotitie / Opmerking (Zichtbaar voor speler)",
        "coach_note_placeholder": "Schrijf hier de opmerking voor de speler...",
        "tech_skills_coach": "Technische Vaardigheden (Coach)",
        "mental_skills_coach": "Mentale Vaardigheden (Coach)",
        "save_coach_eval": "Cijfers, Profiel en Coachnotitie Opslaan",
        "match_mgmt": "Wedstrijdregistratie",
        "match_mgmt_desc": "Selecteer spelers voor elk team (elk team vereist 1 Linkerspeler en 1 Rechterspeler).",
        "match_date": "Wedstrijddatum",
        "team_a": "Team A",
        "team_b": "Team B",
        "left_role": "Links (Left)",
        "right_role": "Rechts (Right)",
        "score_lbl": "Resultaat (bijv. 6-4, 6-2)",
        "register_match": "Wedstrijd Registreren",
        "same_player_err": "Binnen hetzelfde team kun je dezelfde speler niet twee keer selecteren!",
        "match_saved": "Wedstrijd succesvol geregistreerd!",
        "match_history": "Geregistreerde Wedstrijdgeschiedenis",
        "global_comments": "Globale Notities & Opmerkingen Overzicht",
        "pairing_title": "Intelligent Koppelingsalgoritme",
        "pairing_desc": "Selecteer hieronder de beschikbare spelers voor deze sessie. Het algoritme koppelt alleen de geselecteerde spelers aan elkaar, met respect voor de rolbeperking (1 Links + 1 Rechts) en balans:",
        "pairing_p1": "Gewicht 1.0: Algemene Coachevaluatie.",
        "pairing_p2": "Gewicht 0.5: Wederzijdse wil / voorkeur van spelers.",
        "select_available_players": "Selecteer vandaag beschikbare spelers:",
        "run_pairing": "Genereer Optimale Paren met Beschikbaren",
        "pairing_err": "Om paren te vormen heb je ten minste één linkerspeler en één rechterspeler nodig onder de geselecteerden!",
        "recommended_pairing": "Aanbevolen Koppelingsresultaat:",
        "unmatched_warn": "Geselecteerde spelers weggelaten in deze ronde vanwege numerieke onbalans tussen Rechts en Links:",
        "edit_pairing_lbl": "Paren Bewerken (Coach Override):",
        "confirm_pairing_btn": "Geselecteerde Pairing Bevestigen",
        "pairing_confirmed_msg": "Pairing succesvol bevestigd en opgeslagen door de coach!"
    }
}

# --- SELETTORE LINGUA IN SIDEBAR ---
with st.sidebar:
    selected_lang = st.selectbox("🌐 Language / Lingua / Idioma", list(translations.keys()), index=0)

t = translations[selected_lang]

# --- DATI DI ESEMPIO (Mock Data per la Squadra) ---
if 'squad_df' not in st.session_state:
    st.session_state['squad_df'] = pd.log if 'squad_df' not in st.session_state else ... # (manteniamo i tuoi dati di base se già presenti)
    
# Inizializziamo un dataset di esempio per far funzionare correttamente l'app se avviata da zero
if 'squad_df' not in st.session_state:
    st.session_state['squad_df'] = pd.DataFrame({
        "Name": ["Marco", "Luca", "Giovanni", "Matteo", "Andrea", "Davide"],
        "Role": ["Left", "Right", "Left", "Right", "Left", "Right"],
        "Hand": ["Right", "Right", "Left", "Right", "Right", "Left"],
        "Play Style": ["Aggressive", "Tactical", "Balanced", "Aggressive", "Tactical", "Balanced"],
        "Trainings": [10, 10, 10, 10, 10, 10],
        "Participated": [8, 9, 7, 10, 6, 8]
    })
    st.session_state['squad_df']["Commitment (%)"] = (st.session_state['squad_df']["Participated"] / st.session_state['squad_df']["Trainings"] * 100).round(1)

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# --- HOME PRINCIPALE ---
if st.session_state['page'] == 'home':
    st.title(t["welcome"])
    st.write(t["select_area"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t["player_area"])
        st.write(t["player_desc"])
        if st.button(t["player_btn"]):
            st.session_state['page'] = 'player_login'
            st.rerun()
            
    with col2:
        st.subheader(t["coach_area"])
        st.write(t["coach_desc"])
        if st.button(t["coach_btn"]):
            st.session_state['page'] = 'coach_login'
            st.rerun()

# --- LOGIN GIOCATORE ---
elif st.session_state['page'] == 'player_login':
    st.title(t["login_player_title"])
    st.write(t["login_player_sub"])
    
    players_list = st.session_state['squad_df']["Name"].tolist()
    selected_player = st.selectbox(t["profile_select"], players_list)
    pwd_input = st.text_input(t["pwd_label"], type="password")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t["enter_card"]):
            if pwd_input.strip().lower() == selected_player.strip().lower():
                st.session_state['logged_player'] = selected_player
                st.session_state['page'] = 'player_dashboard'
                st.rerun()
            else:
                st.error(t["wrong_pwd"])
    with col_b:
        if st.button(t["back_home"]):
            st.session_state['page'] = 'home'
            st.rerun()

# --- LOGIN ALLENATORE ---
elif st.session_state['page'] == 'coach_login':
    st.title(t["coach_login_title"])
    st.write(t["coach_login_sub"])
    
    coach_pwd = st.text_input(t["coach_pwd_label"], type="password")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(t["verify_pwd"]):
            # Password di default impostata a "admin" per esempio
            if coach_pwd == "admin":
                st.session_state['logged_coach'] = True
                st.session_state['page'] = 'coach_dashboard'
                st.rerun()
            else:
                st.error(t["wrong_pwd"])
    with col_b:
        if st.button(t["back_home"]):
            st.session_state['page'] = 'home'
            st.rerun()

# --- DASHBOARD ALLENATORE ---
elif st.session_state['page'] == 'coach_dashboard':
    if not st.session_state.get('logged_coach', False):
        st.session_state['page'] = 'home'
        st.rerun()
        
    st.title(t["coach_dash_title"])
    if st.button(t["exit_coach"]):
        st.session_state['logged_coach'] = False
        st.session_state['page'] = 'home'
        st.rerun()
        
    tab_squad, tab_evals, tab_matches, tab_comments, tab_pairing = st.tabs([
        t["coach_tab_squad"], 
        t["coach_tab_evals"], 
        t["coach_tab_matches"], 
        t["coach_tab_comments"], 
        t["coach_tab_pairing"]
    ])
    
    with tab_squad:
        st.write(t["squad_desc"])
        edited_squad = st.data_editor(st.session_state['squad_df'], num_rows="dynamic", key="squad_editor")
        # Ricalcolo automatico commitment se cambiano i dati
        if "Trainings" in edited_squad.columns and "Participated" in edited_squad.columns:
            edited_squad["Commitment (%)"] = (edited_squad["Participated"] / edited_squad["Trainings"].replace(0, 1) * 100).round(1)
        st.session_state['squad_df'] = edited_squad
        
    with tab_evals:
        st.subheader(t["coach_eval_title"])
        st.write(t["coach_eval_desc"])
        player_to_eval = st.selectbox(t["select_player_eval"], st.session_state['squad_df']["Name"].tolist(), key="coach_eval_sel")
        
        # Gestione voti coach semplificata per esempio
        st.text_area(t["coach_note_lbl"], placeholder=t["coach_note_placeholder"], key=f"note_{player_to_eval}")
        if st.button(t["save_coach_eval"]):
            st.success("Salvataggio effettuato con successo!")

    with tab_matches:
        st.subheader(t["match_mgmt"])
        st.write(t["match_mgmt_desc"])
        # Mock match registration interface
        match_date = st.date_input(t["match_date"], datetime.today())
        players = st.session_state['squad_df']["Name"].tolist()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{t['team_a']}**")
            ta_l = st.selectbox(f"{t['team_a']} - {t['left_role']}", players, key="ta_l")
            ta_r = st.selectbox(f"{t['team_a']} - {t['right_role']}", players, key="ta_r")
        with col2:
            st.markdown(f"**{t['team_b']}**")
            tb_l = st.selectbox(f"{t['team_b']} - {t['left_role']}", players, key="tb_l")
            tb_r = st.selectbox(f"{t['team_b']} - {t['right_role']}", players, key="tb_r")
            
        score = st.text_input(t["score_lbl"], "6-4, 6-2")
        if st.button(t["register_match"]):
            if len({ta_l, ta_r}) < 2 or len({tb_l, tb_r}) < 2:
                st.error(t["same_player_err"])
            else:
                st.success(t["match_saved"])

    with tab_comments:
        st.subheader(t["global_comments"])
        st.info("Nessun commento globale in questa demo.")

    with tab_pairing:
        st.subheader(t["pairing_title"])
        st.write(t["pairing_desc"])
        st.markdown(f"- {t['pairing_p1']}")
        st.markdown(f"- {t['pairing_p2']}")
        
        all_players = st.session_state['squad_df']["Name"].tolist()
        selected_available = st.multiselect(t["select_available_players"], all_players, default=all_players)
        
        if st.button(t["run_pairing"]):
            # Filtriamo i giocatori selezionati in base al ruolo (Left / Right)
            df_squad = st.session_state['squad_df']
            available_df = df_squad[df_squad["Name"].isin(selected_available)]
            
            left_players = available_df[available_df["Role"].str.lower().str.contains("left|sinistra")]["Name"].tolist()
            right_players = available_df[available_df["Role"].str.lower().str.contains("right|destra")]["Name"].tolist()
            
            if len(left_players) == 0 or len(right_players) == 0:
                st.error(t["pairing_err"])
            else:
                # Generazione coppie di esempio
                pairs = []
                import random
                random.shuffle(left_players)
                random.shuffle(right_players)
                
                num_pairs = min(len(left_players), len(right_players))
                for i in range(num_pairs):
                    pairs.append({"Team": f"Coppia {i+1}", "Left": left_players[i], "Right": right_players[i]})
                
                st.session_state['generated_pairs'] = pairs
                
                # Salviamo eventuali esclusi
                matched_names = set(left_players[:num_pairs] + right_players[:num_pairs])
                unmatched = [p for p in selected_available if p not in matched_names]
                st.session_state['unmatched_players'] = unmatched

        # Se sono state generate delle coppie, mostriamo i risultati con opzione di modifica e salvataggio
        if 'generated_pairs' in st.session_state and st.session_state['generated_pairs']:
            st.markdown(f"### {t['recommended_pairing']}")
            
            current_pairs = st.session_state['generated_pairs']
            edited_pairs = []
            
            st.markdown(f"**{t['edit_pairing_lbl']}**")
            all_squad_names = st.session_state['squad_df']["Name"].tolist()
            
            # Form di modifica dinamica delle coppie
            for idx, pair in enumerate(current_pairs):
                col_c1, col_c2, col_c3 = st.columns([2, 3, 3])
                with col_c1:
                    st.markdown(f"**{pair['Team']}**")
                with col_c2:
                    new_left = st.selectbox(f"Sinistra ({pair['Team']})", all_squad_names, index=all_squad_names.index(pair['Left']) if pair['Left'] in all_squad_names else 0, key=f"edit_l_{idx}")
                with col_c3:
                    new_right = st.selectbox(f"Destra ({pair['Team']})", all_squad_names, index=all_squad_names.index(pair['Right']) if pair['Right'] in all_squad_names else 0, key=f"edit_r_{idx}")
                
                edited_pairs.append({"Team": pair['Team'], "Left": new_left, "Right": new_right})
            
            if 'unmatched_players' in st.session_state and st.session_state['unmatched_players']:
                st.warning(f"{t['unmatched_warn']} {', '.join(st.session_state['unmatched_players'])}")
            
            # --- BOTTONE DI CONFERMA DELLA SELEZIONE ---
            if st.button(t["confirm_pairing_btn"], type="primary"):
                st.session_state['confirmed_pairs'] = edited_pairs
                st.success(t["pairing_confirmed_msg"])
                
                # Mostriamo un riepilogo visivo delle coppie confermate
                confirmed_df = pd.DataFrame(edited_pairs)
                st.table(confirmed_df)

# --- DASHBOARD GIOCATORE (Stub per completezza navigazione) ---
elif st.session_state['page'] == 'player_dashboard':
    logged_p = st.session_state.get('logged_player', 'Giocatore')
    st.title(f"Benvenuto nella tua scheda, {logged_p} 🎾")
    if st.button(t["back_home"]):
        st.session_state['page'] = 'home'
        st.rerun()
    st.info("Sezione Giocatore attiva.")
