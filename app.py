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

# Initialize authentication state
if "authenticated_coach" not in st.session_state:
    st.session_state.authenticated_coach = False

# Complete roster of players (with default values for immediate exploration)
squad_players = [
    {"fname": "Álvaro", "lname": "Gomez", "tech": [7, 7, 7, 6, 8, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 6, 5, 7, 5], "c_mental": [7, 6, 6, 6, 7, 6]},
    {"fname": "Yannik", "lname": "Langeslag", "tech": [8, 6, 7, 7, 7, 5], "mental": [7, 6, 8, 6, 7, 6], "c_tech": [7, 5, 6, 6, 6, 4], "c_mental": [6, 5, 7, 5, 6, 5]},
    {"fname": "Josu", "lname": "Usabiaga", "tech": [6, 8, 7, 7, 6, 7], "mental": [6, 8, 6, 8, 7, 7], "c_tech": [5, 7, 6, 6, 5, 6], "c_mental": [5, 7, 5, 7, 6, 6]},
    {"fname": "Benjamin", "lname": "Thyrell", "tech": [7, 7, 8, 6, 7, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 7, 5, 6, 5], "c_mental": [7, 6, 6, 6, 7, 6]},
    {"fname": "Alexander", "lname": "Wennstam", "tech": [8, 8, 7, 7, 8, 6], "mental": [7, 7, 8, 8, 7, 7], "c_tech": [7, 7, 6, 6, 7, 5], "c_mental": [6, 6, 7, 7, 6, 6]},
    {"fname": "Andrea", "lname": "Lonoce", "tech": [8, 7, 8, 7, 9, 6], "mental": [9, 7, 8, 8, 9, 7], "c_tech": [8, 7, 8, 7, 9, 6], "c_mental": [9, 7, 8, 8, 9, 7]},
    {"fname": "Mikkel", "lname": "Hoff", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]},
    {"fname": "Pedro", "lname": "Rios", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7]},
    {"fname": "Hector", "lname": "Guerrero", "tech": [7, 7, 7, 7, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 6, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6]},
    {"fname": "Gonzalo", "lname": "Diez de Onate", "tech": [8, 7, 8, 7, 8, 6], "mental": [8, 7, 8, 8, 8, 7], "c_tech": [7, 6, 7, 6, 7, 5], "c_mental": [7, 6, 7, 7, 7, 6]},
    {"fname": "Julio", "lname": "Morales", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]},
    {"fname": "Lars", "lname": "Mikkelsen", "tech": [7, 7, 7, 6, 8, 6], "mental": [8, 7, 7, 7, 8, 7], "c_tech": [6, 6, 6, 5, 7, 5], "c_mental": [7, 6, 6, 6, 7, 6]},
    {"fname": "Joahn", "lname": "Lohman", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]},
    {"fname": "Nacho", "lname": "Saracho", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7]},
    {"fname": "Peter", "lname": "Gustafsson", "tech": [7, 7, 7, 6, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6]},
    {"fname": "Juanjo", "lname": "Lopez Benitez", "tech": [8, 8, 8, 7, 8, 7], "mental": [8, 8, 8, 8, 8, 8], "c_tech": [7, 7, 7, 6, 7, 6], "c_mental": [7, 7, 7, 7, 7, 7]},
    {"fname": "Sascha", "lname": "Van De Bilt", "tech": [7, 7, 7, 6, 7, 6], "mental": [7, 7, 7, 7, 7, 7], "c_tech": [6, 6, 6, 5, 6, 5], "c_mental": [6, 6, 6, 6, 6, 6]},
    {"fname": "Fernando", "lname": "Oribe", "tech": [8, 7, 8, 7, 8, 6], "mental": [8, 7, 8, 8, 8, 7], "c_tech": [7, 6, 7, 6, 7, 5], "c_mental": [7, 6, 7, 7, 7, 6]},
    {"fname": "Doug", "lname": "Ramsay", "tech": [7, 6, 7, 6, 7, 5], "mental": [7, 6, 7, 7, 7, 6], "c_tech": [6, 5, 6, 5, 6, 4], "c_mental": [6, 5, 6, 6, 6, 5]}
]

# Sidebar for navigation and security
st.sidebar.title("🎾 Padel Hub - Access")
modalita = st.sidebar.radio(
    "Select Area:",
    ["👤 Player Area", "📋 Coach Area"]
)

if modalita == "📋 Coach Area":
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Coach Restricted Area")
    
    COACH_PASSWORD = "padelcoach2026" 
    
    if not st.session_state.authenticated_coach:
        pwd_input = st.sidebar.text_input("Enter Coach Password", type="password")
        if st.sidebar.button("Log In"):
            if pwd_input == COACH_PASSWORD:
                st.session_state.authenticated_coach = True
                st.rerun()
            else:
                st.sidebar.error("Incorrect password!")
    else:
        st.sidebar.success("✅ Access Granted (Coach)")
        if st.sidebar.button("🔒 Log Out"):
            st.session_state.authenticated_coach = False
            st.rerun()

# ACCESS CONTROL: If Coach area is selected but not authenticated
if modalita == "📋 Coach Area" and not st.session_state.authenticated_coach:
    st.title("🔒 Restricted Area for Coach")
    st.warning("Please enter the correct password in the sidebar on the left to view the team overview and training groups.")

elif modalita == "👤 Player Area":
    # Streamlit native subtabs for personal evaluation and team directory
    tab_compila, tab_directory = st.tabs(["✏️ My Evaluation", "👥 Player Directory"])
    
    with tab_compila:
        # Full HTML, CSS and JavaScript for Player Dashboard (in English)
        html_code = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <title>Padel Performance Dashboard</title>
            <style>
                * { box-sizing: border-box; touch-action: manipulation; }
                :root {
                    --bg-primary: #0f172a;
                    --bg-card: #1e293b;
                    --accent-blue: #38bdf8;
                    --accent-purple: #a855f7;
                    --accent-green: #22c55e;
                    --accent-whatsapp: #25d366;
                    --text-main: #f8fafc;
                    --text-muted: #94a3b8;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    background-color: var(--bg-primary);
                    color: var(--text-main);
                    margin: 0;
                    padding: 12px;
                    -webkit-tap-highlight-color: transparent;
                }
                header { text-align: center; margin-bottom: 16px; }
                header h1 { color: var(--accent-blue); margin: 0 0 4px 0; font-size: 1.4rem; }
                header p { color: var(--text-muted); margin: 0; font-size: 0.8rem; }
                
                .main-container {
                    max-width: 1000px;
                    margin: 0 auto;
                    display: flex;
                    flex-direction: column;
                    gap: 16px;
                }
                .card {
                    background-color: var(--bg-card);
                    border-radius: 14px;
                    padding: 16px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                    border: 1px solid rgba(255,255,255,0.05);
                    width: 100%;
                }
                .card h2 { margin-top: 0; text-align: center; font-size: 1.05rem; }
                
                .profile-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; }
                .input-group { display: flex; flex-direction: column; gap: 4px; flex: 1 1 130px; }
                .input-group label { font-size: 0.8rem; color: var(--text-muted); }
                .input-group input[type="text"] {
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.15);
                    border-radius: 8px;
                    padding: 10px;
                    color: #fff;
                    font-size: 0.95rem;
                    width: 100%;
                    outline: none;
                }
                
                .actions-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
                    gap: 10px;
                }
                
                .btn {
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
                }
                .btn:active { transform: scale(0.98); }
                .btn-whatsapp { background-color: #25d366; color: #fff; }
                .btn-save-img { background-color: var(--accent-purple); color: #fff; }
                .btn-share-link { background-color: var(--accent-blue); color: #0f172a; }
                .btn-export { background-color: #f59e0b; color: #0f172a; }

                .charts-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                    gap: 16px;
                }
                .tech-title { color: var(--accent-blue); }
                .mental-title { color: var(--accent-purple); }
                .coach-title { color: #f59e0b; }
                
                .chart-container {
                    position: relative;
                    width: 100%;
                    height: 260px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                canvas {
                    width: 100% !important;
                    height: 100% !important;
                }

                .controls-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                    gap: 16px;
                }
                .control-group { display: flex; flex-direction: column; gap: 8px; }
                .control-item {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    gap: 8px;
                    background: rgba(255, 255, 255, 0.03);
                    padding: 8px 12px;
                    border-radius: 8px;
                }
                .control-item label { font-size: 0.85rem; flex: 1; }
                .control-item input[type="range"] {
                    flex: 1.2;
                    height: 24px;
                    accent-color: var(--accent-blue);
                }
                .control-item.purple input[type="range"] { accent-color: var(--accent-purple); }
                .control-item.amber input[type="range"] { accent-color: #f59e0b; }
                .control-item .val-badge { font-weight: bold; min-width: 20px; text-align: right; }

                .diff-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                    font-size: 0.85rem;
                }
                .diff-table th, .diff-table td {
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid rgba(255,255,255,0.08);
                }
                .diff-table th { color: var(--text-muted); }
                .badge-pos { color: #22c55e; font-weight: bold; }
                .badge-neg { color: #ef4444; font-weight: bold; }
                .badge-eq { color: var(--text-muted); }

                .insights-box {
                    background: rgba(245, 158, 11, 0.08);
                    border: 1px solid rgba(245, 158, 11, 0.2);
                    border-radius: 10px;
                    padding: 14px;
                    margin-top: 16px;
                }
                .insights-box h3 {
                    color: #f59e0b;
                    margin-top: 0;
                    font-size: 0.95rem;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }
                .insights-list {
                    margin: 0;
                    padding-left: 20px;
                    font-size: 0.85rem;
                    color: var(--text-main);
                    display: flex;
                    flex-direction: column;
                    gap: 6px;
                }

                .modal-overlay {
                    display: none;
                    position: fixed;
                    top:0; left:0; right:0; bottom:0;
                    background: rgba(0,0,0,0.85);
                    z-index: 1000;
                    align-items: center;
                    justify-content: center;
                    padding: 16px;
                    overflow-y: auto;
                }
                .modal {
                    background: var(--bg-card);
                    border-radius: 14px;
                    padding: 20px;
                    width: 100%;
                    max-width: 460px;
                    text-align: center;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                .modal img {
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    margin: 12px 0;
                    border: 1px solid rgba(255,255,255,0.2);
                }
                .modal input[type="text"], .modal textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.2);
                    color: #fff;
                    border-radius: 6px;
                }
                .modal-btn {
                    background: var(--accent-blue);
                    color: #0f172a;
                    border: none;
                    padding: 10px 18px;
                    border-radius: 8px;
                    font-weight: bold;
                    cursor: pointer;
                    margin-top: 8px;
                }
                
                .toast {
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
                }
            </style>
        </head>
        <body>

            <header>
                <h1 id="playerTitle">Padel Performance Dashboard</h1>
                <p>Ratings from 1 to 10 • Auto-saved on device</p>
            </header>

            <div class="main-container">
                <!-- PLAYER PROFILE & ACTIONS -->
                <div class="card">
                    <h2>Player Profile & Sharing</h2>
                    <div class="profile-grid">
                        <div class="input-group">
                            <label for="firstName">First Name</label>
                            <input type="text" id="firstName" placeholder="First Name" oninput="onDataChange()">
                        </div>
                        <div class="input-group">
                            <label for="lastName">Last Name</label>
                            <input type="text" id="lastName" placeholder="Last Name" oninput="onDataChange()">
                        </div>
                    </div>
                    
                    <div class="actions-grid">
                        <button class="btn btn-whatsapp" onclick="shareOnWhatsApp()">💬 WhatsApp</button>
                        <button class="btn btn-save-img" onclick="saveResultAsImage()">💾 Save PNG</button>
                        <button class="btn btn-share-link" onclick="shareOrCopyLink()">🔗 Copy Link</button>
                        <button class="btn btn-export" onclick="exportJsonFile()">📥 Export JSON (for Coach)</button>
                    </div>
                </div>

                <!-- NATIVE CANVAS CHARTS -->
                <div class="charts-grid">
                    <div class="card">
                        <h2 class="tech-title">Technical Skills</h2>
                        <div class="chart-container">
                            <canvas id="techCanvas"></canvas>
                        </div>
                    </div>
                    <div class="card">
                        <h2 class="mental-title">Attitude & Tactics</h2>
                        <div class="chart-container">
                            <canvas id="mentalCanvas"></canvas>
                        </div>
                    </div>
                </div>

                <!-- SELF-EVALUATION CONTROLS -->
                <div class="card">
                    <h2>My Ratings (Self-Evaluation)</h2>
                    <div class="controls-grid">
                        <div class="control-group">
                            <h3 class="tech-title" style="margin:0 0 4px 0; font-size:0.95rem;">Technique</h3>
                            <div class="control-item"><label>Volley</label><input type="range" id="volley" min="1" max="10" value="8" oninput="onDataChange()"><span id="volley-val" class="val-badge">8</span></div>
                            <div class="control-item"><label>Smash</label><input type="range" id="smash" min="1" max="10" value="7" oninput="onDataChange()"><span id="smash-val" class="val-badge">7</span></div>
                            <div class="control-item"><label>Bandeja</label><input type="range" id="bandeja" min="1" max="10" value="8" oninput="onDataChange()"><span id="bandeja-val" class="val-badge">8</span></div>
                            <div class="control-item"><label>Serve</label><input type="range" id="serve" min="1" max="10" value="7" oninput="onDataChange()"><span id="serve-val" class="val-badge">7</span></div>
                            <div class="control-item"><label>Defense</label><input type="range" id="defense" min="1" max="10" value="9" oninput="onDataChange()"><span id="defense-val" class="val-badge">9</span></div>
                            <div class="control-item"><label>Chiquita</label><input type="range" id="chiquita" min="1" max="10" value="6" oninput="onDataChange()"><span id="chiquita-val" class="val-badge">6</span></div>
                        </div>
                        <div class="control-group">
                            <h3 class="mental-title" style="margin:0 0 4px 0; font-size:0.95rem;">Tactics & Mental</h3>
                            <div class="control-item purple"><label>Pair Chemistry</label><input type="range" id="chemistry" min="1" max="10" value="9" oninput="onDataChange()"><span id="chemistry-val" class="val-badge">9</span></div>
                            <div class="control-item purple"><label>Error Management</label><input type="range" id="errorManagement" min="1" max="10" value="7" oninput="onDataChange()"><span id="errorManagement-val" class="val-badge">7</span></div>
                            <div class="control-item purple"><label>Positioning</label><input type="range" id="positioning" min="1" max="10" value="8" oninput="onDataChange()"><span id="positioning-val" class="val-badge">8</span></div>
                            <div class="control-item purple"><label>Focus</label><input type="range" id="focus" min="1" max="10" value="8" oninput="onDataChange()"><span id="focus-val" class="val-badge">8</span></div>
                            <div class="control-item purple"><label>Stamina</label><input type="range" id="stamina" min="1" max="10" value="9" oninput="onDataChange()"><span id="stamina-val" class="val-badge">9</span></div>
                            <div class="control-item purple"><label>Intensity</label><input type="range" id="intensity" min="1" max="10" value="7" oninput="onDataChange()"><span id="intensity-val" class="val-badge">7</span></div>
                        </div>
                    </div>
                </div>

                <!-- COACH EVALUATION & ANALYSIS SECTION -->
                <div class="card">
                    <h2 class="coach-title">📋 Coach Evaluation & Comparison</h2>
                    <p style="font-size:0.85rem; color:var(--text-muted); text-align:center; margin-top:0;">Enter the ratings given by your coach to analyze areas for improvement.</p>
                    
                    <div class="controls-grid">
                        <div class="control-group">
                            <h3 class="coach-title" style="margin:0 0 4px 0; font-size:0.95rem;">Technique (Coach)</h3>
                            <div class="control-item amber"><label>Volley (Coach)</label><input type="range" id="c_volley" min="1" max="10" value="8" oninput="onDataChange()"><span id="c_volley-val" class="val-badge">8</span></div>
                            <div class="control-item amber"><label>Smash (Coach)</label><input type="range" id="c_smash" min="1" max="10" value="7" oninput="onDataChange()"><span id="c_smash-val" class="val-badge">7</span></div>
                            <div class="control-item amber"><label>Bandeja (Coach)</label><input type="range" id="c_bandeja" min="1" max="10" value="8" oninput="onDataChange()"><span id="c_bandeja-val" class="val-badge">8</span></div>
                            <div class="control-item amber"><label>Serve (Coach)</label><input type="range" id="c_serve" min="1" max="10" value="7" oninput="onDataChange()"><span id="c_serve-val" class="val-badge">7</span></div>
                            <div class="control-item amber"><label>Defense (Coach)</label><input type="range" id="c_defense" min="1" max="10" value="9" oninput="onDataChange()"><span id="c_defense-val" class="val-badge">9</span></div>
                            <div class="control-item amber"><label>Chiquita (Coach)</label><input type="range" id="c_chiquita" min="1" max="10" value="6" oninput="onDataChange()"><span id="c_chiquita-val" class="val-badge">6</span></div>
                        </div>
                        <div class="control-group">
                            <h3 class="coach-title" style="margin:0 0 4px 0; font-size:0.95rem;">Tactics & Mental (Coach)</h3>
                            <div class="control-item amber"><label>Chemistry (Coach)</label><input type="range" id="c_chemistry" min="1" max="10" value="9" oninput="onDataChange()"><span id="c_chemistry-val" class="val-badge">9</span></div>
                            <div class="control-item amber"><label>Errors (Coach)</label><input type="range" id="c_errorManagement" min="1" max="10" value="7" oninput="onDataChange()"><span id="c_errorManagement-val" class="val-badge">7</span></div>
                            <div class="control-item amber"><label>Positioning (Coach)</label><input type="range" id="c_positioning" min="1" max="10" value="8" oninput="onDataChange()"><span id="c_positioning-val" class="val-badge">8</span></div>
                            <div class="control-item amber"><label>Focus (Coach)</label><input type="range" id="c_focus" min="1" max="10" value="8" oninput="onDataChange()"><span id="c_focus-val" class="val-badge">8</span></div>
                            <div class="control-item amber"><label>Stamina (Coach)</label><input type="range" id="c_stamina" min="1" max="10" value="9" oninput="onDataChange()"><span id="c_stamina-val" class="val-badge">9</span></div>
                            <div class="control-item amber"><label>Intensity (Coach)</label><input type="range" id="c_intensity" min="1" max="10" value="7" oninput="onDataChange()"><span id="c_intensity-val" class="val-badge">7</span></div>
                        </div>
                    </div>

                    <!-- Differences Table -->
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

                    <!-- IMPROVEMENT INSIGHTS SUMMARY -->
                    <div class="insights-box">
                        <h3>🎯 Focus on Areas for Improvement (Coach Feedback)</h3>
                        <ul class="insights-list" id="insightsList"></ul>
                    </div>
                </div>
            </div>

            <!-- MODAL -->
            <div class="modal-overlay" id="mainModal">
                <div class="modal">
                    <h3 id="modalTitle" style="margin-top:0">Generated Card</h3>
                    <div id="modalContent"></div>
                    <button class="modal-btn" onclick="closeModal()">Close</button>
                </div>
            </div>

            <!-- TOAST NOTIFICATION -->
            <div class="toast" id="toastMsg">✓ Action completed!</div>

            <script>
                const techKeys = ['volley', 'smash', 'bandeja', 'serve', 'defense', 'chiquita'];
                const techLabels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita'];
                
                const mentalKeys = ['chemistry', 'errorManagement', 'positioning', 'focus', 'stamina', 'intensity'];
                const mentalLabels = ['Chemistry', 'Errors', 'Positioning', 'Focus', 'Stamina', 'Intensity'];

                function drawRadarChart(canvasId, labels, dataValues, lineColor, fillColor) {
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

                    for (let l = 1; l <= levels; l++) {
                        const r = (radius / levels) * l;
                        ctx.beginPath();
                        for (let i = 0; i < numAxes; i++) {
                            const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                            const x = centerX + r * Math.cos(angle);
                            const y = centerY + r * Math.sin(angle);
                            if (i === 0) ctx.moveTo(x, y);
                            else ctx.lineTo(x, y);
                        }
                        ctx.closePath();
                        ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    }

                    ctx.font = 'bold 10px -apple-system, sans-serif';
                    ctx.fillStyle = '#94a3b8';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';

                    for (let i = 0; i < numAxes; i++) {
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
                    }

                    ctx.beginPath();
                    for (let i = 0; i < numAxes; i++) {
                        const val = Math.max(1, Math.min(10, dataValues[i]));
                        const r = (radius / 10) * val;
                        const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                        const x = centerX + r * Math.cos(angle);
                        const y = centerY + r * Math.sin(angle);
                        if (i === 0) ctx.moveTo(x, y);
                        else ctx.lineTo(x, y);
                    }
                    ctx.closePath();
                    ctx.fillStyle = fillColor;
                    ctx.fill();
                    ctx.strokeStyle = lineColor;
                    ctx.lineWidth = 2.5;
                    ctx.stroke();

                    for (let i = 0; i < numAxes; i++) {
                        const val = Math.max(1, Math.min(10, dataValues[i]));
                        const r = (radius / 10) * val;
                        const angle = (Math.PI * 2 / numAxes) * i - Math.PI / 2;
                        const x = centerX + r * Math.cos(angle);
                        const y = centerY + r * Math.sin(angle);
                        ctx.beginPath();
                        ctx.arc(x, y, 4, 0, Math.PI * 2);
                        ctx.fillStyle = lineColor;
                        ctx.fill();
                    }
                }

                function updateAnalysisAndTable() {
                    const tbody = document.getElementById('diffTableBody');
                    const insightsList = document.getElementById('insightsList');
                    tbody.innerHTML = '';
                    insightsList.innerHTML = '';
                    
                    const allKeys = [...techKeys, ...mentalKeys];
                    const allLabels = [...techLabels, ...mentalLabels];

                    let gaps = [];

                    allKeys.forEach((key, index) => {
                        const myVal = parseInt(document.getElementById(key).value);
                        const coachVal = parseInt(document.getElementById('c_' + key).value);
                        const diff = myVal - coachVal;
                        
                        let diffHtml = '';
                        if (diff > 0) {
                            diffHtml = `<span class="badge-pos">+${diff} (You > Coach)</span>`;
                        } else if (diff < 0) {
                            diffHtml = `<span class="badge-neg">${diff} (You < Coach)</span>`;
                            gaps.push({ label: allLabels[index], myVal, coachVal, diff });
                        } else {
                            diffHtml = `<span class="badge-eq">= (Perfect)</span>`;
                        }

                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${allLabels[index]}</td>
                            <td><b>${myVal}</b></td>
                            <td><b>${coachVal}</b></td>
                            <td>${diffHtml}</td>
                        `;
                        tbody.appendChild(row);
                    });

                    if (gaps.length === 0) {
                        const li = document.createElement('li');
                        li.innerHTML = `<b>Great job!</b> There are no areas where the coach rates you below your expectations.`;
                        insightsList.appendChild(li);
                    } else {
                        gaps.sort((a, b) => a.diff - b.diff);
                        gaps.forEach(item => {
                            const li = document.createElement('li');
                            li.innerHTML = `<b>${item.label} (You ${item.myVal} vs Coach ${item.coachVal}):</b> The coach identifies an important growth margin to work on.`;
                            insightsList.appendChild(li);
                        });
                    }
                }

                function renderAll() {
                    const tVals = techKeys.map(id => parseInt(document.getElementById(id).value));
                    const mVals = mentalKeys.map(id => parseInt(document.getElementById(id).value));

                    techKeys.forEach((id, i) => document.getElementById(id + '-val').innerText = tVals[i]);
                    mentalKeys.forEach((id, i) => document.getElementById(id + '-val').innerText = mVals[i]);

                    techKeys.forEach(id => document.getElementById('c_' + id + '-val').innerText = document.getElementById('c_' + id).value);
                    mentalKeys.forEach(id => document.getElementById('c_' + id + '-val').innerText = document.getElementById('c_' + id).value);

                    drawRadarChart('techCanvas', techLabels, tVals, '#38bdf8', 'rgba(56, 189, 248, 0.3)');
                    drawRadarChart('mentalCanvas', mentalLabels, mVals, '#a855f7', 'rgba(168, 85, 247, 0.3)');

                    updateAnalysisAndTable();

                    const fname = document.getElementById('firstName').value.trim();
                    const lname = document.getElementById('lastName').value.trim();
                    const fullName = `${fname} ${lname}`.trim();
                    document.getElementById('playerTitle').innerText = fullName ? `${fullName} - Dashboard` : `Padel Performance Dashboard`;
                }

                function onDataChange() {
                    renderAll();
                    saveToLocalStorage();
                }

                function saveToLocalStorage() {
                    const data = {
                        fname: document.getElementById('firstName').value,
                        lname: document.getElementById('lastName').value,
                        tech: techKeys.map(id => document.getElementById(id).value),
                        mental: mentalKeys.map(id => document.getElementById(id).value),
                        c_tech: techKeys.map(id => document.getElementById('c_' + id).value),
                        c_mental: mentalKeys.map(id => document.getElementById('c_' + id).value)
                    };
                    try { localStorage.setItem('padel_dashboard_data_coach', JSON.stringify(data)); } catch(e){}
                }

                function exportJsonFile() {
                    const data = {
                        fname: document.getElementById('firstName').value.trim() || 'Player',
                        lname: document.getElementById('lastName').value.trim() || '',
                        tech: techKeys.map(id => parseInt(document.getElementById(id).value)),
                        mental: mentalKeys.map(id => parseInt(document.getElementById(id).value)),
                        c_tech: techKeys.map(id => parseInt(document.getElementById('c_' + id).value)),
                        c_mental: mentalKeys.map(id => parseInt(document.getElementById('c_' + id).value))
                    };
                    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data, null, 2));
                    const downloadAnchor = document.createElement('a');
                    downloadAnchor.setAttribute("href", dataStr);
                    downloadAnchor.setAttribute("download", `padel_${data.fname}_${data.lname}.json`.toLowerCase().replace(/\\s+/g, '_'));
                    document.body.appendChild(downloadAnchor);
                    downloadAnchor.click();
                    downloadAnchor.remove();
                }

                function generateShareUrl() {
                    const fname = document.getElementById('firstName').value;
                    const lname = document.getElementById('lastName').value;
                    const tVals = techKeys.map(id => document.getElementById(id).value).join(',');
                    const mVals = mentalKeys.map(id => document.getElementById(id).value).join(',');
                    const cTech = techKeys.map(id => document.getElementById('c_' + id).value).join(',');
                    const cMental = mentalKeys.map(id => document.getElementById('c_' + id).value).join(',');

                    let baseUrl = window.location.href.split('?')[0];
                    if (!baseUrl.startsWith('http')) baseUrl = 'https://padel-dashboard.local/';

                    const url = new URL(baseUrl);
                    if (fname) url.searchParams.set('fname', fname);
                    if (lname) url.searchParams.set('lname', lname);
                    url.searchParams.set('tech', tVals);
                    url.searchParams.set('mental', mVals);
                    url.searchParams.set('ctech', cTech);
                    url.searchParams.set('cmental', cMental);
                    return url.toString();
                }

                function shareOnWhatsApp() {
                    const fname = document.getElementById('firstName').value.trim();
                    const lname = document.getElementById('lastName').value.trim();
                    const name = `${fname} ${lname}`.trim() || 'Player';
                    const shareUrl = generateShareUrl();
                    const text = `🎾 *Padel Card*\\n👤 *Player:* ${name}\\n\\nOpen card and comparison here:\\n${shareUrl}`;
                    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
                }

                function saveResultAsImage() {
                    const fname = document.getElementById('firstName').value.trim() || 'Player';
                    const lname = document.getElementById('lastName').value.trim() || '';
                    const fullName = `${fname} ${lname}`.trim();

                    const cCanvas = document.createElement('canvas');
                    cCanvas.width = 800;
                    cCanvas.height = 700;
                    const ctx = cCanvas.getContext('2d');

                    ctx.fillStyle = '#0f172a';
                    ctx.fillRect(0, 0, 800, 700);
                    ctx.fillStyle = '#1e293b';
                    ctx.fillRect(20, 20, 760, 80);

                    ctx.font = 'bold 24px -apple-system, sans-serif';
                    ctx.fillStyle = '#38bdf8';
                    ctx.textAlign = 'center';
                    ctx.fillText(fullName ? `${fullName} - Padel Card` : 'Padel Performance Dashboard', 400, 55);

                    ctx.font = '14px -apple-system, sans-serif';
                    ctx.fillStyle = '#94a3b8';
                    ctx.fillText('Self-Evaluation vs Coach Comparison', 400, 80);

                    const techCanvas = document.getElementById('techCanvas');
                    ctx.fillStyle = '#1e293b';
                    ctx.fillRect(20, 110, 370, 360);
                    ctx.drawImage(techCanvas, 30, 150, 350, 300);

                    const mentalCanvas = document.getElementById('mentalCanvas');
                    ctx.fillStyle = '#1e293b';
                    ctx.fillRect(410, 110, 370, 360);
                    ctx.drawImage(mentalCanvas, 420, 150, 350, 300);

                    const dataUrl = cCanvas.toDataURL('image/png');
                    const link = document.createElement('a');
                    link.download = `Padel_Comparison_${fname}_${lname}.png`.replace(/\\s+/g, '_');
                    link.href = dataUrl;
                    
                    document.getElementById('modalTitle').innerText = '🖼️ Image Generated!';
                    document.getElementById('modalContent').innerHTML = `
                        <p style="font-size:0.85rem; color:var(--text-muted); margin-top:0;">Press and hold on the image to save it:</p>
                        <img src="${dataUrl}" alt="Padel Card">
                        <br>
                        <a href="${dataUrl}" download="${link.download}" style="display:inline-block; padding:10px 16px; background:var(--accent-purple); color:#fff; text-decoration:none; font-weight:bold; border-radius:8px; margin-top:6px;">⬇️ Download Image</a>
                    `;
                    document.getElementById('mainModal').style.display = 'flex';
                }

                async function shareOrCopyLink() {
                    const shareUrl = generateShareUrl();
                    if (navigator.clipboard && window.isSecureContext) {
                        navigator.clipboard.writeText(shareUrl).then(showToast);
                    } else {
                        document.getElementById('modalTitle').innerText = '📋 Copy your link';
                        document.getElementById('modalContent').innerHTML = `
                            <p style="font-size:0.85rem; color:var(--text-muted)">Select and copy the link:</p>
                            <input type="text" value="${shareUrl}" readonly onclick="this.select()">
                        `;
                        document.getElementById('mainModal').style.display = 'flex';
                    }
                }

                function showToast() {
                    const toast = document.getElementById('toastMsg');
                    toast.style.display = 'block';
                    setTimeout(() => { toast.style.display = 'none'; }, 2000);
                }

                function closeModal() {
                    document.getElementById('mainModal').style.display = 'none';
                }

                function loadInitialData() {
                    const params = new URLSearchParams(window.location.search);
                    if (params.has('fname') || params.has('tech')) {
                        if (params.has('fname')) document.getElementById('firstName').value = params.get('fname');
                        if (params.has('lname')) document.getElementById('lastName').value = params.get('lname');
                        if (params.has('tech')) {
                            const t = params.get('tech').split(',');
                            techKeys.forEach((id, i) => { if (t[i]) document.getElementById(id).value = t[i]; });
                        }
                        if (params.has('mental')) {
                            const m = params.get('mental').split(',');
                            mentalKeys.forEach((id, i) => { if (m[i]) document.getElementById(id).value = m[i]; });
                        }
                        if (params.has('ctech')) {
                            const ct = params.get('ctech').split(',');
                            techKeys.forEach((id, i) => { if (ct[i]) document.getElementById('c_' + id).value = ct[i]; });
                        }
                        if (params.has('cmental')) {
                            const cm = params.get('cmental').split(',');
                            mentalKeys.forEach((id, i) => { if (cm[i]) document.getElementById('c_' + id).value = cm[i]; });
                        }
                    } else {
                        try {
                            const saved = localStorage.getItem('padel_dashboard_data_coach');
                            if (saved) {
                                const parsed = JSON.parse(saved);
                                if (parsed.fname) document.getElementById('firstName').value = parsed.fname;
                                if (parsed.lname) document.getElementById('lastName').value = parsed.lname;
                                if (parsed.tech) techKeys.forEach((id, i) => { if (parsed.tech[i]) document.getElementById(id).value = parsed.tech[i]; });
                                if (parsed.mental) mentalKeys.forEach((id, i) => { if (parsed.mental[i]) document.getElementById(id).value = parsed.mental[i]; });
                                if (parsed.c_tech) techKeys.forEach((id, i) => { if (parsed.c_tech[i]) document.getElementById('c_' + id).value = parsed.c_tech[i]; });
                                if (parsed.c_mental) mentalKeys.forEach((id, i) => { if (parsed.c_mental[i]) document.getElementById('c_' + id).value = parsed.c_mental[i]; });
                            }
                        } catch(e){}
                    }
                    renderAll();
                }

                window.addEventListener('resize', renderAll);
                window.addEventListener('load', loadInitialData);
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=1400, scrolling=True)

    with tab_directory:
        st.subheader("👥 Team Player Directory")
        st.markdown("Select a player from the list to quickly review their profile and ratings.")
        
        player_names = [f"{p['fname']} {p['lname']}" for p in squad_players]
        selected_player_name = st.selectbox("Search or select a player:", player_names)
        
        selected_player = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_player_name), None)
        
        if selected_player:
            st.markdown(f"---")
            st.markdown(f"### Player Card: **{selected_player['fname']} {selected_player['lname']}**")
            
            tech_labels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita']
            mental_labels = ['Chemistry', 'Errors', 'Positioning', 'Focus', 'Stamina', 'Intensity']
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ⚡ Technical Skills")
                df_tech = pd.DataFrame({
                    "Skill": tech_labels,
                    "Self-Evaluation": selected_player['tech'],
                    "Coach Rating": selected_player['c_tech']
                })
                st.dataframe(df_tech, use_container_width=True, hide_index=True)
                
            with col2:
                st.markdown("#### 🧠 Mental / Tactical Skills")
                df_mental = pd.DataFrame({
                    "Skill": mental_labels,
                    "Self-Evaluation": selected_player['mental'],
                    "Coach Rating": selected_player['c_mental']
                })
                st.dataframe(df_mental, use_container_width=True, hide_index=True)
                
            avg_my = (sum(selected_player['tech']) + sum(selected_player['mental'])) / 12
            avg_coach = (sum(selected_player['c_tech']) + sum(selected_player['c_mental'])) / 12
            
            st.info(f"📊 **Overall Self-Evaluation Average:** {round(avg_my, 1)} / 10  |  📊 **Overall Coach Average:** {round(avg_coach, 1)} / 10")

elif modalita == "📋 Coach Area" and st.session_state.authenticated_coach:
    # COACH AREA (UNLOCKED ONLY WITH PASSWORD)
    st.title("📋 Padel Coach - Group Management & Analysis")
    st.markdown("Centralized overview of player evaluations and automatic generation of targeted training groups.")

    tech_labels = ['Volley', 'Smash', 'Bandeja', 'Serve', 'Defense', 'Chiquita']
    mental_labels = ['Chemistry', 'Errors', 'Positioning', 'Focus', 'Stamina', 'Intensity']
    all_labels = tech_labels + mental_labels

    st.sidebar.header("📁 Upload Player Data")
    uploaded_files = st.sidebar.file_uploader(
        "Upload JSON files exported by players", 
        type=["json"], 
        accept_multiple_files=True
    )

    players_data = []

    if uploaded_files:
        for file in uploaded_files:
            try:
                data = json.load(file)
                players_data.append({
                    "fname": data.get("fname", "Name"),
                    "lname": data.get("lname", "Lastname"),
                    "tech": [int(x) for x in data.get("tech", [5]*6)],
                    "mental": [int(x) for x in data.get("mental", [5]*6)],
                    "c_tech": [int(x) for x in data.get("c_tech", [5]*6)],
                    "c_mental": [int(x) for x in data.get("c_mental", [5]*6)]
                })
            except Exception as e:
                st.sidebar.error(f"Error in file {file.name}: {e}")
    else:
        players_data = squad_players
        st.sidebar.info("💡 You are viewing the complete squad loaded in memory. Players can send you JSON files to update data.")

    summary_rows = []
    player_weaknesses = {}

    for p in players_data:
        full_name = f"{p['fname']} {p['lname']}"
        ct_vals = p['c_tech']
        cm_vals = p['c_mental']
        
        avg_tech_coach = sum(ct_vals) / len(ct_vals)
        avg_mental_coach = sum(cm_vals) / len(cm_vals)
        
        summary_rows.append({
            "Player": full_name,
            "Tech Average (Coach)": round(avg_tech_coach, 1),
            "Mental Average (Coach)": round(avg_mental_coach, 1),
            "Overall Average": round((avg_tech_coach + avg_mental_coach) / 2, 1)
        })
        
        all_coach_scores = ct_vals + cm_vals
        combined_skills = list(zip(all_labels, all_coach_scores))
        combined_skills.sort(key=lambda x: x[1])
        
        worst_skills = [skill[0] for skill in combined_skills if skill[1] <= 6]
        if not worst_skills:
            worst_skills = [combined_skills[0][0]]
            
        player_weaknesses[full_name] = worst_skills

    df_summary = pd.DataFrame(summary_rows)

    st.subheader("📊 Team Summary Table")
    st.dataframe(df_summary, use_container_width=True)

    st.subheader("🎯 Recommended Training Groups for Targeted Sessions")
    st.markdown("The app has automatically grouped players sharing the same areas for improvement:")

    skill_to_players = {}
    for player, skills in player_weaknesses.items():
        for skill in skills:
            if skill not in skill_to_players:
                skill_to_players[skill] = []
            skill_to_players[skill].append(player)

    sorted_groups = sorted(skill_to_players.items(), key=lambda x: len(x[1]), reverse=True)

    col1, col2 = st.columns(2)
    for idx, (skill, members) in enumerate(sorted_groups):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            st.info(f"**🛠️ Focus on: {skill}**\n\nPlayers:\n" + "".join([f"\n* **{m}**" for m in members]))
