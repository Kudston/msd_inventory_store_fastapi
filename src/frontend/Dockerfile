FROM node:16

WORKDIR /app

COPY package*.json package-lock.json ./

COPY . .

COPY .env .

RUN npm install

RUN npm run build

EXPOSE 3000