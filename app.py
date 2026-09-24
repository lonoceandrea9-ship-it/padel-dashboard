

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
        
        st.markdown("---")
        st.markdown(f"**🔐 {lang_dict.get('sec_section_title', 'Security question')}**")
        st.caption(lang_dict.get('sec_section_desc', ''))
        fl_q_key, fl_custom, fl_answer = security_question_inputs(lang_dict, "first_login_sec", current_player)
        
        if st.form_submit_button("Salva Password e Accedi", type="primary"):
            sec_error = validate_security_inputs(fl_q_key, fl_custom, fl_answer, lang_dict)
            if not new_pwd1.strip():
                st.warning("La password non può essere vuota.")
            elif new_pwd1 != new_pwd2:
                st.error("Le password non coincidono. Riprova.")
            elif sec_error:
                st.warning(sec_error)
            else:
                current_player["password"] = new_pwd1
                current_player["first_login_done"] = True
                apply_security_question(current_player, fl_q_key, fl_custom, fl_answer)
                if save_data_to_server():
                    st.session_state.force_password_change = False
                    st.session_state.nav_mode = "Player_Dashboard"
                    st.success("✅ Password impostata e salvata correttamente!")
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
                if save_data_to_server():
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

