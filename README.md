# Tron Info Test

Микросервис для получения информации о кошельках в сети TRON.

## Описание проекта

FastAPI-приложение, предоставляющее API для работы с кошельками в сети TRON. 

### Что можно было сделать, но не стал:

- Миграции Alembic - т.к это тестовое задание, посчитал ненужным.
- htmlcov

### Что добавил от себя:

- Data Access Object - при работе с большим проектом освобождает от написания самописных стейтментов.
- PostgreSQL - в качестве БД
- asyncpg - в качестве асинхронного интерфейса

## Требования

- Использовать FastAPI
- Аннотации от typing
- SQLAlchemy ORM
- tronpy
- Pytest


## Установка и запуск

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