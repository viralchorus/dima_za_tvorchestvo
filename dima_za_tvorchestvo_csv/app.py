import streamlit as st
import pandas as pd
from datetime import datetime

CSV_FILE = "dima_za_tvorchestvo.csv"

# --------------------------------
# Загрузка данных
# --------------------------------
try:
    df = pd.read_csv(CSV_FILE)
except (FileNotFoundError, pd.errors.EmptyDataError):
    df = pd.DataFrame(columns=["Категория", "Название", "Баллы", "Рецензия", "Пользователь", "Дата"])
    df.to_csv(CSV_FILE, index=False)

# --------------------------------
# Функция вычисления оценки
# --------------------------------
def flomaster_score(R, S, T, H, V):
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return round(B_prime * M)

# --------------------------------
# UI
# --------------------------------
st.title("🎨 Дима За Творчество")
st.write("Оцени музло как Дмитрий Кузнецов. (Только не намочи писюн!)")

# Авторизация
username = st.text_input("Введите ваше имя (если не хотите — останетесь 'Серая Мышь (Не зареган)')")
if username.strip() == "":
    username = "Серая Мышь (Не зареган)"

category = st.radio("Что оцениваем?", ["Исполнитель", "Трек", "Альбом"], horizontal=True)
name = st.text_input(f"Введите название {category.lower()}:")

# Оценки
R = st.slider("🎭 Рифмы / Образы", 1, 10, 5)
S = st.slider("🎵 Структура / Ритмика", 1, 10, 5)
T = st.slider("🔥 Реализация стиля", 1, 10, 5)
H = st.slider("💫 Индивидуальность / Харизма", 1, 10, 5)

st.markdown("### 🌌 Атмосфера / Вайб")
st.markdown(
    "<div style='padding:8px; border:2px solid #6C63FF; border-radius:10px; background-color:#F3F0FF; color:#000;'>"
    "<b>Чем сильнее вайб — тем вкуснее квас. Этот критерий влияет на множитель общей оценки!</b></div>",
    unsafe_allow_html=True
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5, key="vibe_slider")

review = st.text_area("✍️ Напиши рецензию (необязательно):")

if st.button("И чё у нас в итоге?"):
    if name.strip() == "":
        st.warning("⚠️ Введи название, не будь мышью!")
    else:
        score = flomaster_score(R, S, T, H, V)
        st.success(f"Итоговая оценка для {category.lower()} '{name}': {score} / 90 🎯")
        st.balloons()

        new_row = {
            "Категория": category,
            "Название": name,
            "Баллы": int(score),
            "Рецензия": review.strip(),
            "Пользователь": username,
            "Дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

# --------------------------------
# Таблица рейтингов
# --------------------------------
st.subheader(f"🏆 Квас Чарт: {category}")
cat_df = df[df["Категория"] == category]
if not cat_df.empty:
    sorted_df = cat_df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    sorted_df.index += 1
    st.dataframe(sorted_df[["Название", "Баллы", "Пользователь", "Рецензия", "Дата"]], use_container_width=True)
else:
    st.info("👀 Пока нет ни одной оценки в этой категории.")
