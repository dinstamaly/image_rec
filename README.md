# Discount card (дисконтные карты)
> Программа для сканирование дискотных кард и штрих кода
>
## Требования
- PostgreSQL
- Python 3.6 и выше

## Переменные окружения 
> Переменные среды - это глобальные системные переменные, доступные для всех 
> процессов / пользователей, работающих под управлением операционной 
> системы (ОС), например Windows, macOS и Linux.

> Для примера в качестве операционной системы был выбран OS Linux.
> Необходмо перед запуском тестового сервера или продакшен сервера, 
> экспортировать переменные что внизу в таблице в окружение операционной системы

| Key              | Description                        | Default value  |
| :---             | :---                               | :---           |
| `POSTGRES_USER`  | postgres database user (not root)  | postgres       |
| `POSTGRES_PASS`  | postgres database password         | postgres       |
| `POSTGRES_DB`    | postgres database name             | False          |
| `POSTGRES_HOST`  | postgres service host              | localhost      |
| `POSTGRES_PORT`  | postgres service port              | 5432 (default) |

## Иструкция по подняю проета на сервере

## Иструкция по подняю проекта локально
> Пример продемонстрирован на операционной системе (ОС) MAC OS, также будет 
> работать и на ОС Linux.
> 1. Необходимо склонить проект из локального репоризитория: 
> https://git.bakai.local/bakai24/discount-cards-back.git
> 2. Пройти в директорию склоненного проекта:
``` bash
$ cd discount-cards-back/
```
> Создать пользователя, базу данных (БД), кастомную схему в БД:
``` bash
$ psql postgres

psql (13.1)
Type "help" for help.

postgres=# CREATE USER discount_user WITH ENCRYPTED PASSWORD 'discount_pass';
postgres=# GRANT ALL PRIVILEGES ON DATABASE discount_db TO youruser;
```
> После сделать команды для миграции:
``` bash
$ manage.py db init # Создает папку migrations;
$ manage.py db migrate # Создает версию миграции в папке migrations
$ manage.py db upgrade # Применяет изменении в базе
```
> После успешной миграции, можно запустить локальный сервер.
> протестить можно по этому url http://localhost:5000/discount


# Документация по API
>localhost:5000/discount/  