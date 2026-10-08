# 📄 Software Specification Document (SSD) - Trycore EVM Tool

## 1. Objetivo del Sistema
Construir una herramienta de gestión de proyectos basada en la metodología **Earned Value Management (EVM)** para monitorear el desempeño de costos y cronograma en tiempo real.

## 2. Modelo de Dominio (Datos)

### Entidad: `Project`
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | UUID | Identificador único. |
| `name` | String | Nombre del proyecto. |
| `description` | String | Descripción breve. |
| `created_at` | DateTime | Fecha de creación. |

### Entidad: `Activity`
| Campo | Tipo | Descripción |
| :--- | :--- | :--- |
| `id` | UUID | Identificador único. |
| `project_id` | UUID | Relación con el proyecto (FK). |
| `name` | String | Nombre de la actividad. |
| `bac` | Float | Budget at Completion (Presupuesto Total Planificado). |
| `planned_progress` | Float | % de avance planificado a la fecha (0.0 a 1.0). |
| `actual_progress` | Float | % de avance real completado (0.0 a 1.0). |
| `actual_cost` | Float | AC (Costo real incurrido hasta hoy). |

---

## 3. Lógica de Negocio (Motor de Cálculo EVM)

El sistema implementará una clase `EVMCalculator` que procesará los datos de cada actividad y los consolidará a nivel de proyecto.

### Fórmulas a Implementar:
| Indicador | Fórmula | Interpretación |
| :--- | :--- | :--- |
| **PV** (Planned Value) | `planned_progress * BAC` | Lo que deberíamos haber gastado. |
| **EV** (Earned Value) | `actual_progress * BAC` | El valor real del trabajo completado. |
| **CV** (Cost Variance) | `EV - AC` | Negativo: Sobre presupuesto / Positivo: Bajo presupuesto. |
| **SV** (Schedule Variance) | `EV - PV` | Negativo: Atrasado / Positivo: Adelantado. |
| **CPI** (Cost Performance Index) | `EV / AC` | >1: Eficiente / <1: Ineficiente. |
| **SPI** (Schedule Performance Index) | `EV / PV` | >1: Adelantado / <1: Atrasado. |
| **EAC** (Estimate at Completion) | `BAC / CPI` | Proyección del costo final del proyecto. |
| **VAC** (Variance at Completion) | `BAC - EAC` | Diferencia proyectada entre presupuesto y costo final. |

**⚠️ Manejo de Casos Borde:**
- Si `AC = 0` y `EV = 0` $\to$ `CPI = 1.0` (evitar división por cero).
- Si `PV = 0` y `EV = 0` $\to$ `SPI = 1.0` (evitar división por cero).
- El sistema debe validar que los porcentajes estén entre 0 y 1.

---

## 4. Contrato de la API (REST)

### Proyectos
- `GET /projects` $\to$ Lista todos los proyectos.
- `POST /projects` $\to$ Crea un nuevo proyecto.
- `GET /projects/{id}` $\to$ Detalle del proyecto + **Indicadores Consolidados**.
- `PUT /projects/{id}` $\to$ Actualiza datos del proyecto.
- `DELETE /projects/{id}` $\to$ Elimina proyecto y sus actividades.

### Actividades
- `GET /projects/{id}/activities` $\to$ Lista actividades de un proyecto.
- `POST /projects/{id}/activities` $\to$ Crea actividad vinculada al proyecto.
- `PUT /activities/{id}` $\to$ Actualiza datos $\to$ **Recalcula métricas**.
- `DELETE /activities/{id}` $\to$ Elimina actividad.

### Respuesta de Métricas (Esquema JSON)
Cada actividad y el consolidado del proyecto devolverán:
```json
{
  "metrics": {
    "pv": 1000.0,
    "ev": 800.0,
    "cv": -200.0,
    "sv": -200.0,
    "cpi": 0.8,
    "spi": 0.8,
    "eac": 1250.0,
    "vac": -250.0,
    "status": {
      "cost": "Over Budget",
      "schedule": "Behind Schedule"
    }
  }
}
