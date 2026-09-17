with coach_tab_evals:
        st.subheader("✏️ Gestione Voti Coach & Profilo di Gioco")
        st.markdown("Seleziona un giocatore per aggiornare le sue valutazioni, il profilo tattico e la nota ufficiale.")
        
        selected_player_name = st.selectbox("Seleziona giocatore da valutare:", [f"{p['fname']} {p['lname']}" for p in squad_players], key="coach_eval_select")
        p_obj = next((p for p in squad_players if f"{p['fname']} {p['lname']}" == selected_player_name), None)
        
        if p_obj:
            with st.form("coach_eval_form"):
                st.markdown(f"**Modifica voti e profilo per: {selected_player_name}**")
                
                # --- CAMPO STILE DI GIOCO (VALUTAZIONE COACH) ---
                style_options = ["offensive", "defensive", "equilibrated", "counterattack"]
                current_style = p_obj.get("play_style", "equilibrated")
                if current_style not in style_options:
                    current_style = "equilibrated"
                
                st.markdown("### Valutazione Coach")
                selected_style = st.selectbox(
                    "Stile di Gioco",
                    options=style_options,
                    index=style_options.index(current_style)
                )
                
                st.markdown("---")
                st.markdown("📝 **Nota / Commento Ufficiale del Coach (Visibile al giocatore)**")
                new_coach_note = st.text_area("Scrivi qui il commento per il giocatore...", value=p_obj.get("coach_note", ""), key="coach_note_input")
                
                st.markdown("---")
                col_c_left, col_c_right = st.columns(2)
                
                c_tech_new = []
                c_mental_new = []
                
                with col_c_left:
                    st.markdown("🎾 *Competenze Tecniche (Coach)*")
                    for idx, t_label in enumerate(TECH_SKILLS):
                        val = st.slider(f"Coach - {t_label}", 1, 10, int(p_obj['c_tech'][idx]), key=f"scoach_tech_{idx}")
                        c_tech_new.append(val)
                
                with col_c_right:
                    st.markdown("🧠 *Competenze Mentali (Coach)*")
                    for idx, m_label in enumerate(MENTAL_SKILLS):
                        val = st.slider(f"Coach - {m_label}", 1, 10, int(p_obj['c_mental'][idx]), key=f"scoach_mental_{idx}")
                        c_mental_new.append(val)
                        
                if st.form_submit_button("Salva Voti, Profilo e Nota Coach", type="primary"):
                    p_obj.setdefault("history", []).append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "values": c_tech_new + c_mental_new
                    })
                    p_obj['c_tech'] = c_tech_new
                    p_obj['c_mental'] = c_mental_new
                    p_obj['play_style'] = selected_style
                    p_obj['coach_note'] = new_coach_note
                    st.success(f"✅ Scheda aggiornata con successo per {selected_player_name}!")
