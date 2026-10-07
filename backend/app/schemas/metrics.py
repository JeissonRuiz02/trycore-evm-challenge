from pydantic import BaseModel, ConfigDict

from app.services.evm_calculator import EVMMetrics


class MetricsStatus(BaseModel):
    cost: str
    schedule: str


class EVMMetricsResponse(BaseModel):
    pv: float
    ev: float
    cv: float
    sv: float
    cpi: float | None
    spi: float | None
    eac: float | None
    vac: float | None
    status: MetricsStatus

    model_config = ConfigDict(ser_json_inf_nan="null")

    @classmethod
    def from_calculator(cls, metrics: EVMMetrics) -> "EVMMetricsResponse":
        return cls(
            pv=metrics.pv,
            ev=metrics.ev,
            cv=metrics.cv,
            sv=metrics.sv,
            cpi=_finite_or_none(metrics.cpi),
            spi=_finite_or_none(metrics.spi),
            eac=_finite_or_none(metrics.eac),
            vac=_finite_or_none(metrics.vac),
            status=MetricsStatus(
                cost=metrics.status_cost,
                schedule=metrics.status_schedule,
            ),
        )


def _finite_or_none(value: float) -> float | None:
    if value in (float("inf"), float("-inf")):
        return None
    return value
