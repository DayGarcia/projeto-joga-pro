# pull official base image
FROM python:3.9.6-alpine

COPY ./trusted-certs.pem /usr/local/share/ca-certificates/
RUN cat /usr/local/share/ca-certificates/trusted-certs.pem >> /etc/ssl/certs/ca-certificates.crt

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev ca-certificates 

# install dependencies
RUN pip install --upgrade pip
# RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
COPY ./requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# copy project
COPY . .