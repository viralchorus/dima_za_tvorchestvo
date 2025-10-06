# app.py — Дима За Творчество (исправленная v)
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# -----------------------------
# Настройки
# -----------------------------
st.set_page_config(page_title="Дима За Творчество", page_icon="🎨", layout="centered")
CSV_FILE = "dima_za_tvorchestvo.csv"
EXPECTED_COLS = ["Категория", "Название", "Исполнитель", "Баллы", "Рецензия", "Оценщик", "Дата"]

# -----------------------------
# Вспомогательные функции
# -----------------------------
def ensure_columns(df, cols):
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    # вернуть df с нужным порядком колонок
    return df[[c for c in cols if c in df.columns]]

def flomaster_score(R, S, T, H, V):
    """Вычисление оценки по системе Фломастера (округлённое целое)."""
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return int(round(B_prime * M))

# -----------------------------
# Загрузка CSV (устойчиво к старым/пустым файлам)
# -----------------------------
if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
    try:
        df_all = pd.read_csv(CSV_FILE)
    except Exception:
        df_all = pd.DataFrame(columns=EXPECTED_COLS)
else:
    df_all = pd.DataFrame(columns=EXPECTED_COLS)

# добавим недостающие столбцы и приведём порядок
df_all = ensure_columns(df_all, EXPECTED_COLS)

# -----------------------------
# Заголовок
# -----------------------------
st.title("🎨 Дима За Творчество")
st.write("Оценивай треки, альбомы и исполнителей по системе — объективно и с вайбом. (Квас Чарт — это топ треков.)")

# -----------------------------
# Выбор категории и поля ввода
# -----------------------------
category = st.radio("Что оцениваем?", ["Исполнитель", "Трек", "Альбом"], horizontal=True)
# падежи/названия
forms = {
    "Исполнитель": {"who": "исполнителя", "title": "Исполнители"},
    "Трек": {"who": "трека", "title": "Треки"},
    "Альбом": {"who": "альбома", "title": "Альбомы"},
}[category]

# артист (только для Трек/Альбом)
artist = ""
if category in ["Трек", "Альбом"]:
    artist = st.text_input("Введите псевдоним исполнителя:")

# название (трек/альбом/исполнитель)
name = st.text_input(f"Введите название {forms['who']}:")

# -----------------------------
# Слайдеры (оценки)
# -----------------------------
R = st.slider("🎭 Рифмы / Образы", 1, 10, 5)
S = st.slider("🎵 Структура / Ритмика", 1, 10, 5)
T = st.slider("🔥 Реализация стиля", 1, 10, 5)
H = st.slider("💫 Индивидуальность / Харизма", 1, 10, 5)

st.markdown("### 🌌 Атмосфера / Вайб")
st.markdown(
    """
    <div style='padding:8px; border:2px solid #6C63FF; border-radius:10px; background-color:#F3F0FF; color:#000;'>
        <b>Чем сильнее вайб — тем вкуснее квас. Этот критерий влияет на множитель общей оценки.</b>
    </div>
    """,
    unsafe_allow_html=True,
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5)

# -----------------------------
# Никнейм оценщика и рецензия
# -----------------------------
st.markdown("### 🧠 Оценщик и рецензия")
reviewer = st.text_input("Введите свой никнейм (по желанию):")
review_text = st.text_area("✍️ Твоя рецензия (необязательно):", "")

# -----------------------------
# Кнопка сохранения оценки
# -----------------------------
if st.button("И чё у нас в итоге?"):
    # валидация
    if not name.strip():
        st.warning("⚠️ Введи название для оценки.")
    elif category in ["Трек", "Альбом"] and not artist.strip():
        st.warning("⚠️ Укажи исполнителя для трека/альбома.")
    else:
        score = flomaster_score(R, S, T, H, V)
        reviewer_final = reviewer.strip() if reviewer.strip() else "Серая мышь (Не зареган)"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row = {
            "Категория": category,
        "Название": name.strip(),
            "Исполнитель": artist.strip() if category in ["Трек", "Альбом"] else "",
            "Баллы": score,
            "Рецензия": review_text.strip(),
            "Оценщик": reviewer_final,
            "Дата": now
        }
        # добавляем запись и сохраняем CSV (utf-8-sig для Excel)
        df_all = pd.concat([df_all, pd.DataFrame([new_row])], ignore_index=True)
        df_all = ensure_columns(df_all, EXPECTED_COLS)  # на всякий случай
        df_all.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        st.success(f"✅ Оценка добавлена: {score} / 90")
        st.balloons()

# -----------------------------
# Отображение Квас Чарта (топ по выбранной категории)
# -----------------------------
st.markdown("---")
st.subheader(f"🏆 Квас Чарт: {forms['title']}")

# отфильтруем и отсортируем
category_df = df_all[df_all["Категория"] == category].copy()
if not category_df.empty:
    category_df["Баллы"] = pd.to_numeric(category_df["Баллы"], errors="coerce").fillna(0).astype(int)
    sorted_df = category_df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    sorted_df.index += 1
    for idx, row in sorted_df.iterrows():
        artist_part = f" — {row['Исполнитель']}" if str(row.get("Исполнитель", "")).strip() else ""
        st.markdown(f"{idx}. {row['Название']}{artist_part} — 🎯 {int(row['Баллы'])} / 90")
        if str(row.get("Рецензия", "")).strip():
            with st.expander(f"Показать рецензию ({row.get('Оценщик','')})"):
                st.write(row["Рецензия"])
                st.caption(f"Дата: {row.get('Дата','')}")
        else:
            st.caption(f"Оценил: {row.get('Оценщик','')}")
else:
    st.info(f"👀 Пока нет оценок для категории {forms['title'].lower()}.")

# -----------------------------
# Невидимая/невзрачная админ-панель (внизу)
# -----------------------------
st.markdown("---")
admin_code = st.text_input("🔐 Код администратора:", type="password", help="Введите код, если вы админ.")

if admin_code == "characterai":
    # невзрачный контейнер
    st.markdown(
        """
        <div style='background:#f7f7f7; border:1px solid #e6e6e6; border-radius:8px; padding:10px;'>
        <small style='color:#666;'>🧩 Админ-панель (тонкая и незаметная). Удаление записи приведёт к её немедленному удалению из CSV.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not df_all.empty:
        # используем reset_index чтобы сохранить оригинальные индексы для удаления
        df_with_index = df_all.reset_index()
        for _, r in df_with_index.iterrows():
            orig_idx = int(r["index"])
            with st.expander(f"{r['Категория']}: {r['Название']} — {r['Баллы']} / 90"):
                st.write(f"Исполнитель: {r['Исполнитель']}")
                st.write(f"Рецензия: {r['Рецензия'] or '_(пусто)_'}")
                st.write(f"Оценщик: {r['Оценщик']}")
                st.write(f"Дата: {r.get('Дата','')}")
                if st.button(f"🗑 Удалить запись #{orig_idx+1}", key=f"del_{orig_idx}"):
                    # удаляем по оригинальному индексу и сохраняем — без вызова rerun
                    df_all = df_all.drop(index=orig_idx).reset_index(drop=True)
                    df_all = ensure_columns(df_all, EXPECTED_COLS)
                    df_all.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
                    st.success("✅ Запись удалена. Страница будет обновлена автоматически.")
                    # при нажатии кнопки Streamlit сам перезапустит скрипт, изменений будет видно
    else:
        st.info("Нет данных для управления.")
        
# -----------------------------
# Нижняя подпись (по центру)
# -----------------------------
st.markdown(
    """
    <div style='text-align:center; margin-top:40px; color:#999999; font-size:13px;'>
        # мыши всегда ниже
    </div>
    """,
    unsafe_allow_html=True,
)
