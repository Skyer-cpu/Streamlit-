import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Установка языка интерфейса
st.set_page_config(page_title="Многостраничное приложение", layout="wide")

# Кеширование данных
@st.cache_data
def load_stock_data(ticker="AAPL", start="2010-01-01"):
    return yf.download(ticker, start=start).reset_index()

@st.cache_data
def load_tips_data():
    url = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
    tips = pd.read_csv(url)
    tips['time_order'] = pd.to_datetime(
        np.random.choice(pd.date_range('2023-01-01', '2023-01-31'), size=len(tips))
    )
    return tips

# Функция для отображения графика и кнопки скачивания
def plot_and_download(fig, filename):
    st.pyplot(fig)
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    st.download_button("Скачать график", data=buffer, file_name=filename, mime="image/png")

# Выбор страницы
page = st.sidebar.selectbox("Выберите страницу:", ["Котировки Apple", "Анализ чаевых"])

# Страница 1: Котировки Apple
if page == "Котировки Apple":
    st.title("Котировки компании Apple")
    data = load_stock_data()

    st.subheader("Данные о котировках")
    st.dataframe(data)

    st.subheader("График цен акций")
    st.line_chart(data.set_index("Date")["Close"])

    # Слайдер для выбора диапазона
    st.subheader("Выбор периода")
    min_date, max_date = data["Date"].min().date(), data["Date"].max().date()
    start_date, end_date = st.slider("Выберите диапазон дат", min_date, max_date, 
                                     (pd.to_datetime("2020-01-01").date(), max_date))
    filtered_data = data[(data["Date"] >= pd.to_datetime(start_date)) & 
                         (data["Date"] <= pd.to_datetime(end_date))]

    st.write(f"Данные с {start_date} по {end_date}:")
    st.dataframe(filtered_data)

    # График для выбранного диапазона
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(filtered_data["Date"], filtered_data["Close"], label="Цена закрытия", color="green")
    ax.set_title("График цен акций Apple")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Цена закрытия")
    ax.legend()
    plt.xticks(rotation=45)
    plot_and_download(fig, "apple_stock_chart.png")

# Страница 2: Анализ чаевых
elif page == "Анализ чаевых":
    st.title("Анализ чаевых")

    # Загрузка данных
    uploaded_file = st.sidebar.file_uploader("Загрузите CSV-файл", type=["csv"])
    tips = pd.read_csv(uploaded_file) if uploaded_file else load_tips_data()

    # Выбор графика
    graph_type = st.sidebar.selectbox("Выберите график:", 
                                       ["Динамика чаевых во времени", "Гистограмма total_bill", "Связь total_bill и tip"])

    # Построение графиков
    fig, ax = plt.subplots(figsize=(8, 6))
    if graph_type == "Динамика чаевых во времени":
        sns.lineplot(data=tips, x='time_order', y='tip', ax=ax)
        ax.set_title("Динамика чаевых во времени")
    elif graph_type == "Гистограмма total_bill":
        sns.histplot(data=tips, x='total_bill', bins=20, kde=True, ax=ax)
        ax.set_title("Гистограмма total_bill")
    elif graph_type == "Связь total_bill и tip":
        sns.scatterplot(data=tips, x='total_bill', y='tip', ax=ax)
        ax.set_title("Связь между total_bill и tip")
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=45)
    plot_and_download(fig, f"{graph_type.replace(' ', '_')}.png")