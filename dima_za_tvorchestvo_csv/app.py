import streamlit as st
import pandas as pd
import os

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
CSV_FILE = "dima_za_tvorchestvo.csv"

if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
    old_df = pd.read_csv(CSV_FILE)
else:
    old_df = pd.DataFrame(columns=["Категория", "Название", "Баллы", "Рецензия", "Пользователь"])

# -----------------------------
# Хранилище для сессии
# -----------------------------
if "ratings" not in st.session_state:
    st.session_state["ratings"] = old_df.copy()

# -----------------------------
# Падежи
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

category = st.radio(
    "Что сегодня в ротации krap'n'kvas?",
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

review = st.text_area("📝 Оставь рецензию (по желанию):", "")

user = st.text_input("Введите свой никнейм (или оставь пустым — будешь Серой Мышью):")
if not user.strip():
    user = "Серая Мышь (Не зареган)"

# -----------------------------
# Кнопка подсчёта
# -----------------------------
if st.button("И чё у нас в итоге?"):
    if name.strip() == "":
        st.warning("⚠️ Ты чё, Чупа? Введи название перед оценкой!")
    else:
        score = flomaster_score(R, S, T, H, V)
        st.success(f"Итоговая оценка для {forms['who']} {name}: {score} / 90 🎯")
        st.balloons()

        new_row = {
            "Категория": category,
            "Название": name,
            "Баллы": score,
            "Рецензия": review,
            "Пользователь": user
        }
        st.session_state["ratings"] = pd.concat([st.session_state["ratings"], pd.DataFrame([new_row])], ignore_index=True)
        st.session_state["ratings"].to_csv(CSV_FILE, index=False)

# -----------------------------
# Квас Чарт
# -----------------------------
df = st.session_state["ratings"]
category_df = df[df["Категория"] == category]

if not category_df.empty:
    st.subheader(f"🏆 Квас Чарт: {forms['title']}")
    sorted_df = category_df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    sorted_df.index += 1
    st.dataframe(sorted_df[["Название", "Баллы", "Пользователь"]], use_container_width=True)

    st.markdown("### ✍️ Рецензии")
    for _, row in sorted_df.iterrows():
        if isinstance(row["Рецензия"], str) and row["Рецензия"].strip():
            with st.expander(f"💬 {row['Название']} ({row['Пользователь']}) — {row['Баллы']} / 90"):
                st.write(row["Рецензия"])
else:
    st.info(f"👀 Пока нет ни одной оценки для категории: {forms['title'].lower()}.")
