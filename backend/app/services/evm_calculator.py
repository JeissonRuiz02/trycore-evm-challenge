from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass
class EVMMetrics:
    pv: float
    ev: float
    cv: float
    sv: float
    cpi: float
    spi: float
    eac: float
    vac: float
    status_cost: str
    status_schedule: str


class ActivityEVMInput(Protocol):
    bac: float
    planned_progress: float
    actual_progress: float
    actual_cost: float


class EVMCalculator:
    """
    Servicio responsable de calcular las métricas de Earned Value Management (EVM).
    Implementa la lógica definida en el SSD y maneja casos borde como divisiones por cero.
    """

    @staticmethod
    def calculate_metrics(
        bac: float, planned_progress: float, actual_progress: float, actual_cost: float
    ) -> EVMMetrics:
        if not (0 <= planned_progress <= 1) or not (0 <= actual_progress <= 1):
            raise ValueError("Los porcentajes de avance deben estar entre 0 y 1 (ej: 0.5 para 50%)")

        if bac < 0 or actual_cost < 0:
            raise ValueError("El presupuesto (BAC) y el costo real (AC) no pueden ser negativos")

        pv = planned_progress * bac
        ev = actual_progress * bac
        cv = ev - actual_cost
        sv = ev - pv

        # AC=0 y EV=0 → CPI=1. AC=0 y EV>0 → infinito (JSON lo serializa como null).
        cpi = ev / actual_cost if actual_cost > 0 else (1.0 if ev == 0 else float("inf"))
        spi = ev / pv if pv > 0 else (1.0 if ev == 0 else float("inf"))

        if 0 < cpi != float("inf"):
            eac = bac / cpi
        else:
            eac = bac if cpi == 1.0 else (0.0 if cpi == float("inf") else float("inf"))

        vac = bac - eac

        # El JSON del SSD usa estas etiquetas en inglés.
        status_cost = "Under Budget" if cpi >= 1.0 else "Over Budget"
        status_schedule = "On Track/Ahead" if spi >= 1.0 else "Behind Schedule"

        return EVMMetrics(
            pv=round(pv, 2),
            ev=round(ev, 2),
            cv=round(cv, 2),
            sv=round(sv, 2),
            cpi=round(cpi, 2) if cpi != float("inf") else float("inf"),
            spi=round(spi, 2) if spi != float("inf") else float("inf"),
            eac=round(eac, 2) if eac != float("inf") else float("inf"),
            vac=round(vac, 2) if vac != float("inf") else float("inf"),
            status_cost=status_cost,
            status_schedule=status_schedule,
        )

    @staticmethod
    def calculate_project_metrics(activities: Sequence[ActivityEVMInput]) -> EVMMetrics:
        """Consolida por suma de BAC, PV, EV y AC (no promedia los CPI)."""
        if not activities:
            return EVMCalculator.calculate_metrics(0.0, 0.0, 0.0, 0.0)

        bac = sum(activity.bac for activity in activities)
        actual_cost = sum(activity.actual_cost for activity in activities)
        planned_value = sum(activity.planned_progress * activity.bac for activity in activities)
        earned_value = sum(activity.actual_progress * activity.bac for activity in activities)
        planned_progress = planned_value / bac if bac > 0 else 0.0
        actual_progress = earned_value / bac if bac > 0 else 0.0
        return EVMCalculator.calculate_metrics(bac, planned_progress, actual_progress, actual_cost)
