FROM python:3.10 

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install  --no-cache-dir --upgrade -r requirements.txt

WORKDIR /app

COPY . .
