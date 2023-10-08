# FATA(FastApi Tasks App)
Данный проект представляет собой пространство команды для ведения задач пользователей и их уведомления через email.
Завершённость проекта ~ 55%

## Содержание
- [Технологии](#Технологии)
- [Первый запуск](#первый-запуск)
- [Тестирование](#тестирование)
- [Deploy и CI/CD](#deploy-и-cicd)
- [Contributing](#contributing)
- [To do](#to-do)
- [FAQ](#faq-)
- [Команда проекта](#команда-проекта)

## Технологии
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [FastApi](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Poetry](https://python-poetry.org/)


## Первый запуск
### Запуск на локальной машине
Прежде всего необходимо добавить файл окружения .env
Он имеет следующую структуру:
```text
DB_HOST=...
DB_PORT=...
DB_USER=...
DB_PSW=...
DB_NAME=...

REDIS_NAME=...
REDIS_HOST=...
REDIS_PORT=...
REDIS_DB=...
REDIS_NOTIFICATIONS_KEY=...
REDISMAXPULL=...

TOKEN_UPDATE_TIME=...

EMAIL_SENDER=...
SMTP_PASSWORD=...
```
Развернём проект с помощью [pyenv и poetry](https://habr.com/ru/articles/599441/)

Установим зависимости:
```commandline
poetry init
```
Зайдём в виртуальное окружение с помощью команды:
```commandline
poetry shell
```
Запустим файл main.py
```commandline
python main.py
```
Для проверки обратитесь к swagger-у проекта по адресу: http://127.0.0.1:8000/docs 
### Docker
Добавим файл окружения .docker_env
```text
REDIS_NAME=...
REDIS_DB=...
REDIS_NOTIFICATIONS_KEY=...
REDISMAXPULL=...
REDIS_PORT=...
REDIS_HOST=...

DB_PORT=...
DB_HOST=...
DB_PSW=...
DB_NAME=...
DB_USER=...
POSTGRES_PASSWORD=...
POSTGRES_USER=...
POSTGRES_DB=...

TOKEN_UPDATE_TIME=...

EMAIL_SENDER=...
SMTP_PASSWORD=...
```

Сначала необходимо собрать билд проекта.
```commandline
docker compose build
```
Далее следует его запустить.
```commandline
docker compose up
```
Проверяем доступность сервиса по обращению к swagger-у: http://127.0.0.1:9090/docs

## Тестирование
В разработке... 
Планируется использовать pytest

## Deploy и CI/CD
В разработке... 

## Contributing
В разработке... 

## FAQ 
- Взаимодействие с базами данных PostgreSQL и Redis - асинхронное.
- Паттерн "Репозиторий"
- Паттерн "Unit of work"
- Как получить [SMTP_PASSWORD](https://timeweb.cloud/tutorials/mail/kak-ispolzovat-smtp-server-google) для отправки сообщений по почте

## To do
- [ ] Доработать README.md
- [ ] Создать README.md на английском
- [ ] Доработать модуль задач пользователей
- [ ] Добавить тестирование с помощью pytest
- [ ] Добавить логирование 
- [ ] Добавить docstrings 
- [ ] Добавить мониторинг приложения

## Команда проекта
- [Шумов Алексей](https://t.me/ShumovAlex) — Back-end developer.
