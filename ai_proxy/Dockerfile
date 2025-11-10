FROM python:3.11-slim

WORKDIR /app

# تثبيت dependencies اللازمة لـ mysqlclient و build
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt
RUN pip install django-prometheus   

# نسخ المشروع كله
COPY . /app

# PYTHONPATH يضمن Django يرى my_poll_project
ENV PYTHONPATH=/app

CMD ["sh", "-c", "python manage.py setup_localstack && python manage.py runserver 0.0.0.0:8000"]
