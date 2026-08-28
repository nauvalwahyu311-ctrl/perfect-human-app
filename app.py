import streamlit as st
import json
import os
import random
from datetime import date, datetime
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Perfect Human RPG", page_icon="🏰", layout="centered")

# ==========================================
# 🎨 STYLING UI RPG MODERN DARK MODE (ENHANCED)
# ==========================================
st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%); 
        color: #f8fafc; 
    }
    h1 {
        color: #38bdf8;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    .stButton>button { 
        background: linear-gradient(90deg, #4f46e5 0%, #6366f1 100%); 
        color: white; 
        border-radius: 8px; 
        font-weight: bold; 
        border: 1px solid #818cf8;
        box-shadow: 0px 4px 10px rgba(79, 70, 229, 0.3);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(99, 102, 241, 0.5);
        background: linear-gradient(90deg, #6366f1 0%, #4f46e5 100%);
    }
    div[data-testid="stMetricValue"] { 
        font-size: 1.8rem; 
        color: #38bdf8; 
        font-weight: bold;
    }
    .rpg-box {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ⚙️ DATA STRUCTURE & INITIALIZATION
# ==========================================
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
    "skill_points": 0,
    "skills": {
        # Cabang Scholar
        "quick_reader": 0,
        "notes_keeper": 0,
        "hyperfocus": 0,
        "coffee_efficiency": 0,
        "memory_palace": 0,
        "exam_crusher": 0,
        # Cabang Warrior
        "warm_up": 0,
        "cardio_boost": 0,
        "iron_skin": 0,
        "athletic_body": 0,
        "adrenaline_rush": 0,
        "second_wind": 0,
        # Cabang Merchant
        "bargain_hunter": 0,
        "streak_multiplier_skill": 0,
        "gold_digger": 0,
        "armory_discount": 0,
        "lucky_charm": 0,
        # Cabang Guardian
        "willpower": 0,
        "distraction_barrier": 0,
        "absorb_harm": 0,
        "unshakable_focus": 0,
        # Cabang Beastmaster
        "animal_lover": 0,
        "pet_training": 0,
        "pack_mentality": 0,
        "loyal_companion": 0
    },
    "active_skills_cd": {
        "omniscience": 0,
        "titan_form": 0,
        "midas_touch": 0,
        "awakened_beast": 0
    },
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
    "boss_defeated_count": 0,
    "equipped_items": [],
    "last_gacha_date": "",
    "active_pet": "Tidak Ada",
    "pet_bonus": None,
    "activity_log": [],
    "custom_quests": [],
    "achievements": [],
    "total_study_hours": 0.0,
    "total_worship_count": 0,
    "last_weekly_reset": "",
    "daily_event": None,
    "last_event_date": ""
}

if "data" not in st.session_state:
    if os.path.exists("save_data.json"):
        try:
            with open("save_data.json", "r") as f:
                st.session_state.data = json.load(f)
        except:
            st.session_state.data = default_data
    else:
        st.session_state.data = default_data

d = st.session_state.data

# Safety Check
for key, val in default_data.items():
    if key not in d:
        d[key] = val
for sk_key, sk_val in default_data["skills"].items():
    if sk_key not in d["skills"]:
        d["skills"][sk_key] = sk_val

# ==========================================
# 🛠️ HELPER FUNCTIONS
# ==========================================
def play_sfx(audio_type):
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
    today_str = str(date.today())
    d["activity_log"].append({"date": today_str, "activity": activity_name, "value": value})

def update_title():
    if d["level"] >= 30: d["title"] = "👑 THE PERFECT HUMAN EMPEROR"
    elif d["level"] >= 20: d["title"] = "⚔️ Supreme Shadow Knight"
    elif d["level"] >= 10: d["title"] = "🛡️ Guardian of Discipline"
    elif d["level"] >= 5: d["title"] = "📜 Elite Initiate"
    else: d["title"] = "🌱 Novice Initiate"

def check_achievements():
    now = datetime.now()
    current_year_week = f"{now.year}-W{now.isocalendar()[1]}"
    
    if d["last_weekly_reset"] != current_year_week:
        d["last_weekly_reset"] = current_year_week
        d["achievements"] = [a for a in d["achievements"] if not a.endswith("(Weekly Target)")]

    new_achievements = []

    if d["total_study_hours"] >= 10.0 and "📚 Bookworm Master" not in d["achievements"]:
        new_achievements.append("📚 Bookworm Master")
    
    if d["streak"] >= 7 and "🔥 Iron Warrior (7 Days Streak)" not in d["achievements"]:
        new_achievements.append("🔥 Iron Warrior (7 Days Streak)")
        
    if d["boss_defeated_count"] >= 5 and "⚔️ Demon Slayer Elite" not in d["achievements"]:
        new_achievements.append("⚔️ Demon Slayer Elite")

    if d.get("total_worship_count", 0) >= 10 and "🕌 Spiritual Devotee" not in d["achievements"]:
        new_achievements.append("🕌 Spiritual Devotee")

    if d["quests_done_today"] >= 5 and "🎯 Weekly Champion (Weekly Target)" not in d["achievements"]:
        new_achievements.append("🎯 Weekly Champion (Weekly Target)")

    for ach in new_achievements:
        d["achievements"].append(ach)
        st.toast(f"🏆 ACHIEVEMENT UNLOCKED: {ach}!", icon="🎉")
        d["gold"] += 100
        save_game()

def add_exp(amount, stat_type=None, stat_gain=1):
    # Skill: Omniscience (3x EXP)
    has_omniscience = any(b["name"] == "✨ Omniscience Buff (3x EXP)" for b in d["active_buffs"])
    if has_omniscience and stat_type == "INT":
        amount *= 3
        st.info("🔮 Skill Omniscience Aktif! 3x EXP Belajar diperoleh.")

    # Buff item Double EXP
    has_double_exp = any(b["name"] == "🧪 Double EXP Elixir" for b in d["active_buffs"])
    if has_double_exp:
        amount *= 2
        st.info("✨ Buff Double EXP Aktif! EXP dilipatgandakan.")

    # FITUR 1: Real-Time Early Bird Buff
    current_hour = datetime.now().hour
    if 5 <= current_hour <= 8 and stat_type == "INT":
        amount = int(amount * 1.3)
        st.info("🌅 Buff Early Bird Aktif! +30% Extra EXP Belajar Pagi Hari.")

    # Synergy Perfect Balance
    if d["stats"]["STR"] >= 30 and d["stats"]["INT"] >= 30 and d["stats"]["AGI"] >= 30 and d["stats"]["VIT"] >= 30:
        amount = int(amount * 1.25)

    # Synergy Mind & Muscle
    if d["stats"]["STR"] >= 25 and d["stats"]["INT"] >= 25:
        amount = int(amount * 1.15)

    # Skill Beastmaster Pack Mentality
    if d["skills"]["pack_mentality"] > 0 and d["active_pet"] != "Tidak Ada":
        amount = int(amount * 1.10)

    if d["daily_event"] and d["daily_event"]["type"] == "exp_boost":
        amount = int(amount * d["daily_event"]["val"])

    if "👓 Glasses of Wisdom" in d["equipped_items"] and stat_type == "INT":
        amount = int(amount * 1.1)
    if "🎧 Noise-Canceling Headphones" in d["equipped_items"] and stat_type == "INT":
        amount = int(amount * 1.2)
        st.info("🎧 Headphones aktif! +20% Extra EXP Belajar.")

    d["exp"] += amount
    d["quests_done_today"] += 1
    d["goal_progress"] = min(100, d["goal_progress"] + 1)
    
    if stat_type and stat_type in d["stats"]:
        pet_bonus = 1 if (d["active_pet"] == "🦉 Baby Owl of Wisdom" and stat_type == "INT") else 0
        pet_stat_bonus = 2 if (d["active_pet"] == "🦅 Golden Eagle of Vision" and stat_type in ["STR", "INT"]) else 0
        
        # Skill Pet Training multiplier
        if d["skills"]["pet_training"] > 0 and (pet_bonus > 0 or pet_stat_bonus > 0):
            pet_bonus = int(pet_bonus * 1.5)
            pet_stat_bonus = int(pet_stat_bonus * 1.5)

        d["stats"][stat_type] += (stat_gain + pet_bonus + pet_stat_bonus)
    
    # Calculate Max Stamina including Memory Palace Skill
    base_max_sta = 100 + (d["level"] * 15)
    if d["skills"]["memory_palace"] > 0:
        base_max_sta += 25
    d["max_stamina"] = base_max_sta

    while d["exp"] >= d["exp_needed"]:
        d["exp"] -= d["exp_needed"]
        d["level"] += 1
        d["skill_points"] += 1
        d["exp_needed"] = int(d["exp_needed"] * 1.3)
        d["max_hp"] += 15
        d["hp"] = d["max_hp"]
        d["stamina"] = d["max_stamina"]
        d["gold"] += 50
        update_title()
        play_sfx("level_up")
        st.balloons()
        st.success(f"🎉 LEVEL UP! Nauval naik ke Level {d['level']}! (+50 Gold, +1 Skill Point)")
    
    check_achievements()
    save_game()

def apply_penalty(hp_loss, exp_loss):
    # Skill Guardian: Distraction Barrier (EXP Loss Immunity)
    if d["skills"]["distraction_barrier"] > 0:
        exp_loss = 0
        st.info("🛡️ Skill Distraction Barrier mencegah pengurangan EXP!")

    if "🛡️ Potion Kebal Penundaan" in d["inventory"]:
        d["inventory"].remove("🛡️ Potion Kebal Penundaan")
        st.success("🛡️ Potion Kebal Penundaan digunakan otomatis! Hukuman dibatalkan.")
        save_game()
        return

    # FITUR 1: Real-Time Jam Kalong Debuff (Penalti HP bertambah saat malam hari)
    current_hour = datetime.now().hour
    if current_hour >= 22 or current_hour < 4:
        hp_loss = int(hp_loss * 1.2)
        st.error("🌙 Debuff Jam Kalong! Kerusakan HP meningkat 20% karena dilakukan di malam hari.")

    d["hp"] = max(0, d["hp"] - hp_loss)
    d["exp"] = max(0, d["exp"] - exp_loss)
    save_game()

# ==========================================
# 🕒 DISPLAY HEADER & REAL-TIME BUFF BANNER
# ==========================================
st.title("🏰 Perfect Human RPG")
st.caption(f"Selamat Datang kembali, **{d['name']}**! Status: **{d['title']}**")

# Banner Tampilan Fitur 1 (Real-Time Time System)
current_hour = datetime.now().hour
now_str = datetime.now().strftime("%H:%M")

if 5 <= current_hour <= 8:
    st.info(f"🌅 **[ Jam {now_str} ] - Buff Early Bird Aktif!** Belajar di pagi hari memberikan bonus +30% EXP INT.")
elif current_hour >= 22 or current_hour < 4:
    st.error(f"🌙 **[ Jam {now_str} ] - Debuff Jam Kalong!** Melakukan pelanggaran/hukuman di malam hari memberikan ekstra 20% kerusakan HP.")
else:
    st.caption(f"🕒 Jam Sistem: **{now_str} WIB** (Kondisi Waktu Normal)")

    has_shield = any(b["name"] == "🛡️ Focus Shield Buff" for b in d["active_buffs"])
    if has_shield:
        st.warning("🛡️ Focus Shield melindungi Nauval dari hukuman!")
        return

    # Skill Warrior: Iron Skin
    if d["skills"]["iron_skin"] > 0:
        hp_loss = int(hp_loss * 0.85)

    # Skill Guardian: Willpower
    if d["skills"]["willpower"] > 0:
        hp_loss = int(hp_loss * 0.90)

    # Synergy Iron Will
    if d["stats"]["VIT"] >= 25 and d["streak"] >= 7:
        hp_loss = int(hp_loss * 0.5)

    if "🛡️ Shield of Iron Will" in d["equipped_items"]:
        hp_loss = int(hp_loss * 0.8)
        exp_loss = int(exp_loss * 0.8)

    if d["active_pet"] == "🐈‍⬛ Shadow Cat of Discipline":
        hp_loss = int(hp_loss * 0.75)
        st.info("🐈‍⬛ Shadow Cat mengurangi 25% hukuman HP!")

    # Skill Guardian: Absorb Harm (Convert HP loss to stamina recovery)
    if d["skills"]["absorb_harm"] > 0:
        recovered = int(hp_loss * 0.2)
        d["stamina"] = min(d["max_stamina"], d["stamina"] + recovered)
        st.info(f"⚡ Skill Absorb Harm menyerap damage menjadi +{recovered} Stamina!")

    d["hp"] -= hp_loss
    d["exp"] = max(0, d["exp"] - exp_loss)

    # Skill Warrior: Second Wind (HP Auto Revive)
    if d["hp"] <= 0:
        if d["skills"]["second_wind"] > 0:
            d["hp"] = int(d["max_hp"] * 0.3)
            st.warning("🔥 Skill Second Wind teruji! Nauval bangkit dari kematian dengan 30% HP!")
        else:
            d["hp"] = 0

    save_game()
    st.error(f"⚠️ Hukuman Diterima: -{hp_loss} HP | -{exp_loss} EXP")

def trigger_daily_event():
    today_str = str(date.today())
    if d["last_event_date"] != today_str:
        d["last_event_date"] = today_str
        events = [
            {"name": "🌧️ Hujan Deras", "desc": "+20% EXP Belajar hari ini!", "type": "exp_boost", "val": 1.2},
            {"name": "🪙 Penemu Koin", "desc": "Menemukan koin kuno! (+50 Gold)", "type": "gold", "val": 50},
            {"name": "☀️ Cuaca Cerah", "desc": "Stamina Pulih Sepenuhnya!", "type": "stamina", "val": d["max_stamina"]},
            {"name": "☕ Kafe Diskon", "desc": "Semangat membara! +10 Stamina Bonus", "type": "stamina_bonus", "val": 10}
        ]
        chosen = random.choice(events)
        d["daily_event"] = chosen
        if chosen["type"] == "gold":
            d["gold"] += chosen["val"]
        elif chosen["type"] == "stamina":
            d["stamina"] = d["max_stamina"]
        save_game()

# Synchronize System Time & Random Event
check_achievements()
trigger_daily_event()

# ==========================================
# 🎛️ SIDEBAR CONTROL & SYSTEM
# ==========================================
with st.sidebar:
    st.header("⚙️ Pengaturan RPG")
    st.write(f"User: **{d['name']}**")
    st.write(f"Waktu Real-Time: **{datetime.now().strftime('%Y-%m-%d %H:%M')}**")
    st.write(f"Minggu Ke: **{datetime.now().isocalendar()[1]}**")
    st.divider()
    
    if st.button("💾 Simpan Game Manual"):
        save_game()
        st.success("Data berhasil disimpan!")

    st.divider()
    st.subheader("📦 Export & Backup Data")
    
    json_data = json.dumps(d, indent=4)
    st.download_button(
        label="📥 Download Save Data (JSON)",
        data=json_data,
        file_name=f"save_data_{date.today()}.json",
        mime="application/json",
        use_container_width=True
    )
    
    if d["activity_log"]:
        df_log = pd.DataFrame(d["activity_log"])
        csv_data = df_log.to_csv(index=False)
        st.download_button(
            label="📊 Export Log Aktivitas (CSV)",
            data=csv_data,
            file_name=f"activity_log_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.divider()
    with st.expander("🚨 Zona Bahaya (Reset Game)"):
        st.caption("Untuk mereset seluruh data, ketik kata **yakin** sebanyak 3 kali dipisah spasi: `yakin yakin yakin`")
        confirm_code = st.text_input("Kode Konfirmasi Reset", value="", placeholder="yakin yakin yakin", key="reset_code_input")
        if st.button("⚠️ Reset Seluruh Data", use_container_width=True):
            if confirm_code.strip() == "yakin yakin yakin":
                if os.path.exists("save_data.json"):
                    os.remove("save_data.json")
                st.session_state.data = default_data
                st.rerun()
            else:
                st.error("Kode konfirmasi salah! Ketik 'yakin yakin yakin' untuk melanjutkan.")

# ==========================================
# 🏰 HEADER STATUS KARAKTER
# ==========================================
st.title(f"🏰 KETUA {d['name'].upper()}")
st.caption(f"Gelar Kedisiplinan: **{d['title']}** | Pet: **{d['active_pet']}**")

if d["daily_event"]:
    st.warning(f"🎲 **Peristiwa Hari Ini:** {d['daily_event']['name']} — {d['daily_event']['desc']}")

st.subheader(f"🎯 Main Goal: {d['main_goal']}")
st.progress(d["goal_progress"] / 100, text=f"Progres Utama: {d['goal_progress']}%")

st.divider()

exp_ratio = min(d["exp"] / d["exp_needed"], 1.0)
st.progress(exp_ratio, text=f"EXP: {d['exp']} / {d['exp_needed']} (Level {d['level']})")

col_hp, col_sta = st.columns(2)
with col_hp:
    st.caption(f"❤️ Health (HP): {d['hp']}/{d['max_hp']}")
    st.progress(min(max(0.0, d['hp'] / d['max_hp']), 1.0))
with col_sta:
    st.caption(f"⚡ Stamina: {d['stamina']}/{d['max_stamina']}")
    st.progress(min(max(0.0, d['stamina'] / d['max_stamina']), 1.0))

c1, c2, c3, c4 = st.columns(4)
streak_bonus_mult = 2 if "💍 Ring of Consistency" in d["equipped_items"] else 1
if d["skills"]["streak_multiplier_skill"] > 0:
    streak_bonus_mult += int(d["streak"] / 5) * 0.15

c1.metric("🪙 Gold", f"{d['gold']}")
c2.metric("🔥 Streak", f"{d['streak']} Hr (x{round(streak_bonus_mult, 2)})")
c3.metric("💧 Air", f"{d['water_ml']} ml")
c4.metric("⚔️ Quest", f"{d['quests_done_today']}")

if d["active_buffs"] or d["equipped_items"] or d["inventory"]:
    st.write("✨ **Buff, Inventory & Equipment:**")
    for buff in d["active_buffs"]:
        st.success(f"• Buff: **{buff['name']}** ({buff['expires']})")
    for eq in d["equipped_items"]:
        st.info(f"🛡️ Equipment: **{eq}**")
    for inv in d["inventory"]:
        st.warning(f"🎒 Item Storage: **{inv}**")

with st.expander("📊 Lihat Atribut & Skill Karakter", expanded=False):
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("🏋️ STR", d["stats"]["STR"])
    s2.metric("📚 INT", d["stats"]["INT"])
    s3.metric("⚡ AGI", d["stats"]["AGI"])
    s4.metric("🛡️ VIT", d["stats"]["VIT"])

st.divider()

# ==========================================
# 📑 TAB UTAMA APLIKASI
# ==========================================
tab_quest, tab_skill, tab_boss, tab_penalty, tab_shop, tab_equips, tab_gacha, tab_pet, tab_achieve, tab_analytics = st.tabs([
    "⚔️ Quest", "🌳 Skill Tree", "👾 Boss", "🚨 Penalty", "🧪 Shop", "🗡️ Armory", "🎡 Gacha", "🐾 Pet", "🏆 Badges", "📈 Analytics"
])

# ================= TAB 1: QUEST =================
with tab_quest:
    st.subheader("📌 Misi Kedisiplinan Harian")
    
    # --- QUEST 1: BELAJAR ---
    with st.expander("📚 1. Sesi Belajar & Skill", expanded=True):
        study_hours = st.number_input("Berapa jam belajar hari ini?", min_value=0.5, max_value=12.0, value=1.0, step=0.5)
        
        # Skill Quick Reader
        base_cost_rate = 20 - (5 if d["skills"]["quick_reader"] > 0 and study_hours < 1.0 else 0)
        stamina_cost = max(5, int(study_hours * base_cost_rate))
        
        # Skill Notes Keeper & Gold Digger
        extra_gold_notes = int(study_hours * 5) if d["skills"]["notes_keeper"] > 0 else 0
        gold_gained = int((study_hours * 25 + extra_gold_notes) * streak_bonus_mult)

        if st.button(f"🚀 Selesaikan Belajar ({study_hours} Jam)", use_container_width=True):
            if d["stamina"] >= stamina_cost:
                d["stamina"] -= stamina_cost

                # Skill Gold Digger Chance
                if d["skills"]["gold_digger"] > 0 and random.random() < 0.25:
                    gold_gained += 20
                    st.info("🪙 Skill Gold Digger Aktif! +20 Bonus Gold.")

                d["gold"] += gold_gained
                d["total_study_hours"] += study_hours
                
                exp_earned = int(study_hours * 100)
                # Skill Hyperfocus
                if d["skills"]["hyperfocus"] > 0 and study_hours >= 2.0:
                    exp_earned = int(exp_earned * 1.3)
                    st.info("🧠 Skill Hyperfocus Aktif! +30% Extra EXP Belajar.")

                add_exp(exp_earned, "INT", int(study_hours * 2))
                log_activity("Belajar (Jam)", study_hours)
                st.success(f"Selesai Belajar! (+{gold_gained} Gold)")
                st.rerun()
            else:
                st.warning("Stamina tidak cukup!")

    # --- QUEST 2: WORKOUT ---
    with st.expander("🏋️ 2. Workout & Olahraga"):
        workout_mins = st.number_input("Berapa menit workout?", min_value=10, max_value=180, value=30, step=10)
        
        # Skill Athletic Body & Running Shoes
        cost_work = int(workout_mins * 0.5)
        if "👟 Running Shoes of Agility" in d["equipped_items"]:
            cost_work = int(cost_work * 0.7)
        if d["skills"]["athletic_body"] > 0:
            cost_work = int(cost_work * 0.75)
        cost_work = max(5, cost_work)

        gold_gained_work = int(workout_mins * 0.6 * streak_bonus_mult)

        if st.button(f"🏋️ Selesaikan Workout ({workout_mins} Mnt)", use_container_width=True):
            if d["stamina"] >= cost_work:
                d["stamina"] -= cost_work

                # Skill Cardio Boost
                if d["skills"]["cardio_boost"] > 0:
                    d["hp"] = min(d["max_hp"], d["hp"] + 10)
                    st.info("❤️ Skill Cardio Boost Aktif! +10 HP dipulihkan.")

                d["gold"] += gold_gained_work
                add_exp(int(workout_mins * 2.5), "STR", max(1, int(workout_mins / 20)))
                log_activity("Workout (Menit)", workout_mins)
                st.success(f"Workout Selesai! (+{gold_gained_work} Gold)")
                st.rerun()
            else:
                st.warning("Stamina tidak cukup!")

    # --- QUEST 3: BERIBADAH & SPIRITUAL ---
    with st.expander("🕌 3. Ibadah & Spiritual Quest"):
        worship_type = st.selectbox("Pilih Jenis Ibadah / Refleksi:", [
            "Sholat Wajib 5 Waktu / Doa Utama (+30 EXP, +15 Gold)",
            "Membaca Kitab Suci / Meditasi 15 Mnt (+40 EXP, +20 Gold)",
            "Amalan Sunnah / Kebajikan Harian (+50 EXP, +30 Gold)"
        ])
        if st.button("🤲 Selesaikan Ibadah", use_container_width=True):
            if "5 Waktu" in worship_type:
                exp_g, gold_g = 30, 15
            elif "Kitab Suci" in worship_type:
                exp_g, gold_g = 40, 20
            else:
                exp_g, gold_g = 50, 30

            d["gold"] += int(gold_g * streak_bonus_mult)
            d["total_worship_count"] = d.get("total_worship_count", 0) + 1
            add_exp(exp_g, "VIT", 1)
            log_activity("Ibadah", 1)
            st.success(f"Alhamdulillah / Selesai! (+{exp_g} EXP, +{int(gold_g * streak_bonus_mult)} Gold)")
            st.rerun()

    # --- QUEST 4: MINUM AIR ---
    with st.expander("💧 4. Asupan Air Minum Harian"):
        st.write(f"Konsumsi Air Saat Ini: **{d['water_ml']} / 2000 ml**")
        st.progress(min(d['water_ml'] / 2000, 1.0))
        
        c_w1, c_w2, c_w3 = st.columns(3)
        if c_w1.button("+ 250 ml (Gelas)"):
            d["water_ml"] += 250
            if d["water_ml"] >= 2000:
                add_exp(50, "VIT", 1)
                st.balloons()
                st.success("💧 Target Air 2000ml Tercapai! (+50 EXP, +1 VIT)")
            save_game()
            st.rerun()
        if c_w2.button("+ 600 ml (Botol)"):
            d["water_ml"] += 600
            if d["water_ml"] >= 2000:
                add_exp(50, "VIT", 1)
                st.balloons()
                st.success("💧 Target Air 2000ml Tercapai! (+50 EXP, +1 VIT)")
            save_game()
            st.rerun()
        if c_w3.button("🔄 Reset Air"):
            d["water_ml"] = 0
            save_game()
            st.rerun()

    # --- INSTANT ITEM ---
    with st.expander("📜 5. Gunakan Instant Scroll Item"):
        if "📜 Scroll of Instant Focus" in d["inventory"]:
            if st.button("⚡ Gunakan Scroll Instant Focus", use_container_width=True):
                d["inventory"].remove("📜 Scroll of Instant Focus")
                add_exp(150, "INT", 2)
                st.success("Quest diselesaikan instant tanpa menguras stamina!")
                st.rerun()
        else:
            st.caption("Kamu tidak memiliki Scroll of Instant Focus. Beli di Toko Shop!")

# ================= TAB 2: SKILL TREE =================
with tab_skill:
    st.subheader("🌳 Skill Tree (Perluasan Cabang Keterampilan)")
    st.write(f"Sisa Skill Points (SP): **{d['skill_points']}**")
    st.divider()

    st.markdown("### 🏛️ 1. Cabang Scholar")
    sk_c1, sk_c2, sk_c3 = st.columns(3)
    with sk_c1:
        st.write(f"**Quick Reader (Lvl {d['skills']['quick_reader']}/1)**")
        st.caption("Hemat 5 stamina untuk belajar < 1 jam.")
        if st.button("Ambil Skill", key="sk_qr", disabled=(d["skill_points"] <= 0 or d["skills"]["quick_reader"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["quick_reader"] = 1; save_game(); st.rerun()
    with sk_c2:
        st.write(f"**Notes Keeper (Lvl {d['skills']['notes_keeper']}/1)**")
        st.caption("+5 Extra Gold per jam belajar.")
        if st.button("Ambil Skill", key="sk_nk", disabled=(d["skill_points"] <= 0 or d["skills"]["notes_keeper"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["notes_keeper"] = 1; save_game(); st.rerun()
    with sk_c3:
        st.write(f"**Hyperfocus (Lvl {d['skills']['hyperfocus']}/1)**")
        st.caption("+30% EXP Belajar jika durasi >= 2 jam.")
        if st.button("Ambil Skill", key="sk_hf", disabled=(d["skill_points"] <= 0 or d["skills"]["hyperfocus"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["hyperfocus"] = 1; save_game(); st.rerun()

    sk_c4, sk_c5, sk_c6 = st.columns(3)
    with sk_c4:
        st.write(f"**Coffee Efficiency (Lvl {d['skills']['coffee_efficiency']}/1)**")
        st.caption("+50% Efek stamina Espresso Shot.")
        if st.button("Ambil Skill", key="sk_ce", disabled=(d["skill_points"] <= 0 or d["skills"]["coffee_efficiency"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["coffee_efficiency"] = 1; save_game(); st.rerun()
    with sk_c5:
        st.write(f"**Memory Palace (Lvl {d['skills']['memory_palace']}/1)**")
        st.caption("+25 Permanen Max Stamina.")
        if st.button("Ambil Skill", key="sk_mp", disabled=(d["skill_points"] <= 0 or d["skills"]["memory_palace"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["memory_palace"] = 1; d["max_stamina"] += 25; save_game(); st.rerun()
    with sk_c6:
        st.write(f"**Exam Crusher (Lvl {d['skills']['exam_crusher']}/1)**")
        st.caption("+25% Damage ke Boss bertipe INT.")
        if st.button("Ambil Skill", key="sk_ec", disabled=(d["skill_points"] <= 0 or d["skills"]["exam_crusher"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["exam_crusher"] = 1; save_game(); st.rerun()

    st.divider()
    st.markdown("### 🏋️ 2. Cabang Warrior")
    w_c1, w_c2, w_c3 = st.columns(3)
    with w_c1:
        st.write(f"**Warm Up (Lvl {d['skills']['warm_up']}/1)**")
        st.caption("Kurangi 20% risiko kehilangan HP.")
        if st.button("Ambil Skill", key="sk_wu", disabled=(d["skill_points"] <= 0 or d["skills"]["warm_up"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["warm_up"] = 1; save_game(); st.rerun()
    with w_c2:
        st.write(f"**Cardio Boost (Lvl {d['skills']['cardio_boost']}/1)**")
        st.caption("+10 HP gratis tiap kali workout.")
        if st.button("Ambil Skill", key="sk_cb", disabled=(d["skill_points"] <= 0 or d["skills"]["cardio_boost"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["cardio_boost"] = 1; save_game(); st.rerun()
    with w_c3:
        st.write(f"**Iron Skin (Lvl {d['skills']['iron_skin']}/1)**")
        st.caption("Kurangi 15% hukuman damage HP.")
        if st.button("Ambil Skill", key="sk_isk", disabled=(d["skill_points"] <= 0 or d["skills"]["iron_skin"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["iron_skin"] = 1; save_game(); st.rerun()

    w_c4, w_c5, w_c6 = st.columns(3)
    with w_c4:
        st.write(f"**Athletic Body (Lvl {d['skills']['athletic_body']}/1)**")
        st.caption("Hemat 25% stamina workout.")
        if st.button("Ambil Skill", key="sk_ab", disabled=(d["skill_points"] <= 0 or d["skills"]["athletic_body"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["athletic_body"] = 1; save_game(); st.rerun()
    with w_c5:
        st.write(f"**Adrenaline Rush (Lvl {d['skills']['adrenaline_rush']}/1)**")
        st.caption("Meningkatkan damage Boss saat HP rendah.")
        if st.button("Ambil Skill", key="sk_ar", disabled=(d["skill_points"] <= 0 or d["skills"]["adrenaline_rush"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["adrenaline_rush"] = 1; save_game(); st.rerun()
    with w_c6:
        st.write(f"**Second Wind (Lvl {d['skills']['second_wind']}/1)**")
        st.caption("Otomatis pulih 30% HP jika menyentuh 0.")
        if st.button("Ambil Skill", key="sk_sw", disabled=(d["skill_points"] <= 0 or d["skills"]["second_wind"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["second_wind"] = 1; save_game(); st.rerun()

    st.divider()
    st.markdown("### 🪙 3. Cabang Merchant & Guardian")
    mg_c1, mg_c2, mg_c3 = st.columns(3)
    with mg_c1:
        st.write(f"**Bargain Hunter (Lvl {d['skills']['bargain_hunter']}/1)**")
        st.caption("Diskon 10% belanja di Potion Shop.")
        if st.button("Ambil Skill", key="sk_bh", disabled=(d["skill_points"] <= 0 or d["skills"]["bargain_hunter"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["bargain_hunter"] = 1; save_game(); st.rerun()
    with mg_c2:
        st.write(f"**Gold Digger (Lvl {d['skills']['gold_digger']}/1)**")
        st.caption("Peluang 25% +20 Gold ekstra tiap quest.")
        if st.button("Ambil Skill", key="sk_gd", disabled=(d["skill_points"] <= 0 or d["skills"]["gold_digger"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["gold_digger"] = 1; save_game(); st.rerun()
    with mg_c3:
        st.write(f"**Distraction Barrier (Lvl {d['skills']['distraction_barrier']}/1)**")
        st.caption("Hukuman sosmed TIDAK mengurangi EXP.")
        if st.button("Ambil Skill", key="sk_db", disabled=(d["skill_points"] <= 0 or d["skills"]["distraction_barrier"] >= 1)):
            d["skill_points"] -= 1; d["skills"]["distraction_barrier"] = 1; save_game(); st.rerun()

    st.divider()
    st.markdown("### ⚡ Skill Aktif Special")
    act_c1, act_c2 = st.columns(2)
    with act_c1:
        st.write("**Omniscience (3x EXP Belajar)**")
        if st.button("🔮 Aktifkan Omniscience", disabled=(d["active_skills_cd"]["omniscience"] > 0)):
            d["active_buffs"].append({"name": "✨ Omniscience Buff (3x EXP)", "expires": "1 Hari"})
            save_game()
            st.success("Omniscience Aktif!")
            st.rerun()
    with act_c2:
        st.write("**Titan Form (4x Damage Boss)**")
        if st.button("💥 Aktifkan Titan Form", disabled=(d["active_skills_cd"]["titan_form"] > 0)):
            d["active_buffs"].append({"name": "💥 Titan Form Buff (4x Damage)", "expires": "1 Serangan"})
            save_game()
            st.success("Titan Form Aktif!")
            st.rerun()

# ================= TAB 3: BOSS RAID =================
with tab_boss:
    boss_list = [
        {"name": "👾 Procrastination Demon", "weakness": "INT", "desc": "Sensitif terhadap Sesi Belajar!"},
        {"name": "🐉 Distraction Dragon", "weakness": "STR", "desc": "Hanya lemah terhadap Latihan Fisik/Workout!"},
        {"name": "🔥 Burnout Demon", "weakness": "VIT", "desc": "Butuh konsistensi pemulihan stamina & fokus!"}
    ]
    current_week = datetime.now().isocalendar()[1]
    active_boss = boss_list[current_week % len(boss_list)]
    d["boss_name"] = active_boss["name"]

    st.subheader(f"⚔️ Dungeon RAID Mingguan: {d['boss_name']}")
    st.caption(f"Kelemahan Boss: **Atribut {active_boss['weakness']}** ({active_boss['desc']})")
    st.progress(max(0.0, min(d["boss_hp"] / d["boss_max_hp"], 1.0)), text=f"HP Boss: {d['boss_hp']} / {d['boss_max_hp']}")

    stat_bonus = d["stats"][active_boss["weakness"]] * 3
    base_damage = d["stats"]["STR"] * 2 + d["stats"]["INT"] * 2 + stat_bonus
    
    # Skill Exam Crusher Bonus
    if d["skills"]["exam_crusher"] > 0 and active_boss["weakness"] == "INT":
        base_damage = int(base_damage * 1.25)

    # Skill Adrenaline Rush
    if d["skills"]["adrenaline_rush"] > 0 and (d["hp"] / d["max_hp"]) < 0.3:
        base_damage = int(base_damage * 1.5)
        st.info("🔥 Adrenaline Rush menambah +50% Damage saat HP sekarat!")

    if "🗡️ Steel Sword of Focus" in d["equipped_items"]:
        base_damage = int(base_damage * 1.15)
    if d["active_pet"] == "🐺 Spirit Wolf":
        base_damage += 25

    # Check Titan Form Buff
    has_titan = any(b["name"] == "💥 Titan Form Buff (4x Damage)" for b in d["active_buffs"])
    if has_titan:
        base_damage *= 4
        st.warning("⚡ Titan Form Aktif! 4x Multiplier Damage!")

    st.info(f"💥 Total Damage Serangan Nauval: **{base_damage} HP**")

    if st.button(f"⚔️ Serang {d['boss_name']} (-20 Stamina)", use_container_width=True):
        if d["stamina"] >= 20:
            play_sfx("attack")
            d["stamina"] -= 20
            d["boss_hp"] -= base_damage

            if has_titan:
                d["active_buffs"] = [b for b in d["active_buffs"] if b["name"] != "💥 Titan Form Buff (4x Damage)"]

            if d["boss_hp"] <= 0:
                play_sfx("level_up")
                st.balloons()
                d["boss_defeated_count"] += 1
                d["gold"] += 100
                add_exp(250)
                d["boss_max_hp"] = int(d["boss_max_hp"] * 1.4)
                d["boss_hp"] = d["boss_max_hp"]
                st.success(f"🔥 VICTORY! Nauval mengalahkan {d['boss_name']}!")
            save_game()
            st.rerun()
        else:
            st.warning("Stamina tidak mencukupi!")

# ================= TAB 4: PENALTY =================
with tab_penalty:
    st.subheader("🚨 Fitur Hukuman Pelanggaran")
    sosmed_mins = st.number_input("Berapa menit buang waktu / sosmed?", min_value=15, max_value=300, value=30, step=15)
    if st.button(f"⚠️ Laporkan Sosmed ({sosmed_mins} Mnt)", use_container_width=True):
        apply_penalty(int(sosmed_mins * 0.8), int(sosmed_mins * 2))
        st.rerun()

# ================= TAB 5: SHOP =================
with tab_shop:
    st.subheader("🧪 Toko Potion & Items")
    potions = [
        {"name": "☕ Espresso Shot", "cost": 45, "type": "instant_stamina", "val": 30, "desc": "+30 Stamina Instan"},
        {"name": "⚡ Vitality Potion", "cost": 60, "type": "instant_stamina", "val": 50, "desc": "+50 Stamina Instan"},
        {"name": "📜 Scroll of Instant Focus", "cost": 100, "type": "item", "desc": "Selesaikan 1 quest instant tanpa stamina."},
        {"name": "🛡️ Potion Kebal Penundaan", "cost": 180, "type": "item", "desc": "Tolak 1x hukuman sosmed otomatis."},
        {"name": "🍀 Clover of Luck", "cost": 200, "type": "buff", "duration": 24, "desc": "+25% Hoki Gacha Harian"},
        {"name": "🧪 Double EXP Elixir", "cost": 150, "type": "buff", "duration": 2, "desc": "2x EXP selama 2 Jam"},
        {"name": "📜 Scroll of Oblivion", "cost": 300, "type": "respec", "desc": "Reset semua Skill Points untuk alokasi ulang."}
    ]
    
    # Skill Bargain Hunter Discount
    discount_mult = 0.9 if d["skills"]["bargain_hunter"] > 0 else 1.0

    for p in potions:
        final_cost = int(p["cost"] * discount_mult)
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{p['name']}** — 🪙 **{final_cost} Gold**\n\n*{p['desc']}*")
        if c2.button("Beli", key="shop_"+p["name"]):
            if d["gold"] >= final_cost:
                d["gold"] -= final_cost
                if p["type"] == "instant_stamina":
                    rec_val = p["val"]
                    if p["name"] == "☕ Espresso Shot" and d["skills"]["coffee_efficiency"] > 0:
                        rec_val = int(rec_val * 1.5)
                    d["stamina"] = min(d["max_stamina"], d["stamina"] + rec_val)
                elif p["type"] == "item":
                    d["inventory"].append(p["name"])
                elif p["type"] == "buff":
                    d["active_buffs"].append({"name": p["name"], "expires": f"{p['duration']} Jam"})
                elif p["type"] == "respec":
                    # Reset All Skills
                    total_points = sum(d["skills"].values())
                    for k in d["skills"]: d["skills"][k] = 0
                    d["skill_points"] += total_points
                    st.success("Skill Points berhasil di-reset!")
                save_game()
                st.success(f"Berhasil membeli {p['name']}!")
                st.rerun()

# ================= TAB 6: ARMORY =================
with tab_equips:
    st.subheader("🗡️ Armory & Equipment RPG")
    equips = [
        {"name": "🎧 Noise-Canceling Headphones", "cost": 350, "desc": "+20% EXP ekstra Belajar."},
        {"name": "👟 Running Shoes of Agility", "cost": 280, "desc": "Hemat 30% stamina saat workout."},
        {"name": "💍 Ring of Consistency", "cost": 500, "desc": "Double bonus Gold dari Streak Harian."},
        {"name": "🗡️ Steel Sword of Focus", "cost": 250, "desc": "+15% Damage Boss Dungeon."},
        {"name": "🛡️ Shield of Iron Will", "cost": 200, "desc": "Kurangi 20% efek Hukuman."}
    ]
    for eq in equips:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{eq['name']}** — 🪙 **{eq['cost']} Gold**\n\n*{eq['desc']}*")
        if eq["name"] in d["equipped_items"]:
            c2.button("Terpasang ✅", key="eq_"+eq["name"], disabled=True)
        else:
            if c2.button("Beli & Equip", key="eq_"+eq["name"]):
                if d["gold"] >= eq["cost"]:
                    d["gold"] -= eq["cost"]
                    d["equipped_items"].append(eq["name"])
                    save_game()
                    st.rerun()

# ================= TAB 7: GACHA =================
with tab_gacha:
    st.subheader("🎡 Daily Spin Wheel")
    today_str = str(date.today())
    if d["last_gacha_date"] == today_str:
        st.info("⏰ Sudah Spin hari ini. Kembali besok!")
    else:
        if st.button("🎰 Putar Spin Harian", use_container_width=True):
            d["last_gacha_date"] = today_str
            streak_multiplier = 1 + (d["streak"] * 0.1)
            rewards = [
                ("🪙 Bonus Gold", "gold", int(100 * streak_multiplier)), 
                ("✨ Bonus EXP", "exp", int(150 * streak_multiplier))
            ]
            if any(b["name"] == "🍀 Clover of Luck" for b in d["active_buffs"]):
                rewards.append(("💎 Jackpot Super (+300 Gold)", "gold", int(300 * streak_multiplier)))
            chosen = random.choice(rewards)
            if chosen[1] == "gold": d["gold"] += chosen[2]
            elif chosen[1] == "exp": add_exp(chosen[2])
            save_game()
            st.rerun()

# ================= TAB 8: PET =================
with tab_pet:
    st.subheader("🐾 Pet Companions")
    pets = [
        {"name": "🐈‍⬛ Shadow Cat of Discipline", "cost": 300, "desc": "Kurangi damage hukuman sosmed 25%."},
        {"name": "🦅 Golden Eagle of Vision", "cost": 400, "desc": "+2 STR & +2 INT pasif permanen."},
        {"name": "🦉 Baby Owl of Wisdom", "cost": 150, "desc": "+1 INT ekstra tiap sesi belajar."},
        {"name": "🐺 Spirit Wolf", "cost": 220, "desc": "+25 Damage Boss."}
    ]
    for p in pets:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{p['name']}** — 🪙 **{p['cost']} Gold**\n\n*{p['desc']}*")
        if d["active_pet"] == p["name"]:
            c2.button("Aktif 🐾", key="p_"+p["name"], disabled=True)
        else:
            if c2.button("Adopt", key="p_"+p["name"]):
                if d["gold"] >= p["cost"]:
                    d["gold"] -= p["cost"]
                    d["active_pet"] = p["name"]
                    save_game()
                    st.rerun()

# ================= TAB 9: ACHIEVEMENTS =================
with tab_achieve:
    st.subheader("🏆 Real-Time & Weekly Achievements")
    st.caption("Pencapaian ini diperbarui secara otomatis menggunakan Waktu Real-Time Server.")
    
    st.write(f"📅 Status Minggu Ini: **{d['last_weekly_reset']}**")
    st.divider()
    
    if d["achievements"]:
        for ach in d["achievements"]:
            st.success(f"🏆 Lencana Terbuka: **{ach}**")
    else:
        st.info("Belum ada Achievement yang didapatkan. Tingkatkan level dan quest harianmu!")

# ================= TAB 10: ANALYTICS =================
with tab_analytics:
    st.subheader("📈 Analytics Kedisiplinan")
    if d["activity_log"]:
        df = pd.DataFrame(d["activity_log"])
        st.bar_chart(df, x="date", y="value", color="activity")
    else:
        st.info("Belum ada data aktivitas.")
# ==========================================
# 🧱 MODUL KOMPLEKS TAMBAHAN (EXTENSIONS)
# ==========================================

# 1. INITIALIZATION & HELPER UNTUK FITUR BARU
if "tower_floor" not in d:
    d["tower_floor"] = 1
if "gem_inventory" not in d:
    d["gem_inventory"] = []
if "equipment_gems" not in d:
    d["equipment_gems"] = {}
if "active_debuffs" not in d:
    d["active_debuffs"] = []
if "random_event_active" not in d:
    d["random_event_active"] = None

# Cek Debuff Burnout jika HP dibawah 20%
if (d["hp"] / d["max_hp"]) < 0.2 and "🔥 Burnout / Injured" not in d["active_debuffs"]:
    d["active_debuffs"].append("🔥 Burnout / Injured")
elif (d["hp"] / d["max_hp"]) >= 0.2 and "🔥 Burnout / Injured" in d["active_debuffs"]:
    d["active_debuffs"].remove("🔥 Burnout / Injured")

# 2. RENDER TAB-TAB KOMPLEKS BARU
st.divider()
st.header("⚡ Sistem Lanjutan & Modul Kompleks")

tab_tower, tab_event, tab_craft, tab_debuff = st.tabs([
    "🏰 Tower of Discipline", "🎴 Event Cards", "💎 Gem Crafting", "⚠️ Status & Debuff"
])

# --- TAB A: TOWER OF DISCIPLINE (50 FLOORS) ---
with tab_tower:
    st.subheader(f"🏰 Tower of Discipline — Lantai {d['tower_floor']} / 50")
    
    req_study = d["tower_floor"] * 2.0
    req_level = d["tower_floor"] * 1
    
    st.write(f"**Syarat Menembus Lantai {d['tower_floor']}:**")
    st.write(f"• Total Jam Belajar Kumulatif: **{d['total_study_hours']} / {req_study} Jam**")
    st.write(f"• Level Karakter: **{d['level']} / {req_level}**")

    can_pass = (d['total_study_hours'] >= req_study) and (d['level'] >= req_level)
    
    if can_pass:
        st.success("✅ Seluruh syarat terpenuhi! Nauval siap menaklukkan lantai ini.")
        if st.button(f"⚔️ Taklukkan Lantai {d['tower_floor']}", use_container_width=True):
            d["tower_floor"] += 1
            reward_gold = d["tower_floor"] * 50
            reward_exp = d["tower_floor"] * 100
            d["gold"] += reward_gold
            add_exp(reward_exp)
            st.balloons()
            st.success(f"🎉 Lantai ditaklukkan! Hadiah: +{reward_gold} Gold, +{reward_exp} EXP!")
            save_game()
            st.rerun()
    else:
        st.warning("🔒 Syarat belum terpenuhi. Tingkatkan level dan durasi belajar untuk naik lantai!")

# --- TAB B: RANDOM EVENT CARDS ---
with tab_event:
    st.subheader("🎴 Random Encounter & Event Cards")
    
    if st.button("🎲 Tarik Kartu Event Acak (-10 Stamina)", use_container_width=True):
        if d["stamina"] >= 10:
            d["stamina"] -= 10
            events_pool = [
                {"title": "📚 Menemukan Buku Kuno", "desc": "Membacanya memberi +80 INT EXP tapi menghabiskan waktu.", "exp": 80, "gold": 0, "hp": 0},
                {"title": "💰 Peti Harta Karun", "desc": "Peti tersembunyi berisi koin emas!", "exp": 0, "gold": 120, "hp": 0},
                {"title": "⚠️ Jebakan Buruk", "desc": "Terdistraksi oleh godaan! HP berkurang.", "exp": 0, "gold": 0, "hp": -15},
                {"title": "🥗 Makanan Bergizi", "desc": "Menemukan porsi nutrisi tinggi. Memulihkan HP!", "exp": 0, "gold": 0, "hp": 25}
            ]
            d["random_event_active"] = random.choice(events_pool)
            save_game()
        else:
            st.warning("Stamina tidak cukup!")

    if d["random_event_active"]:
        ev = d["random_event_active"]
        st.info(f"**{ev['title']}**\n\n{ev['desc']}")
        if st.button("Klaim Hasil Event", key="claim_ev"):
            if ev["exp"] > 0: add_exp(ev["exp"])
            if ev["gold"] > 0: d["gold"] += ev["gold"]
            if ev["hp"] != 0: 
                d["hp"] = max(0, min(d["max_hp"], d["hp"] + ev["hp"]))
            d["random_event_active"] = None
            save_game()
            st.rerun()

# --- TAB C: GEM CRAFTING & SOCKETING ---
with tab_craft:
    st.subheader("💎 Equipment Gem Crafting")
    st.caption("Gabungkan 100 Gold untuk membuat Gem statistik pasif permanen!")

    c_g1, c_g2 = st.columns(2)
    with c_g1:
        st.markdown("**Crafting Gem Baru**")
        if st.button("🔨 Craft Random Gem (100 Gold)", use_container_width=True):
            if d["gold"] >= 100:
                d["gold"] -= 100
                gem_type = random.choice(["💎 Ruby (+5 STR)", "🔷 Sapphire (+5 INT)", "🟢 Emerald (+5 VIT)"])
                d["gem_inventory"].append(gem_type)
                save_game()
                st.success(f"Berhasil membuat **{gem_type}**!")
                st.rerun()
            else:
                st.warning("Gold tidak cukup!")

    with c_g2:
        st.markdown("**Inventory Gem Milikmu**")
        if d["gem_inventory"]:
            for gem in d["gem_inventory"]:
                st.write(f"• {gem}")
        else:
            st.caption("Belum memiliki Gem di dalam inventory.")

# --- TAB D: STATUS DEBUFF & INJURY ---
with tab_debuff:
    st.subheader("⚠️ Status Kondisi Karakter")
    
    if d["active_debuffs"]:
        for deb in d["active_debuffs"]:
            st.error(f"🚨 Status Aktif: **{deb}** (Perolehan EXP & Gold berkurang 50% karena HP kritis!)")
        
        st.markdown("---")
        st.write("🏥 **Sistem Pemulihan Istirahat (Rest & Recovery)**")
        if st.button("💤 Lakukan Istirahat Total (+40 HP, -50 Gold)", use_container_width=True):
            if d["gold"] >= 50:
                d["gold"] -= 50
                d["hp"] = min(d["max_hp"], d["hp"] + 40)
                save_game()
                st.success("Nauval telah beristirahat dan memulihkan kesehatan!")
                st.rerun()
            else:
                st.warning("Gold tidak cukup untuk membeli obat pemulihan!")
    else:
        st.success("✅ Kondisi fisik & mental Nauval sangat prima! Tidak ada debuff aktif.")
# ==========================================
# 🛒 MODUL EXTENSION: SUPER EXPANDED SHOP & ARMORY
# ==========================================

st.divider()
st.header("🛍️ Toko Pasar Gelap & Blacksmith Kerajaan")

tab_potions_extra, tab_armory_extra, tab_relics = st.tabs([
    "🧪 Potions & Elixirs Super", "⚔️ Senjata & Zirah Baru", "🔮 Relic & Artifact Kuno"
])

# --- TAB 1: CONSUMABLE POTIONS & ELIXIRS ---
with tab_potions_extra:
    st.subheader("🧪 Ramuan & Elixir Langka")
    
    extra_potions = [
        {"name": "🧪 Mega Stamina Potion", "cost": 120, "type": "stamina", "val": 100, "desc": "Memulihkan 100 Stamina secara instan."},
        {"name": "🧪 Elixir of Phoenix", "cost": 250, "type": "hp", "val": 100, "desc": "Memulihkan 100 HP secara penuh saat sekarat."},
        {"name": "⚡ Hyper Coffee Shot", "cost": 85, "type": "stamina", "val": 60, "desc": "Espresso dosis tinggi (+60 Stamina)."},
        {"name": "📜 Scroll of Double Gold", "cost": 175, "type": "item", "desc": "Mendapatkan 2x lipat Gold dari quest harian."},
        {"name": "🧪 Potion of Pure Focus", "cost": 220, "type": "item", "desc": "Menghilangkan seluruh efek Debuff secara instan."},
        {"name": "🍬 Candy of Speed", "cost": 50, "type": "stamina", "val": 25, "desc": "Permen peningkat energi ringan (+25 Stamina)."}
    ]

    for item in extra_potions:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{item['name']}** — 🪙 **{item['cost']} Gold**\n\n*{item['desc']}*")
        if c2.button("Beli", key="ex_pot_"+item["name"]):
            if d["gold"] >= item["cost"]:
                d["gold"] -= item["cost"]
                if item["type"] == "stamina":
                    d["stamina"] = min(d["max_stamina"], d["stamina"] + item["val"])
                    st.success(f"Berhasil diminum! +{item['val']} Stamina.")
                elif item["type"] == "hp":
                    d["hp"] = min(d["max_hp"], d["hp"] + item["val"])
                    st.success(f"Berhasil diminum! +{item['val']} HP.")
                elif item["type"] == "item":
                    d["inventory"].append(item["name"])
                    st.success(f"{item['name']} disimpan ke inventory!")
                save_game()
                st.rerun()
            else:
                st.warning("Gold tidak cukup!")

# --- TAB 2: EXTRA ARMORY & EQUIPMENT ---
with tab_armory_extra:
    st.subheader("⚔️ Perlengkapan & Zirah Tempur")

    extra_equips = [
        {"name": "🛡️ Aegis Shield of Discipline", "cost": 450, "desc": "+30 Max HP & mengurangi damage hukuman sebesar 30%."},
        {"name": "🗡️ Excalibur of Productivity", "cost": 600, "desc": "+50 Damage ekstra saat menyerang Boss RAID."},
        {"name": "👑 Crown of Scholar King", "cost": 550, "desc": "+30% EXP ekstra dari setiap Sesi Belajar."},
        {"name": "👢 Boots of Swiftness", "cost": 320, "desc": "Menghemat 35% stamina dari semua jenis quest."},
        {"name": "🦺 Platinum Armor of Iron Will", "cost": 700, "desc": "+50 Max HP & Kebal terhadap status Debuff HP Rendah."}
    ]

    for eq in extra_equips:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{eq['name']}** — 🪙 **{eq['cost']} Gold**\n\n*{eq['desc']}*")
        if eq["name"] in d["equipped_items"]:
            c2.button("Terpasang ✅", key="ex_eq_"+eq["name"], disabled=True)
        else:
            if c2.button("Beli & Equip", key="ex_eq_"+eq["name"]):
                if d["gold"] >= eq["cost"]:
                    d["gold"] -= eq["cost"]
                    d["equipped_items"].append(eq["name"])
                    save_game()
                    st.rerun()
                else:
                    st.warning("Gold tidak cukup!")

# --- TAB 3: ANCIENT RELICS & ARTIFACTS ---
with tab_relics:
    st.subheader("🔮 Relic & Artefak Kuno (Permanen Buff)")

    relics = [
        {"name": "🔮 Orb of Infinite Wisdom", "cost": 850, "desc": "Meningkatkan seluruh perolehan EXP karakter sebesar 25% permanen."},
        {"name": "🪙 Midas Golden Chalice", "cost": 1000, "desc": "Meningkatkan perolehan Gold dari semua quest sebesar 50% permanen."},
        {"name": "🏺 Ancient Urn of Stamina", "cost": 750, "desc": "+50 Maksimum Stamina permanen secara instan."}
    ]

    for r in relics:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{r['name']}** — 🪙 **{r['cost']} Gold**\n\n*{r['desc']}*")
        if r["name"] in d["equipped_items"]:
            c2.button("Dimiliki 🔮", key="rel_"+r["name"], disabled=True)
        else:
            if c2.button("Klaim Relic", key="rel_"+r["name"]):
                if d["gold"] >= r["cost"]:
                    d["gold"] -= r["cost"]
                    d["equipped_items"].append(r["name"])
                    if r["name"] == "🏺 Ancient Urn of Stamina":
                        d["max_stamina"] += 50
                        d["stamina"] += 50
                    save_game()
                    st.rerun()
                else:
                    st.warning("Gold tidak cukup!")
