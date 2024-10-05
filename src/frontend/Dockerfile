FROM node:18

WORKDIR /app

RUN npm install -g serve

COPY package*.json package-lock.json ./

COPY . .

COPY .env .

RUN npm ci

RUN npm run build

EXPOSE 3000