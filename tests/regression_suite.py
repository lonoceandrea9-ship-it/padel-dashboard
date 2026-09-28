#!/usr/bin/env python3
"""Regression test suite for the Padel AI dashboard (app.py).

A single, self-contained file (deliberately not split across many files,
since every change to this repo has to be pasted by hand into GitHub's web
editor - one file to paste beats seventeen) that:

  1. Generates three stubbed copies of app.py in a temp directory, each
     swapping out only the database layer so the rest of the real
     application code runs unmodified under test:
       - a "plain" stub: save/load always succeed trivially, no real
         persistence. Used by tests that don't care about the database.
       - a "shareddb" stub: save/load share one JSON file on disk,
         simulating two independent browser sessions/tabs hitting the
         same Postgres row.
       - a "backups" stub: keeps the REAL save/load/backup/optimistic-
         locking SQL logic, swapping only the actual Postgres connection
         for an in-memory-via-JSON fake cursor, so the real application
         logic (not a reimplementation of it) is what's under test.
  2. Runs every test_* function against those stubs using Streamlit's
     AppTest, printing a PASS/FAIL summary and exiting non-zero if any
     test fails - the exit code is what a CI workflow checks.

Usage: python tests/regression_suite.py
"""
import os
import re
import shutil
import sys
import tempfile
import traceback

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_SRC = os.path.join(REPO_ROOT, "app.py")

GENERATED_DIR = tempfile.mkdtemp(prefix="padel_ci_")
APP_TEST = os.path.join(GENERATED_DIR, "app_test.py")
APP_TEST_SHAREDDB = os.path.join(GENERATED_DIR, "app_test_shareddb.py")
APP_TEST_BACKUPS = os.path.join(GENERATED_DIR, "app_test_backups.py")
FAKE_SHARED_DB = os.path.join(GENERATED_DIR, "fake_shared_db.json")
FAKE_PG_DB = os.path.join(GENERATED_DIR, "fake_pg_db.json")

SAVE_PATTERN = re.compile(
    r"def save_data_to_server\(retries=3, delay=0\.7\):.*?\n    return False\n",
    re.DOTALL
)
LOAD_PATTERN = re.compile(
    r"def load_data_from_server\(retries=3, delay=0\.7\):.*?\n    return False, None\n",
    re.DOTALL
)
CONN_PATTERN = re.compile(
    r"def get_db_connection\(\):.*?\n        return None\n",
    re.DOTALL
)


def _read_app_src():
    with open(APP_SRC, encoding="utf-8") as f:
        return f.read()


def make_plain():
    src = _read_app_src()
    assert SAVE_PATTERN.search(src), "save_data_to_server pattern not found"
    src = SAVE_PATTERN.sub("def save_data_to_server(retries=3, delay=0.7):\n    return True\n", src, count=1)
    assert LOAD_PATTERN.search(src), "load_data_from_server pattern not found"
    src = LOAD_PATTERN.sub("def load_data_from_server(retries=3, delay=0.7):\n    return True, None\n", src, count=1)
    with open(APP_TEST, "w", encoding="utf-8") as f:
        f.write(src)


def make_shareddb():
    src = _read_app_src()
    assert SAVE_PATTERN.search(src), "save_data_to_server pattern not found"
    save_stub = f'''def save_data_to_server(retries=3, delay=0.7):
    import json
    data_to_save = {{
        "squad_data": st.session_state.squad_data,
        "planned_trainings": st.session_state.planned_trainings,
        "match_results": st.session_state.match_results,
        "snp_lineups": st.session_state.get("snp_lineups", {{}}),
        "activity_log": st.session_state.get("activity_log", [])
    }}
    with open({FAKE_SHARED_DB!r}, "w") as f:
        json.dump(data_to_save, f)
    return True
'''
    src = SAVE_PATTERN.sub(save_stub, src, count=1)
    assert LOAD_PATTERN.search(src), "load_data_from_server pattern not found"
    load_stub = f'''def load_data_from_server(retries=3, delay=0.7):
    import json, os
    if not os.path.exists({FAKE_SHARED_DB!r}):
        return True, None
    with open({FAKE_SHARED_DB!r}) as f:
        return True, json.load(f)
'''
    src = LOAD_PATTERN.sub(load_stub, src, count=1)
    with open(APP_TEST_SHAREDDB, "w", encoding="utf-8") as f:
        f.write(src)


def make_backups():
    src = _read_app_src()
    assert CONN_PATTERN.search(src), "get_db_connection pattern not found"
    fake_backend = f'''
import json as _fakepg_json
import datetime as _fakepg_datetime

_FAKE_PG_FILE = {FAKE_PG_DB!r}

def _fakepg_load():
    import os
    if not os.path.exists(_FAKE_PG_FILE):
        return {{"app_state": None, "app_state_version": None, "backups": [], "next_backup_id": 1, "_version_counter": 0}}
    with open(_FAKE_PG_FILE) as f:
        raw = _fakepg_json.load(f)
    if raw.get("app_state_version"):
        raw["app_state_version"] = _fakepg_datetime.datetime.fromisoformat(raw["app_state_version"])
    for b in raw.get("backups", []):
        b["created_at"] = _fakepg_datetime.datetime.fromisoformat(b["created_at"])
    raw.setdefault("_version_counter", 0)
    return raw

def _fakepg_save(db):
    to_write = {{
        "app_state": db["app_state"],
        "app_state_version": db["app_state_version"].isoformat() if db.get("app_state_version") else None,
        "backups": [
            {{"id": b["id"], "data": b["data"], "created_at": b["created_at"].isoformat()}}
            for b in db["backups"]
        ],
        "next_backup_id": db["next_backup_id"],
        "_inject_conflict_once": db.get("_inject_conflict_once", False),
        "_version_counter": db.get("_version_counter", 0),
    }}
    with open(_FAKE_PG_FILE, "w") as f:
        _fakepg_json.dump(to_write, f)

def _fakepg_next_version(db):
    db["_version_counter"] = db.get("_version_counter", 0) + 1
    return _fakepg_datetime.datetime(2026, 1, 1) + _fakepg_datetime.timedelta(seconds=db["_version_counter"])

class _FakeCursor:
    def __init__(self):
        self._last_result = None

    def execute(self, sql, params=None):
        sql_norm = " ".join(sql.split())
        db = _fakepg_load()
        if sql_norm.startswith("CREATE TABLE IF NOT EXISTS app_state ("):
            pass
        elif sql_norm.startswith("CREATE TABLE IF NOT EXISTS app_state_backups"):
            pass
        elif sql_norm.startswith("INSERT INTO app_state_backups (data, created_at) VALUES"):
            val = params[0]
            data = val.adapted if hasattr(val, "adapted") else val
            bid = db["next_backup_id"]
            db["next_backup_id"] += 1
            db["backups"].append({{
                "id": bid,
                "data": _fakepg_json.loads(_fakepg_json.dumps(data)),
                "created_at": _fakepg_next_version(db),
            }})
        elif sql_norm.startswith("DELETE FROM app_state_backups WHERE id NOT IN"):
            limit = params[0]
            sorted_backups = sorted(db["backups"], key=lambda b: b["created_at"], reverse=True)
            keep_ids = {{b["id"] for b in sorted_backups[:limit]}}
            db["backups"] = [b for b in db["backups"] if b["id"] in keep_ids]
        elif sql_norm.startswith("INSERT INTO app_state (id, data, updated_at)"):
            val = params[0]
            db["app_state"] = val.adapted if hasattr(val, "adapted") else val
            db["app_state_version"] = _fakepg_next_version(db)
            self._last_result = (db["app_state_version"],)
        elif sql_norm.startswith("SELECT data, updated_at FROM app_state WHERE id = 1"):
            if "FOR UPDATE" in sql_norm and db.get("_inject_conflict_once"):
                db["_inject_conflict_once"] = False
                phantom_data = _fakepg_json.loads(_fakepg_json.dumps(db["app_state"])) if db["app_state"] else {{}}
                phantom_data["_phantom_writer_marker"] = True
                db["app_state"] = phantom_data
                db["app_state_version"] = _fakepg_next_version(db)
            self._last_result = (db["app_state"], db["app_state_version"]) if db["app_state"] is not None else None
        elif sql_norm.startswith("SELECT id, created_at FROM app_state_backups ORDER BY created_at DESC LIMIT"):
            limit = params[0]
            sorted_backups = sorted(db["backups"], key=lambda b: b["created_at"], reverse=True)[:limit]
            self._last_result = [(b["id"], b["created_at"]) for b in sorted_backups]
        elif sql_norm.startswith("SELECT data FROM app_state_backups WHERE id ="):
            bid = params[0]
            match = next((b for b in db["backups"] if b["id"] == bid), None)
            self._last_result = (match["data"],) if match else None
        else:
            raise AssertionError("Unhandled SQL in fake cursor: " + sql_norm)
        _fakepg_save(db)

    def fetchone(self):
        return self._last_result

    def fetchall(self):
        return self._last_result or []

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

class _FakeConn:
    def cursor(self):
        return _FakeCursor()

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

def get_db_connection():
    return _FakeConn()
'''
    src = CONN_PATTERN.sub(fake_backend.lstrip("\n") + "\n", src, count=1)
    with open(APP_TEST_BACKUPS, "w", encoding="utf-8") as f:
        f.write(src)


def generate_all():
    os.makedirs(GENERATED_DIR, exist_ok=True)
    make_plain()
    make_shareddb()
    make_backups()


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

def test_match_and_training():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    def fresh():
        at = AppTest.from_file(APP, default_timeout=60)
        at.session_state["nav_mode"] = "Coach"
        at.session_state["authenticated_coach"] = True
        at.session_state["force_password_change"] = False
        at.run()
        assert not at.exception, [e.message for e in at.exception]
        return at

    at = fresh()
    p1_sel = [s for s in at.selectbox if s.key == "lineup_day1_pista1_p1"][0]
    p2_sel = [s for s in at.selectbox if s.key == "lineup_day1_pista1_p2"][0]
    p1_sel.set_value("Andrea Lonoce").run()
    p2_sel.set_value("Alvaro Gomez").run()
    assert not at.exception, [e.message for e in at.exception]

    lineup_btn = [b for b in at.button if b.label == "💾 Save Lineup"][0]
    lineup_btn.click().run()
    assert not at.exception, [e.message for e in at.exception]

    res_input = [t for t in at.text_input if t.key == "results_day1_pista1_res"]
    assert len(res_input) == 1, "expected results input for pista 1 to now exist"
    res_input[0].set_value("6-4, 6-2").run()
    assert not at.exception, [e.message for e in at.exception]

    save_res_btn = [b for b in at.button if b.label == "🏆 Save Results"][0]
    save_res_btn.click().run()
    assert not at.exception, [e.message for e in at.exception]

    lineup_state = at.session_state["snp_lineups"][1]
    assert lineup_state["pista_1_p1"] == "Andrea Lonoce"
    assert lineup_state["pista_1_p2"] == "Alvaro Gomez"
    assert lineup_state["pista_1_risultato"] == "6-4, 6-2"

    match_result_rows = [m for m in at.session_state["match_results"] if m.get("Tipo") == "SNP" and m.get("Giornata_ID") == 1 and m.get("Pista") == "Pista 1"]
    assert len(match_result_rows) == 1
    assert match_result_rows[0]["Risultato_Pista"] == "6-4, 6-2"
    assert match_result_rows[0]["Giocatori_NAC"] == "Andrea Lonoce / Alvaro Gomez"

    # Matchday 1 (27-Sep) is auto-seeded on startup with the real SNP Galaxy
    # result once it's actually played, so it's no longer the "empty" matchday
    # to check the no-lineup-yet message against — matchday 2 still is.
    at2 = fresh()
    day_sel = [s for s in at2.selectbox if isinstance(s.value, str) and s.value.startswith("27-Sep")][0]
    day_sel.set_value("03-Oct  La Ultima Ronda  vs  NAC").run()
    assert not at2.exception, [e.message for e in at2.exception]
    info_texts = [i.value for i in at2.info if "First assign the players" in i.value]
    assert len(info_texts) > 0

    at3 = fresh()
    group_metrics = [m for m in at3.get("metric") if "weakness" in (m.label or "").lower()]
    assert len(group_metrics) >= 1
    group_headers = [m.value for m in at3.markdown if m.value.startswith("**Group")]
    assert len(group_headers) >= 1
    save_groups_btn = [b for b in at3.button if b.label == "✅ Save Group Trainings"]
    assert len(save_groups_btn) == 1
    save_groups_btn[0].click().run()
    assert not at3.exception, [e.message for e in at3.exception]
    group_trainings = [t for t in at3.session_state["planned_trainings"] if "Gruppo" in t]
    assert len(group_trainings) >= 1


def test_admin_no_cross_player_widget_leak():
    """Regression test for a real bug: an Admin browsing from one player's
    dashboard to another's (in the same browser session, no page reload)
    must see THAT player's own saved data in the Partner Ranking and
    Evaluation forms - not the previous player's leftover widget selections.
    Streamlit remembers widget values by key across reruns, so any widget
    key that isn't scoped to the viewed player leaks state between them."""
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.run()

    for p in at.session_state["squad_data"]:
        if p["fname"] == "Lars":
            p["partners"] = {
                "Jairo Lopez": 5, "Pedro Rios": 4, "Mikkel Hoff": 3,
                "Josu Usabiaga": 2, "Doug Ramsay": 1,
            }
        if p["fname"] == "Josu":
            p["partners"] = {"Alvaro Gomez": 5}
            p["tech"] = [1] * len(p["tech"])

    at.session_state["authenticated_admin"] = True
    at.session_state["admin_viewing_player"] = True
    at.session_state["authenticated_player"] = "Josu"
    at.session_state["nav_mode"] = "Player_Dashboard"
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    at.session_state["authenticated_player"] = "Lars"
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    lars_partner_sel0 = [s for s in at.selectbox if s.key == "partner_sel_Lars_Mikkelsen_0"][0]
    lars_partner_sel3 = [s for s in at.selectbox if s.key == "partner_sel_Lars_Mikkelsen_3"][0]
    assert lars_partner_sel0.value == "Jairo Lopez", lars_partner_sel0.value
    assert lars_partner_sel3.value == "Josu Usabiaga", lars_partner_sel3.value

    lars_tech0 = [s for s in at.selectbox if s.key == "p_tech_Lars_Mikkelsen_0"][0]
    assert lars_tech0.value != 1, "Lars's evaluation tab is showing Josu's leftover tech score"

    # Swap position 1 and 4, save, and confirm the write lands correctly
    # and doesn't disturb Josu's own (untouched) data.
    lars_partner_sel0.set_value("Josu Usabiaga").run()
    lars_partner_sel3 = [s for s in at.selectbox if s.key == "partner_sel_Lars_Mikkelsen_3"][0]
    lars_partner_sel3.set_value("Jairo Lopez").run()
    save_btn = [b for b in at.button if b.label == "Save Partner Ranking"][0]
    save_btn.click().run()
    assert not at.exception, [e.message for e in at.exception]

    lars_final = next(p for p in at.session_state["squad_data"] if p["fname"] == "Lars")["partners"]
    assert lars_final["Josu Usabiaga"] == 5
    assert lars_final["Jairo Lopez"] == 2
    josu_final = next(p for p in at.session_state["squad_data"] if p["fname"] == "Josu")["partners"]
    assert josu_final == {"Alvaro Gomez": 5}


def test_login_and_admin_pwd():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.run()
    assert not at.exception, [e.message for e in at.exception]
    at.session_state["nav_mode"] = "Player_Login"
    at.run()
    player_select = at.selectbox[0]
    player_select.set_value(player_select.options[0]).run()
    pwd_input = at.text_input[0]
    fname = player_select.options[0].split(" ")[0]
    pwd_input.set_value(fname).run()
    enter_btn = [b for b in at.button if "Enter" in b.label or "Accedi" in b.label or "card" in b.label.lower()]
    enter_btn = enter_btn[0] if enter_btn else at.button[0]
    enter_btn.click().run()
    assert not at.exception, [e.message for e in at.exception]
    logs = at.session_state["activity_log"]
    login_logs = [l for l in logs if "login" in l["action"].lower()]
    assert any("Player login" in l["action"] for l in login_logs)

    at2 = AppTest.from_file(APP, default_timeout=60)
    at2.session_state["nav_mode"] = "Coach"
    at2.session_state["authenticated_coach"] = True
    at2.session_state["authenticated_admin"] = True
    at2.session_state["force_password_change"] = False
    at2.run()
    assert not at2.exception, [e.message for e in at2.exception]

    target_name = at2.session_state["squad_data"][0]["fname"]
    pwd_field_key = None
    for ti in at2.text_input:
        if ti.key and ti.key.startswith(f"admin_pwd_{target_name}_"):
            pwd_field_key = ti.key
            break
    assert pwd_field_key, "password field for target player not found"

    field = [ti for ti in at2.text_input if ti.key == pwd_field_key][0]
    field.set_value("NuovaPasswordTest123").run()
    assert not at2.exception, [e.message for e in at2.exception]

    save_btn = [b for b in at2.button if "Save All Passwords" in b.label]
    assert len(save_btn) == 1
    save_btn[0].click().run()
    assert not at2.exception, [e.message for e in at2.exception]

    updated_player = next(p for p in at2.session_state["squad_data"] if p["fname"] == target_name)
    assert updated_player["password"] == "NuovaPasswordTest123"

    admin_logs = [l for l in at2.session_state["activity_log"] if "password" in l["action"].lower()]
    assert any("Admin updated player password" in l["action"] for l in admin_logs)


def test_partner_prefs():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["nav_mode"] = "Coach"
    at.session_state["authenticated_coach"] = True
    at.session_state["force_password_change"] = False
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    sel = [s for s in at.selectbox if s.key == "coach_eval_select"][0]
    target = next(o for o in sel.options if o.startswith("Alvaro"))
    sel.set_value(target).run()
    assert not at.exception, [e.message for e in at.exception]

    md_texts = [m.value for m in at.markdown]
    assert [m for m in md_texts if "prefers to play with" in m]
    assert [m for m in md_texts if "Yannik Langeslag" in m and "table-container" in m]
    assert [m for m in md_texts if "ranked" in m and "Alvaro" in m]


def test_languages():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["language"] = "Svenska"
    at.session_state["nav_mode"] = "Coach"
    at.session_state["authenticated_coach"] = True
    at.session_state["force_password_change"] = False
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    subheaders = [s.value for s in at.subheader]
    snp_sub = [s for s in subheaders if "SNP" in s]
    assert any("Kalender" in s for s in snp_sub), "expected Swedish SNP title"

    markdowns = [m.value for m in at.markdown]
    assert [m for m in markdowns if "Uppställning" in m]
    italian_leftovers = [m for m in markdowns if "Formazione" in m or "Giornata" in m or "Salva Formazione" in m]
    assert not italian_leftovers

    buttons = [b.label for b in at.button]
    assert any("Spara" in b for b in buttons)

    at2 = AppTest.from_file(APP, default_timeout=60)
    at2.session_state["language"] = "Italiano"
    at2.session_state["nav_mode"] = "Coach"
    at2.session_state["authenticated_coach"] = True
    at2.session_state["force_password_change"] = False
    at2.run()
    assert not at2.exception, [e.message for e in at2.exception]
    markdowns2 = [m.value for m in at2.markdown]
    assert [m for m in markdowns2 if "Formazione" in m]


def test_selected_player_header():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["nav_mode"] = "Coach"
    at.session_state["authenticated_coach"] = True
    at.session_state["force_password_change"] = False
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    sel = [s for s in at.selectbox if s.key == "coach_eval_select"][0]
    target1 = next(o for o in sel.options if o.startswith("Alexander"))
    sel.set_value(target1).run()
    assert not at.exception, [e.message for e in at.exception]

    target2 = next(o for o in sel.options if o.startswith("Gonzalo"))
    sel.set_value(target2).run()
    assert not at.exception, [e.message for e in at.exception]
    md_texts2 = [m.value for m in at.markdown]
    hdr2 = [m for m in md_texts2 if "Partner Preferences of" in m]
    assert "Gonzalo" in hdr2[0], f"BUG: header still shows old player: {hdr2}"


def test_resync():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST_SHAREDDB

    admin = AppTest.from_file(APP, default_timeout=60)
    admin.session_state["nav_mode"] = "Coach"
    admin.session_state["authenticated_coach"] = True
    admin.session_state["authenticated_admin"] = True
    admin.session_state["force_password_change"] = False
    admin.run()
    assert not admin.exception, [e.message for e in admin.exception]

    player = AppTest.from_file(APP, default_timeout=60)
    player.session_state["nav_mode"] = "Player_Login"
    player.run()
    assert not player.exception, [e.message for e in player.exception]

    player_select = player.selectbox[0]
    yannik_option = next(o for o in player_select.options if o.startswith("Yannik"))
    player_select.set_value(yannik_option).run()
    pwd_input = player.text_input[0]
    pwd_input.set_value("Yannik").run()
    enter_btn = player.button[0]
    enter_btn.click().run()
    assert not player.exception, [e.message for e in player.exception]

    if player.session_state.get("force_password_change"):
        text_inputs = player.text_input
        pwd1_field = [t for t in text_inputs if "New password" in t.label][0]
        pwd1_field.set_value("NewPass123").run()
        pwd2_field = [t for t in player.text_input if "Confirm new password" in t.label][0]
        pwd2_field.set_value("NewPass123").run()
        answer_field = [t for t in player.text_input if t.label == "Answer"][0]
        answer_field.set_value("blue").run()
        submit_btns = [b for b in player.button if "Save Password and Login" in b.label]
        submit_btns[0].click().run()
        assert not player.exception, [e.message for e in player.exception]

    tech_select_keys = [s.key for s in player.selectbox if s.key and s.key.startswith("p_tech_")]
    for key in tech_select_keys:
        sb = [s for s in player.selectbox if s.key == key][0]
        sb.set_value(10).run()
        assert not player.exception, [e.message for e in player.exception]

    save_btns = [b for b in player.button if "Self-Evaluation" in b.label]
    save_btns[0].click().run()
    assert not player.exception, [e.message for e in player.exception]
    saved_tech = [p for p in player.session_state["squad_data"] if p["fname"] == "Yannik"][0]["tech"]
    assert all(v == 10 for v in saved_tech), "player's own save didn't take"

    admin.session_state["_dummy_trigger"] = True
    admin.run()
    assert not admin.exception, [e.message for e in admin.exception]
    admin_after = [p for p in admin.session_state["squad_data"] if p["fname"] == "Yannik"][0]
    assert all(v == 10 for v in admin_after["tech"]), "BUG: admin's open session did not resync from DB"

    admin.run()
    squad_save_btn = [b for b in admin.button if "Save Squad" in b.label]
    if squad_save_btn:
        squad_save_btn[0].click().run()
        assert not admin.exception, [e.message for e in admin.exception]
        reloaded = [p for p in admin.session_state["squad_data"] if p["fname"] == "Yannik"][0]
        assert all(v == 10 for v in reloaded["tech"]), "DATA LOSS: admin's save overwrote the player's self-eval!"


def test_ux_batch1():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["nav_mode"] = "Coach"
    at.session_state["authenticated_coach"] = True
    at.session_state["authenticated_admin"] = True
    at.session_state["force_password_change"] = False
    at.session_state["show_roster_modal"] = True
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    initial_count = len(at.session_state["squad_data"])
    remove_btn = [b for b in at.button if "Remove Player" in b.label][0]
    remove_btn.click().run()
    assert not at.exception, [e.message for e in at.exception]
    assert len(at.session_state["squad_data"]) == initial_count, "BUG: player removed without confirmation!"
    warn_texts = [w.value for w in at.warning]
    assert any("confirm" in w.lower() or "conferma" in w.lower() for w in warn_texts)

    confirm_cb = [c for c in at.checkbox if c.key == "confirm_roster_delete"][0]
    confirm_cb.set_value(True).run()
    remove_btn = [b for b in at.button if "Remove Player" in b.label][0]
    remove_btn.click().run()
    assert not at.exception, [e.message for e in at.exception]
    assert len(at.session_state["squad_data"]) == initial_count - 1, "BUG: player NOT removed after confirming!"

    snp_reset_btn = [b for b in at.button if "Delete ALL SNP" in b.label or "reset" in b.label.lower() or "Elimina" in b.label][0]
    assert snp_reset_btn.disabled, "BUG: SNP reset button should be disabled before confirmation"

    player = AppTest.from_file(APP, default_timeout=60)
    player.session_state["nav_mode"] = "Player_Login"
    player.run()
    assert not player.exception, [e.message for e in player.exception]

    player_select = player.selectbox[0]
    alexander_option = next(o for o in player_select.options if o.startswith("Alexander"))
    player_select.set_value(alexander_option).run()
    pwd_input = player.text_input[0]
    pwd_input.set_value("Alexander").run()
    enter_btn = player.button[0]
    enter_btn.click().run()
    assert not player.exception, [e.message for e in player.exception]

    if player.session_state.get("force_password_change"):
        pwd1_field = [t for t in player.text_input if "New password" in t.label][0]
        pwd1_field.set_value("NewPass123").run()
        pwd2_field = [t for t in player.text_input if "Confirm new password" in t.label][0]
        pwd2_field.set_value("NewPass123").run()
        answer_field = [t for t in player.text_input if t.label == "Answer"][0]
        answer_field.set_value("blue").run()
        submit_btns = [b for b in player.button if "Save Password and Login" in b.label]
        submit_btns[0].click().run()
        assert not player.exception, [e.message for e in player.exception]

    captions_before = [c.value for c in player.caption]
    assert any("All changes saved" in c or "🟢" in c for c in captions_before)

    tech_key = [s.key for s in player.selectbox if s.key and s.key.startswith("p_tech_")][0]
    sb = [s for s in player.selectbox if s.key == tech_key][0]
    new_val = 0 if sb.value != 0 else 1
    sb.set_value(new_val).run()
    assert not player.exception, [e.message for e in player.exception]

    captions_after = [c.value for c in player.caption]
    assert any("unsaved" in c.lower() or "🟡" in c for c in captions_after)


def test_backups_and_restore():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST_BACKUPS

    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["nav_mode"] = "Coach"
    at.session_state["authenticated_coach"] = True
    at.session_state["authenticated_admin"] = True
    at.session_state["force_password_change"] = False
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    yannik_before = [p for p in at.session_state["squad_data"] if p["fname"] == "Yannik"][0]
    original_tech = list(yannik_before["tech"])

    for i in range(3):
        at.session_state["squad_data"][0]["tech"] = [original_tech[j] + i + 1 for j in range(len(original_tech))]
        confirm_clear_cb = [c for c in at.checkbox if c.key == "confirm_log_clear"][0]
        confirm_clear_cb.set_value(True).run()
        assert not at.exception, [e.message for e in at.exception]
        clear_btn = [b for b in at.button if "Clear Activity Log" in b.label or "Cancella Registro" in b.label][0]
        clear_btn.click().run()
        assert not at.exception, [e.message for e in at.exception]

    backup_selects = [s for s in at.selectbox if s.key == "backup_select"]
    assert backup_selects, "Backups selectbox not found"
    backup_select = backup_selects[0]
    assert len(backup_select.options) >= 3, f"expected at least 3 backups, got {len(backup_select.options)}"

    oldest_backup_label = backup_select.options[-1]
    backup_select.set_value(oldest_backup_label).run()
    assert not at.exception, [e.message for e in at.exception]

    confirm_cb = [c for c in at.checkbox if c.key == "confirm_backup_restore"][0]
    confirm_cb.set_value(True).run()

    restore_btn = [b for b in at.button if "Restore this backup" in b.label or "Ripristina" in b.label][0]
    restore_btn.click().run()
    assert not at.exception, [e.message for e in at.exception]

    restored_tech = [p for p in at.session_state["squad_data"] if p["fname"] == "Yannik"][0]["tech"]
    assert restored_tech == original_tech, f"restore didn't bring back pre-change values: {restored_tech} != {original_tech}"


def test_optimistic_locking():
    import json
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST_BACKUPS

    a = AppTest.from_file(APP, default_timeout=60)
    a.session_state["nav_mode"] = "Coach"
    a.session_state["authenticated_coach"] = True
    a.session_state["authenticated_admin"] = True
    a.session_state["force_password_change"] = False
    a.run()
    assert not a.exception, [e.message for e in a.exception]
    version_a = a.session_state.get("_db_version")

    with open(FAKE_PG_DB) as f:
        db = json.load(f)
    db["_inject_conflict_once"] = True
    with open(FAKE_PG_DB, "w") as f:
        json.dump(db, f)

    confirm_cb_a = [c for c in a.checkbox if c.key == "confirm_log_clear"][0]
    confirm_cb_a.set_value(True).run()
    assert not a.exception, [e.message for e in a.exception]
    clear_btn_a = [bt for bt in a.button if "Clear Activity Log" in bt.label][0]
    clear_btn_a.click().run()
    assert not a.exception, [e.message for e in a.exception]

    warnings_a = [w.value for w in a.warning]
    assert any("someone else" in w.lower() or "un altro" in w.lower() for w in warnings_a), \
        f"expected a conflict warning, got: {warnings_a}"

    with open(FAKE_PG_DB) as f:
        db_after = json.load(f)
    version_a_after = str(a.session_state.get("_db_version"))
    assert version_a_after != str(version_a), "Session A should have picked up the newer version"
    assert "_phantom_writer_marker" in db_after["app_state"], \
        "the DB's real current data should still be the competing writer's"


def test_avatars():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["nav_mode"] = "Player_Dashboard"
    at.session_state["authenticated_player"] = "Yannik"
    at.session_state["force_password_change"] = False
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    markdowns = [m.value for m in at.markdown]
    avatar_markdowns = [m for m in markdowns if "border-radius:50%" in m]
    assert avatar_markdowns, "expected at least one avatar div on the player dashboard"
    assert any("YO" in m or ">Y" in m for m in avatar_markdowns)

    at2 = AppTest.from_file(APP, default_timeout=60)
    at2.session_state["nav_mode"] = "Coach"
    at2.session_state["authenticated_coach"] = True
    at2.session_state["authenticated_admin"] = True
    at2.session_state["force_password_change"] = False
    at2.run()
    assert not at2.exception, [e.message for e in at2.exception]

    pwd_expander = next((e for e in at2.expander if "password" in (e.label or "").lower()), None)
    assert pwd_expander is not None, "password management expander not found"

    md2 = [m.value for m in at2.markdown]
    avatar_md2 = [m for m in md2 if "border-radius:50%" in m]
    assert avatar_md2, "expected avatars in the coach's player password list"


def test_analytics_and_pdf():
    from streamlit.testing.v1 import AppTest
    APP = APP_TEST

    at = AppTest.from_file(APP, default_timeout=60)
    at.session_state["nav_mode"] = "Coach"
    at.session_state["authenticated_coach"] = True
    at.session_state["authenticated_admin"] = True
    at.session_state["force_password_change"] = False
    at.run()
    assert not at.exception, [e.message for e in at.exception]

    metric_labels = [m.label for m in at.metric]
    for expected in ("Players", "Avg Self Score", "Avg Coach Score", "Avg Attendance"):
        assert expected in metric_labels, f"expected {expected!r} metric, got {metric_labels}"

    markdowns = [m.value for m in at.markdown]
    for expected in ("Team Averages by Skill", "Squad by Play Style", "Squad by Side",
                     "Top & Bottom Performers", "Top 5", "Bottom 5"):
        assert any(expected in m for m in markdowns), f"expected {expected!r} in Team Analytics tab"

    downloads = [d for d in at.get("download_button") if "report card" in (d.label or "").lower()]
    assert downloads, "expected at least one player report-card download button"
    assert not at.exception, [e.message for e in at.exception]

    at2 = AppTest.from_file(APP, default_timeout=60)
    at2.session_state["nav_mode"] = "Player_Dashboard"
    at2.session_state["authenticated_player"] = "Yannik"
    at2.session_state["force_password_change"] = False
    at2.run()
    assert not at2.exception, [e.message for e in at2.exception]
    my_downloads = [d for d in at2.get("download_button") if "report card" in (d.label or "").lower()]
    assert my_downloads, "expected the player's own report-card download button"


def test_pdf_generation():
    """Unit-tests generate_player_report_pdf() in isolation (extracted
    straight out of app.py by source, not reimplemented), verifying it
    produces a real, well-formed PDF. Kept separate from the AppTest-based
    checks above since Streamlit's DownloadButton test double doesn't expose
    the generated file's raw bytes, only that the button rendered."""
    src = _read_app_src()
    match = re.search(r"def generate_player_report_pdf\(.*?\n    return buffer\.getvalue\(\)\n", src, re.DOTALL)
    assert match, "generate_player_report_pdf() not found in app.py"
    func_src = match.group(0)

    ns = {}
    exec(
        "import io\n"
        "from datetime import datetime\n"
        "from reportlab.lib.pagesizes import A4\n"
        "from reportlab.lib.units import cm\n"
        "from reportlab.lib import colors as pdf_colors\n"
        "from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle\n"
        "from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer\n"
        + func_src,
        ns
    )
    pdf_bytes = ns["generate_player_report_pdf"](
        {"fname": "Test", "lname": "Player", "side": "Left", "player_play_style": "Offensive", "play_style": "Defensive"},
        ["Volley", "Smash"], [8, 7], [6, 5], 75
    )
    assert pdf_bytes[:4] == b"%PDF", f"expected PDF magic bytes, got {pdf_bytes[:20]!r}"
    assert len(pdf_bytes) > 800, "generated PDF looks suspiciously small"


TESTS = [
    test_match_and_training,
    test_admin_no_cross_player_widget_leak,
    test_login_and_admin_pwd,
    test_partner_prefs,
    test_languages,
    test_selected_player_header,
    test_resync,
    test_ux_batch1,
    test_backups_and_restore,
    test_optimistic_locking,
    test_avatars,
    test_analytics_and_pdf,
    test_pdf_generation,
]


def main():
    print(f"Generating test app stubs from {APP_SRC} ...")
    generate_all()
    print("Stubs generated in", GENERATED_DIR)
    print()

    results = []
    for fn in TESTS:
        name = fn.__name__
        print("=" * 70)
        print("RUNNING:", name)
        print("=" * 70)
        try:
            fn()
            print(f"[PASS] {name}")
            results.append((name, True))
        except Exception:
            traceback.print_exc()
            print(f"[FAIL] {name}")
            results.append((name, False))
        print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    all_ok = True
    for name, ok in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if not ok:
            all_ok = False

    shutil.rmtree(GENERATED_DIR, ignore_errors=True)

    if all_ok:
        print(f"\nAll {len(results)} tests passed.")
        return 0
    else:
        print(f"\n{sum(1 for _, ok in results if not ok)} of {len(results)} tests FAILED.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
