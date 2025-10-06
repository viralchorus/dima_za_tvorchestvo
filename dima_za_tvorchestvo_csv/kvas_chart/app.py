import streamlit as st
import pandas as pd
from datetime import datetime
import os

def flomaster_score(R, S, T, H, V):
    B = R + S + T + H
    B_prime = B * 1.4
    M = 1.0 + ((V - 1) / 9) * (1.6072 - 1.0)
    return round(B_prime * M)

st.set_page_config(page_title="Квас Чарт", page_icon="🍺")

def _create_empty_store():
    return {"Исполнитель": [], "Трек": [], "Альбом": []}

if "ratings" not in st.session_state:
    st.session_state["ratings"] = _create_empty_store()
elif isinstance(st.session_state["ratings"], list):
    st.session_state["ratings"] = _create_empty_store()

CSV_FILE = "ratings.csv"

if os.path.exists(CSV_FILE):
    old_df = pd.read_csv(CSV_FILE)
    for cat in ["Исполнитель", "Трек", "Альбом"]:
        st.session_state["ratings"][cat] = old_df[old_df["Категория"] == cat].to_dict("records")

category_forms = {
    "Исполнитель": {"who": "исполнителя", "title": "Исполнители"},
    "Трек": {"who": "трека", "title": "Треки"},
    "Альбом": {"who": "альбома", "title": "Альбомы"},
}

st.title("🍺 Квас Чарт — Дима За Творчество")
st.write("Оцени музло как Дмитрий Кузнецов. (Только не пролей квас на микрофон!)")

category = st.radio(
    "Что оцениваем сегодня?",
    ["Исполнитель", "Трек", "Альбом"],
    horizontal=True
)
forms = category_forms[category]

nickname = st.text_input("Введите свой никнейм (по желанию):")
if nickname.strip() == "":
    nickname = "Серая мышь (Не зареган)"

name = st.text_input(f"Введите название {forms['who']}:")

R = st.slider("🎭 Рифмы / Образы", 1, 10, 5)
S = st.slider("🎵 Структура / Ритмика", 1, 10, 5)
T = st.slider("🔥 Реализация стиля", 1, 10, 5)
H = st.slider("💫 Индивидуальность / Харизма", 1, 10, 5)

st.markdown("### 🌌 Атмосфера / Вайб")
st.markdown(
    """
    <div style='padding:8px; border:2px solid #6C63FF; border-radius:10px;
    background-color:#F3F0FF; color:#000000;'>
        <b>Чем сильнее вайб — тем вкуснее квас. Этот критерий влияет на множитель общей оценки, бро!</b>
    </div>
    """ ,
    unsafe_allow_html=True
)
V = st.slider("🌌 Атмосфера / Вайб", 1, 10, 5, key="vibe_slider")

review = st.text_area("✍️ Напиши рецензию (по желанию):", "")

if st.button("И чё у нас в итоге?"):
    if name.strip() == "":
        st.warning("⚠️ Ты чё, Чупа? Введи название перед оценкой, не будь мышью!")
    else:
        score = flomaster_score(R, S, T, H, V)
        st.success(f"Итоговая оценка для {forms['who']} {name}: {score} / 90 🎯")
        st.balloons()

        entry = {
            "Категория": category,
            "Название": name.strip(),
            "Баллы": int(score),
            "Рецензия": review.strip(),
            "Никнейм": nickname.strip(),
            "Дата": datetime.now().strftime("%d.%m.%Y"),
        }

        st.session_state["ratings"][category].append(entry)

        all_data = []
        for cat, items in st.session_state["ratings"].items():
            all_data.extend(items)
        pd.DataFrame(all_data).to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

ratings_list = st.session_state["ratings"][category]

if ratings_list:
    st.subheader(f"🏆 Квас Чарт: {forms['title']}")
    df = pd.DataFrame(ratings_list)
    df = df.sort_values(by="Баллы", ascending=False).reset_index(drop=True)
    df.index += 1
    st.dataframe(df[["Название", "Баллы", "Никнейм", "Дата"]], use_container_width=True)
else:
    st.info(f"👀 Пока нет ни одной оценки для категории: {forms['title'].lower()}.")

if st.button("📜 Показать отзывы"):
    all_reviews = [
        r for cat in st.session_state["ratings"].values()
        for r in cat if r["Рецензия"].strip() != ""
    ]

    if all_reviews:
        st.subheader("💬 Рецензии от квасеров:")
        for r in sorted(all_reviews, key=lambda x: x["Дата"], reverse=True):
            st.markdown(f"""
            **{r['Никнейм']}** 🕓 *{r['Дата']}*  
            **{r['Категория']}:** {r['Название']} — **{r['Баллы']} / 90**  
            > {r['Рецензия']}
            """)
            st.markdown("---")
    else:
        st.info("🍺 Пока никто не высказался. Будь первым, бро!")

if st.button(f"♻️ Сбросить рейтинг ({forms['title'].lower()})"):
    st.session_state["ratings"][category] = []
    all_data = []
    for cat, items in st.session_state["ratings"].items():
        all_data.extend(items)
    pd.DataFrame(all_data).to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
    st.success(f"Рейтинг для категории {forms['title']} сброшен.")
