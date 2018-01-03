FROM amsterdam/docker
MAINTAINER datapunt@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN adduser --system datapunt

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY overlastgebieden /app/overlastgebieden
COPY import.sh /app
COPY flake.cfg /app
COPY tests /app/tests
COPY Makefile /app
COPY docker-compose.yml /app

USER datapunt

#CMD uwsgi

