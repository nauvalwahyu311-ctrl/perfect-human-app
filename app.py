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
    "last_weekly_reset": ""
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
    """Mengecek pencapaian berdasarkan real-time data dan mingguan"""
    now = datetime.now()
    current_year_week = f"{now.year}-W{now.isocalendar()[1]}"
    
    # Reset Logika Mingguan jika minggu baru berganti
    if d["last_weekly_reset"] != current_year_week:
        d["last_weekly_reset"] = current_year_week
        # Menghapus achievement mingguan bertipe temporary jika ada
        d["achievements"] = [a for a in d["achievements"] if not a.endswith("(Weekly Target)")]

    new_achievements = []

    # Target 1: Bookworm
    if d["total_study_hours"] >= 10.0 and "📚 Bookworm Master" not in d["achievements"]:
        new_achievements.append("📚 Bookworm Master")
    
    # Target 2: Iron Warrior (Streak)
    if d["streak"] >= 7 and "🔥 Iron Warrior (7 Days Streak)" not in d["achievements"]:
        new_achievements.append("🔥 Iron Warrior (7 Days Streak)")
        
    # Target 3: Demon Slayer
    if d["boss_defeated_count"] >= 5 and "⚔️ Demon Slayer Elite" not in d["achievements"]:
        new_achievements.append("⚔️ Demon Slayer Elite")

    # Target Mingguan (Automated Weekly Refresh)
    if d["quests_done_today"] >= 5 and "🎯 Weekly Champion (Weekly Target)" not in d["achievements"]:
        new_achievements.append("🎯 Weekly Champion (Weekly Target)")

    for ach in new_achievements:
        d["achievements"].append(ach)
        st.toast(f"🏆 ACHIEVEMENT UNLOCKED: {ach}!", icon="🎉")
        d["gold"] += 100
        save_game()

def add_exp(amount, stat_type=None, stat_gain=1):
    has_double_exp = any(b["name"] == "🧪 Double EXP Elixir" for b in d["active_buffs"])
    if has_double_exp:
        amount *= 2
        st.info("✨ Buff Double EXP Aktif! EXP dilipatgandakan.")

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
        d["stats"][stat_type] += (stat_gain + pet_bonus + pet_stat_bonus)
    
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
        st.success(f"🎉 LEVEL UP! Nauval naik ke Level {d['level']}! (+50 Gold)")
    
    check_achievements()
    save_game()

def apply_penalty(hp_loss, exp_loss):
    if "🛡️ Potion Kebal Penundaan" in d["inventory"]:
        d["inventory"].remove("🛡️ Potion Kebal Penundaan")
        st.success("🛡️ Potion Kebal Penundaan digunakan otomatis! Hukuman dibatalkan.")
        save_game()
        return

    has_shield = any(b["name"] == "🛡️ Focus Shield Buff" for b in d["active_buffs"])
    if has_shield:
        st.warning("🛡️ Focus Shield melindungi Nauval dari hukuman!")
        return

    if "🛡️ Shield of Iron Will" in d["equipped_items"]:
        hp_loss = int(hp_loss * 0.8)
        exp_loss = int(exp_loss * 0.8)

    if d["active_pet"] == "🐈‍⬛ Shadow Cat of Discipline":
        hp_loss = int(hp_loss * 0.75)
        st.info("🐈‍⬛ Shadow Cat mengurangi 25% hukuman HP!")

    d["hp"] = max(0, d["hp"] - hp_loss)
    d["exp"] = max(0, d["exp"] - exp_loss)
    save_game()
    st.error(f"⚠️ Hukuman Diterima: -{hp_loss} HP | -{exp_loss} EXP")

# Synchronize System Time
check_achievements()

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
    with st.expander("🚨 Zona Bahaya (Reset Game)"):
        st.caption("Menghapus semua progress dan mengulang dari awal.")
        if st.button("⚠️ Reset Seluruh Data", use_container_width=True):
            if os.path.exists("save_data.json"):
                os.remove("save_data.json")
            st.session_state.data = default_data
            st.rerun()

# ==========================================
# 🏰 HEADER STATUS KARAKTER
# ==========================================
st.title(f"🏰 KETUA {d['name'].upper()}")
st.caption(f"Gelar Kedisiplinan: **{d['title']}** | Pet: **{d['active_pet']}**")

st.subheader(f"🎯 Main Goal: {d['main_goal']}")
st.progress(d["goal_progress"] / 100, text=f"Progres Utama: {d['goal_progress']}%")

st.divider()

exp_ratio = min(d["exp"] / d["exp_needed"], 1.0)
st.progress(exp_ratio, text=f"EXP: {d['exp']} / {d['exp_needed']} (Level {d['level']})")

col_hp, col_sta = st.columns(2)
with col_hp:
    st.caption(f"❤️ Health (HP): {d['hp']}/{d['max_hp']}")
    st.progress(min(d['hp'] / d['max_hp'], 1.0))
with col_sta:
    st.caption(f"⚡ Stamina: {d['stamina']}/{d['max_stamina']}")
    st.progress(min(d['stamina'] / d['max_stamina'], 1.0))

c1, c2, c3, c4 = st.columns(4)
c1.metric("🪙 Gold", f"{d['gold']}")
c2.metric("🔥 Streak", f"{d['streak']} Hr")
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

with st.expander("📊 Lihat Atribut Karakter", expanded=False):
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("🏋️ STR", d["stats"]["STR"])
    s2.metric("📚 INT", d["stats"]["INT"])
    s3.metric("⚡ AGI", d["stats"]["AGI"])
    s4.metric("🛡️ VIT", d["stats"]["VIT"])

st.divider()

# ==========================================
# 📑 TAB UTAMA APLIKASI
# ==========================================
tab_quest, tab_boss, tab_penalty, tab_shop, tab_equips, tab_gacha, tab_pet, tab_achieve, tab_analytics = st.tabs([
    "⚔️ Quest", "👾 Boss", "🚨 Penalty", "🧪 Shop", "🗡️ Armory", "🎡 Gacha", "🐾 Pet", "🏆 Badges", "📈 Analytics"
])

# ================= TAB 1: QUEST =================
with tab_quest:
    st.subheader("📌 Misi Kedisiplinan Harian")
    
    with st.expander("📚 1. Sesi Belajar & Skill", expanded=True):
        study_hours = st.number_input("Berapa jam belajar hari ini?", min_value=0.5, max_value=12.0, value=1.0, step=0.5)
        stamina_cost = int(study_hours * 20)
        if st.button(f"🚀 Selesaikan Belajar ({study_hours} Jam)", use_container_width=True):
            if d["stamina"] >= stamina_cost:
                d["stamina"] -= stamina_cost
                d["gold"] += int(study_hours * 25)
                d["total_study_hours"] += study_hours
                add_exp(int(study_hours * 100), "INT", int(study_hours * 2))
                log_activity("Belajar (Jam)", study_hours)
                st.success("Selesai Belajar!")
                st.rerun()
            else:
                st.warning("Stamina tidak cukup!")

    with st.expander("🏋️ 2. Workout & Olahraga"):
        workout_mins = st.number_input("Berapa menit workout?", min_value=10, max_value=180, value=30, step=10)
        cost_work = int(workout_mins * 0.5)
        if "👟 Running Shoes of Agility" in d["equipped_items"]:
            cost_work = int(cost_work * 0.7)
        if st.button(f"🏋️ Selesaikan Workout ({workout_mins} Mnt)", use_container_width=True):
            if d["stamina"] >= cost_work:
                d["stamina"] -= cost_work
                d["gold"] += int(workout_mins * 0.6)
                add_exp(int(workout_mins * 2.5), "STR", max(1, int(workout_mins / 20)))
                log_activity("Workout (Menit)", workout_mins)
                st.success("Workout Selesai!")
                st.rerun()

    with st.expander("📜 3. Gunakan Instant Scroll Item"):
        if "📜 Scroll of Instant Focus" in d["inventory"]:
            if st.button("⚡ Gunakan Scroll Instant Focus", use_container_width=True):
                d["inventory"].remove("📜 Scroll of Instant Focus")
                add_exp(150, "INT", 2)
                st.success("Quest diselesaikan instant tanpa menguras stamina!")
                st.rerun()
        else:
            st.caption("Kamu tidak memiliki Scroll of Instant Focus. Beli di Toko Shop!")

# ================= TAB 2: BOSS =================
with tab_boss:
    st.subheader(f"⚔️ Dungeon RAID: {d['boss_name']}")
    st.progress(max(0.0, min(d["boss_hp"] / d["boss_max_hp"], 1.0)), text=f"HP Boss: {d['boss_hp']} / {d['boss_max_hp']}")

    base_damage = d["stats"]["STR"] * 2 + d["stats"]["INT"] * 2
    if "🗡️ Steel Sword of Focus" in d["equipped_items"]:
        base_damage = int(base_damage * 1.15)
    if d["active_pet"] == "🐺 Spirit Wolf":
        base_damage += 25

    st.info(f"💥 Total Damage Serangan Nauval: **{base_damage} HP**")

    if st.button(f"⚔️ Serang {d['boss_name']} (-20 Stamina)", use_container_width=True):
        if d["stamina"] >= 20:
            play_sfx("attack")
            d["stamina"] -= 20
            d["boss_hp"] -= base_damage
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

# ================= TAB 3: PENALTY =================
with tab_penalty:
    st.subheader("🚨 Fitur Hukuman Pelanggaran")
    sosmed_mins = st.number_input("Berapa menit buang waktu / sosmed?", min_value=15, max_value=300, value=30, step=15)
    if st.button(f"⚠️ Laporkan Sosmed ({sosmed_mins} Mnt)", use_container_width=True):
        apply_penalty(int(sosmed_mins * 0.8), int(sosmed_mins * 2))
        st.rerun()

# ================= TAB 4: SHOP =================
with tab_shop:
    st.subheader("🧪 Toko Potion & Items")
    potions = [
        {"name": "☕ Espresso Shot", "cost": 45, "type": "instant_stamina", "val": 30, "desc": "+30 Stamina Instan"},
        {"name": "⚡ Vitality Potion", "cost": 60, "type": "instant_stamina", "val": 50, "desc": "+50 Stamina Instan"},
        {"name": "📜 Scroll of Instant Focus", "cost": 100, "type": "item", "desc": "Selesaikan 1 quest instant tanpa stamina."},
        {"name": "🛡️ Potion Kebal Penundaan", "cost": 180, "type": "item", "desc": "Tolak 1x hukuman sosmed otomatis."},
        {"name": "🍀 Clover of Luck", "cost": 200, "type": "buff", "duration": 24, "desc": "+25% Hoki Gacha Harian"},
        {"name": "🧪 Double EXP Elixir", "cost": 150, "type": "buff", "duration": 2, "desc": "2x EXP selama 2 Jam"},
    ]
    for p in potions:
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"**{p['name']}** — 🪙 **{p['cost']} Gold**\n\n*{p['desc']}*")
        if c2.button("Beli", key="shop_"+p["name"]):
            if d["gold"] >= p["cost"]:
                d["gold"] -= p["cost"]
                if p["type"] == "instant_stamina":
                    d["stamina"] = min(d["max_stamina"], d["stamina"] + p["val"])
                elif p["type"] == "item":
                    d["inventory"].append(p["name"])
                elif p["type"] == "buff":
                    d["active_buffs"].append({"name": p["name"], "expires": f"{p['duration']} Jam"})
                save_game()
                st.success(f"Berhasil membeli {p['name']}!")
                st.rerun()

# ================= TAB 5: ARMORY =================
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

# ================= TAB 6: GACHA =================
with tab_gacha:
    st.subheader("🎡 Daily Spin Wheel")
    today_str = str(date.today())
    if d["last_gacha_date"] == today_str:
        st.info("⏰ Sudah Spin hari ini. Kembali besok!")
    else:
        if st.button("🎰 Putar Spin Harian", use_container_width=True):
            d["last_gacha_date"] = today_str
            rewards = [("🪙 Bonus +100 Gold", "gold", 100), ("✨ Bonus +150 EXP", "exp", 150)]
            if any(b["name"] == "🍀 Clover of Luck" for b in d["active_buffs"]):
                rewards.append(("💎 Jackpot Super (+300 Gold)", "gold", 300))
            chosen = random.choice(rewards)
            if chosen[1] == "gold": d["gold"] += chosen[2]
            elif chosen[1] == "exp": add_exp(chosen[2])
            save_game()
            st.rerun()

# ================= TAB 7: PET =================
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

# ================= TAB 8: ACHIEVEMENTS =================
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

# ================= TAB 9: ANALYTICS =================
with tab_analytics:
    st.subheader("📈 Analytics Kedisiplinan")
    if d["activity_log"]:
        df = pd.DataFrame(d["activity_log"])
        st.bar_chart(df, x="date", y="value", color="activity")
    else:
        st.info("Belum ada data aktivitas.")
