from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api import api_router

app = FastAPI(
    title="Trycore EVM Tool API",
    description=(
        "API REST para seguimiento de proyectos y actividades con Valor Ganado (EVM). "
        "Las métricas (PV, EV, CV, SV, CPI, SPI, EAC, VAC) se calculan al consultar o actualizar, "
        "no se persisten. El estado de CPI/SPI va en `metrics.status`."
    ),
    version="0.1.0",
    docs_url="/swagger-ui",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/api-docs", include_in_schema=False)
def api_docs_redirect():
    return RedirectResponse(url="/swagger-ui")
