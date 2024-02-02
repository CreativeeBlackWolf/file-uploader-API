FROM python:3.12.1-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade --no-cache-dir pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
