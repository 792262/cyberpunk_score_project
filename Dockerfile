FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
CMD ["streamlit", "run", "app/webapp/app.py", "server.port=8501", "--server.address=0.0.0.0"]