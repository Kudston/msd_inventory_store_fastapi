FROM python:3.9-slim-bullseye

RUN apt-get update -y
RUN apt-get install gcc -y

RUN mkdir /usr/src/inventory_system_backends/
WORKDIR /usr/src/inventory_system_backends/

RUN mkdir requirements/
COPY requirements.txt requirements/prod.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements/prod.txt

ADD . /usr/src/inventory_system_backends/

# Copy SSL certificates
COPY ./ssl/key.pem ./ssl/key.pem
COPY ./ssl/cert.pem ./ssl/cert.pem


EXPOSE 8500
