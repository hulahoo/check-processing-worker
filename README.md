# data-processing-worker

Сервис создан для актуализации скоринга Индикаторов, обогащения их инфромацией и удаления архивных Индикаторов.

## Информация о файлах конфигурации

Все конфигурции можно найти в директории:

```bash
src/events_gateway/config
```

## Информаци о ENV-параметрах

Имеющиеся env-параметры в проекте:
```bash
APP_POSTGRESQL_NAME=test_name
APP_POSTGRESQL_USER=user
APP_POSTGRESQL_PASSWORD=password
APP_POSTGRESQL_HOST=localhost
APP_POSTGRESQL_PORT=5432

DAGSTER_HOME=~/dagster_home
DAGIT_ENABLED=false
```

### Запуск воркера

1. Создайте виртуальное окружение

```
python3 -m venv venv
```

2. Активировать виртуальное окружение: 

```
source venv/bin/activate
```

3. Установить зависимости: 

```
pip3 install -r requirements.txt
```

4. Соберите модуль

```
python setup.py install
```

5. Запустите сервис
```
data-processing-worker
```

Для отладки можно запустить dagit (dagster web UI) установив env DAGIT_ENABLED=true.
В этом случае dagit запуститься на 3000 порту.

Для настроек dagster используется файл /config/dagster.yaml


### Требования к инфраструктуре
1. Минимальная версия Kafka:
  ```yaml
    wurstmeister/kafka:>=2.13-2.7.2
  ```
2. Минимальная версия Postgres:
  ```yaml
    postgres:>=14-alpine
  ```
3. Минимальная версия zookeper:
  ```yaml
    wurstmeister/zookeeper
  ```

### Запуск с помощью Dockerfile

1. Очень часто для разработки полезно запустить сервис локально в Dockerfile или в docker-compose (когда нужна сопутствующая инфраструктуруа). Для этого мы ниже опишем содержимое этих файлов. Просто положить их в репу для данного проекта нельзя в соответствии с регламентом CI/CD.

2. Мы используем следующее содержимое для Dockerfile

```dockerfile
FROM python:3.10.8-slim as deps
WORKDIR /app
COPY . ./
RUN apt-get update -y && apt-get -y install gcc python3-dev
RUN pip --no-cache-dir install -r requirements.txt 
RUN pip --no-cache-dir install -r requirements.setup.txt 
RUN pip install -e .

FROM deps as build
ARG ARTIFACT_VERSION=local
RUN python setup.py sdist bdist_wheel
RUN ls -ll /app/
RUN ls -ll /app/dist/


FROM python:3.10.8-slim as runtime
COPY --from=build /app/dist/*.whl /app/
RUN apt-get update -y && apt-get -y install gcc python3-dev
RUN pip --no-cache-dir install /app/*.whl
ENTRYPOINT ["data-processing-worker"]
```

2. Мы используем следующее содержимое для docker-compose.yml
```yaml
version: '3'


services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
  kafka:
    image: wurstmeister/kafka:latest
    ports:
      - target: 9094
        published: 9094
        protocol: tcp
        mode: host
    environment:
      HOSTNAME_COMMAND: "docker info | grep ^Name: | cut -d' ' -f 2"
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: INSIDE://:9092,OUTSIDE://_{HOSTNAME_COMMAND}:9094
      KAFKA_LISTENERS: INSIDE://:9092,OUTSIDE://:9094
      KAFKA_INTER_BROKER_LISTENER_NAME: INSIDE
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  db:
    image: rshb-cti-db-postgres:staging

  worker:
    restart: always
    build: ./
    ports:
    - "8080:8080"
    environment:
      EVENTS_PORT: 9000
      EVENTS_HOST: 0.0.0.0
      KAFKA_GROUP_ID: main
      KAFKA_BOOTSTRAP_SERVER: kafka:9092
      EVENTS_COLLECTOR_TOPIC: syslog

      APP_POSTGRESQL_USER: dbuser
      APP_POSTGRESQL_PASSWORD: test
      APP_POSTGRESQL_NAME: db
      APP_POSTGRESQL_HOST: db
      APP_POSTGRESQL_PORT: 5432
    depends_on:
      - db

 
networks:
    external:
      name: kafka_net
```

3. Запуск контейнеров:
```bash
docker-compose up --build
```
