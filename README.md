# Trycore EVM Tool

API para registrar proyectos y actividades y calcular indicadores de Valor Ganado (EVM).

El frontend todavía no está. Mientras tanto puedes usar la API y Swagger.

## Requisitos

- Python 3.12
- [Poetry](https://python-poetry.org/)

La base de datos de desarrollo es **SQLite** (`backend/evm_project.db`) para poder correr el proyecto sin instalar Postgres. El esquema se aplica con Alembic.

## Setup

```bash
git clone https://github.com/JeissonRuiz02/trycore-evm-challenge.git
cd trycore-evm-challenge
poetry install
```

## Base de datos

Desde la carpeta `backend`:

```bash
cd backend
poetry run alembic upgrade head
```

Eso crea las tablas `projects` y `activities`.

## Correr la API

Desde `backend`:

```bash
poetry run uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/swagger-ui
- Alias: http://127.0.0.1:8000/api-docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## Tests

Desde la raíz del repo:

```bash
poetry run pytest
poetry run pytest --cov=app --cov-report=term-missing
```

Linter:

```bash
poetry run flake8 backend/app backend/tests
poetry run black --check backend/app backend/tests
```

## Flujo git

Trabajo en `feature/*`, integración en `develop`, PRs hacia `develop`. `master` es el commit inicial (equivalente a `main` en el PDF).

## Documentos

- `docs/SSD.md` — contrato de datos, fórmulas y API
- `AI_PROCESS.md` — cómo se usó IA en la prueba
