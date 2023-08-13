# pull official base image
FROM python:3.10-slim

#install dependencies
RUN apt-get update \
    && apt-get install -y gcc wget make coinor-cbc coinor-libcbc-dev\
    && apt-get clean

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# create shared folder
RUN mkdir -p /app/app_data/shared 

# Execute Tests
RUN python -m unittest discover -v -s ./app -p test_*.py

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser




