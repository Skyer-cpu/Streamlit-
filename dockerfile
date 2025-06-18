FROM python:3.10-slim
WORKDIR /app
COPY apple_quotes.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "apple_quotes.py", "--server.port=8501", "--server.address=0.0.0.0"]