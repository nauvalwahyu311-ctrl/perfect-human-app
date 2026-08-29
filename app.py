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

# ================= TAB 1: ADVANCED AI-GUIDED QUEST & MENTOR SYSTEM =================
with tab_quest:
    st.subheader("📌 Papan Misi Disiplin & AI Academic Mentor")
    st.caption("Selesaikan misi harian untuk menempa atribut karakter, mengumpulkan Gold, dan dapatkan rekomendasi serta bimbingan langsung dari AI Mentor anime imutmu, Nauval!")
    
    # --- INFO BAR STATUS USER ---
    st.info(f"⚡ Stamina: **{d['stamina']} / {d['max_stamina']}** | ❤️ HP: **{d['hp']} / {d['max_hp']}** | 🪙 Gold: **{d['gold']}**")
    st.divider()

    # Hitung multiplier dasar dari streak
    streak_bonus_mult = 1.0 + (d["streak"] * 0.05)

    # =========================================================================
    # 🌸 FITUR AI MENTOR ANIME IMUT (RECOMMENDER & INTERACTIVE GUIDE)
    # =========================================================================
    if "ai_mentor_chat" not in st.session_state:
        st.session_state["ai_mentor_chat"] = [
            {"role": "assistant", "content": "Halo, Master Nauval! (｡♥‿♥｡) Aku *Mimi*, AI mentor akademiknya hari ini. Semangat ya belajarnya! Ketik atau pilih tombol di bawah kalau butuh rekomendasi misi atau motivasi dari aku, ya!"}
        ]

    with st.container(border=True):
        st.markdown("### 🌸 Ruang Diskusi AI Mentor: **Mimi (Chibi Assistant)**")
        
        # Tampilkan avatar / banner gaya anime imut interaktif
        col_m1, col_m2 = st.columns([1, 4])
        with col_m1:
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, #ffb6c1 0%, #ff69b4 100%); padding: 15px; border-radius: 12px; text-align: center; color: white;">
                    <h2 style="margin: 0;">🌸 (˶˃ᆺ˂˶)</h2>
                    <p style="margin: 5px 0 0 0; font-size: 12px; font-weight: bold;">Mimi-chan</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
        with col_m2:
            # Ambil pesan terakhir dari Mimi
            last_msg = st.session_state["ai_mentor_chat"][-1]["content"]
            st.markdown(f"*{last_msg}*")

        # Tombol interaksi cepat rekomendasi quest dari AI
        rc1, rc2, rc3 = st.columns(3)
        if rc1.button("✨ Minta Rekomendasi Hari Ini"):
            import random
            recommendations = [
                "Mimi menyarankan Master Nauval fokus belajar materi inti minimal 1.5 jam hari ini demi mendongkrak status INT!",
                "Stamina Master Nauval masih cukup nih! Bagaimana kalau selingi dengan workout 30 menit biar badan segar?",
                "Jangan lupa hidrasi tubuh dan lakukan ibadah sebentar ya, Master, biar pikiran tenang dan fokus naik!"
            ]
            chosen_rec = random.choice(recommendations)
            st.session_state["ai_mentor_chat"].append({"role": "assistant", "content": chosen_rec})
            st.rerun()
            
        if rc2.button("💖 Kata-Kata Motivasi"):
            quotes = [
                "Disiplin adalah jembatan antara tujuan dan pencapaian. You can do it, Nauval! (๑>◡<๑)",
                "Kecil-kecil lama-lama jadi bukit! Setiap 1 jam belajar membawamu lebih dekat ke impianmu!",
                "Kalau lelah, istirahat sebentar ya Master, jangan dipaksakan sampai burnout! Mimi selalu dukung kok!"
            ]
            chosen_q = random.choice(quotes)
            st.session_state["ai_mentor_chat"].append({"role": "assistant", "content": chosen_q})
            st.rerun()

        if rc3.button("🧹 Cek Kesiapan Misi"):
            status_report = f"Laporan status Master Nauval saat ini: Level {d['level']}, Stamina {d['stamina']}/{d['max_stamina']}, Streak {d['streak']} hari. Semua quest siap diselesaikan!"
            st.session_state["ai_mentor_chat"].append({"role": "assistant", "content": status_report})
            st.rerun()

    st.markdown("---")

    # --- QUEST 1: SESI BELAJAR & LITERASI MENDALAM ---
    with st.expander("📚 1. Sesi Belajar & Penguasaan Skill Akademik", expanded=True):
        study_topic = st.text_input("Topik/Materi yang Dipelajari Hari Ini:", placeholder="Contoh: Pemrograman Python, Algoritma, atau Psikologi")
        study_hours = st.slider("Durasi Belajar (Jam)", min_value=0.5, max_value=8.0, value=1.0, step=0.5)
        
        # Skill Quick Reader & Stamina Cost
        base_cost_rate = 20 - (5 if d["skills"]["quick_reader"] > 0 and study_hours < 1.0 else 0)
        stamina_cost = max(5, int(study_hours * base_cost_rate))
        
        # Kalkulasi Reward Gold & EXP
        extra_gold_notes = int(study_hours * 8) if d["skills"]["notes_keeper"] > 0 else 0
        base_gold_study = int((study_hours * 30 + extra_gold_notes) * streak_bonus_mult)
        base_exp_study = int(study_hours * 120)
        
        if d["skills"]["hyperfocus"] > 0 and study_hours >= 2.0:
            base_exp_study = int(base_exp_study * 1.35)

        st.markdown(f"ℹ️ **Kebutuhan & Estimasi:** ⚡ **{stamina_cost} Stamina** | 🪙 **+{base_gold_study} Gold** | ✨ **+{base_exp_study} EXP (INT)**")

        if st.button("🚀 SELESAIKAN SESI BELAJAR", use_container_width=True, type="primary"):
            if d["stamina"] >= stamina_cost:
                d["stamina"] -= stamina_cost

                # Peluang Gold Digger
                if d["skills"]["gold_digger"] > 0 and random.random() < 0.30:
                    base_gold_study += 35
                    st.info("🪙 Skill Gold Digger Aktif! Menemukan harta karun tersembunyi (+35 Bonus Gold).")

                d["gold"] += base_gold_study
                d["total_study_hours"] = d.get("total_study_hours", 0) + study_hours
                
                if d["skills"]["hyperfocus"] > 0 and study_hours >= 2.0:
                    st.info("🧠 Skill Hyperfocus Aktif! Bonus +35% EXP terkumpul.")

                add_exp(base_exp_study, "INT", max(1, int(study_hours * 2)))
                log_activity(f"Belajar: {study_topic if study_topic else 'General'}", study_hours)
                
                st.success(f"🎉 Sesi belajar '{study_topic or 'Materi Utama'}' berhasil diselesaikan! (+{base_gold_study} Gold, +{base_exp_study} EXP)")
                save_game()
                st.rerun()
            else:
                st.warning(f"❌ Stamina tidak mencukupi! Butuh {stamina_cost} Stamina (Sisa: {d['stamina']}). Istirahatlah atau gunakan item pemulih!")

    # --- QUEST 2: WORKOUT & FISIK ---
    with st.expander("🏋️ 2. Latihan Fisik & Kebugaran Tubuh (Workout)"):
        workout_type = st.selectbox("Jenis Latihan Fisik:", [
            "Push Up & Strength Training (Pemberatan Otot)",
            "Cardio & Jogging (Ketahanan Jantung)",
            "Stretching & Yoga (Kelenturan & Relaksasi)",
            "Full Body Workout Intensif"
        ])
        workout_mins = st.slider("Durasi Latihan (Menit)", min_value=15, max_value=120, value=30, step=15)
        
        # Perhitungan stamina workout
        cost_work = int(workout_mins * 0.45)
        if "👟 Running Shoes of Agility" in d["equipped_items"]:
            cost_work = int(cost_work * 0.7)
        if d["skills"]["athletic_body"] > 0:
            cost_work = int(cost_work * 0.75)
        cost_work = max(5, cost_work)

        gold_gained_work = int(workout_mins * 0.75 * streak_bonus_mult)
        exp_work = int(workout_mins * 3.0)

        st.markdown(f"ℹ️ **Kebutuhan & Estimasi:** ⚡ **{cost_work} Stamina** | 🪙 **+{gold_gained_work} Gold** | 💪 **+{exp_work} EXP (STR)**")

        if st.button("💪 SELESAIKAN WORKOUT", use_container_width=True):
            if d["stamina"] >= cost_work:
                d["stamina"] -= cost_work

                if d["skills"]["cardio_boost"] > 0:
                    d["hp"] = min(d["max_hp"], d["hp"] + 15)
                    st.info("❤️ Skill Cardio Boost Aktif! Pulih +15 HP.")

                d["gold"] += gold_gained_work
                add_exp(exp_work, "STR", max(1, int(workout_mins / 25)))
                log_activity(f"Workout: {workout_type}", workout_mins)
                
                st.success(f"💪 Workout '{workout_type}' selesai! Tubuh semakin bugar. (+{gold_gained_work} Gold, +{exp_work} EXP)")
                save_game()
                st.rerun()
            else:
                st.warning(f"❌ Stamina tidak cukup! Kamu butuh {cost_work} Stamina.")

    # --- QUEST 3: IBADAH & SPIRITUAL ---
    with st.expander("🕌 3. Ibadah, Meditasi & Ketenangan Jiwa"):
        worship_choice = st.selectbox("Pilih Amalan Spiritual:", [
            "Sholat Wajib 5 Waktu & Doa Harian (+40 EXP VIT, +25 Gold)",
            "Membaca Kitab Suci / Dzikir & Tadarus 20 Mnt (+60 EXP VIT, +35 Gold)",
            "Sedekah / Berbuat Kebaikan Sosial (+50 EXP VIT, +40 Gold)",
            "Meditasi Sunyi / Refleksi Diri 15 Mnt (+45 EXP VIT, +30 Gold)"
        ])
        
        st.markdown("ℹ️ **Info:** Misi Spiritual bernilai **0 Stamina** (Gratis memulihkan kedamaian jiwa raga).")

        if st.button("🤲 SELESAIKAN IBADAH & SPIRITUAL", use_container_width=True):
            if "Sholat" in worship_choice:
                ex, go = 40, 25
            elif "Kitab Suci" in worship_choice:
                ex, go = 60, 35
            elif "Sedekah" in worship_choice:
                ex, go = 50, 40
            else:
                ex, go = 45, 30

            final_go = int(go * streak_bonus_mult)
            d["gold"] += final_go
            d["total_worship_count"] = d.get("total_worship_count", 0) + 1
            
            add_exp(ex, "VIT", 2)
            log_activity("Ibadah & Spiritual", 1)
            
            st.success(f"✨ Amal ibadah tercatat! Jiwa menjadi tenang. (+{ex} EXP Vitality, +{final_go} Gold)")
            save_game()
            st.rerun()

    # --- QUEST 4: HIDRASI TUBUH (MINUM AIR) ---
    with st.expander("💧 4. Manajemen Hidrasi Tubuh (Asupan Air)"):
        st.write(f"Target Hidrasi Hari Ini: **{d.get('water_ml', 0)} / 2500 ml**")
        st.progress(min(d.get('water_ml', 0) / 2500, 1.0))
        st.caption("ℹ️ Minum air secara berkala menjaga metabolisme otak dan stamina tubuh tetap prima.")

        cw1, cw2, cw3, cw4 = st.columns(4)
        if cw1.button("+ 250 ml"):
            d["water_ml"] = d.get("water_ml", 0) + 250
            save_game(); st.rerun()
        if cw2.button("+ 500 ml"):
            d["water_ml"] = d.get("water_ml", 0) + 500
            save_game(); st.rerun()
        if cw3.button("+ 600 ml"):
            d["water_ml"] = d.get("water_ml", 0) + 600
            save_game(); st.rerun()
        if cw4.button("🔄 Reset"):
            d["water_ml"] = 0
            save_game(); st.rerun()

        if d.get("water_ml", 0) >= 2500 and not d.get("water_reward_claimed", False):
            d["water_reward_claimed"] = True
            add_exp(75, "VIT", 1)
            d["gold"] += 50
            st.balloons()
            st.success("💧 Target Hidrasi 2500ml Tercapai! Bonus +75 EXP & +50 Gold diberikan!")
            save_game()

    # --- QUEST 5: KREATIVITAS & SKILL PENGEMBANGAN DIRI ---
    with st.expander("🎨 5. Proyek Kreatif, Menulis & Problem Solving"):
        creative_task = st.text_input("Nama Proyek / Tugas Kreatif:", placeholder="Contoh: Menulis Artikel, Membuat Desain, Coding Proyek Game")
        task_difficulty = st.selectbox("Tingkat Kompleksitas:", ["Ringan (15 Mnt)", "Menengah (45 Mnt)", "Berat & Kompleks (90 Mnt+)"])
        
        st.markdown("ℹ️ Mengasah logika dan kreativitas (Agility & Intelligence boost).")

        if st.button("💡 SELESAIKAN PROYEK KREATIF", use_container_width=True):
            if d["stamina"] >= 25:
                d["stamina"] -= 25
                
                exp_c = 100 if "Ringan" in task_difficulty else (250 if "Menengah" in task_difficulty else 450)
                gold_c = int(exp_c * 0.4 * streak_bonus_mult)
                
                d["gold"] += gold_c
                add_exp(exp_c, "AGI", 2)
                log_activity(f"Proyek Kreatif: {creative_task or 'General'}", 1)
                
                st.success(f"🎨 Proyek '{creative_task or 'Kreatif'}' berhasil diselesaikan! (+{gold_c} Gold, +{exp_c} EXP)")
                save_game()
                st.rerun()
            else:
                st.warning("Stamina tidak cukup! Butuh minimal 25 Stamina.")

    # --- QUEST 6: BERSIH-BERSIH & LINGKUNGAN (RAPIH & DISIPLIN RUANGAN) ---
    with st.expander("🧹 6. Kebersihan Lingkungan & Kerapihan Meja Kerja"):
        st.caption("Lingkungan yang bersih menciptakan pikiran yang fokus dan terhindar dari rasa malas.")
        
        cleaning_type = st.selectbox("Pilih Aktivitas:", [
            "Merapikan Meja Belajar & Setup Komputer (+30 EXP, +20 Gold)",
            "Membersihkan Seluruh Ruangan / Kamar (+70 EXP, +50 Gold)",
            "Mencuci Pakaian / Peralatan Pribadi (+50 EXP, +30 Gold)"
        ])

        if st.button("🧽 SELESAIKAN TUGAS KEBERSIHAN", use_container_width=True):
            if "Meja" in cleaning_type:
                ce, cg = 30, 20
            elif "Ruangan" in cleaning_type:
                ce, cg = 70, 50
            else:
                ce, cg = 50, 30

            final_cg = int(cg * streak_bonus_mult)
            d["gold"] += final_cg
            add_exp(ce, "VIT", 1)
            log_activity("Kebersihan & Lingkungan", 1)
            
            st.success(f"✨ Lingkungan bersih dan nyaman! (+{ce} EXP Vitality, +{final_cg} Gold)")
            save_game()
            st.rerun()

    # --- QUEST 7: INSTANT SCROLL CONSUMABLE ---
    with st.expander("📜 7. Penggunaan Instant Scroll Spesial"):
        st.caption("Gunakan item gulungan ajaib dari inventory untuk menuntaskan misi instan tanpa menguras stamina.")
        
        if "📜 Scroll of Instant Focus" in d["inventory"]:
            if st.button("⚡ Gunakan Scroll of Instant Focus", use_container_width=True):
                d["inventory"].remove("📜 Scroll of Instant Focus")
                add_exp(200, "INT", 3)
                d["gold"] += 75
                st.success("✨ Semburan energi gulungan ajaib aktif! Misi diselesaikan secara instan (+200 EXP, +75 Gold).")
                save_game()
                st.rerun()
        else:
            st.info("⚠️ Kamu tidak memiliki 'Scroll of Instant Focus' di dalam Inventory. Beli di Shop atau dapatkan dari Gacha Wheel!")
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

# ================= TAB 3: BOSS RAID (FIXED INVENTORY DUPLICATION & DAMAGE BUG) =================
with tab_boss:
    import random

    boss_list = [
        {
            "name": "👾 Procrastination Demon", 
            "weakness": "INT", 
            "desc": "Sensitif terhadap Sesi Belajar!", 
            "drop_rate": 0.45, 
            "legendary_drop": "🗡️ Excalibur of Focus",
            "effect_desc": "+50% Damage Serangan & +15% INT Boost"
        },
        {
            "name": "🐉 Distraction Dragon", 
            "weakness": "STR", 
            "desc": "Hanya lemah terhadap Latihan Fisik/Workout!", 
            "drop_rate": 0.40, 
            "legendary_drop": "🛡️ Aegis Shield of Willpower",
            "effect_desc": "+30% Damage & Mengurangi Hukuman Penalty HP"
        },
        {
            "name": "🔥 Burnout Demon", 
            "weakness": "VIT", 
            "desc": "Butuh konsistensi pemulihan stamina & fokus!", 
            "drop_rate": 0.35, 
            "legendary_drop": "💍 Ring of Endless Energy",
            "effect_desc": "Menggandakan (2x) Bonus Streak Harian"
        },
        {
            "name": "📱 Social Media Overlord", 
            "weakness": "AGI", 
            "desc": "Sangat cepat! Lemah terhadap kecepatan penyelesaian tugas!", 
            "drop_rate": 0.30, 
            "legendary_drop": "👟 Boots of Hyper Productivity",
            "effect_desc": "Menghemat 30% Stamina saat melakukan Workout"
        },
        {
            "name": "👑 Lord of Comfort Zone", 
            "weakness": "INT", 
            "desc": "Membuat malas bergerak! Hancurkan dengan kecerdasan strategi!", 
            "drop_rate": 0.25, 
            "legendary_drop": "👑 Crown of Unstoppable Discipline",
            "effect_desc": "+75% Damage & Bonus EXP berlimpah"
        },
        {
            "name": "💀 Nightmare of Deadlines", 
            "weakness": "STR", 
            "desc": "Sangat mematikan dekat batas waktu! Serang dengan kekuatan penuh!", 
            "drop_rate": 0.20, 
            "legendary_drop": "⚔️ Scythe of Zero Delay",
            "effect_desc": "2x Lipat Damage murni ke semua jenis Boss!"
        },
        {
            "name": "💤 Slothful Giant", 
            "weakness": "VIT", 
            "desc": "Tubuh raksasa penuh kemalasan! Kuras staminanya!", 
            "drop_rate": 0.18, 
            "legendary_drop": "📿 Amulet of Endless Vitality",
            "effect_desc": "+50 Max Stamina Permanen saat di-equip"
        },
        {
            "name": "🌀 Chaos Phantom", 
            "weakness": "AGI", 
            "desc": "Berpindah-pindah dimensi waktu! Kecepatan adalah kunci!", 
            "drop_rate": 0.15, 
            "legendary_drop": "⌛ Cloak of Chronos",
            "effect_desc": "Mengurangi waktu Cooldown Skill aktif sebanyak 1 Turn"
        },
        {
            "name": "🌪️ Tornado of Doubt", 
            "weakness": "INT", 
            "desc": "Menggoyahkan keyakinan belajar! Lawan dengan logika tajam!", 
            "drop_rate": 0.12, 
            "legendary_drop": "🔮 Orb of Absolute Clarity",
            "effect_desc": "+40% Critical Chance untuk semua serangan"
        },
        {
            "name": "🌋 Titan of Chaos", 
            "weakness": "STR", 
            "desc": "Boss pamungkas dengan kekuatan vulkanik! Hancurkan dengan kekuatan maksimal!", 
            "drop_rate": 0.10, 
            "legendary_drop": "🔥 Armor of the Overlord",
            "effect_desc": "2.5x Lipat Damage & Kekebalan mutlak dari kekalahan"
        }
    ]
    
    current_week = datetime.now().isocalendar()[1]
    active_boss = boss_list[current_week % len(boss_list)]
    d["boss_name"] = active_boss["name"]

    if "battle_logs" not in st.session_state:
        st.session_state["battle_logs"] = ["Dungeon raid dibuka. Bersiaplah bertempur, Nauval!"]

    # Inisialisasi struktur data aman & bersih dari duplikasi silang
    if "equipped_items" not in d:
        d["equipped_items"] = []
    if "inventory" not in d:
        d["inventory"] = []

    # Pastikan item yang sudah di-equip TIDAK ADA di dalam inventory secara bersamaan
    for eq in d["equipped_items"]:
        while eq in d["inventory"]:
            d["inventory"].remove(eq)

    # --- UI HEADER & INFO BOSS ---
    st.subheader(f"⚔️ Dungeon RAID Mingguan: {d['boss_name']}")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(f"**🎯 Kelemahan:** Atribut `{active_boss['weakness']}`")
        st.caption(f"📝 {active_boss['desc']}")
        st.markdown(f"🎁 **Drop:** `{active_boss['legendary_drop']}` *(Rate: {int(active_boss['drop_rate']*100)}%)*")
    with col_info2:
        st.markdown(f"💡 **Efek Item:** {active_boss['effect_desc']}")
        st.markdown(f"🏆 **Boss Dikalahkan:** `{d.get('boss_defeated_count', 0)}x`")

    st.markdown("---")

    # --- BOSS HP BAR ---
    hp_percentage = max(0.0, min(d["boss_hp"] / d["boss_max_hp"], 1.0))
    st.progress(hp_percentage, text=f"🔴 HP Boss: {d['boss_hp']} / {d['boss_max_hp']} ({int(hp_percentage * 100)}%)")

    # --- PERHITUNGAN DAMAGE & BONUS (HANYA MENGHITUNG DARI EQUIPPED_ITEMS) ---
    stat_bonus = d["stats"][active_boss["weakness"]] * 3
    base_damage = d["stats"]["STR"] * 2 + d["stats"]["INT"] * 2 + stat_bonus

    if d["skills"]["exam_crusher"] > 0 and active_boss["weakness"] == "INT":
        base_damage = int(base_damage * 1.25)
    if d["skills"]["adrenaline_rush"] > 0 and (d["hp"] / d["max_hp"]) < 0.3:
        base_damage = int(base_damage * 1.5)

    # PENTING: Perhitungan buff damage MURNI berasal dari item yang sedang di-equip saja!
    active_gear = d["equipped_items"]
    
    if "🗡️ Steel Sword of Focus" in active_gear: base_damage = int(base_damage * 1.15)
    if "🗡️ Excalibur of Focus" in active_gear: base_damage = int(base_damage * 1.50)
    if "🛡️ Aegis Shield of Willpower" in active_gear: base_damage = int(base_damage * 1.30)
    if "👑 Crown of Unstoppable Discipline" in active_gear: base_damage = int(base_damage * 1.75)
    if "⚔️ Scythe of Zero Delay" in active_gear: base_damage = int(base_damage * 2.00)
    if "🔥 Armor of the Overlord" in active_gear: base_damage = int(base_damage * 2.50)

    if d["active_pet"] == "🐺 Spirit Wolf": base_damage += 25
    elif d["active_pet"] == "🐲 Baby Dragon": base_damage = int(base_damage * 1.20)

    has_titan = any(b["name"] == "💥 Titan Form Buff (4x Damage)" for b in d["active_buffs"])
    if has_titan:
        base_damage *= 4

    crit_chance = min(0.60, d["stats"]["AGI"] * 0.025)
    if "🔮 Orb of Absolute Clarity" in active_gear:
        crit_chance += 0.40 
    
    is_crit = random.random() < crit_chance
    if is_crit:
        base_damage = int(base_damage * 2.0)

    # --- DASHBOARD STATS ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("⚡ Stamina", f"{d['stamina']} / {d['max_stamina']}")
    m2.metric("💥 Potensi Damage", f"{base_damage} HP")
    m3.metric("🎯 Critical Rate", f"{int(crit_chance * 100)}%")
    m4.metric("🛡️ Status Buff", "Aktif" if has_titan or len(d["active_buffs"]) > 0 else "Normal")

    if has_titan:
        st.warning("⚡ Titan Form Aktif! 4x Multiplier Damage siap dilepaskan!")

    st.markdown("### 🕹️ Panel Aksi Pertempuran")
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        if st.button(f"⚔️ Serang Boss (-20 Stamina)", use_container_width=True):
            if d["stamina"] >= 20:
                play_sfx("attack")
                d["stamina"] -= 20
                
                boss_dodged = (active_boss["weakness"] == "AGI") and (random.random() < 0.12)
                
                if boss_dodged:
                    log_msg = f"💨 Serangan Meleset! {d['boss_name']} berhasil mengelak!"
                    st.session_state["battle_logs"].insert(0, log_msg)
                    st.error(log_msg)
                else:
                    d["boss_hp"] -= base_damage
                    crit_text = "⚡ (CRITICAL HIT!)" if is_crit else ""
                    log_msg = f"💥 Nauval menyerang dan memberikan {base_damage} Damage! {crit_text}"
                    st.session_state["battle_logs"].insert(0, log_msg)
                    st.success(log_msg)

                if has_titan:
                    d["active_buffs"] = [b for b in d["active_buffs"] if b["name"] != "💥 Titan Form Buff (4x Damage)"]

                if d["boss_hp"] <= 0:
                    play_sfx("level_up")
                    d["boss_defeated_count"] += 1
                    reward_gold = 200 + (d["boss_defeated_count"] * 30)
                    reward_exp = 400 + (d["boss_defeated_count"] * 60)
                    d["gold"] += reward_gold
                    add_exp(reward_exp)

                    drop_roll = random.random()
                    dropped_item = active_boss["legendary_drop"]
                    
                    all_existing_items = d["inventory"] + d["equipped_items"]
                    if drop_roll <= active_boss["drop_rate"]:
                        if dropped_item not in all_existing_items:
                            d["inventory"].append(dropped_item)
                            drop_msg = f"🎁 LEGENDARY DROP! Nauval mendapatkan: **{dropped_item}**!"
                            st.session_state["battle_logs"].insert(0, drop_msg)
                            st.success(drop_msg)
                            st.info(f"✨ Item masuk ke tas inventory. Silakan pasang (*equip*) dari tab manajemen item!")
                        else:
                            d["gold"] += 400
                            dup_msg = f"🎁 Drop {dropped_item} sudah dimiliki! Ditukar bonus +400 Gold."
                            st.session_state["battle_logs"].insert(0, dup_msg)
                            st.info(dup_msg)

                    d["boss_max_hp"] = int(d["boss_max_hp"] * 1.4)
                    d["boss_hp"] = d["boss_max_hp"]
                    win_msg = f"🔥 VICTORY! Boss dikalahkan! +{reward_gold} Gold & +{reward_exp} EXP!"
                    st.session_state["battle_logs"].insert(0, win_msg)
                    st.balloons()
                    st.success(win_msg)
                
                save_game()
                st.rerun()
            else:
                st.warning("Stamina tidak cukup untuk menyerang!")

    with col_b:
        if "💣 Procrastination Bomb" in d["inventory"]:
            if st.button("💣 Lempar Bomb (-250 HP)", use_container_width=True):
                d["inventory"].remove("💣 Procrastination Bomb")
                d["boss_hp"] = max(0, d["boss_hp"] - 250)
                bomb_msg = "💣 Procrastination Bomb meledak memberikan 250 Damage instan!"
                st.session_state["battle_logs"].insert(0, bomb_msg)
                st.success(bomb_msg)
                
                if d["boss_hp"] <= 0:
                    d["boss_defeated_count"] += 1
                    d["gold"] += 250
                    add_exp(350)
                    d["boss_max_hp"] = int(d["boss_max_hp"] * 1.4)
                    d["boss_hp"] = d["boss_max_hp"]
                    st.balloons()
                
                save_game()
                st.rerun()
        else:
            st.button("💣 Beli Bomb di Shop", disabled=True, use_container_width=True)

    with col_c:
        if st.button("🧪 Gunakan Mega Elixir", use_container_width=True):
            if "🧪 Mega Elixir" in d["inventory"]:
                d["inventory"].remove("🧪 Mega Elixir")
                d["hp"] = d["max_hp"]
                d["stamina"] = d["max_stamina"]
                elixir_msg = "🧪 Mega Elixir digunakan! HP & Stamina pulih 100%."
                st.session_state["battle_logs"].insert(0, elixir_msg)
                st.success(elixir_msg)
                save_game()
                st.rerun()
            else:
                st.warning("Tidak punya Mega Elixir di Inventory!")

    st.markdown("---")

    # --- FITUR TAMBAHAN: LIVE COMBAT LOG & MANAJEMEN ITEM AMAN ---
    tab_log, tab_collection = st.tabs(["📜 Live Battle Log", "🛡️ Rincian & Manajemen Efek Item"])
    
    with tab_log:
        st.markdown("Aktivitas pertempuran terkini:")
        recent_logs = st.session_state["battle_logs"][:5]
        for log in recent_logs:
            st.text(f"• {log}")
            
    with tab_collection:
        st.markdown("### 🎒 Manajemen Tas Inventory & Equip Gear")
        st.caption("Klik tombol **'Pakai (Equip)'** agar item aktif memperkuat atributmu dalam pertempuran, atau **'Lepas (Unequip)'** untuk menyimpannya kembali ke tas.")

        item_effects_database = {
            "🗡️ Steel Sword of Focus": "Memberikan tambahan +15% kekuatan Damage saat menyerang musuh atau boss.",
            "💣 Procrastination Bomb": "Item habis pakai (consumable). Memberikan 250 Damage murni instan langsung ke HP Boss saat dilempar.",
            "🧪 Mega Elixir": "Item habis pakai (consumable). Memulihkan HP dan Stamina Nauval kembali penuh 100% seketika.",
            "🗡️ Excalibur of Focus": "+50% Damage Serangan dasar & +15% INT Boost penunjang kecerdasan.",
            "🛡️ Aegis Shield of Willpower": "+30% Damage serangan & mengurangi hukuman penalty pengurangan HP saat gagal.",
            "💍 Ring of Endless Energy": "Menggandakan (2x lipat) bonus perolehan Streak Harian.",
            "👟 Boots of Hyper Productivity": "Menghemat 30% konsumsi Stamina saat melakukan sesi latihan fisik (workout).",
            "👑 Crown of Unstoppable Discipline": "+75% Damage besar-besaran & mendatangkan bonus EXP berlimpah.",
            "⚔️ Scythe of Zero Delay": "Memberikan 2x lipat (200%) Damage murni ke semua jenis Boss Raid.",
            "📿 Amulet of Endless Vitality": "Memberikan tambahan +50 batas maksimal (Max) Stamina secara permanen saat di-equip.",
            "⌛ Cloak of Chronos": "Mengurangi waktu tunggu (Cooldown) penggunaan Skill aktif sebanyak 1 Turn.",
            "🔮 Orb of Absolute Clarity": "Menambahkan +40% peluang Critical Chance untuk seluruh variasi serangan.",
            "🔥 Armor of the Overlord": "Memberikan 2.5x Lipat Damage murni & proteksi kekebalan mutlak dari kekalahan."
        }

        # Gabungkan item unik dari kedua list secara bersih tanpa duplikat ganda
        unique_owned_items = list(set(d["inventory"] + d["equipped_items"]))

        if unique_owned_items:
            for item in unique_owned_items:
                effect_explanation = item_effects_database.get(item, "Item khusus dengan efek misterius yang membantu produktivitasmu.")
                is_equipped = item in d["equipped_items"]
                
                with st.container(border=True):
                    col_item1, col_item2, col_item3 = st.columns([1.5, 2, 1])
                    with col_item1:
                        st.markdown(f"**{item}**")
                        if is_equipped:
                            st.caption("🟢 Status: Dipakai (Equipped)")
                        else:
                            st.caption("🔵 Status: Dalam Tas (Inventory)")
                    with col_item2:
                        st.markdown(f"*Efek:* {effect_explanation}")
                    with col_item3:
                        if not is_equipped:
                            if item not in ["💣 Procrastination Bomb", "🧪 Mega Elixir"]:
                                if st.button("🟢 Pakai", key=f"equip_{item}", use_container_width=True):
                                    # Pindahkan item secara bersih: hapus dari inventory, masukkan ke equipped
                                    if item in d["inventory"]:
                                        d["inventory"].remove(item)
                                    if item not in d["equipped_items"]:
                                        d["equipped_items"].append(item)
                                    save_game()
                                    st.success(f"Berhasil memakai {item}!")
                                    st.rerun()
                            else:
                                st.caption("Gunakan langsung di panel aksi")
                        else:
                            if st.button("🔴 Lepas", key=f"unequip_{item}", use_container_width=True):
                                # Pindahkan item secara bersih: hapus dari equipped, masukkan ke inventory
                                if item in d["equipped_items"]:
                                    d["equipped_items"].remove(item)
                                if item not in d["inventory"]:
                                    d["inventory"].append(item)
                                save_game()
                                st.warning(f"Berhasil melepas {item}!")
                                st.rerun()
        else:
            st.info("Tas inventori Nauval masih kosong. Selesaikan misi, belanja di shop, atau taklukkan Boss Raid untuk mengisinya!")
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
        # --- ITEM LAMA ---
        {"name": "☕ Espresso Shot", "cost": 45, "type": "instant_stamina", "val": 30, "desc": "+30 Stamina Instan"},
        {"name": "⚡ Vitality Potion", "cost": 60, "type": "instant_stamina", "val": 50, "desc": "+50 Stamina Instan"},
        {"name": "📜 Scroll of Instant Focus", "cost": 100, "type": "item", "desc": "Selesaikan 1 quest instant tanpa stamina."},
        {"name": "🛡️ Potion Kebal Penundaan", "cost": 180, "type": "item", "desc": "Tolak 1x hukuman sosmed otomatis."},
        {"name": "🍀 Clover of Luck", "cost": 200, "type": "buff", "duration": 24, "desc": "+25% Hoki Gacha Harian"},
        {"name": "🧪 Double EXP Elixir", "cost": 150, "type": "buff", "duration": 2, "desc": "2x EXP selama 2 Jam"},
        {"name": "📜 Scroll of Oblivion", "cost": 300, "type": "respec", "desc": "Reset semua Skill Points untuk alokasi ulang."},
        
        # --- ITEM TAMBAHAN BARU ---
        {"name": "❤️ Health Potion", "cost": 50, "type": "instant_hp", "val": 40, "desc": "+40 HP Instan saat sekarat"},
        {"name": "🧪 Mega Elixir", "cost": 150, "type": "instant_full", "desc": "Pulihkan HP & Stamina ke 100% Seketika"},
        {"name": "🍎 Apple of Eden", "cost": 400, "type": "perm_stat", "stat": "INT", "val": 3, "desc": "+3 INT Permanen"},
        {"name": "🥊 Titan Serum", "cost": 400, "type": "perm_stat", "stat": "STR", "val": 3, "desc": "+3 STR Permanen"},
        {"name": "⚡ Hermes Feather", "cost": 400, "type": "perm_stat", "stat": "AGI", "val": 3, "desc": "+3 AGI Permanen"},
        {"name": "🛡️ Heart of Iron", "cost": 400, "type": "perm_stat", "stat": "VIT", "val": 3, "desc": "+3 VIT Permanen"},
        {"name": "👑 Elixir of Perfection", "cost": 700, "type": "perm_all_stat", "val": 2, "desc": "+2 All Stats Permanen"},
        {"name": "📖 Tome of Knowledge", "cost": 350, "type": "direct_sp", "val": 1, "desc": "Langsung dapat +1 Skill Point (SP)"},
        {"name": "✨ EXP Tonic", "cost": 120, "type": "direct_exp", "val": 250, "desc": "+250 EXP Instan"},
        {"name": "💣 Procrastination Bomb", "cost": 220, "type": "boss_nuke", "val": 200, "desc": "Serang Boss langsung -200 HP"},
        {"name": "⌛ Hourglass of Time", "cost": 250, "type": "instant_cd", "desc": "Reset seluruh cooldown skill aktif"}
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
                
                # --- LOGIKA LAMA (TETAP DIJAGA) ---
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
                
                # --- LOGIKA TAMBAHAN UNTUK ITEM BARU ---
                elif p["type"] == "instant_hp":
                    d["hp"] = min(d["max_hp"], d["hp"] + p["val"])
                elif p["type"] == "instant_full":
                    d["hp"] = d["max_hp"]
                    d["stamina"] = d["max_stamina"]
                elif p["type"] == "perm_stat":
                    d["stats"][p["stat"]] += p["val"]
                elif p["type"] == "perm_all_stat":
                    for st_k in d["stats"]:
                        d["stats"][st_k] += p["val"]
                elif p["type"] == "direct_sp":
                    d["skill_points"] += p["val"]
                elif p["type"] == "direct_exp":
                    add_exp(p["val"])
                elif p["type"] == "boss_nuke":
                    d["boss_hp"] = max(0, d["boss_hp"] - p["val"])
                elif p["type"] == "instant_cd":
                    for sk_cd in d["active_skills_cd"]:
                        d["active_skills_cd"][sk_cd] = 0

                save_game()
                st.success(f"Berhasil membeli {p['name']}!")
                st.rerun()
            else:
                st.error("Gold tidak cukup!")

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

# ================= TAB 7: GACHA SPIN WHEEL (ULTRA COMPLEX & EPIC ANIMATED) =================
with tab_gacha:
    import time
    
    st.subheader("🎡 Mega Gacha Spin Wheel - Hall of Fortune")
    st.caption("Putar roda keberuntungan tingkat lanjut! Rasakan sensasi animasi spin real-time, sistem Tier Gacha (Bronze, Silver, Gold, Prismatic), dan ragam hadiah legendaris yang disesuaikan dengan Streak-mu, Nauval.")
    
    today_str = str(date.today())
    
    # Inisialisasi state gacha di session_state
    if "gacha_tier" not in st.session_state:
        st.session_state["gacha_tier"] = "Silver" # Default tier harian
    if "is_spinning" not in st.session_state:
        st.session_state["is_spinning"] = False
    if "gacha_history" not in st.session_state:
        st.session_state["gacha_history"] = []

    # Hitung Streak Multiplier & Level Keberuntungan
    streak_multiplier = 1.0 + (d["streak"] * 0.15)
    
    # Dashboard Metrik Gacha
    mg1, mg2, mg3, mg4 = st.columns(4)
    mg1.metric("🔥 Streak Aktif", f"{d['streak']} Hari")
    mg2.metric("⚡ Multiplier Reward", f"{round(streak_multiplier, 2)}x")
    mg3.metric("🎫 Status Tiket Harian", "Tersedia" if d["last_gacha_date"] != today_str else "Sudah Diklaim")
    mg4.metric("📦 Riwayat Gacha", f"{len(st.session_state['gacha_history'])} Item")

    st.markdown("---")

    # --- POOL HADIAH GACHA SUPER KOMPLEKS (DIKELOMPOKKAN BERDASARKAN KATEGORI & RARITY) ---
    epic_wheel_pool = [
        # --- COMMON (Kategori: Sumber Daya Kecil) ---
        {"name": "🪙 75 Gold Nugget", "type": "gold", "val": 75, "icon": "🪙", "rarity": "Common", "weight": 25},
        {"name": "✨ 120 Spark EXP", "type": "exp", "val": 120, "icon": "✨", "rarity": "Common", "weight": 25},
        {"name": "⚡ +25 Stamina Flask", "type": "stamina", "val": 25, "icon": "⚡", "rarity": "Common", "weight": 20},
        
        # --- UNCOMMON (Kategori: Sumber Daya Menengah & Konsumtif) ---
        {"name": "🪙 200 Gold Pouch", "type": "gold", "val": 200, "icon": "🪙", "rarity": "Uncommon", "weight": 15},
        {"name": "✨ 350 Radiant EXP", "type": "exp", "val": 350, "icon": "✨", "rarity": "Uncommon", "weight": 15},
        {"name": "💣 Procrastination Bomb", "type": "item", "val": "💣 Procrastination Bomb", "icon": "💣", "rarity": "Uncommon", "weight": 10},
        {"name": "🧪 Mega Elixir", "type": "item", "val": "🧪 Mega Elixir", "icon": "🧪", "rarity": "Uncommon", "weight": 10},
        
        # --- RARE (Kategori: Gear Dasar & Buff Sementara) ---
        {"name": "🗡️ Steel Sword of Focus", "type": "item", "val": "🗡️ Steel Sword of Focus", "icon": "🗡️", "rarity": "Rare", "weight": 6},
        {"name": "🛡️ Aegis Shield of Willpower", "type": "item", "val": "🛡️ Aegis Shield of Willpower", "icon": "🛡️", "rarity": "Rare", "weight": 5},
        {"name": "💍 Ring of Endless Energy", "type": "item", "val": "💍 Ring of Endless Energy", "icon": "💍", "rarity": "Rare", "weight": 5},
        
        # --- EPIC (Kategori: Gear Tingkat Lanjut & Bonus Atribut) ---
        {"name": "👟 Boots of Hyper Productivity", "type": "item", "val": "👟 Boots of Hyper Productivity", "icon": "👟", "rarity": "Epic", "weight": 3},
        {"name": "📿 Amulet of Endless Vitality", "type": "item", "val": "📿 Amulet of Endless Vitality", "icon": "📿", "rarity": "Epic", "weight": 3},
        {"name": "⌛ Cloak of Chronos", "type": "item", "val": "⌛ Cloak of Chronos", "icon": "⌛", "rarity": "Epic", "weight": 2},
        {"name": "🔮 Orb of Absolute Clarity", "type": "item", "val": "🔮 Orb of Absolute Clarity", "icon": "🔮", "rarity": "Epic", "weight": 2},
        
        # --- LEGENDARY (Kategori: Item Dewa & Harta Karun Utama) ---
        {"name": "💎 JACKPOT GRAND 1,000 Gold!", "type": "gold", "val": 1000, "icon": "💎", "rarity": "Legendary", "weight": 1.5},
        {"name": "🗡️ Excalibur of Focus", "type": "item", "val": "🗡️ Excalibur of Focus", "icon": "⚔️", "rarity": "Legendary", "weight": 1},
        {"name": "👑 Crown of Unstoppable Discipline", "type": "item", "val": "👑 Crown of Unstoppable Discipline", "icon": "👑", "rarity": "Legendary", "weight": 0.8},
        {"name": "⚔️ Scythe of Zero Delay", "type": "item", "val": "⚔️ Scythe of Zero Delay", "icon": "🔪", "rarity": "Legendary", "weight": 0.5},
        {"name": "🔥 Armor of the Overlord", "type": "item", "val": "🔥 Armor of the Overlord", "icon": "🛡️", "rarity": "Legendary", "weight": 0.3}
    ]

    # Cek Buff Clover of Luck untuk memodifikasi bobot drop rate
    has_clover = any(b["name"] == "🍀 Clover of Luck" for b in d["active_buffs"])
    if has_clover:
        st.success("🍀 Clover of Luck aktif! Keberuntunganmu meningkat: Bobot item Epic & Legendary dilipatgandakan!")
        # Modifikasi bobot jika clover aktif (tingkatkan item kategori Rare, Epic, Legendary)
        for item in epic_wheel_pool:
            if item["rarity"] in ["Rare", "Epic", "Legendary"]:
                item["weight"] *= 2.5

    # Area Kontainer Utama Roda Gacha
    spin_display_container = st.empty()

    if d["last_gacha_date"] == today_str:
        spin_display_container.markdown(
            """
            <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #1e1e1e 0%, #2d2d2d 100%); border-radius: 16px; border: 2px dashed #555;">
                <h2 style="color: #ff4b4b;">🔒 Tiket Spin Hari Ini Sudah Digunakan</h2>
                <p style="color: #ccc; font-size: 16px;">Roda keberuntungan sedang dalam cooldown pengisian energi kosmik. Silakan kembali besok untuk memutar ulang, Nauval!</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        # Pilihan Mode Spin (Bisa Normal atau Menggunakan Gold Tambahan jika ingin gacha ekstra)
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            st.info("🎟️ **Spin Harian Utama:** Gratis (1x Sehari)")
        with col_opt2:
            extra_spin_cost = 250
            if st.button(f"💎 Beli Extra Spin (🪙 {extra_spin_cost} Gold)", use_container_width=True):
                if d["gold"] >= extra_spin_cost:
                    d["gold"] -= extra_spin_cost
                    # Izinkan spin instan dengan membuka paksa temporary flag
                    d["last_gacha_date"] = "" # Reset sementara untuk extra spin
                    st.success("💎 Extra Spin dibeli! Silakan putar rodanya sekarang!")
                    save_game()
                    st.rerun()
                else:
                    st.warning("Gold kamu tidak cukup untuk membeli Extra Spin!")

        if not st.session_state["is_spinning"]:
            spin_display_container.markdown(
                """
                <div style="text-align: center; padding: 35px; background: linear-gradient(135deg, #121212 0%, #1f1f2e 100%); border-radius: 16px; border: 2px solid #ff4b4b;">
                    <h2>🎡 SIAP MEMUTAR RODA KEBERUNTUNGAN?</h2>
                    <p style="color: #aaa;">Hadiah eksklusif menanti ketulusan disiplin belajarmu hari ini!</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            if st.button("🚀 TEKAN UNTUK PUTAR RODA (SPIN NOW!)", use_container_width=True, type="primary"):
                st.session_state["is_spinning"] = True
                st.rerun()
        else:
            # Simulasi Animasi Roda Slot Interaktif Real-time
            animation_box = st.empty()
            sample_icons = ["🪙", "✨", "⚡", "🗡️", "🛡️", "💍", "💣", "🧪", "👟", "👑", "💎", "🔥"]
            
            # Efek visual animasi berputar kencang lalu melambat
            for i in range(12):
                rand_visual = random.choice(epic_wheel_pool)
                animation_box.markdown(
                    f"""
                    <div style="text-align: center; padding: 45px; background-color: #111; border-radius: 16px; border: 2px solid #ff4b4b;">
                        <h1 style="font-size: 50px; margin: 0;">{rand_visual['icon']}</h1>
                        <h3 style="color: #ff4b4b; margin-top: 10px;">Memutar Roda... (Kecepatan Level {12-i})</h3>
                        <p style="color: #888;">Menyeleksi takdir item: <i>{rand_visual['name']}</i></p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                time.sleep(0.12)

            # Eksekusi Pemilihan Hadiah Berdasarkan Bobot (Weighted Random Choice)
            pool_names = [item["name"] for item in epic_wheel_pool]
            pool_weights = [item["weight"] for item in epic_wheel_pool]
            chosen_item_data = random.choices(epic_wheel_pool, weights=pool_weights, k=1)[0]

            # Update Tanggal Gacha Harian
            d["last_gacha_date"] = today_str
            
            # Proses Hadiah ke State Game (d)
            reward_summary_text = ""
            if chosen_item_data["type"] == "gold":
                final_val = int(chosen_item_data["val"] * streak_multiplier)
                d["gold"] += final_val
                reward_summary_text = f"🪙 {final_val} Gold (Termasuk Bonus Streak {round(streak_multiplier, 2)}x)"
            elif chosen_item_data["type"] == "exp":
                final_val = int(chosen_item_data["val"] * streak_multiplier)
                add_exp(final_val)
                reward_summary_text = f"✨ {final_val} EXP (Termasuk Bonus Streak {round(streak_multiplier, 2)}x)"
            elif chosen_item_data["type"] == "stamina":
                d["stamina"] = min(d["max_stamina"], d["stamina"] + chosen_item_data["val"])
                reward_summary_text = f"⚡ +{chosen_item_data['val']} Stamina berhasil dipulihkan!"
            elif chosen_item_data["type"] == "item":
                item_name = chosen_item_data["val"]
                all_existing_gear = d["inventory"] + d["equipped_items"]
                if item_name not in all_existing_gear:
                    d["inventory"].append(item_name)
                    reward_summary_text = f"🎁 Item Spesial Langka Didapatkan: **{item_name}**!"
                else:
                    # Jika item sudah ada, kompensasi konversi jadi Gold melimpah
                    d["gold"] += 500
                    reward_summary_text = f"🎁 Item {item_name} sudah dimiliki! Dikonversi otomatis menjadi +500 Gold Kompensasi."

            # Simpan ke riwayat gacha session
            st.session_state["gacha_history"].insert(0, {
                "time": str(datetime.now().strftime("%H:%M:%S")),
                "reward": reward_summary_text,
                "rarity": chosen_item_data["rarity"]
            })

            st.session_state["is_spinning"] = False
            save_game()
            st.balloons()
            st.rerun()

    st.markdown("---")

    # --- TABEL DETAIL KEMUNGKINAN HADIAH & RIWAYAT GACHA ---
    tab_pool_info, tab_history = st.tabs(["📚 Katalog Pool Hadiah & Rarity", "📜 Riwayat Gacha Sesi Ini"])

    with tab_pool_info:
        st.markdown("### 🌟 Klasifikasi Tingkat Kelangkaan (Rarity Tier)")
        st.caption("Berikut adalah seluruh daftar item, mata uang, dan bonus yang dapat ditarik dari Roda Gacha:")

        # Tampilkan dalam bentuk card rapi berdasarkan rarity
        for item in epic_wheel_pool:
            with st.container(border=True):
                col_i1, col_i2, col_i3, col_i4 = st.columns([0.5, 2, 1.5, 3])
                col_i1.markdown(f"### {item['icon']}")
                col_i2.markdown(f"**{item['name']}**")
                
                # Warna label rarity
                rarity_color = {
                    "Common": "🔵 Common",
                    "Uncommon": "🟢 Uncommon",
                    "Rare": "🟣 Rare",
                    "Epic": "🟠 Epic",
                    "Legendary": "🌟 LEGENDARY"
                }.get(item["rarity"], item["rarity"])
                
                col_i3.markdown(f"`{rarity_color}`")
                
                effect_desc_map = {
                    "gold": "Menambah pundi-pundi tabungan mata uang emas.",
                    "exp": "Mempercepat progres kenaikan level karakter Nauval.",
                    "stamina": "Mengisi ulang cadangan energi aksi harian.",
                    "item": "Gear/Senjata spesial penambah status kekuatan pertempuran."
                }
                col_i4.text(effect_desc_map.get(item["type"], "Bonus spesial produktivitas."))

    with tab_history:
        st.markdown("### 🕒 Catatan Riwayat Tarikan Gacha")
        if st.session_state["gacha_history"]:
            for hist in st.session_state["gacha_history"]:
                st.text(f"[{hist['time']}] - Rarity: ({hist['rarity']}) -> {hist['reward']}")
        else:
            st.info("Belum ada riwayat tarikan gacha pada sesi ini. Ayo putar rodanya sekarang!")

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

    # DAFTAR SELURUH ACHIEVEMENTS DALAM GAME
    all_achievements = [
        # PERMANENT TARGETS (ACADEMIC & STUDY)
        {"name": "📚 Bookworm Master", "desc": "Total belajar mencapai 10 jam", "req_type": "study", "req_val": 10.0, "reward": 100},
        {"name": "🎓 Scholar Legend", "desc": "Total belajar mencapai 50 jam", "req_type": "study", "req_val": 50.0, "reward": 300},
        {"name": "🏛️ Grand Academician", "desc": "Total belajar mencapai 100 jam", "req_type": "study", "req_val": 100.0, "reward": 500},
        
        # PERMANENT TARGETS (STREAK & DISCIPLINE)
        {"name": "🔥 Iron Warrior (7 Days Streak)", "desc": "Pertahankan streak selama 7 hari berturut-turut", "req_type": "streak", "req_val": 7, "reward": 150},
        {"name": "⚡ Unstoppable Force (14 Days Streak)", "desc": "Pertahankan streak selama 14 hari berturut-turut", "req_type": "streak", "req_val": 14, "reward": 300},
        {"name": "👑 Emperor of Consistency (30 Days Streak)", "desc": "Pertahankan streak selama 30 hari berturut-turut", "req_type": "streak", "req_val": 30, "reward": 1000},
        
        # PERMANENT TARGETS (DUNGEON & BOSS)
        {"name": "⚔️ Demon Slayer Elite", "desc": "Kalahkan Boss Raid sebanyak 5 kali", "req_type": "boss", "req_val": 5, "reward": 200},
        {"name": "🐲 Dragon Vanquisher", "desc": "Kalahkan Boss Raid sebanyak 15 kali", "req_type": "boss", "req_val": 15, "reward": 500},
        
        # PERMANENT TARGETS (SPIRITUAL & STATS)
        {"name": "🕌 Spiritual Devotee", "desc": "Selesaikan 10 kali ibadah/refleksi", "req_type": "worship", "req_val": 10, "reward": 100},
        {"name": "🌟 Saint of Light", "desc": "Selesaikan 50 kali ibadah/refleksi", "req_type": "worship", "req_val": 50, "reward": 400},
        {"name": "💪 Hercules Candidate", "desc": "Miliki Stat STR minimal 50", "req_type": "stat_str", "req_val": 50, "reward": 250},
        {"name": "🧠 Mastermind Genius", "desc": "Miliki Stat INT minimal 50", "req_type": "stat_int", "req_val": 50, "reward": 250},

        # PERMANENT TARGETS (LEVEL & ECONOMY)
        {"name": "🌟 Rising Star", "desc": "Capai Karakter Level 5", "req_type": "level", "req_val": 5, "reward": 100},
        {"name": "🛡️ Veteran Adventurer", "desc": "Capai Karakter Level 15", "req_type": "level", "req_val": 15, "reward": 300},
        {"name": "👑 Perfect Human Ascended", "desc": "Capai Karakter Level 30", "req_type": "level", "req_val": 30, "reward": 1000},
        {"name": "💰 Gold Hoarder", "desc": "Kumpulkan 1,000 Total Gold", "req_type": "gold", "req_val": 1000, "reward": 200},
        {"name": "💎 Millionaire Mindset", "desc": "Kumpulkan 5,000 Total Gold", "req_type": "gold", "req_val": 5000, "reward": 800},

        # WEEKLY TARGETS (RESET SETIAP MINGGU)
        {"name": "🎯 Weekly Champion (Weekly Target)", "desc": "Selesaikan 5 quest harian dalam satu hari", "req_type": "quests_today", "req_val": 5, "reward": 150},
        {"name": "📖 Weekly Scholar (Weekly Target)", "desc": "Belajar minimal 5 jam dalam minggu ini", "req_type": "study", "req_val": 5.0, "reward": 150},
        {"name": "💧 Hydration Hero (Weekly Target)", "desc": "Minum air 2000ml dalam satu hari", "req_type": "water", "req_val": 2000, "reward": 100}
    ]

    # RINGKASAN PROGRESS & TERBUKA
    unlocked_count = len(d["achievements"])
    total_count = len(all_achievements)
    st.write(f"📊 **Pencapaian Terbuka:** {unlocked_count} / {total_count} ({int((unlocked_count/total_count)*100)}%)")
    st.progress(unlocked_count / total_count)
    st.divider()

    # LOGIKA LAMA (MENAMPILKAN ACHIEVEMENT TERBUKA)
    st.markdown("### 🎉 Lencana yang Sudah Didapatkan")
    if d["achievements"]:
        for ach in d["achievements"]:
            st.success(f"🏆 Lencana Terbuka: **{ach}**")
    else:
        st.info("Belum ada Achievement yang didapatkan. Tingkatkan level dan quest harianmu!")

    st.divider()

    # LOGIKA TAMBAHAN (PROGRESS DAFTAR SELURUH ACHIEVEMENTS)
    st.markdown("### 📜 Daftar Seluruh Misi Achievement & Progress")
    for ach in all_achievements:
        is_unlocked = ach["name"] in d["achievements"]
        
        curr_val = 0
        if ach["req_type"] == "study":
            curr_val = d["total_study_hours"]
        elif ach["req_type"] == "streak":
            curr_val = d["streak"]
        elif ach["req_type"] == "boss":
            curr_val = d["boss_defeated_count"]
        elif ach["req_type"] == "worship":
            curr_val = d.get("total_worship_count", 0)
        elif ach["req_type"] == "stat_str":
            curr_val = d["stats"]["STR"]
        elif ach["req_type"] == "stat_int":
            curr_val = d["stats"]["INT"]
        elif ach["req_type"] == "level":
            curr_val = d["level"]
        elif ach["req_type"] == "gold":
            curr_val = d["gold"]
        elif ach["req_type"] == "quests_today":
            curr_val = d["quests_done_today"]
        elif ach["req_type"] == "water":
            curr_val = d["water_ml"]

        pct = min(1.0, float(curr_val) / float(ach["req_val"]))
        
        name_str = ach['name']
        desc_str = ach['desc']
        reward_val = ach['reward']
        req_val = ach['req_val']

        if is_unlocked:
            st.caption(f"✅ **{name_str}** — *{desc_str}* (Hadiah: +{reward_val} Gold)")
            st.progress(1.0)
        else:
            st.caption(f"🔒 **{name_str}** — *{desc_str}* ({curr_val}/{req_val}) — Hadiah: 🪙 {reward_val} Gold")
            st.progress(pct)

# ================= TAB 10: ANALYTICS =================
with tab_analytics:
    st.subheader("📈 Analytics Kedisiplinan")
    if d["activity_log"]:
        df = pd.DataFrame(d["activity_log"])
        st.bar_chart(df, x="date", y="value", color="activity")
     else:
        st.info("Belum ada data aktivitas.")
