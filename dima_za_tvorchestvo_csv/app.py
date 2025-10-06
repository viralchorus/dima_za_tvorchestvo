import streamlit as st
import pandas as pd
import os

CSV_FILE = "kvas_chart.csv"

# -----------------------------
# Функция вычисления оценки
# -----------------------------
def flomaster_score(R, S, T, H, V):
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return round(B_prime * M)

# -----------------------------
# Инициализация CSV
# -----------------------------
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Категория", "Исполнитель", "Название", "Баллы", "Рецензия"]).to_csv(CSV_FILE, index=False)

try:
    df = pd.read_csv(CSV_FILE)
except pd.errors.EmptyDataError:
    df = pd.DataFrame(columns=["Категория", "Исполнитель", "Название", "Баллы", "Рецензия"])

# -----------------------------
# Справочник падежей
# -----------------------------
category_forms = {
    "Исполнитель": {"who": "исполнителя", "title": "Исполнители"},
    "Трек": {"who": "трека", "title": "Треки"},
    "Альбом": {"who": "альбома", "title": "Альбомы"},
}

# -----------------------------
# Интерфейс
# -----------------------------
st.title("🎨 Дима За Творчество")
st.write("Оцени музло как Дмитрий Кузнецов. (Только не намочи писюн!)")

category = st.radio("Что в ротации krap’n’kvas сегодня?", ["Исполнитель", "Трек", "Альбом"], horizontal=True)
forms = category_forms[category]

# Для треков и альбомов добавляем поле "Исполнитель"
artist = ""
if category in ["Трек", "Альбом"]:
    artist = st.text_input("Введите псевдоним исполнителя:")

name = st.text_input(f"Введите название {forms['who']}:")

R = st.slider("🎭 Рифмы / Образы", 1, 10, 5)
S = st.slider("🎵 Структура / Ритмика", 1, 10, 5)
T = st.slider("🔥 Реализация стиля", 1, 10, 5)
H = st.slider("💫 Индивидуальность / Харизма", 1, 10, 5)

st.markdown("### 🌌 Атмосфера / Вайб")
st.markdown(
    "<div style='padding:8px; border:2px solid #6C63FF; border-radius:10px; background-color:#F3F0FF; color:#000;'>"
    "<b>Чем сильнее вайб — тем вкуснее квас. Этот критерий влияет на множитель общей оценки, бро!</b>"
    "</div>",
    unsafe_allow_html=True
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5)

review = st.text_area("📝 Рецензия (необязательно):", placeholder="Напиши пару слов о вайбе, рифмах, структуре...")

if st.button("И чё у нас в итоге?"):
    if name.strip() == "" or (category in ["Трек", "Альбом"] and artist.strip() == ""):
        st.warning("⚠️ Введи все необходимые данные перед оценкой!")
    else:
        score = flomaster_score(R, S, T, H, V)
        display_name = f"{artist} — {name}" if artist else name
        st.success(f"Итоговая оценка для {forms['who']} {display_name}: {score} / 90 🎯")
        st.balloons()

        new_row = pd.DataFrame([{
            "Категория": category,
            "Исполнитель": artist if artist else "",
            "Название": name,
            "Баллы": score,
            "Рецензия": review.strip() if review else ""
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

# -----------------------------
# Таблица (Квас Чарт)
# -----------------------------
filtered = df[df["Категория"] == category]
if not filtered.empty:
    st.subheader(f"🏆 Квас Чарт: {forms['title']}")
    filtered = filtered.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    filtered.index += 1

    for i, row in filtered.iterrows():
        artist_part = f" — {row['Исполнитель']}" if row['Исполнитель'] else ""
        st.markdown(f"**{i}. {row['Название']}{artist_part}** — {row['Баллы']} / 90")
        if row["Рецензия"] and str(row["Рецензия"]).strip():
            with st.expander("Показать рецензию"):
                st.write(row["Рецензия"])
else:
    st.info(f"👀 Пока нет ни одной оценки для категории {forms['title'].lower()}.")

# -----------------------------
# Сброс рейтинга
# -----------------------------
if st.button(f"Сбросить рейтинг ({forms['title'].lower()})"):
    df = df[df["Категория"] != category]
    df.to_csv(CSV_FILE, index=False)
    st.success(f"Рейтинг для категории {forms['title']} сброшен.")

