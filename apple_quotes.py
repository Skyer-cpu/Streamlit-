import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Установка языка интерфейса
st.set_page_config(page_title="Многостраничное приложение", layout="wide")

# Сайдбар для выбора страницы
page = st.sidebar.selectbox(
    "Выберите страницу:",
    ["Котировки Apple", "Анализ чаевых"]
)

# Страница 1: Котировки Apple
if page == "Котировки Apple":
    st.title("Котировки компании Apple")
    st.write("Это приложение отображает данные о котировках компании Apple (AAPL) с использованием библиотеки yfinance.")

    # Функция для загрузки данных с кешированием
    @st.cache_data
    def load_data(ticker):
        """
        Загружает данные о котировках акций с использованием yfinance.
        Данные кешируются для ускорения работы приложения.
        """
        data = yf.download(ticker, start="2010-01-01", end=None)
        data.reset_index(inplace=True)
        return data

    # Загрузка данных
    ticker_symbol = "AAPL"
    st.write(f"Загружаем данные для компании: {ticker_symbol}")
    data = load_data(ticker_symbol)

    # Отображение данных
    st.subheader("Данные о котировках")
    st.write("Ниже представлены данные о котировках компании Apple:")
    st.dataframe(data)

    # График цен
    st.subheader("График цен акций")
    st.write("График изменения цен акций компании Apple:")
    st.line_chart(data.set_index("Date")["Close"])

    # Выбор временного диапазона с помощью слайдера
    st.subheader("Выбор периода с помощью слайдера")
    min_date = data["Date"].min().date()  # Преобразуем в datetime.date
    max_date = data["Date"].max().date()  # Преобразуем в datetime.date

    # Слайдер для выбора диапазона
    slider_start, slider_end = st.slider(
        "Выберите диапазон дат",
        min_value=min_date,
        max_value=max_date,
        value=(pd.to_datetime("2020-01-01").date(), pd.to_datetime("today").date()),  # Преобразуем в datetime.date
        format="YYYY-MM-DD"
    )

    # Фильтрация данных по слайдеру
    slider_filtered_data = data[(data["Date"] >= pd.to_datetime(slider_start)) & (data["Date"] <= pd.to_datetime(slider_end))]

    st.write(f"Данные за период с {slider_start} по {slider_end}:")
    st.dataframe(slider_filtered_data)

    # График для выбранного диапазона слайдера
    st.subheader("График для выбранного диапазона (слайдер)")
    fig_slider, ax_slider = plt.subplots(figsize=(10, 6))
    ax_slider.plot(slider_filtered_data["Date"], slider_filtered_data["Close"], label="Цена закрытия", color="green")
    ax_slider.set_title("График цен акций Apple (слайдер)")
    ax_slider.set_xlabel("Дата")
    ax_slider.set_ylabel("Цена закрытия")
    ax_slider.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig_slider)

    # Добавление кнопки для скачивания графика слайдера
    buffer_slider = BytesIO()
    fig_slider.savefig(buffer_slider, format="png")
    buffer_slider.seek(0)
    st.download_button(
        label="Скачать график (слайдер) в формате PNG",
        data=buffer_slider,
        file_name="apple_stock_chart_slider.png",
        mime="image/png"
    )

    # Завершение
    st.write("Спасибо за использование приложения!")

# Страница 2: Анализ чаевых
elif page == "Анализ чаевых":
    st.title("Анализ чаевых")

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
        # Если файл не загружен, используем данные по умолчанию
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