# base image
FROM node:latest

# RUN apt-get update
RUN npm install -g @angular/cli

WORKDIR /app
COPY package.json yarn.lock ./


RUN yarn

COPY . .

