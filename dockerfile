FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt
RUN pip install mysql-connector-python

COPY . /app

CMD ["sh", "-c", "python wait_for_db.py && python manage.py setup_localstack && tail -f /dev/null"]
