import streamlit as st
import pandas as pd
import os

# -----------------------------
# Настройки
# -----------------------------
st.set_page_config(page_title="Дима За Творчество", page_icon="🎨", layout="centered")
CSV_FILE = "ratings.csv"

# -----------------------------
# Функция вычисления оценки
# -----------------------------
def flomaster_score(R, S, T, H, V):
    """Вычисление оценки по системе Фломастера"""
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return round(B_prime * M)

# -----------------------------
# Справочники для падежей
# -----------------------------
category_forms = {
    "Исполнитель": {"who": "исполнителя", "title": "Исполнители"},
    "Трек": {"who": "трека", "title": "Треки"},
    "Альбом": {"who": "альбома", "title": "Альбомы"},
}

# -----------------------------
# Загрузка и инициализация CSV
# -----------------------------
if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
    try:
        df_all = pd.read_csv(CSV_FILE)
    except pd.errors.EmptyDataError:
        df_all = pd.DataFrame(columns=["Категория", "Название", "Исполнитель", "Баллы", "Рецензия", "Оценщик"])
else:
    df_all = pd.DataFrame(columns=["Категория", "Название", "Исполнитель", "Баллы", "Рецензия", "Оценщик"])

# -----------------------------
# Заголовок
# -----------------------------
st.title("🎨 Дима За Творчество")
st.write("Оцени музло как Дмитрий Кузнецов. (Только не намочи писюн!)")

# -----------------------------
# Выбор категории
# -----------------------------
category = st.radio(
    "Что в ротации krap'n'kvas сегодня?",
    ["Исполнитель", "Трек", "Альбом"],
    horizontal=True
)
forms = category_forms[category]

# -----------------------------
# Поля для ввода объекта оценки
# -----------------------------
name = st.text_input(f"Введите название {forms['who']}:")
artist = ""
if category in ["Трек", "Альбом"]:
    artist = st.text_input("Введите псевдоним исполнителя:")

# -----------------------------
# Слайдеры
# -----------------------------
R = st.slider("🎭 Рифмы / Образы", 1, 10, 5)
S = st.slider("🎵 Структура / Ритмика", 1, 10, 5)
T = st.slider("🔥 Реализация стиля", 1, 10, 5)
H = st.slider("💫 Индивидуальность / Харизма", 1, 10, 5)

st.markdown("### 🌌 Атмосфера / Вайб")
st.markdown(
    """
    <div style='padding:8px; border:2px solid #6C63FF; border-radius:10px; background-color:#F3F0FF; color:#000000;'>
        <b>Чем сильнее вайб — тем вкуснее квас. Этот критерий влияет на множитель общей оценки, бро!</b>
    </div>
    """,
    unsafe_allow_html=True
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5)

# -----------------------------
# Никнейм и рецензия
# -----------------------------
st.markdown("### 🧠 Оценщик и рецензия")
username = st.text_input("Введите свой никнейм (чтобы знали, кто оценил):")
review = st.text_area("📝 Напиши рецензию (необязательно):", "")

# -----------------------------
# Кнопка "И чё у нас в итоге?"
# -----------------------------
if st.button("И чё у нас в итоге?"):
    if name.strip() == "":
        st.warning("⚠️ Ты чё, Чупа? Название введи, не будь мышью!")
    else:
        score = flomaster_score(R, S, T, H, V)
        reviewer = username.strip() if username.strip() else "Серая мышь (Не зареган)"
        st.success(f"Итоговая оценка для {forms['who']} {name}: {score} / 90 🎯")
        st.balloons()

        new_row = pd.DataFrame([{
            "Категория": category,
            "Название": name,
            "Исполнитель": artist,
            "Баллы": int(score),
            "Рецензия": review.strip(),
            "Оценщик": reviewer,
        }])

        df_all = pd.concat([df_all, new_row], ignore_index=True)
        df_all.to_csv(CSV_FILE, index=False)

# -----------------------------
# Таблица "Квас Чарт"
# -----------------------------
category_df = df_all[df_all["Категория"] == category]

if not category_df.empty:
    st.subheader(f"🏆 Квас Чарт: {forms['title']}")
    sorted_df = category_df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    sorted_df.index += 1
    for i, row in sorted_df.iterrows():
        artist_part = ""
        if category in ["Трек", "Альбом"] and "Исполнитель" in row and pd.notna(row["Исполнитель"]) and row["Исполнитель"]:
            artist_part = f" — {row['Исполнитель']}"
        st.markdown(f"{i}. {row['Название']}{artist_part} — 🎯 {row['Баллы']} / 90")
        if row["Рецензия"]:
            with st.expander(f"Показать рецензию ({row['Оценщик']})"):
                st.write(row["Рецензия"])
else:
    st.info(f"👀 Пока нет ни одной оценки для категории: {forms['title'].lower()}.")

# -----------------------------
# Нижняя подпись
# -----------------------------
st.markdown(
    """
    <div style='text-align:center; margin-top:50px; color:#999999; font-size:13px;'>
        # мыши всегда ниже
    </div>
    """,
    unsafe_allow_html=True
)
