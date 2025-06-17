import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Установка языка интерфейса
st.set_page_config(page_title="Котировки Apple", layout="wide")

# Заголовок приложения
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