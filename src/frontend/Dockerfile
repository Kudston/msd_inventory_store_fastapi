FROM node:18

WORKDIR /app

COPY package*.json package-lock.json ./

COPY . .

COPY .env .

RUN npm ci

RUN npm run build

EXPOSE 3000