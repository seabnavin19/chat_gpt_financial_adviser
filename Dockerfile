FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get update && apt-get install -y gnupg2 
RUN apt-get install -y curl apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
WORKDIR /prefect-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt