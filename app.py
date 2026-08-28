import streamlit as st
import json
import os
import random
from datetime import date, datetime
import pandas as pd

st.set_page_config(page_title="Perfect Human RPG", page_icon="🏰", layout="centered")

# Styling UI RPG Modern Dark Mode
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    .stButton>button { background-color: #4f46e5; color: white; border-radius: 10px; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #6366f1; }
    div[data-testid="stMetricValue"] { font-size: 1.6rem; color: #38bdf8; }
    </style>
""", unsafe_allow_html=True)

# Default Structure Data Karakter
default_data = {
    "name": "Nauval",
    "level": 1,
    "exp": 0,
    "exp_needed": 200,
    "gold": 100,
    "streak": 1,
    "title": "🌱 Novice Initiate",
    "hp": 100, "max_hp": 100,
    "stamina": 100, "max_stamina": 100,
    "stats": {"STR": 10, "INT": 10, "AGI": 10, "VIT": 10},
    "water_ml": 0,
    "quests_done_today": 0,
    "inventory": [],
    "active_buffs": [],
    "journal": [],
    "main_goal": "Menjadi Versi Terbaik Diri Sendiri (Perfect Human)",
    "goal_progress": 0,
    "boss_hp": 500,
    "boss_max_hp": 500,
    "boss_name": "👾 Procrastination Demon",
    # Data Baru Fitur 1-5
    "equipped_items": [],
    "last_gacha_date": "",
    "active_pet": "Tidak Ada",
    "pet_bonus": None,
    "activity_log": []
}

# Inisialisasi Data Karakter & Auto-Fix Struktur Data
if "data" not in st.session_state:
    if os.path.exists("save_data.json"):
        try:
            with open("save_data.json", "r") as f:
                loaded_data = json.load(f)
                for key, val in default_data.items():
                    if key not in loaded_data:
                        loaded_data[key] = val
                st.session_state.data = loaded_data
        except:
            st.session_state.data = default_data
    else:
        st.session_state.data = default_data

d = st.session_state.data

def play_sfx(audio_type):
    # Fitur 5: Sound Effects via Web Audio API
    sounds = {
        "level_up": "https://assets.mixkit.co/active_storage/sfx/2019/2019-preview.mp3",
        "attack": "https://assets.mixkit.co/active_storage/sfx/2764/2764-preview.mp3",
        "gacha": "https://assets.mixkit.co/active_storage/sfx/2000/2000-preview.mp3"
    }
    if audio_type in sounds:
        st.components.v1.html(f"""
            <audio autoplay style="display:none;">
                <source src="{sounds[audio_type]}" type="audio/mpeg">
            </audio>
        """, height=0)

def save_game():
    with open("save_data.json", "w") as f:
        json.dump(d, f)

def log_activity(activity_name, value):
    # Fitur 4: Histori Log untuk Analytics Chart
    today_str = str(date.today())
    d["activity_log"].append({"date": today_str, "activity": activity_name, "value": value})

def update_title():
    if d["level"] >= 30: d["title"] = "👑 THE PERFECT HUMAN EMPEROR"
    elif d["level"] >= 20: d["title"] = "⚔️ Supreme Shadow Knight"
    elif d["level"] >= 10: d["title"] = "🛡️ Guardian of Discipline"
    elif d["level"] >= 5: d["title"] = "📜 Elite Initiate"
    else: d["title"] = "🌱 Novice Initiate"

def add_exp(amount, stat_type=None, stat_gain=1):
    has_double_exp = any(b["name"] == "🧪 Double EXP Elixir" for b in d["active_buffs"])
    if has_double_exp:
        amount *= 2
        st.info("✨ Buff Double EXP Aktif! EXP dilipatgandakan.")

    # Check Equipment Bonus EXP (Fitur 1)
    if "👓 Glasses of Wisdom" in d["equipped_items"] and stat_type == "INT":
        amount = int(amount * 1.1)
        st.info("👓 Glasses of Wisdom memberi bonus +10% EXP!")

    d["exp"] += amount
    d["quests_done_today"] += 1
    d["goal_progress"] = min(100, d["goal_progress"] + 1)
    
    if stat_type and stat_type in d["stats"]:
        d["stats"][stat_type] += stat_gain
    
    while d["exp"] >= d["exp_needed"]:
        d["exp"] -= d["exp_needed"]
        d["level"] += 1
        d["exp_needed"] = int(d["exp_needed"] * 1.3)
        d["max_hp"] += 15
        d["hp"] = d["max_hp"]
        d["max_stamina"] += 15
        d["stamina"] = d["max_stamina"]
        d["gold"] += 50
        update_title()
        play_sfx("level_up")
        st.balloons()
        st.success(f"🎉 LEVEL UP! Selamat Nauval naik ke Level {d['level']}! (+50 Gold, Stat Boost)")
    save_game()

def apply_penalty(hp_loss, exp_loss):
    has_shield = any(b["name"] == "🛡️ Focus Shield Buff" for b in d["active_buffs"])
    if has_shield:
        st.warning("🛡️ Focus Shield melindungi Nauval dari hukuman!")
        return

    # Check Equipment Mitigation (Fitur 1)
    if "🛡️ Shield of Iron Will" in d["equipped_items"]:
        hp_loss = int(hp_loss * 0.8)
        exp_loss = int(exp_loss * 0.8)
        st.info("🛡️ Shield of Iron Will mengurangi 20% dampak hukuman!")

    d["hp"] = max(0, d["hp"] - hp_loss)
    d["exp"] = max(0, d["exp"] - exp_loss)
    save_game()
    st.error(f"⚠️ Hukuman Diterima: -{hp_loss} HP | -{exp_loss} EXP")

# --- HEADER STATUS KARAKTER ---
st.title(f"🏰 KETUA {d['name'].upper()}")
st.caption(f"Gelar Kedisiplinan: **{d['title']}** | Pet: **{d['active_pet']}**")

# MAIN GOAL BAR
st.subheader(f"🎯 Main Goal: {d['main_goal']}")
st.progress(d["goal_progress"] / 100, text=f"Progres Tujuan Utama: {d['goal_progress']}%")

st.divider()

# Bar EXP
st.progress(min(d["exp"] / d["exp_needed"], 1.0), text=f"EXP: {d['exp']} / {d['exp_needed']} (Level {d['level']})")

# Visual Bar Meter Status Utama
col_hp, col_sta = st.columns(2)
with col_hp:
    st.caption(f"❤️ Health (HP): {d['hp']}/{d['max_hp']}")
    st.progress(min(d['hp'] / d['max_hp'], 1.0))
with col_sta:
    st.caption(f"⚡ Stamina: {d['stamina']}/{d['max_stamina']}")
    st.progress(min(d['stamina'] / d['max_stamina'], 1.0))

# Status Atribut & Keuangan
c1, c2, c3, c4 = st.columns(4)
c1.metric("🪙 Gold", f"{d['gold']}")
c2.metric("🔥 Streak", f"{d['streak']} Hr")
c3.metric("💧 Air", f"{d['water_ml']} ml")
c4.metric("⚔️ Quest", f"{d['quests_done_today']}")

# Tampilan Buff & Equipment Aktif
if d["active_buffs"] or d["equipped_items"]:
    st.write("✨ **Buff & Equipment Aktif:**")
    for buff in d["active_buffs"]:
        st.success(f"• **{buff['name']}** (Aktif s.d {buff['expires']})")
    for eq in d["equipped_items"]:
        st.info(f"🛡️ Equipment Dipakai: **{eq}**")

# Detail Stats Atribut RPG
with st.expander("📊 Lihat Atribut & Kekuatan Karakter (STR, INT, AGI, VIT)", expanded=True):
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("🏋️ STR (Fisik)", d["stats"]["STR"])
    s2.metric("📚 INT (Otak)", d["stats"]["INT"])
    s3.metric("⚡ AGI (Gesit)", d["stats"]["AGI"])
    s4.metric("🛡️ VIT (Daya Tahan)", d["stats"]["VIT"])

st.divider()

# --- TAB UTAMA APLIKASI ---
tab_quest, tab_boss, tab_penalty, tab_shop, tab_journal, tab_equips, tab_gacha, tab_pet, tab_analytics = st.tabs([
    "⚔️ Quest & Rutinitas",
    "👾 Boss & Dungeon", 
    "🚨 Hukuman", 
    "🧪 Toko Potion", 
    "📓 Jurnal",
    "🗡️ Equipment",
    "🎡 Daily Gacha",
    "🐾 Pet Companion",
    "📈 Analytics"
])

# ================= TAB 1: QUEST DENGAN CUSTOM DURASI =================
with tab_quest:
    st.subheader("📌 Misi Kedisiplinan Harian")
    
    with st.expander("📚 1. Sesi Belajar & Skill (Input Durasi Jam)", expanded=True):
        study_hours = st.number_input("Berapa jam Nauval belajar/fokus hari ini?", min_value=0.5, max_value=12.0, value=1.0, step=0.5, key="study_h")
        gained_exp_study = int(study_hours * 100)
        gained_gold_study = int(study_hours * 25)
        stamina_cost_study = int(study_hours * 20)
        gained_int = int(study_hours * 2)

        st.caption(f"🎁 Hadiah: +{gained_exp_study} EXP | +{gained_gold_study} Gold | +{gained_int} INT | -{stamina_cost_study} Stamina")
        
        if st.button(f"🚀 Selesaikan Belajar ({study_hours} Jam)", use_container_width=True):
            if d["stamina"] >= stamina_cost_study:
                d["stamina"] -= stamina_cost_study
                d["gold"] += gained_gold_study
                add_exp(gained_exp_study, "INT", gained_int)
                log_activity("Belajar (Jam)", study_hours)
                st.success(f"Luar biasa! Belajar {study_hours} Jam selesai.")
                st.rerun()
            else:
                st.warning("Stamina Nauval tidak cukup! Harap minum Potion atau istirahat.")

    with st.expander("🏋️ 2. Olahraga & Latihan Fisik (Input Menit)"):
        workout_mins = st.number_input("Berapa menit Nauval berolahraga/gym/pushup?", min_value=10, max_value=180, value=30, step=10, key="work_m")
        gained_exp_work = int(workout_mins * 2.5)
        gained_gold_work = int(workout_mins * 0.6)
        stamina_cost_work = int(workout_mins * 0.5)
        gained_str = max(1, int(workout_mins / 20))

        st.caption(f"🎁 Hadiah: +{gained_exp_work} EXP | +{gained_gold_work} Gold | +{gained_str} STR | -{stamina_cost_work} Stamina")

        if st.button(f"🏋️ Selesaikan Workout ({workout_mins} Menit)", use_container_width=True):
            if d["stamina"] >= stamina_cost_work:
                d["stamina"] -= stamina_cost_work
                d["gold"] += gained_gold_work
                add_exp(gained_exp_work, "STR", gained_str)
                log_activity("Workout (Menit)", workout_mins)
                st.success(f"Fisik semakin kuat! Workout {workout_mins} Mnt selesai.")
                st.rerun()
            else:
                st.warning("Stamina Nauval tidak cukup!")

    with st.expander("📖 3. Membaca Buku & Literasi (Input Menit)"):
        read_mins = st.number_input("Berapa menit Nauval membaca buku hari ini?", min_value=10, max_value=180, value=20, step=5, key="read_m")
        gained_exp_read = int(read_mins * 2)
        gained_int_read = max(1, int(read_mins / 20))

        st.caption(f"🎁 Hadiah: +{gained_exp_read} EXP | +{gained_int_read} INT")

        if st.button(f"📖 Selesaikan Membaca ({read_mins} Menit)", use_container_width=True):
            add_exp(gained_exp_read, "INT", gained_int_read)
            log_activity("Membaca (Menit)", read_mins)
            st.success(f"Wawasan bertambah! Membaca {read_mins} Mnt selesai.")
            st.rerun()

    with st.expander("🕌 4. Spiritual, Hidrasi & Kebersihan"):
        if st.button("🕌 Solat Fardhu Tepat Waktu (+80 EXP, +15 Gold, +1 VIT)", use_container_width=True):
            d["gold"] += 15
            add_exp(80, "VIT", 1)
            st.rerun()

        if st.button("💧 Minum Air 500ml (+20 EXP, +5 HP, +1 VIT)", use_container_width=True):
            d["water_ml"] += 500
            d["hp"] = min(d["max_hp"], d["hp"] + 5)
            add_exp(20, "VIT", 1)
            st.rerun()

        if st.button("😴 Tidur & Istirahat Berkualitas (Pulihkan HP & Stamina)", use_container_width=True):
            d["stamina"] = d["max_stamina"]
            d["hp"] = d["max_hp"]
            save_game()
            st.success("HP dan Stamina Nauval telah pulih sepenuhnya!")
            st.rerun()

# ================= TAB 2: BOSS & DUNGEON (SERANGAN MONSTER) =================
with tab_boss:
    st.subheader(f"⚔️ Dungeon RAID: {d['boss_name']}")
    st.caption("Kalahkan monster rasa malas & penundaan untuk mendapatkan EXP & Gold melimpah!")
    
    st.progress(max(0.0, min(d["boss_hp"] / d["boss_max_hp"], 1.0)), text=f"HP Boss: {d['boss_hp']} / {d['boss_max_hp']}")

    # Check Base Damage & Pet / Equipment Boost
    base_damage = d["stats"]["STR"] * 2 + d["stats"]["INT"] * 2
    if "🗡️ Steel Sword of Focus" in d["equipped_items"]:
        base_damage = int(base_damage * 1.15)
    if d["active_pet"] == "🐺 Spirit Wolf":
        base_damage += 25

    st.info(f"💥 Total Damage Serangan Nauval: **{base_damage} HP** (Bonus Equipment & Pet Termasuk)")

    if st.button(f"⚔️ Serang {d['boss_name']} (-20 Stamina)", use_container_width=True):
        if d["stamina"] >= 20:
            play_sfx("attack")
            d["stamina"] -= 20
            d["boss_hp"] -= base_damage
            if d["boss_hp"] <= 0:
                play_sfx("level_up")
                st.balloons()
                st.success(f"🔥 VICTORY! Nauval telah mengalahkan {d['boss_name']}! (+250 EXP, +100 Gold)")
                d["gold"] += 100
                add_exp(250)
                # Respawn Boss Baru
                d["boss_max_hp"] = int(d["boss_max_hp"] * 1.4)
                d["boss_hp"] = d["boss_max_hp"]
                if d["boss_name"] == "👾 Procrastination Demon":
                    d["boss_name"] = "🐉 Distraction Overlord"
                else:
                    d["boss_name"] = "👹 Chaos Lord of Laziness"
            else:
                st.success(f"Serangan berhasil! Memberikan {base_damage} damage ke Boss.")
            save_game()
            st.rerun()
        else:
            st.warning("Stamina Nauval tidak cukup untuk menyerang Boss!")

# ================= TAB 3: PENALTY DENGAN CUSTOM WAKTU =================
with tab_penalty:
    st.subheader("🚨 Fitur Hukuman Pelanggaran Kedisiplinan")

    sosmed_mins = st.number_input("Berapa menit Nauval scrol sosmed / buang waktu?", min_value=15, max_value=300, value=30, step=15, key="sos_m")
    lost_hp_sosmed = int(sosmed_mins * 0.8)
    lost_exp_sosmed = int(sosmed_mins * 2)

    if st.button(f"⚠️ Laporkan Scrol Sosmed ({sosmed_mins} Mnt) -> -{lost_hp_sosmed} HP | -{lost_exp_sosmed} EXP", use_container_width=True):
        apply_penalty(lost_hp_sosmed, lost_exp_sosmed)
        st.rerun()

# ================= TAB 4: TOKO POTION & BUFF =================
with tab_shop:
    st.subheader("🧪 Toko Ramuan Magic & Buff Kedisiplinan")
    st.caption("Tukarkan Gold hasil kerja keras Nauval untuk membeli Potion berdurasi jam!")

    potions = [
        {"name": "⚡ Vitality Potion", "cost": 60, "desc": "Pemulihan Instan +50 Stamina", "type": "instant_stamina", "val": 50},
        {"name": "❤️ Health Potion", "cost": 60, "desc": "Pemulihan Instan +50 HP", "type": "instant_hp", "val": 50},
        {"name": "🧪 Double EXP Elixir", "cost": 150, "desc": "EXP 2x Lipat dari semua Quest (Berlaku 2 Jam)", "type": "buff", "duration": 2},
        {"name": "🛡️ Focus Shield Buff", "cost": 120, "desc": "Kebal dari Hukuman Sosmed/Distraksi (Berlaku 4 Jam)", "type": "buff", "duration": 4},
        {"name": "👑 Crown of Focus", "cost": 300, "desc": "Meningkatkan Semua Stat +2 secara sementara (Berlaku 24 Jam)", "type": "buff", "duration": 24},
    ]

    for p in potions:
        with st.container():
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"**{p['name']}** — 🪙 **{p['cost']} Gold**\n\n*{p['desc']}*")
            if col2.button("Beli & Pakai", key=p["name"]):
                if d["gold"] >= p["cost"]:
                    d["gold"] -= p["cost"]
                    
                    if p["type"] == "instant_stamina":
                        d["stamina"] = min(d["max_stamina"], d["stamina"] + p["val"])
                        st.success(f"Berhasil menggunakan {p['name']}! Stamina +{p['val']}")
                    elif p["type"] == "instant_hp":
                        d["hp"] = min(d["max_hp"], d["hp"] + p["val"])
                        st.success(f"Berhasil menggunakan {p['name']}! HP +{p['val']}")
                    elif p["type"] == "buff":
                        d["active_buffs"].append({
                            "name": p["name"],
                            "expires": f"{p['duration']} Jam ke depan"
                        })
                        st.success(f"Buff {p['name']} aktif selama {p['duration']} Jam!")

                    save_game()
                    st.rerun()
                else:
                    st.error("Gold Nauval tidak cukup!")
        st.divider()

# ================= TAB 5: JURNAL & CATATAN =================
with tab_journal:
    st.subheader("📓 Jurnal Evaluation & Reflection")
    j_input = st.text_area("Tuliskan pencapaian, rasa syukur, atau evaluasi hari ini:")
    if st.button("Simpan Jurnal (+30 EXP, +1 INT)", use_container_width=True):
        if j_input.strip():
            today = str(date.today())
            d["journal"].append({"date": today, "note": j_input})
            add_exp(30, "INT", 1)
            st.success("Jurnal berhasil disimpan!")
            st.rerun()

    st.divider()
    st.write("📜 **Riwayat Jurnal Nauval:**")
    for j in reversed(d["journal"][-5:]):
        st.info(f"📅 **{j['date']}**\n\n{j['note']}")

# ================= TAB 6: FITUR 1 - EQUIPS & ARMORS =================
with tab_equips:
    st.subheader("🗡️ Armory & Equipment RPG")
    st.caption("Gunakan perlengkapan permanen untuk meningkatkan performa karakter Nauval!")
    
    equips_list = [
        {"name": "🗡️ Steel Sword of Focus", "cost": 250, "desc": "Menambah +15% Damage saat melawan Boss Dungeon."},
        {"name": "🛡️ Shield of Iron Will", "cost": 200, "desc": "Mengurangi efek Hukuman (HP & EXP loss) sebesar 20%."},
        {"name": "👓 Glasses of Wisdom", "cost": 180, "desc": "Bonus +10% EXP dari setiap Quest Belajar/Membaca."}
    ]

    for eq in equips_list:
        with st.container():
            col1, col2 = st.columns([3, 1])
            col1.markdown(f"**{eq['name']}** — 🪙 **{eq['cost']} Gold**\n\n*{eq['desc']}*")
            if eq["name"] in d["equipped_items"]:
                col2.button("Terpasang ✅", key=eq["name"], disabled=True)
            else:
                if col2.button("Beli & Equip", key=eq["name"]):
                    if d["gold"] >= eq["cost"]:
                        d["gold"] -= eq["cost"]
                        d["equipped_items"].append(eq["name"])
                        save_game()
                        st.success(f"Berhasil melengkapi {eq['name']}!")
                        st.rerun()
                    else:
                        st.error("Gold tidak cukup!")
        st.divider()

# ================= TAB 7: FITUR 2 - DAILY GACHA =================
with tab_gacha:
    st.subheader("🎡 Roda Keberuntungan Harian (Daily Spin)")
    today_str = str(date.today())
    
    if d["last_gacha_date"] == today_str:
        st.info("⏰ Nauval sudah melakukan Spin hari ini. Kembali lagi besok!")
    else:
        st.write("Putar roda keberuntungan gratis 1x setiap hari untuk mendapatkan reward acak!")
        if st.button("🎰 Putar Spin Harian", use_container_width=True):
            play_sfx("gacha")
            d["last_gacha_date"] = today_str
            rewards = [
                ("🪙 Bonus Gold Melimpah (+100 Gold)", "gold", 100),
                ("⚡ Potion Stamina Instan (+50 Stamina)", "stamina", 50),
                ("✨ Bonus EXP Gratis (+150 EXP)", "exp", 150),
                ("💣 Zonk! Terlambat bangun (-10 HP)", "hp", -10)
            ]
            chosen = random.choice(rewards)
            st.success(f"🎉 Result: {chosen[0]}")
            
            if chosen[1] == "gold": d["gold"] += chosen[2]
            elif chosen[1] == "stamina": d["stamina"] = min(d["max_stamina"], d["stamina"] + chosen[2])
            elif chosen[1] == "exp": add_exp(chosen[2])
            elif chosen[1] == "hp": d["hp"] = max(0, d["hp"] + chosen[2])
            
            save_game()
            st.rerun()

# ================= TAB 8: FITUR 3 - PET COMPANION =================
with tab_pet:
    st.subheader("🐾 Pet Companion System")
    st.caption("Pilih pendamping setia yang memberikan buff pasif harian!")
    
    pets = [
        {"name": "🦉 Baby Owl of Wisdom", "cost": 150, "desc": "Memberikan +1 INT tambahan gratis tiap sesi belajar."},
        {"name": "🐺 Spirit Wolf", "cost": 220, "desc": "Memberikan +25 Damage tambahan di Dungeon Boss."},
        {"name": "🐢 Shield Turtle", "cost": 180, "desc": "Menambah Max HP sebesar +30 secara permanen."}
    ]

    for p in pets:
        with st.container():
            c_p1, c_p2 = st.columns([3, 1])
            c_p1.markdown(f"**{p['name']}** — 🪙 **{p['cost']} Gold**\n\n*{p['desc']}*")
            if d["active_pet"] == p["name"]:
                c_p2.button("Aktif 🐾", key="pet_"+p["name"], disabled=True)
            else:
                if c_p2.button("Adopt Pet", key="pet_"+p["name"]):
                    if d["gold"] >= p["cost"]:
                        d["gold"] -= p["cost"]
                        d["active_pet"] = p["name"]
                        if p["name"] == "🐢 Shield Turtle":
                            d["max_hp"] += 30
                            d["hp"] += 30
                        save_game()
                        st.success(f"Berhasil mengadopsi {p['name']}!")
                        st.rerun()
                    else:
                        st.error("Gold tidak cukup!")
        st.divider()

# ================= TAB 9: FITUR 4 - ANALYTICS CHART =================
with tab_analytics:
    st.subheader("📈 Visualisasi & Analytics Kedisiplinan")
    st.caption("Pantau perkembangan fokus dan aktivitas harian Nauval!")
    
    if d["activity_log"]:
        df = pd.DataFrame(d["activity_log"])
        st.write("📊 **Grafik Aktivitas Kedisiplinan:**")
        st.bar_chart(df, x="date", y="value", color="activity")
    else:
        st.info("Belum ada data aktivitas yang tersimpan. Selesaikan Quest untuk merekam grafik!")
