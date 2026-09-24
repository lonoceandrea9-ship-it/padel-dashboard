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
                                if save_data_to_server():
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
                        if save_data_to_server():
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
                if save_data_to_server():
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
                    if save_data_to_server():
                        st.success(f"🎉 Allenamento salvato con successo per il giorno {training_date}!")
                        st.rerun()

            st.markdown("---")
            st.markdown("### 👥 Suddivisione in Gruppi da 4 (in base alla debolezza)")
            st.markdown("I giocatori selezionati vengono raggruppati in **gruppi da 4** in base alla loro **debolezza principale**, così ogni gruppo può lavorare su un obiettivo specifico e mirato invece di un'unica priorità per tutti.")

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
                st.info(f"Servono almeno {GROUP_SIZE} giocatori disponibili per formare un gruppo. Al momento ce ne sono {len(attending_players)}.")
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

                        title_suffix = " (gruppo incompleto)" if is_partial else ""
                        st.markdown(f"**Gruppo {gi + 1}{title_suffix}** — {names}")

                        col_g1, col_g2 = st.columns([1, 1.6])
                        with col_g1:
                            st.metric(label="🎯 Debolezza principale", value=top_skill, delta=f"Media: {round(top_val, 1)}/10", delta_color="inverse")
                        with col_g2:
                            default_idx = ALL_SKILLS.index(top_skill) if top_skill in ALL_SKILLS else 0
                            chosen_focus = st.selectbox(
                                f"Focus allenamento — Gruppo {gi + 1}",
                                options=ALL_SKILLS,
                                index=default_idx,
                                key=f"group_focus_{gi}"
                            )
                        group_focus_selections.append((group_players, chosen_focus))
                        st.markdown("---")

                    group_training_date = st.date_input(
                        "📅 In quale data vuoi salvare questi allenamenti di gruppo?",
                        datetime.now() + timedelta(days=2),
                        key="group_training_date"
                    )

                    submit_groups = st.form_submit_button("✅ Salva Allenamenti per Gruppo", type="primary")

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
                            st.success(f"🎉 {len(group_focus_selections)} allenamenti di gruppo salvati per il giorno {group_training_date}!")
                            st.rerun()

            st.markdown("---")
            st.markdown("### 📅 Storico Calendario Allenamenti Pianificati")
            if st.session_state.planned_trainings:
                df_planned = pd.DataFrame(st.session_state.planned_trainings).sort_values(by="Data").reset_index(drop=True)
                st.markdown(f"<div class='table-container'>{df_planned.to_html(escape=False, index=False, classes='custom-table')}</div>", unsafe_allow_html=True)
                
                st.markdown("#### ✏️ Modifica Allenamento")
                training_options_edit = [f"{t['Data']} - {t['1° Priorità']} ({t['Partecipanti'][:25]}...)" for t in st.session_state.planned_trainings]
                selected_training_to_edit_label = st.selectbox(
                    "Seleziona allenamento da modificare",
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
                    edit_date = st.date_input("📅 Data allenamento", default_edit_date, key="edit_training_date")

                    all_player_names_edit = [f"{p['fname']} {p['lname']}" for p in squad_players]
                    current_participant_fnames = [x.strip() for x in training_to_edit.get("Partecipanti", "").split(",") if x.strip()]
                    default_selected_full = [name for name in all_player_names_edit if name.split(" ")[0] in current_participant_fnames]
                    edit_attendees = st.multiselect(
                        "Partecipanti",
                        options=all_player_names_edit,
                        default=default_selected_full,
                        key="edit_training_attendees"
                    )

                    edit_p1_default = training_to_edit.get("1° Priorità")
                    edit_p2_default = training_to_edit.get("2° Priorità")
                    edit_p3_default = training_to_edit.get("3° Priorità")
                    edit_p1 = st.selectbox("1° Priorità", options=ALL_SKILLS, index=ALL_SKILLS.index(edit_p1_default) if edit_p1_default in ALL_SKILLS else 0, key="edit_training_p1")
                    edit_p2 = st.selectbox("2° Priorità", options=ALL_SKILLS, index=ALL_SKILLS.index(edit_p2_default) if edit_p2_default in ALL_SKILLS else 1, key="edit_training_p2")
                    edit_p3 = st.selectbox("3° Priorità", options=ALL_SKILLS, index=ALL_SKILLS.index(edit_p3_default) if edit_p3_default in ALL_SKILLS else 2, key="edit_training_p3")

                    if st.form_submit_button("💾 Salva Modifiche Allenamento", type="primary"):
                        if not edit_attendees:
                            st.warning("Seleziona almeno un partecipante.")
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
                                st.success("Allenamento modificato con successo!")
                                st.rerun()

                st.markdown("#### 🗑️ Cancella Allenamento dal Calendario")
                with st.form("delete_training_form"):
                    training_options = [f"{t['Data']} - {t['1° Priorità']} ({t['Partecipanti'][:25]}...)" for t in st.session_state.planned_trainings]
                    selected_training_to_delete = st.selectbox("Seleziona allenamento da rimuovere", training_options, key="delete_training_select")

                    if st.form_submit_button("🗑️ Elimina Allenamento Selezionato", type="secondary"):
                        selected_index = training_options.index(selected_training_to_delete)
                        removed_training = st.session_state.planned_trainings.pop(selected_index)
                        if save_data_to_server():
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
        
        
        # Inizializza storage delle formazioni SNP se non esiste
        if "snp_lineups" not in st.session_state:
            st.session_state.snp_lineups = {}
        st.session_state.snp_lineups = normalize_snp_lineups(st.session_state.snp_lineups)
        
        # Selettore giornata
        day_labels = [d["label"] for d in SNP_CALENDAR]
        selected_label = st.selectbox("📆 Seleziona la giornata SNP", day_labels)
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
        st.markdown("#### 1️⃣ Formazione")
        st.caption("Scegli 2 giocatori NAC per ogni pista. Potrai inserire il risultato in un secondo momento, quando la partita sarà giocata.")

        with st.form(f"snp_lineup_form_{day_id}"):
            lineup_inputs = {}

            for pista in range(1, 6):
                st.markdown(f"**Pista {pista}**")
                c1, c2 = st.columns([2, 2])

                default_p1 = existing.get(f"pista_{pista}_p1", "")
                default_p2 = existing.get(f"pista_{pista}_p2", "")

                with c1:
                    opts1 = [""] + all_players_list
                    idx1 = opts1.index(default_p1) if default_p1 in opts1 else 0
                    p1 = st.selectbox(
                        f"Giocatore 1 - Pista {pista}",
                        options=opts1,
                        index=idx1,
                        key=f"lineup_day{day_id}_pista{pista}_p1",
                        label_visibility="collapsed"
                    )
                with c2:
                    opts2 = [""] + all_players_list
                    idx2 = opts2.index(default_p2) if default_p2 in opts2 else 0
                    p2 = st.selectbox(
                        f"Giocatore 2 - Pista {pista}",
                        options=opts2,
                        index=idx2,
                        key=f"lineup_day{day_id}_pista{pista}_p2",
                        label_visibility="collapsed"
                    )

                lineup_inputs[pista] = {"p1": p1, "p2": p2}

            st.markdown("---")
            note_giornata = st.text_area(
                "📝 Note / Commenti giornata (opzionale)",
                value=existing.get("note", ""),
                placeholder="Osservazioni, infortuni, ecc.",
                key=f"lineup_note_{day_id}"
            )

            lineup_submitted = st.form_submit_button("💾 Salva Formazione", type="primary")

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
                    st.success(f"✅ Formazione salvata per **{selected_day['label']}**! Potrai inserire i risultati quando la partita sarà stata giocata.")
                    st.rerun()

        st.markdown("---")

        # --- STEP 2: Risultati — solo per le piste già assegnate ---
        st.markdown("#### 2️⃣ Risultati")

        existing = st.session_state.snp_lineups.get(day_id, {})
        pistas_con_giocatori = [p for p in range(1, 6) if existing.get(f"pista_{p}_p1") or existing.get(f"pista_{p}_p2")]

        if not pistas_con_giocatori:
            st.info("ℹ️ Assegna prima i giocatori nella Formazione qui sopra: potrai poi inserire qui i risultati.")
        else:
            st.caption("Inserisci il risultato di ogni pista quando disponibile. I giocatori restano quelli assegnati nella Formazione.")
            with st.form(f"snp_results_form_{day_id}"):
                result_inputs = {}

                for pista in pistas_con_giocatori:
                    p1_label = existing.get(f"pista_{pista}_p1", "") or "—"
                    p2_label = existing.get(f"pista_{pista}_p2", "") or "—"
                    default_res = existing.get(f"pista_{pista}_risultato", "")

                    c1, c2 = st.columns([2, 1.5])
                    with c1:
                        st.markdown(f"**Pista {pista}** — {p1_label} / {p2_label}")
                    with c2:
                        res = st.text_input(
                            f"Risultato Pista {pista}",
                            value=default_res,
                            placeholder="es. 6-4, 6-2",
                            key=f"results_day{day_id}_pista{pista}_res",
                            label_visibility="collapsed"
                        )
                    result_inputs[pista] = res

                results_submitted = st.form_submit_button("🏆 Salva Risultati", type="primary")

                if results_submitted:
                    lineup_data = dict(existing)
                    for pista, res in result_inputs.items():
                        lineup_data[f"pista_{pista}_risultato"] = res.strip()

                    st.session_state.snp_lineups[day_id] = lineup_data
                    _sync_snp_match_results(day_id, selected_day, lineup_data)

                    log_activity("SNP results saved", selected_day["label"])
                    if save_data_to_server():
                        st.success(f"✅ Risultati salvati per **{selected_day['label']}**!")
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
                if save_data_to_server():
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
                    if save_data_to_server():
                        st.success("Activity log cleared.")
                        st.rerun()
