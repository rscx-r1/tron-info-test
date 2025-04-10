# Tron Info Test

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1F305F?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org)

Микросервис для получения информации о кошельках в сети TRON.

## Описание проекта

FastAPI-приложение, предоставляющее API для работы с кошельками в сети TRON. 

### Что можно было сделать, но не стал:

- htmlcov

### Что добавил от себя:

- Data Access Object - при работе с большим проектом освобождает от написания самописных стейтментов.
- PostgreSQL - в качестве БД
- asyncpg - в качестве асинхронного интерфейса
- CI проверка линтера в качестве RUFF
- CI тестов
Проект полностью готов к деплою на продакшен в любом AWS решении.

## Требования

- Использовать FastAPI
- Аннотации от typing
- SQLAlchemy ORM
- tronpy
- Pytest


## Установка и запуск

### Через Docker

#### Использование Docker Compose (рекомендуется)

1. Убедитесь, что у вас установлены Docker и Docker Compose

2. Создайте файл .env на основе .env.example:
```bash
cp .env.example .env
```

3. Запустите приложение с помощью Docker Compose:
```bash
docker compose up -d
```

Приложение будет доступно по адресу `http://localhost:8000` (или по порту, указанному в .env)

#### Ручной запуск Docker

1. Соберите Docker-образ:
```bash
docker build -t tron-info-test .
```

2. Запустите контейнер:
```bash
docker run -d \
  --name tron-info-test \
  -p 8000:8000 \
  --env-file .env \
  tron-info-test
```

### Локальная установка

0. Установите uv:
[Здесь](https://docs.astral.sh/uv/getting-started/installation/)
либо
```bash
pip install uv
```

1. Клонируйте репозиторий:
```bash
git clone https://github.com/rscx-r1/tron-info-test
cd tron-info-test
```

1. Создайте виртуальное окружение и установите зависимости с помощью uv:
```bash
uv venv
source .venv/bin/activate  # для Unix
# или
.venv\Scripts\activate     # для Windows
uv sync --extra dev
```

1. Создайте файл .env на основе .env.example и настройте переменные окружения:
```bash
cp .env.example .env
```

1. Запустите приложение:
```bash
# Для Unix
./run.sh
```

## Тесты
1. Перед запуском необходимо создать `.env.test` на базе `.env.test.example`:

2. Запустите тесты с помощью `make test`.