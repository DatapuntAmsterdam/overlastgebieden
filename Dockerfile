FROM amsterdam/docker_python:latest
MAINTAINER datapunt.ois@amsterdam.nl

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

RUN apt-get update \
	&& apt-get install -y \
		netcat \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& adduser --system datapunt

WORKDIR /app

COPY overlastgebieden /app/overlastgebieden
COPY requirements.txt /app
COPY import.sh /app
COPY flake.cfg /app
COPY tests /app/tests
COPY Makefile /app

RUN pip install --no-cache-dir -r requirements.txt
USER datapunt

#CMD uwsgi

