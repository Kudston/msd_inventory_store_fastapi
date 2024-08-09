FROM python:3.9-slim-bullseye

RUN apt-get update -y
RUN apt-get install gcc -y

RUN mkdir /usr/src/inventory_system/
WORKDIR /usr/src/inventory_system/

RUN mkdir requirements/
COPY requirements.txt requirements/prod.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements/prod.txt

ADD . /usr/src/inventory_system/

# Copy SSL certificates
COPY ./src/backends/key.pem /app/src/backends/key.pem
COPY ./src/backends/cert.pem /app/src/backends/cert.pem


EXPOSE 8500
EXPOSE 8600
