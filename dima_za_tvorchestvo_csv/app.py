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
    return int(round(B_prime * M))  # округляем до целого и приводим к int

# -----------------------------
# Утилиты для CSV / миграции столбцов
# -----------------------------
EXPECTED_COLS = ["Категория", "Название", "Исполнитель", "Баллы", "Рецензия", "Оценщик", "R", "S", "T", "H", "V"]

def ensure_df_columns(df):
    for c in EXPECTED_COLS:
        if c not in df.columns:
            df[c] = ""  # пустые значения для старых записей
    # привести порядок колонок (необязательно, но удобно)
    return df[EXPECTED_COLS]

# -----------------------------
# Создание CSV, если нет
# -----------------------------
if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    df = pd.DataFrame(columns=EXPECTED_COLS)
    df.to_csv(CSV_FILE, index=False)

# -----------------------------
# Загрузка CSV
# -----------------------------
try:
    df = pd.read_csv(CSV_FILE)
except Exception:
    df = pd.DataFrame(columns=EXPECTED_COLS)

df = ensure_df_columns(df)

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
# Поля ввода (пользователь)
# -----------------------------
name = st.text_input(f"Введите название {forms['who']}:")
artist = ""
if category in ["Трек", "Альбом"]:
    artist = st.text_input("Введите псевдоним исполнителя:")

# критерии — сохраняем их как отдельные поля R,S,T,H,V
R = st.slider("🎭 Рифмы / Образы", 1, 10, 5, key="slider_R")
S = st.slider("🎵 Структура / Ритмика", 1, 10, 5, key="slider_S")
T = st.slider("🔥 Реализация стиля", 1, 10, 5, key="slider_T")
H = st.slider("💫 Индивидуальность / Харизма", 1, 10, 5, key="slider_H")

st.markdown("### 🌌 Атмосфера / Вайб")
st.markdown(
    """
    <div style='padding:8px; border:2px solid #6C63FF; border-radius:10px; background-color:#F3F0FF; color:#000000;'>
        <b>Чем сильнее вайб — тем вкуснее квас. Этот критерий влияет на множитель общей оценки, бро!</b>
    </div>
    """,
    unsafe_allow_html=True,
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5, key="slider_V")

# -----------------------------
# Промежуточный (живой) результат
# -----------------------------
current_score = flomaster_score(R, S, T, H, V)
st.markdown(
    f"""
    <div style='text-align:center; margin-top:14px; margin-bottom:10px;'>
        <span style='font-size:18px; color:#6C63FF;'>
            🔮 Промежуточный результат: <b>{current_score} / 90</b>
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# Поле никнейма оценщика (над рецензией)
reviewer = st.text_input("Введите свой никнейм:")

# Поле для рецензии
review_text = st.text_area("✍️ Напиши рецензию (по желанию):")

# -----------------------------
# Кнопка расчёта / сохранения
# -----------------------------
if st.button("И чё у нас в итоге?"):
    if name.strip() == "":
        st.warning("⚠️ Ты чё Чупа? Введи название перед оценкой, не будь мышью!")
    else:
        score = flomaster_score(R, S, T, H, V)
        st.success(f"Итоговая оценка для {forms['who']} {name}: {score} / 90 🎯")
        st.balloons()
        # 🍻 Вкусняшка — только если 90 баллов (визуал)
        if score == 90:
            st.markdown("""
            <style>
            @keyframes softGlow {
              0% { text-shadow: 0 0 6px #ffd000, 0 0 12px #ffbb00; opacity: 0.6; }
              50% { text-shadow: 0 0 10px #ffe966, 0 0 20px #ffcc33; opacity: 0.9; }
              100% { text-shadow: 0 0 6px #ffd000, 0 0 12px #ffbb00; opacity: 0.6; }
            }
            @keyframes spark {
              0%, 100% { opacity: 0; transform: scale(0.8) translateY(0px); }
              50% { opacity: 0.6; transform: scale(1) translateY(-6px); }
            }
            .vkusnyashka {
              animation: softGlow 3s ease-in-out infinite;
              color: #ffcc33;
              font-weight: bold;
              font-size: 26px;
              text-align: center;
              margin-top: 20px;
              position: relative;
            }
            .spark {
              position: absolute;
              font-size: 14px;
              color: rgba(255,230,128,0.35);
              animation: spark 2.4s ease-in-out infinite;
              opacity: 0.45;
            }
            .spark:nth-child(1) { left: 30%; animation-delay: 0s; }
            .spark:nth-child(2) { left: 50%; animation-delay: 0.6s; }
            .spark:nth-child(3) { left: 70%; animation-delay: 1.2s; }
            </style>

            <div class="vkusnyashka">
                🍻 Вкусняшка от Дмитрия Кузнецова!
                <div class="spark">✦</div>
                <div class="spark">✦</div>
                <div class="spark">✦</div>
            </div>
            <p style="text-align:center; color:#777; font-weight:bold;">ООО НИХУЯ!!</p>
            """, unsafe_allow_html=True)

        # 🧾 Формируем запись — сохраняем также отдельные критерии
        new_row = {
            "Категория": category,
            "Название": name.strip(),
            "Исполнитель": artist.strip() if isinstance(artist, str) else "",
            "Баллы": int(score),
            "Рецензия": review_text.strip() if isinstance(review_text, str) else "",
            "Оценщик": reviewer.strip() if reviewer.strip() else "Серая мышь (Не зареган)",
            "R": int(R),
            "S": int(S),
            "T": int(T),
            "H": int(H),
            "V": int(V)
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df = ensure_df_columns(df)
        df.to_csv(CSV_FILE, index=False)

# -----------------------------
# Отображение рейтинга (Квас Чарт)
# -----------------------------
filtered_df = df[df["Категория"] == category].copy()
if not filtered_df.empty:
    st.subheader(f"🏆 Квас Чарт: {forms['title']}")
    filtered_df["Баллы"] = pd.to_numeric(filtered_df["Баллы"], errors="coerce").fillna(0).astype(int)
    filtered_df = filtered_df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    filtered_df.index += 1

    for i, row in filtered_df.iterrows():
        artist_part = f" — {row['Исполнитель']}" if isinstance(row["Исполнитель"], str) and row["Исполнитель"].strip() else ""
        st.markdown(f"{i}. {row['Название']}{artist_part} — {int(row['Баллы'])} / 90")

        # Рецензия и внутри неё — подробности по критериям и титул Вкусняшка
        if isinstance(row["Рецензия"], str) and row["Рецензия"].strip():
            with st.expander("🗒 Читать рецензию"):
                st.write(row["Рецензия"])
                # показать критерии, если они существуют (не пустые)
                has_criteria = all(str(row.get(k, "")).strip() for k in ["R", "S", "T", "H", "V"])
                if has_criteria:
                    st.markdown("---")
                    st.markdown(
                        f"🎭 Рифмы / Образы: {int(row['R'])}/10  \n"
                        f"🎵 Структура / Ритмика: {int(row['S'])}/10  \n"
                    f"🔥 Реализация стиля: {int(row['T'])}/10  \n"
                        f"💫 Индивидуальность / Харизма: {int(row['H'])}/10  \n"
                        f"🌌 Атмосфера / Вайб: {int(row['V'])}/10"
                    )
                else:
                    st.info("🧩 Подробные оценки по критериям не указаны для этой рецензии.")

                # если 90/90 — титул внутри рецензии (полупрозрачный)
                if int(row["Баллы"]) == 90:
                    st.markdown(
                        "<div style='text-align:right; opacity:0.45; color:#ffcc33; font-weight:bold; margin-top:6px;'>🍻 Вкусняшка</div>",
                        unsafe_allow_html=True
                    )

                st.caption(f"Оценил: {row['Оценщик']}")
        else:
            st.caption(f"Оценил: {row['Оценщик']}")
else:
    st.info(f"👀 Пока нет ни одной оценки для категории {forms['title'].lower()}.")

# -----------------------------
# Админ-панель (простой режим редактирования)
# -----------------------------
st.markdown("---")
admin_code = st.text_input("🔐 Код администратора:", type="password")

if admin_code == "characterai":
    st.markdown(
        """
        <div style='
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 12px;
            margin-top: 10px;
        '>
        <h4 style='color: #555; margin-bottom: 6px;'>🧩 Админ-панель</h4>
        <p style='font-size: 13px; color: #777; margin-top:0;'>
        (Простой режим: редактирование полей и сохранение.)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not df.empty:
        # reset_index чтобы иметь стабильные индексы для редактирования
        df_admin = df.reset_index().rename(columns={"index": "orig_index"})
        for _, r in df_admin.iterrows():
            orig_idx = int(r["orig_index"])
            with st.expander(f"{r['Категория']}: {r['Название']} — {r['Баллы']} / 90"):
                # Поля редактирования
                new_cat = st.selectbox("Категория", ["Исполнитель", "Трек", "Альбом"], index=["Исполнитель","Трек","Альбом"].index(r["Категория"]), key=f"cat_{orig_idx}")
                new_name = st.text_input("Название", value=r["Название"], key=f"name_{orig_idx}")
                # Показать/скрыть поле исполнителя в зависимости от категории
                new_artist = ""
                if new_cat in ["Трек", "Альбом"]:
                    new_artist = st.text_input("Исполнитель", value=r["Исполнитель"], key=f"artist_{orig_idx}")
                else:
                    # если категория «Исполнитель» — поле пустое
                    new_artist = ""
                new_reviewer = st.text_input("Оценщик", value=r["Оценщик"], key=f"rev_{orig_idx}")
                new_review = st.text_area("Рецензия", value=r["Рецензия"], key=f"review_{orig_idx}")
                # Критерии (числовые)
                # При отсутствии значений делаем 5 по умолчанию в интерфейсе
                def val_or_default(x):
                    try:
                        return int(x)
                    except Exception:
                        return 5
                new_R = st.number_input("R (Рифмы / Образы)", min_value=1, max_value=10, value=val_or_default(r["R"]), key=f"R_{orig_idx}")
                new_S = st.number_input("S (Структура / Ритмика)", min_value=1, max_value=10, value=val_or_default(r["S"]), key=f"S_{orig_idx}")
                new_T = st.number_input("T (Реализация стиля)", min_value=1, max_value=10, value=val_or_default(r["T"]), key=f"T_{orig_idx}")
                new_H = st.number_input("H (Индивидуальность / Харизма)", min_value=1, max_value=10, value=val_or_default(r["H"]), key=f"H_{orig_idx}")
                new_V = st.number_input("V (Атмосфера / Вайб)", min_value=1, max_value=10, value=val_or_default(r["V"]), key=f"V_{orig_idx}")
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button("💾 Сохранить изменения", key=f"save_{orig_idx}"):
                        # обновляем df по оригинальному индексу
                        df.at[orig_idx, "Категория"] = new_cat
                        df.at[orig_idx, "Название"] = new_name.strip()
                        df.at[orig_idx, "Исполнитель"] = new_artist.strip() if isinstance(new_artist, str) else ""
                        # пересчитаем баллы автоматически из критериев
                        recalculated = flomaster_score(new_R, new_S, new_T, new_H, new_V)
                        df.at[orig_idx, "Баллы"] = int(recalculated)
                        df.at[orig_idx, "Рецензия"] = new_review
                        df.at[orig_idx, "Оценщик"] = new_reviewer.strip() if new_reviewer.strip() else "Серая мышь (Не зареган)"
                        df.at[orig_idx, "R"] = int(new_R)
                        df.at[orig_idx, "S"] = int(new_S)
                        df.at[orig_idx, "T"] = int(new_T)
                        df.at[orig_idx, "H"] = int(new_H)
                        df.at[orig_idx, "V"] = int(new_V)
                        df.to_csv(CSV_FILE, index=False)
                        st.success("✅ Изменения сохранены.")
                with col2:
                    if st.button("❌ Отменить изменения", key=f"cancel_{orig_idx}"):
                        st.info("Отмена — просто закрой и открой запись заново.")
   else:
        st.info("Нет данных для отображения.")

    # -----------------------------
    # 🩹 Обслуживание данных (восстановление CSV)
    # -----------------------------
    st.markdown("### 🩹 Обслуживание данных")

    if st.button("🩹 Восстановить таблицу данных"):
        import shutil
        BACKUP_FILE = "ratings_backup.csv"
        try:
            if os.path.exists(CSV_FILE):
                shutil.copy(CSV_FILE, BACKUP_FILE)
                st.success(f"✅ Резервная копия сохранена ({BACKUP_FILE})")

            df_repair = pd.read_csv(CSV_FILE)

            # добавляем недостающие колонки
            for col in ["R", "S", "T", "H", "V"]:
                if col not in df_repair.columns:
                    df_repair[col] = 5

            # приводим значения к числовым
            for col in ["R", "S", "T", "H", "V"]:
                df_repair[col] = pd.to_numeric(df_repair[col], errors="coerce").fillna(5).astype(int)

            df_repair.to_csv(CSV_FILE, index=False)
            st.success("🎨 Таблица успешно восстановлена и очищена от ошибок!")

        except Exception as e:
            st.error(f"⚠️ Ошибка при восстановлении: {e}")

# -----------------------------
# Нижняя подпись
# -----------------------------
st.markdown(
    "<div style='text-align:center; margin-top:60px; color:#999;'># мыши всегда ниже</div>",
    unsafe_allow_html=True,
)
