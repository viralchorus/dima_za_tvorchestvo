import streamlit as st
import pandas as pd
from datetime import datetime
import os

def flomaster_score(R, S, T, H, V):
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return round(B_prime * M)

CSV_FILE = "kvas_chart.csv"
if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Категория", "Название", "Баллы", "Дата"])
    df_init.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

def load_data():
    return pd.read_csv(CSV_FILE)

def save_data(df):
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

category_forms = {
    "Исполнитель": {"who": "исполнителя", "title": "Исполнители"},
    "Трек": {"who": "трека", "title": "Треки"},
    "Альбом": {"who": "альбома", "title": "Альбомы"},
}

st.title("🎨 Дима За Творчество")
st.write("Оцени музло как Дмитрий Кузнецов. (Только не намочи писюн!)")

category = st.radio(
    "Что в ротации krap'n'kvas сегодня?",
    ["Исполнитель", "Трек", "Альбом"],
    horizontal=True
)
forms = category_forms[category]

name = st.text_input(f"Введите название {forms['who']}:")

R = st.slider("🎭 Рифмы / Образы", 1, 10, 5)
S = st.slider("🎵 Структура / Ритмика", 1, 10, 5)
T = st.slider("🔥 Реализация стиля", 1, 10, 5)
H = st.slider("💫 Индивидуальность / Харизма", 1, 10, 5)

st.markdown("### 🌌 Атмосфера / Вайб")
st.markdown(
    "<div style='padding:8px; border:2px solid #6C63FF; border-radius:10px; background-color:#F3F0FF; color:#000000;'>"
    "<b>Чем сильнее вайб — тем вкуснее квас. Этот критерий влияет на множитель общей оценки, бро!</b>"
    "</div>",
    unsafe_allow_html=True
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5, key="vibe_slider")

if st.button("И чё у нас в итоге?"):
    if name.strip() == "":
        st.warning("⚠️ Ты чё Чупа? Введи название перед оценкой, не будь мышью!")
    else:
        score = flomaster_score(R, S, T, H, V)
        st.success(f"Итоговая оценка для {forms['who']} {name}: {score} / 90 🎯")
        st.balloons()

        df = load_data()
        new_entry = pd.DataFrame([{
            "Категория": category,
            "Название": name.strip(),
            "Баллы": int(score),
            "Дата": datetime.now().strftime("%d.%m.%Y")
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        save_data(df)

df = load_data()
filtered_df = df[df["Категория"] == category]

if not filtered_df.empty:
    st.subheader(f"🏆 Квас Чарт: {forms['title']}")
    chart = filtered_df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    chart.index += 1
    st.dataframe(chart, use_container_width=True)
else:
    st.info(f"👀 Пока нет ни одной оценки для категории: {forms['title'].lower()}.")

if st.button(f"Сбросить Квас Чарт ({forms['title'].lower()})"):
    df = load_data()
    df = df[df["Категория"] != category]
    save_data(df)
    st.success(f"Квас Чарт для категории {forms['title']} очищен.")
