import streamlit as st
import json, os

st.set_page_config(page_title="Perfect Human RPG", page_icon="🏰", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .stButton>button { background-color: #6366f1; color: white; border-radius: 12px; font-weight: bold; height: 3em; }
    </style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    if os.path.exists("save_data.json"):
        with open("save_data.json", "r") as f:
            st.session_state.data = json.load(f)
    else:
        st.session_state.data = {
            "name": "Nauval", "level": 1, "exp": 0, "exp_needed": 150,
            "gold": 100, "streak": 1, "title": "🌱 Novice Initiate",
            "hp": 100, "max_hp": 100, "stamina": 100, "max_stamina": 100, "water": 0
        }

d = st.session_state.data

def save():
    with open("save_data.json", "w") as f:
        json.dump(d, f)

def update_title():
    if d["level"] >= 15: d["title"] = "👑 THE PERFECT HUMAN EMPEROR"
    elif d["level"] >= 10: d["title"] = "⚔️ Lord of the 7 Knights"
    elif d["level"] >= 5: d["title"] = "📜 Knight of Discipline"

def add_exp(amount):
    d["exp"] += amount
    while d["exp"] >= d["exp_needed"]:
        d["exp"] -= d["exp_needed"]
        d["level"] += 1
        d["exp_needed"] = int(d["exp_needed"] * 1.35)
        d["max_hp"] += 10; d["hp"] = d["max_hp"]
        d["max_stamina"] += 10; d["stamina"] = d["max_stamina"]
        update_title()
        st.balloons()
        st.success(f"🎉 LEVEL UP! Selamat Tuanku Nauval naik ke Level {d['level']}!")
    save()

st.title(f"🏰 KETUA {d['name'].upper()}")
st.caption(f"Gelar: **{d['title']}**")

st.subheader(f"📈 Level {d['level']}")
st.progress(min(d["exp"] / d["exp_needed"], 1.0), text=f"EXP: {d['exp']} / {d['exp_needed']}")

col1, col2 = st.columns(2)
with col1:
    st.metric("🪙 Gold", f"{d['gold']} Gold")
    st.metric("❤️ HP", f"{d['hp']} / {d['max_hp']}")
with col2:
    st.metric("🔥 Streak", f"{d['streak']} Hari")
    st.metric("⚡ Stamina", f"{d['stamina']} / {d['max_stamina']}")

st.divider()
st.subheader("⚔️ Daily Quests & Actions")

if st.button("💧 Minum Air 250ml (+15 EXP)", use_container_width=True):
    d["water"] += 250
    add_exp(15)
    st.rerun()

if st.button("📚 Belajar 1 Jam (+90 EXP, +20 Gold)", use_container_width=True):
    if d["stamina"] >= 15:
        d["stamina"] -= 15
        d["gold"] += 20
        add_exp(90)
        st.rerun()
    else:
        st.warning("Stamina tidak cukup!")

if st.button("🏋️ Workout 30 Mnt (+75 EXP, +15 HP)", use_container_width=True):
    if d["stamina"] >= 24:
        d["stamina"] -= 24
        d["hp"] = min(d["max_hp"], d["hp"] + 15)
        add_exp(75)
        st.rerun()
    else:
        st.warning("Stamina tidak cukup!")

if st.button("😴 Tidur & Istirahat", use_container_width=True):
    d["stamina"] = d["max_stamina"]
    d["hp"] = d["max_hp"]
    save()
    st.success("HP & Stamina dipulihkan!")
    st.rerun()
