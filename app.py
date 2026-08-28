import streamlit as st
import json
import os
from datetime import date

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
    "journal": []
}

# Inisialisasi Data Karakter & Auto-Fix Struktur Data Lama
if "data" not in st.session_state:
    if os.path.exists("save_data.json"):
        try:
            with open("save_data.json", "r") as f:
                loaded_data = json.load(f)
                # Auto-repair jika ada key baru yang belum ada di save_data lama
                for key, val in default_data.items():
                    if key not in loaded_data:
                        loaded_data[key] = val
                st.session_state.data = loaded_data
        except:
            st.session_state.data = default_data
    else:
        st.session_state.data = default_data

d = st.session_state.data

def save_game():
    with open("save_data.json", "w") as f:
        json.dump(d, f)

def update_title():
    if d["level"] >= 30: d["title"] = "👑 THE PERFECT HUMAN EMPEROR"
    elif d["level"] >= 20: d["title"] = "⚔️ Supreme Shadow Knight"
    elif d["level"] >= 10: d["title"] = "🛡️ Guardian of Discipline"
    elif d["level"] >= 5: d["title"] = "📜 Elite Initiate"
    else: d["title"] = "🌱 Novice Initiate"

def add_exp(amount, stat_type=None, stat_gain=1):
    d["exp"] += amount
    d["quests_done_today"] += 1
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
        st.balloons()
        st.success(f"🎉 LEVEL UP! Selamat Tuanku Nauval naik ke Level {d['level']}! (+50 Gold, Stat Boost)")
    save_game()

def apply_penalty(hp_loss, exp_loss):
    d["hp"] = max(0, d["hp"] - hp_loss)
    d["exp"] = max(0, d["exp"] - exp_loss)
    save_game()
    st.error(f"⚠️ Hukuman Diterima: -{hp_loss} HP | -{exp_loss} EXP")

# --- HEADER STATUS KARAKTER ---
st.title(f"🏰 KETUA {d['name'].upper()}")
st.caption(f"Gelar Kedisiplinan: **{d['title']}**")

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

# Detail Stats Atribut RPG
with st.expander("📊 Lihat Atribut & Kekuatan Karakter (STR, INT, AGI, VIT)", expanded=True):
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("🏋️ STR (Fisik)", d["stats"]["STR"])
    s2.metric("📚 INT (Otak)", d["stats"]["INT"])
    s3.metric("⚡ AGI (Gesit)", d["stats"]["AGI"])
    s4.metric("🛡️ VIT (Daya Tahan)", d["stats"]["VIT"])

st.divider()

# --- TAB UTAMA APLIKASI ---
tab_quest, tab_penalty, tab_shop, tab_journal = st.tabs([
    "⚔️ Quest & Rutinitas", 
    "🚨 Hukuman (Penalty)", 
    "🛒 Toko Hadiah", 
    "📓 Jurnal & Catatan"
])

# ================= TAB 1: QUEST DENGAN CUSTOM DURASI =================
with tab_quest:
    st.subheader("📌 Misi Kedisiplinan Harian")
    
    # Kategori 1: Belajar & Karir (Custom Jam)
    with st.expander("📚 1. Sesi Belajar & Skill (Input Durasi Jam)", expanded=True):
        study_hours = st.number_input("Berapa jam Tuanku belajar/fokus hari ini?", min_value=0.5, max_value=12.0, value=1.0, step=0.5, key="study_h")
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
                st.success(f"Luar biasa! Belajar {study_hours} Jam selesai.")
                st.rerun()
            else:
                st.warning("Stamina Tuanku tidak cukup! Harap istirahat atau tidur.")

    # Kategori 2: Olahraga & Workout (Custom Menit)
    with st.expander("🏋️ 2. Olahraga & Latihan Fisik (Input Menit)"):
        workout_mins = st.number_input("Berapa menit Tuanku berolahraga/gym/pushup?", min_value=10, max_value=180, value=30, step=10, key="work_m")
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
                st.success(f"Fisik semakin kuat! Workout {workout_mins} Mnt selesai.")
                st.rerun()
            else:
                st.warning("Stamina Tuanku tidak cukup!")

    # Kategori 3: Membaca Buku Edukasi (Custom Menit)
    with st.expander("📖 3. Membaca Buku & Literasi (Input Menit)"):
        read_mins = st.number_input("Berapa menit Tuanku membaca buku hari ini?", min_value=10, max_value=180, value=20, step=5, key="read_m")
        gained_exp_read = int(read_mins * 2)
        gained_int_read = max(1, int(read_mins / 20))

        st.caption(f"🎁 Hadiah: +{gained_exp_read} EXP | +{gained_int_read} INT")

        if st.button(f"📖 Selesaikan Membaca ({read_mins} Menit)", use_container_width=True):
            add_exp(gained_exp_read, "INT", gained_int_read)
            st.success(f"Wawasan bertambah! Membaca {read_mins} Mnt selesai.")
            st.rerun()

    # Kategori 4: Rutinitas Ibadah & Kebersihan
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

        if st.button("🧹 Merapikan Kamar & Meja Kerja (+50 EXP, +10 Gold, +1 AGI)", use_container_width=True):
            d["gold"] += 10
            add_exp(50, "AGI", 1)
            st.rerun()

        if st.button("😴 Tidur & Istirahat Berkualitas (Pulihkan HP & Stamina)", use_container_width=True):
            d["stamina"] = d["max_stamina"]
            d["hp"] = d["max_hp"]
            save_game()
            st.success("HP dan Stamina Tuanku telah pulih sepenuhnya!")
            st.rerun()

# ================= TAB 2: PENALTY DENGAN CUSTOM WAKTU =================
with tab_penalty:
    st.subheader("🚨 Fitur Hukuman Pelanggaran Kedisiplinan")
    st.caption("Hitung berapa lama Tuanku terdistraksi/scrolling sosmed agar hukuman adil!")

    sosmed_mins = st.number_input("Berapa menit Tuanku scrol sosmed / buang waktu?", min_value=15, max_value=300, value=30, step=15, key="sos_m")
    lost_hp_sosmed = int(sosmed_mins * 0.8)
    lost_exp_sosmed = int(sosmed_mins * 2)

    if st.button(f"⚠️ Laporkan Scrol Sosmed ({sosmed_mins} Mnt) -> -{lost_hp_sosmed} HP | -{lost_exp_sosmed} EXP", use_container_width=True):
        apply_penalty(lost_hp_sosmed, lost_exp_sosmed)
        st.rerun()

    st.divider()

    if st.button("⚠️ Begadang Tanpa Alasan Jelas (-25 HP, -50 EXP)", use_container_width=True):
        apply_penalty(25, 50)
        st.rerun()

    if st.button("⚠️ Meninggalkan Solat / Tugas Utama (-40 HP, -100 EXP)", use_container_width=True):
        apply_penalty(40, 100)
        st.rerun()

# ================= TAB 3: TOKO HADIAH REAL-LIFE =================
with tab_shop:
    st.subheader("🛒 Toko Hadiah Real-Life (Tukar Gold)")
    st.caption("Gunakan Gold hasil kerja keras Tuanku untuk membeli reward nyata!")

    items = [
        {"name": "☕ Beli Kopi / Minuman Favorit", "cost": 100},
        {"name": "🎮 Main Game / Santai 1 Jam", "cost": 150},
        {"name": "🎬 Nonton Film / Episode Serial", "cost": 200},
        {"name": "🍕 Cheat Meal / Snacks Bebas", "cost": 300},
        {"name": "🛍️ Beli Barang Idaman (Self Reward)", "cost": 1000},
    ]

    for item in items:
        col_item, col_buy = st.columns([3, 1])
        col_item.write(f"**{item['name']}** — 🪙 {item['cost']} Gold")
        if col_buy.button("Beli", key=item["name"]):
            if d["gold"] >= item["cost"]:
                d["gold"] -= item["cost"]
                d["inventory"].append(item["name"])
                save_game()
                st.success(f"Berhasil membeli '{item['name']}'!")
                st.rerun()
            else:
                st.error("Gold Tuanku tidak cukup!")

    if d["inventory"]:
        st.divider()
        st.write("🎒 **Tas Hadiah Tuanku (Belum Ditebus):**")
        for inv in d["inventory"]:
            st.write(f"- {inv}")

# ================= TAB 4: JURNAL & CATATAN =================
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
    st.write("📜 **Riwayat Jurnal Tuanku:**")
    for j in reversed(d["journal"][-5:]):
        st.info(f"📅 **{j['date']}**\n\n{j['note']}")
