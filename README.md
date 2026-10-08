# Trycore EVM

Herramienta interna para que un líder de proyecto **registre actividades** y vea, de un vistazo, si el trabajo va bien o mal en **costo** y **cronograma**.

El análisis usa **Valor Ganado (EVM)**: no basta cuánto se gastó ni cuánto se avanzó por separado; importa la relación entre ambos.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/FastAPI-0.142-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black" alt="React 19">
  <img src="https://img.shields.io/badge/SQLite-Alembic-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/tests-30%20passed-success?style=flat-square" alt="30 tests">
</p>

---

## Contenido

- [Capturas y evidencias](#capturas-y-evidencias)
- [Qué hace (y qué no)](#qué-hace-y-qué-no)
- [Cómo se usa](#cómo-se-usa)
- [Glosario](#glosario)
- [Ejemplo numérico](#ejemplo-numérico)
- [Cómo correrlo](#cómo-correrlo)
- [API](#api)
- [Pruebas y calidad](#pruebas-y-calidad)
- [Arquitectura](#arquitectura)
- [Gitflow](#gitflow)
- [Documentos](#documentos)

---

## Capturas y evidencias

Guarda las PNG (o JPG) en [`docs/screenshots/`](docs/screenshots/) con **estos nombres**. Cuando los archivos existan, GitHub las muestra aquí. Hasta entonces el recuadro puede verse vacío: está previsto.

| Archivo | Qué fotografiar |
| :--- | :--- |
| <img width="1373" height="769" alt="image" src="https://github.com/user-attachments/assets/d1b4d199-d7c7-4d67-a988-6db92640e6bf" />  | Home: semáforo y estados en español |
| <img width="1172" height="1137" alt="image" src="https://github.com/user-attachments/assets/b7154628-5569-447c-8c0c-7fd0e14c91c8" /> | Consolidado, gráfica PV / EV / AC y tabla |
| <img width="991" height="394" alt="image" src="https://github.com/user-attachments/assets/3b0f0257-abc9-4c47-abc4-730e698da560" /> | Alta o edición de una actividad |
| <img width="1516" height="1222" alt="image" src="https://github.com/user-attachments/assets/f525fe17-11ab-4aad-8f07-333d10790ad6" /> | `/swagger-ui` con un endpoint abierto |
| <img width="1549" height="876" alt="image" src="https://github.com/user-attachments/assets/360bc6f4-e893-480a-a9ac-7059ca09f7c9" /> | PRs a `develop` y `release/0.1.0` → `main` |

---

## Qué hace (y qué no)

| Hace | No hace |
| :--- | :--- |
| CRUD de proyectos y actividades | Autenticación ni roles |
| Calcula PV, EV, CV, SV, CPI, SPI, EAC, VAC **al consultar** | Persistir métricas (no se guardan en la DB) |
| Consolida el proyecto **sumando** BAC, PV, EV y AC | Promediar CPI de las actividades |
| Semáforo y gráfica en el dashboard | Editar/borrar proyecto desde la UI (sí en la API) |
| Porcentajes en la API entre `0` y `1` | Calendario, recursos ni RPA |

La UI muestra el avance en **porcentaje 0–100**; el backend lo guarda como fracción (`50%` → `0.5`).

---

## Cómo se usa

1. Levanta API y dashboard ([abajo](#cómo-correrlo)).
2. En http://localhost:5173 crea un **proyecto**.
3. Entra al detalle y carga **actividades**: nombre, BAC, % planificado, % real, costo real (AC).
4. Mira el **consolidado** (tarjetas) y la **gráfica** PV vs EV vs AC.
5. El semáforo: **verde** si costo y cronograma van bien; **rojo** si alguno va mal.
6. Edita o elimina actividades en la tabla; las métricas se recalculan al guardar.

Datos mínimos para una demo (como en el video): **1 proyecto y 3 actividades**.

---

## Glosario

Términos PMI / EVM. En el JSON, `status` va **en inglés** (contrato del [SSD](docs/SSD.md)); en pantalla se traduce.

| Sigla | Nombre | Qué significa | Cómo se calcula |
| :--- | :--- | :--- | :--- |
| **BAC** | Budget at Completion | Presupuesto total planificado de la actividad (o la suma en el proyecto) | Lo captura el usuario |
| **AC** | Actual Cost | Dinero ya gastado | Lo captura el usuario |
| **PV** | Planned Value | Valor que *debería* estar ganado a la fecha | `% planificado × BAC` |
| **EV** | Earned Value | Valor del trabajo *realmente* hecho | `% real × BAC` |
| **CV** | Cost Variance | Desvío de costo | `EV − AC` |
| **SV** | Schedule Variance | Desvío de cronograma | `EV − PV` |
| **CPI** | Cost Performance Index | Eficiencia de costo | `EV / AC` |
| **SPI** | Schedule Performance Index | Eficiencia de cronograma | `EV / PV` |
| **EAC** | Estimate at Completion | Costo final proyectado si sigue igual | `BAC / CPI` |
| **VAC** | Variance at Completion | Hueco vs presupuesto al cierre | `BAC − EAC` |

### Cómo leer los semáforos

| Índice | JSON (`metrics.status`) | En la UI | Lectura |
| :--- | :--- | :--- | :--- |
| CPI ≥ 1 | `Under Budget` | Bajo presupuesto | El trabajo ganado cubre (o supera) lo gastado |
| CPI < 1 | `Over Budget` | Sobre presupuesto | Se gasta más de lo que se avanza |
| SPI ≥ 1 | `On Track/Ahead` | En tiempo / adelantado | Se ha ganado al menos lo planificado |
| SPI < 1 | `Behind Schedule` | Atrasado | Se ha ganado menos de lo planificado |

El PDF de la prueba habla de CPI **> 1**. El SSD y este código tratan **≥ 1** como en camino (CPI = 1 es “tal cual el plan”).

### Casos borde

- `AC = 0` y `EV = 0` → CPI = `1` (no se divide por cero).
- `AC = 0` y `EV > 0` → CPI infinito; en JSON sale `null`.
- Igual lógica para SPI con PV.
- Proyecto **sin actividades**: PV y EV en 0, CPI y SPI en 1.
- Porcentajes fuera de 0–1 → error de validación (HTTP 422).

---

## Ejemplo numérico

Actividad: BAC **1000**, plan **50%**, real **40%**, AC **500**.

| PV | EV | CV | SV | CPI | SPI | EAC | VAC |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 500 | 400 | −100 | −100 | 0.80 | 0.80 | 1250 | −250 |

Sobre presupuesto y atrasado: se gastaron 500 para un trabajo que “vale” 400, y se debería haber ganado 500.

El consolidado del proyecto **no** promedia esos CPI: suma BAC, PV, EV y AC de las actividades y vuelve a aplicar las fórmulas.

---

## Cómo correrlo

**Requisitos:** Python 3.12, [Poetry](https://python-poetry.org/), Node.js 20+.

Base de datos de desarrollo: **SQLite** (`backend/evm_project.db`). No hace falta instalar Postgres.

```bash
git clone https://github.com/JeissonRuiz02/trycore-evm-challenge.git
cd trycore-evm-challenge
git checkout main
poetry install

cd backend
poetry run alembic upgrade head
poetry run uvicorn app.main:app --reload
```

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

| Qué | URL |
| :--- | :--- |
| Dashboard | http://localhost:5173 |
| API | http://127.0.0.1:8000 |
| Swagger | http://127.0.0.1:8000/swagger-ui |
| Alias docs | http://127.0.0.1:8000/api-docs |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

La UI llama a `http://127.0.0.1:8000` (CORS abierto para 5173 y 3000). Preferir **localhost** en el navegador si `127.0.0.1:5173` no carga.

**PostgreSQL (opcional):** `poetry add psycopg2-binary`, URL `postgresql://user:password@localhost:5432/evm` en `SQLALCHEMY_DATABASE_URL` (ver `backend/.env.example`) y otra vez `alembic upgrade head`.

---

## API

REST, identificadores UUID. Las métricas viajan en `metrics` en el detalle del proyecto y en cada actividad.

| Método | Ruta | Notas |
| :--- | :--- | :--- |
| `POST` | `/projects` | Alta; la lista no trae métricas |
| `GET` | `/projects` | Listado |
| `GET` | `/projects/{id}` | Detalle + consolidado |
| `PUT` | `/projects/{id}` | Nombre y descripción |
| `DELETE` | `/projects/{id}` | Borra el proyecto y sus actividades |
| `GET` | `/projects/{id}/activities` | 404 si el proyecto no existe |
| `POST` | `/projects/{id}/activities` | Calcula métricas al crear |
| `PUT` | `/activities/{id}` | Recalcula |
| `DELETE` | `/activities/{id}` | — |

Descripciones, esquemas y códigos 404/422 están en Swagger. El contrato de dominio está en [`docs/SSD.md`](docs/SSD.md).

---

## Pruebas y calidad

Desde la raíz del repo:

```bash
poetry run pytest
poetry run pytest --cov=app --cov-report=term-missing
poetry run flake8 backend/app backend/tests
poetry run black --check backend/app backend/tests
```

Cobertura mínima configurada: **80%** (`fail_under`). Hay tests de AC = 0, proyecto vacío, avance real = 0, y un test HTTP por endpoint.

---

## Arquitectura

```
API  →  Services  →  Repositories  →  SQLAlchemy (SQLite)
              ↓
        EVMCalculator
```

El frontend (React + Vite) **pinta** lo que devuelve la API; no calcula EVM. Monorepo: `backend/`, `frontend/`, `docs/`.

---

## Gitflow

`feature/*` → PR a **`develop`** → **`release/*`** → **`main`**.

Tag actual de entrega: `v0.1.0`. `master` es el commit inicial de GitHub; no es producción.

---

## Documentos

| Archivo | Para qué |
| :--- | :--- |
| [`docs/SSD.md`](docs/SSD.md) | Datos, fórmulas y contrato de API |
| [`AI_PROCESS.md`](AI_PROCESS.md) | Herramientas de IA, prompts y decisiones |
| [`docs/screenshots/`](docs/screenshots/) | Capturas de uso y evidencias |
