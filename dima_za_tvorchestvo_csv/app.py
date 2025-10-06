import streamlit as st
import pandas as pd
import os
import shutil

# -----------------------------
# Настройки
# -----------------------------
CSV_FILE = "ratings.csv"
BACKUP_FILE = "ratings_backup.csv"

# -----------------------------
# Функция вычисления оценки
# -----------------------------
def flomaster_score(R, S, T, H, V):
    """Вычисление оценки по системе Фломастера"""
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return int(round(B_prime * M))

# -----------------------------
# Структура CSV
# -----------------------------
EXPECTED_COLS = ["Категория", "Название", "Исполнитель", "Баллы", "Рецензия", "Оценщик", "R", "S", "T", "H", "V"]

def ensure_df_columns(df):
    for c in EXPECTED_COLS:
        if c not in df.columns:
            df[c] = ""
    return df[EXPECTED_COLS]

# -----------------------------
# Инициализация CSV
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
# Поля ввода
# -----------------------------
name = st.text_input(f"Введите название {forms['who']}:")
artist = ""
if category in ["Трек", "Альбом"]:
    artist = st.text_input("Введите псевдоним исполнителя:")

# критерии
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

# -----------------------------
# Промежуточный результат
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

# -----------------------------
# Поля пользователя
# -----------------------------
reviewer = st.text_input("Введите свой никнейм:")
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
        # 🍻 Вкусняшка — визуал
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

        # сохраняем результат
        new_row = {
            "Категория": category,
            "Название": name.strip(),
            "Исполнитель": artist.strip() if isinstance(artist, str) else "",
            "Баллы": int(score),
            "Рецензия": review_text.strip(),
            "Оценщик": reviewer.strip() if reviewer.strip() else "Серая мышь (Не зареган)",
            "R": int(R), "S": int(S), "T": int(T), "H": int(H), "V": int(V)
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df = ensure_df_columns(df)
        df.to_csv(CSV_FILE, index=False)

# -----------------------------
# Квас Чарт
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

        if isinstance(row["Рецензия"], str) and row["Рецензия"].strip():
            with st.expander("🗒 Читать рецензию"):
                st.write(row["Рецензия"])
                st.markdown("---")
                try:
                    st.markdown(
                        f"🎭 Рифмы / Образы: {int(row['R'])}/10  \n"
                        f"🎵 Структура / Ритмика: {int(row['S'])}/10  \n"
                        f"🔥 Реализация стиля: {int(row['T'])}/10  \n"
                        f"💫 Индивидуальность / Харизма: {int(row['H'])}/10  \n"
                        f"🌌 Атмосфера / Вайб: {int(row['V'])}/10"
                    )
                except Exception:
                    st.info("🧩 Подробные оценки не найдены.")

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
# Админ-панель
# -----------------------------
st.markdown("---")
admin_code = st.text_input("🔐 Код администратора:", type="password")

if admin_code == "characterai":
    st.markdown("### 🧩 Админ-панель")

    if not df.empty:
        df_admin = df.reset_index().rename(columns={"index": "orig_index"})
        for _, r in df_admin.iterrows():
            orig_idx = int(r["orig_index"])
            with st.expander(f"{r['Категория']}: {r['Название']} — {r['Баллы']} / 90"):
                new_cat = st.selectbox("Категория", ["Исполнитель", "Трек", "Альбом"], index=["Исполнитель","Трек","Альбом"].index(r["Категория"]), key=f"cat_{orig_idx}")
                new_name = st.text_input("Название", value=r["Название"], key=f"name_{orig_idx}")
                new_artist = st.text_input("Исполнитель", value=r["Исполнитель"], key=f"artist_{orig_idx}")
                new_review = st.text_area("Рецензия", value=r["Рецензия"], key=f"review_{orig_idx}")
                new_reviewer = st.text_input("Оценщик", value=r["Оценщик"], key=f"rev_{orig_idx}")

                def safe_int(x): 
                    try: return int(x)
                    except: return 5

                new_R = st.number_input("R", 1, 10, safe_int(r["R"]), key=f"R_{orig_idx}")
                new_S = st.number_input("S", 1, 10, safe_int(r["S"]), key=f"S_{orig_idx}")
                new_T = st.number_input("T", 1, 10, safe_int(r["T"]), key=f"T_{orig_idx}")
                new_H = st.number_input("H", 1, 10, safe_int(r["H"]), key=f"H_{orig_idx}")
                new_V = st.number_input("V", 1, 10, safe_int(r["V"]), key=f"V_{orig_idx}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Сохранить изменения", key=f"save_{orig_idx}"):
                        recalculated = flomaster_score(new_R, new_S, new_T, new_H, new_V)
                        df.loc[orig_idx, ["Категория","Название","Исполнитель","Рецензия","Оценщик"]] = [new_cat, new_name, new_artist, new_review, new_reviewer]
                        df.loc[orig_idx, ["R","S","T","H","V","Баллы"]] = [new_R,new_S,new_T,new_H,new_V,recalculated]
                        df.to_csv(CSV_FILE, index=False)
                        st.success("✅ Изменения сохранены.")
                with col2:
                    if st.button("🗑 Удалить", key=f"del_{orig_idx}"):
                        df = df.drop(index=orig_idx)
                        df.to_csv(CSV_FILE, index=False)
                        st.warning("❌ Запись удалена.")

    else:
        st.info("Нет данных для отображения.")

# -----------------------------
# Восстановление данных
# -----------------------------
st.markdown("### 🩹 Обслуживание данных")
if st.button("🩹 Восстановить таблицу данных"):
    try:
        if os.path.exists(CSV_FILE):
            shutil.copy(CSV_FILE, BACKUP_FILE)
            st.success(f"✅ Резервная копия сохранена ({BACKUP_FILE})")

        df_repair = pd.read_csv(CSV_FILE)
        for col in ["R","S","T","H","V"]:
            if col not in df_repair.columns:
                df_repair[col] = 5
        for col in ["R","S","T","H","V"]:
            df_repair[col] = pd.to_numeric(df_repair[col], errors="coerce").fillna(5).astype(int)

        df_repair.to_csv(CSV_FILE, index=False)
        st.success("🎨 Таблица успешно восстановлена!")
    except Exception as e:
        st.error(f"⚠️ Ошибка: {e}")
        # -----------------------------
# Нижняя подпись
# -----------------------------
st.markdown(
    "<div style='text-align:center; margin-top:60px; color:#999;'># мыши всегда ниже</div>",
    unsafe_allow_html=True,
)
