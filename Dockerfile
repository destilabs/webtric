FROM python:3.7-slim

WORKDIR /webtric

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONBUFFERED 1

COPY . .