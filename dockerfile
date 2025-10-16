
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip wheel
RUN pip install -r requirements.txt

COPY . /app

CMD ["sh", "-c", "python polls/aws/setup_localstack.py && python -m polls.aws.sqs_listener"]
