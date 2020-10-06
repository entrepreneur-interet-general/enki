# ENKI - Outil de gestion de crise de NexSIS

## Run fake back end data
```
docker run --name  elasticsearch -v /Users/benjaminperney/Documents/WEB/enki_frontend/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml -v /Users/benjaminperney/Documents/WEB/enki_frontend/data/:/usr/share/elasticsearch/data -d -p 9200:9200 -e "ES_JAVA_OPTS=-Xmx256m -Xms256m" -e "discovery.type=single-node" -e "ELASTIC_PASSWORD=changeme" docker.elastic.co/elasticsearch/elasticsearch:7.9.1
```
## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
