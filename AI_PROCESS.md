# AI_PROCESS.md

Empecé el diseño en Ollama (plan, carpetas, SSD y el calculador). Después me pasé a Cursor: API, tests, Alembic, dashboard, PRs. `develop` tiene backend, frontend, README, OpenAPI, linter y polish (PRs #1–#6). Cierre Gitflow: `release/0.1.0` → `main` (GitHub arrancó en `master`; producción es `main`). Falta el video.

Este archivo lo actualicé cuando el código ya estaba casi listo. Debí escribirlo desde el día 1.

## Herramientas

- **Ollama + Claude Code:** arranque local. Ya lo tenía conectado.
- **Cursor:** desde que dije que siguiéramos la implementación acá. Lee archivos, corre tests, arma PRs.
- **pytest:** para no fiarme solo de que “corra”.

El SSD (`docs/SSD.md`) es lo que usé de guía. No le pedí a la IA que inventara las fórmulas: primero el PDF, después el SSD, después el código.

## Cómo entendí EVM

El PDF pide PV, EV, CV, SV, CPI, SPI, EAC y VAC. Lo bajé a un ejemplo y lo calculé a mano:

BAC 1000, planificado 50%, real 40%, costo 500.

- PV = 500
- EV = 400
- CV = -100 (sobre presupuesto)
- SV = -100 (atrasado)
- CPI = 0.8
- SPI = 0.8
- EAC = 1250
- VAC = -250

Ese mismo caso está en los tests. Si AC y EV son 0, CPI = 1 (para no dividir por cero). El consolidado del proyecto no es el promedio de los CPI: sumo BAC, PV, EV y AC y vuelvo a aplicar las fórmulas. Lo probé con dos actividades y me dio PV 1000, EV 900, CPI 0.9.

El PDF dice que CPI > 1 es eficiente. El SSD y el código usan ≥ 1 (CPI = 1 = On Track / Under Budget). Lo dejé así para no pelear con el contrato JSON del SSD.

## Prompts (en orden)

### Ollama

```
quiero que asumas el rol de experto en desarrollo de software, quiero definir el flujo de trabajo, ideas para la arquitectura e implementación para la siguiente prueba tecnica (anexo pdf con la prueba) basandomelos en SSD para la ayuda de implementacion con IA , teniendo en cuenta que te tengo conectado a claude code .
```

```
antes de esto también de anexo una captura con la definición del rol para ver lo qque mejor se acople a lo que buscan:
```

```
antes de eso, como deberiamos tener la arquitectura del proyecto, back, front y demas separados?
```

```
perfecto comencemos creando la estructura de carpetas, dame los comandos para crearlas , uso mac
```

```
Si, procede por favor
```

```
me podrías generar el archivo antes de continuar?
```

```
esto iria en la raiz del back o donde?
```

```
asi quedo el texto dentro del archivo md: [SSD] es correcto?
```

```
quedo correcto? [SSD] que son los “$\to$"
```

(Captura de la estructura de carpetas en `develop`.)

```
si ya trengo el SSD puedo usar claudo code que tengo conectado a ollama?
```

```
olvidalo sigamos con la implementación desde aca mejor
```

Ahí Ollama me pasó `evm_calculator.py` y los tests; los pegué yo. Lo demás fue en Cursor.

### Cursor

```
revisa el proyecto, ver si esta acoplado correctamente, que use pydantic v2 y que las referencias de archivos y demas esten configuradas correctamente para lo que esta actualmente creado
```

```
Para no perder el control, dividiremos esto en dos sub-etapas:
Etapa A: Refactorización y Persistencia (La base)
Mover rutas a /api.
Sincronizar tipos de IDs (UUID).
Configurar Alembic y crear la primera migración.
Implementar PUT/DELETE.
```

```
Lee todo el proyecto, ananila los archivos, revisa SSD.md y quiero que expliques todo lo que entendiste, en que etaba vamos y que tenemos en este momento
```

```
en este momento en que feature estamos?
```

```
nos falta algo para dejar pulida la feaure 2?
```

(Pedí el 404 de actividades, tests HTTP, quitar `datetime.utcnow` y activar FK en SQLite.)

```
perfecto como terminamos el feature 2?
```

```
dime como hago el comit y el pr hace dev y yo lo hago
```

```
y si en vez de un pr hacemos Merge a develop y borramos la rama? igual el historico se mantiene y dejamos las ramas limpias
```

```
listo ya cree la rama con que seguimos?
```

```
explicame de manera clara como funciona el proyecto a nivel de arquitectura, que hace y que no hace
```

```
perfecto, ahora que fase seguiria ?
```

(PDF de la prueba + vacante: cómo vamos.)

```
Cerrar Feature 3 con PR a develop (no merge local).
```

```
te refieres haque haga el merge?
```

```
ahora como dejo mi local igual que la nube?
```

```
segun el documento con lo que piden que desarrollemos estamos bien en el backend?
```

```
y a nivel de los demas requerimientos? @AI_PROCESS.md  y demas?
```

```
me ayudarias a llenarlo con base aa lo que hemos hablado y a esto que fue con lo que inicie en ollama como base?
```

(Pegó el dump de Ollama: el prompt inicial del SSD y la respuesta larga del modelo.)

```
El todo, algunas cosas y demas se ven muy IA toma ejemplo de como te excribo, se un poco mas resumido. elimina copsas que tal vez se vean mal o sean redundantes por favor
```

```
que mas podemos dejar listo o adelantar en esta fase?
```

(Iba pegado el checklist de entregables del PDF.)

```
ya lo reinicie, realizando un check list, que tenemos a la fecha?
```

```
perfecto, hagamoslo siguiendo la estructura segun lo planificado
```

```
Perfecto, revisa los dos proyectos a nivel de arquitectura, se alinea con lo planeado en el SSD y con los requerimientos? te anexo nuevamente el documento
```

```
Mergueemos los PRs por favor
```

```
algun ajuste, refeactor que podemos hacer con lo del .gitignore adicional? consideras oportuno poner docstrings en el codigo para buenas practicas? algo mirar para pulir? mirar que no tengamos comrtarios en ingles y luego en español etc ...
```

```
si, realicemos el commit y PR a develop si consideras que todo deberia ir asi
```

```
Como estamos a nivel de cumplimiento?
```

```
hagamos primero esto:

 mergear #4 → actualizar AI_PROCESS
```

También pedí corregir el 404 de actividades, tests HTTP, `datetime.utcnow` y `PRAGMA foreign_keys=ON`. Y anexé el PDF de la vacante (agentes/MCP/RPA) para ver cómo encajaba: no metí agentes en el producto; el proceso con IA va en este archivo.

No copié cada “ok” ni adjuntos de terminal. El hilo está en Cursor; estos son los que movieron una decisión.

## Donde no seguí a la IA

**1. Postgres + Docker.** Ollama lo daba por hecho. Usé SQLite + Alembic. La prueba es corta y tiene que correr fácil. El PDF pide una DB relacional, no obliga Postgres. Si hace falta, se cambia la URL.

**2. Merge local vs PR.** Ollama cerraba features con `git merge` a `develop`. En Feature 2 (`api-base`) hice eso, sin PR. El PDF pide PR aunque trabaje solo. A partir de Feature 3 usé PRs en GitHub (#1 métricas, #2 README/OpenAPI/tests, #3 dashboard, #4 polish).

Tampoco usé el patrón Strategy que sugería Ollama para el EAC. Con una clase de cálculo alcanza y se testea más fácil.

**3. Docstrings en todo.** En el polish la IA podía haber documentado cada CRUD. No: nombres + SSD alcanzan. Docstring solo donde hay una decisión (rollup del proyecto = suma, no promedio de CPI).

## Cómo comprobé los números

A mano el ejemplo de 1000 / 50% / 40% / 500. Los tests esperan esos mismos valores. Proyecto sin actividades: CPI y SPI en 1. Avance real = 0 entra en los tests. `PUT` de una actividad recalcula; el detalle del proyecto consolida. El dashboard lo revisé creando un proyecto y actividades y mirando semáforo y gráfica, no solo el JSON.

## Arquitectura

Ollama armó el monorepo (backend / frontend / docs). Yo dejé el SSD en `/docs` (es del sistema, no solo del back). La API no habla con la DB: pasa por services y repositories. Las métricas no se guardan: se calculan en cada request. Los ids son UUID de verdad, no strings. FastAPI porque el PDF lo permite y la vacante menciona Python; no por “agentes”.

Al montar la API, `models/project.py` tenía schemas Pydantic en vez del modelo ORM. Eso lo corregimos: el modelo es SQLAlchemy, los schemas se quedan en `schemas/`.

El frontend no es la fuente de verdad: pinta lo que devuelve la API. Lista de proyectos hace un GET de detalle por fila para el semáforo (GET `/projects` no trae métricas; el SSD lo deja así).

## Qué haría distinto

Escribir este archivo desde el día 1. Feature 2 también por PR. Crear `main` al arrancar, no al final. Postgres o Docker solo si sobraba tiempo, no como primer paso. Lo que sigue siendo entrega: el video (EVM en mis palabras, arquitectura, 1 proyecto y 3 actividades).
