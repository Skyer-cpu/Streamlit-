import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Устанавливаем настройки страницы
st.set_page_config(page_title="Анализ чаевых", layout="wide")

# Кэширование функции загрузки данных
@st.cache_data
def load_default_data():
    path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
    tips = pd.read_csv(path)
    tips['time_order'] = pd.to_datetime(
        np.random.choice(pd.date_range('2023-01-01', '2023-01-31'), size=len(tips))
    )
    return tips

# Сайдбар для загрузки данных
st.sidebar.title("Настройки")
uploaded_file = st.sidebar.file_uploader("Загрузите ваш CSV-файл", type=["csv"])

# Загрузка данных
if uploaded_file is not None:
    # Если пользователь загрузил файл, используем его данные
    @st.cache_data
    def load_user_data(file):
        data = pd.read_csv(file)
        return data

    tips = load_user_data(uploaded_file)
    st.sidebar.success("Данные успешно загружены!")
else:
    # Если файл не загружен, используем данные по умолчани��
    tips = load_default_data()
    st.sidebar.info("Используются данные по умолчанию.")

# Сайдбар для выбора графика
graph_type = st.sidebar.selectbox(
    "Выберите график:",
    ["Динамика чаевых во времени", "Гистограмма total_bill", "Связь total_bill и tip"]
)

# Построение графиков
if graph_type == "Динамика чаевых во времени":
    st.subheader("Динамика чаевых во времени")
    if "time_order" in tips.columns and "tip" in tips.columns:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=tips, x='time_order', y='tip', ax=ax)
        ax.set_title("Динамика чаевых во времени")
        ax.set_xlabel("Дата")
        ax.set_ylabel("Чаевые")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.error("Для построения графика необходимы столбцы 'time_order' и 'tip'.")

elif graph_type == "Гистограмма total_bill":
    st.subheader("Гистограмма total_bill")
    if "total_bill" in tips.columns:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(data=tips, x='total_bill', bins=20, kde=True, ax=ax)
        ax.set_title("Гистограмма total_bill")
        ax.set_xlabel("Сумма счета")
        ax.set_ylabel("Частота")
        st.pyplot(fig)
    else:
        st.error("Для построения графика необходим столбец 'total_bill'.")

elif graph_type == "Связь total_bill и tip":
    st.subheader("Связь total_bill и tip")
    if "total_bill" in tips.columns and "tip" in tips.columns:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=tips, x='total_bill', y='tip', ax=ax)
        ax.set_title("Связь между total_bill и tip")
        ax.set_xlabel("Сумма счета (total_bill)")
        ax.set_ylabel("Чаевые (tip)")
        st.pyplot(fig)
    else:
        st.error("Для построения графика необходимы столбцы 'total_bill' и 'tip'.")

# Функционал скачивания графиков
st.sidebar.subheader("Скачать график")
if st.sidebar.button("Скачать как PNG"):
    fig.savefig("tips_chart.png")
    with open("tips_chart.png", "rb") as file:
        st.sidebar.download_button(
            label="Скачать график",
            data=file,
            file_name=f"{graph_type.replace(' ', '_')}.png",
            mime="image/png"
        )