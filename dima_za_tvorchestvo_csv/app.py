import streamlit as st
import pandas as pd
import os

# -----------------------------
# Настройки
# -----------------------------
CSV_FILE = "ratings.csv"

# -----------------------------
# Функция вычисления оценки
# -----------------------------
def flomaster_score(R, S, T, H, V):
    """Вычисление оценки по системе Фломастера"""
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return round(B_prime * M)  # округляем до целого


# -----------------------------
# Создание CSV, если нет
# -----------------------------
if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    df = pd.DataFrame(columns=["Категория", "Название", "Исполнитель", "Баллы", "Рецензия", "Оценщик"])
    df.to_csv(CSV_FILE, index=False)

# -----------------------------
# Загрузка CSV
# -----------------------------
try:
    df = pd.read_csv(CSV_FILE)
except pd.errors.EmptyDataError:
    df = pd.DataFrame(columns=["Категория", "Название", "Исполнитель", "Баллы", "Рецензия", "Оценщик"])

# -----------------------------
# Справочники падежей
# -----------------------------
category_forms = {
    "Исполнитель": {"who": "исполнителя", "title": "Исполнители"},
    "Трек": {"who": "трека", "title": "Треки"},
    "Альбом": {"who": "альбома", "title": "Альбомы"},
}

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
    horizontal=True,
)

forms = category_forms[category]

# -----------------------------
# Поля ввода
# -----------------------------
name = st.text_input(f"Введите название {forms['who']}:")
artist = ""

if category in ["Трек", "Альбом"]:
    artist = st.text_input("Введите псевдоним исполнителя:")

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
    unsafe_allow_html=True,
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5)

# Поле никнейма оценщика
reviewer = st.text_input("Введите свой никнейм:")

# Поле для рецензии
review_text = st.text_area("✍️ Напиши рецензию (по желанию):")

# -----------------------------
# Кнопка расчёта
# -----------------------------
if st.button("И чё у нас в итоге?"):
    if name.strip() == "":
        st.warning("⚠️ Ты чё Чупа? Введи название перед оценкой, не будь мышью!")
    else:
        score = flomaster_score(R, S, T, H, V)
        st.success(f"Итоговая оценка для {forms['who']} {name}: {score} / 90 🎯")
        st.balloons()

        new_row = {
            "Категория": category,
            "Название": name,
            "Исполнитель": artist,
            "Баллы": score,
            "Рецензия": review_text,
            "Оценщик": reviewer if reviewer.strip() else "Серая мышь (Не зареган)"
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

# -----------------------------
# Отображение рейтинга
# -----------------------------
filtered_df = df[df["Категория"] == category].copy()

if not filtered_df.empty:
    st.subheader(f"🏆 Квас Чарт: {forms['title']}")
    filtered_df = filtered_df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    filtered_df.index += 1
    for i, row in filtered_df.iterrows():
        artist_part = f" — {row['Исполнитель']}" if isinstance(row["Исполнитель"], str) and row["Исполнитель"].strip() else ""
        st.markdown(f"{i}. {row['Название']}{artist_part} — {row['Баллы']} / 90")
        if isinstance(row["Рецензия"], str) and row["Рецензия"].strip():
            with st.expander("🗒 Читать рецензию"):
                st.write(row["Рецензия"])
                st.caption(f"Оценил: {row['Оценщик']}")
        else:
            st.caption(f"Оценил: {row['Оценщик']}")

else:
    st.info(f"👀 Пока нет ни одной оценки для категории {forms['title'].lower()}.")

# -----------------------------
# Админ-панель (скрытая)
# -----------------------------
st.markdown("---")
admin_code = st.text_input("🔐 Код администратора:", type="password")

if admin_code == "characterai":
    st.subheader("🧩 Админ-панель")
    st.write("Вы можете удалять отдельные рецензии.")

    if not df.empty:
        for i, row in df.iterrows():
            with st.expander(f"{row['Категория']}: {row['Название']} — {row['Баллы']} / 90"):
                st.write(f"Исполнитель: {row['Исполнитель']}")
                st.write(f"Рецензия: {row['Рецензия']}")
                st.write(f"Оценщик: {row['Оценщик']}")
                if st.button(f"🗑 Удалить запись #{i+1}", key=f"delete_{i}"):
                    df = df.drop(index=i)
                    df.to_csv(CSV_FILE, index=False)
                    st.success("✅ Рецензия удалена!")
                    st.experimental_rerun()
    else:
        st.info("Нет данных для отображения.")

# -----------------------------
# Нижняя подпись
# -----------------------------
st.markdown(
    "<div style='text-align:center; margin-top:60px; color:#999;'># мыши всегда ниже</div>",
    unsafe_allow_html=True,
)
