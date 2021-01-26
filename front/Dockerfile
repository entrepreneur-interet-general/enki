# base image
FROM node:15.2.0

RUN apt-get update
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /app/package.json
RUN yarn

# add app
COPY . /app

EXPOSE 1337

# start app
CMD ng serve --host 0.0.0.0
