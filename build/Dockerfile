FROM python:3.7-slim

RUN apt-get update && apt-get install gcc -y && apt-get clean

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONBUFFERED 1
COPY ./configs ./configs
COPY ./tools ./tools
COPY ./scripts ./scripts
COPY ./spider.py .
COPY ./wait-for-it.sh .

RUN chmod +x ./scripts/quotes.sh

