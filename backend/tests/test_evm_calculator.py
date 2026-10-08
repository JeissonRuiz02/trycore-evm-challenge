import pytest
from app.services.evm_calculator import EVMCalculator


def test_standard_calculation():
    """Test de cálculo estándar con valores típicos."""
    # BAC=1000, Planned=50%, Actual=40%, Cost=500
    # PV=500, EV=400, CV=-100, SV=-100, CPI=0.8, SPI=0.8
    metrics = EVMCalculator.calculate_metrics(1000, 0.5, 0.4, 500)
    assert metrics.pv == 500.0
    assert metrics.ev == 400.0
    assert metrics.cv == -100.0
    assert metrics.sv == -100.0
    assert metrics.cpi == 0.8
    assert metrics.spi == 0.8
    assert metrics.status_cost == "Over Budget"
    assert metrics.status_schedule == "Behind Schedule"


def test_perfect_execution():
    """Test cuando el proyecto va exactamente según lo planeado."""
    metrics = EVMCalculator.calculate_metrics(1000, 0.5, 0.5, 500)
    assert metrics.cpi == 1.0
    assert metrics.spi == 1.0
    assert metrics.status_cost == "Under Budget"
    assert metrics.status_schedule == "On Track/Ahead"


def test_division_by_zero_ac():
    """Caso borde: Costo real es 0 pero hay progreso (Eficiencia infinita)."""
    metrics = EVMCalculator.calculate_metrics(1000, 0.5, 0.1, 0)
    assert metrics.cpi == float("inf")


def test_division_by_zero_pv():
    """Caso borde: Avance planificado es 0 pero hay progreso real."""
    metrics = EVMCalculator.calculate_metrics(1000, 0.0, 0.1, 100)
    assert metrics.spi == float("inf")


def test_invalid_progress_raises_error():
    """Debe lanzar ValueError si el progreso está fuera del rango 0-1."""
    with pytest.raises(ValueError, match="Los porcentajes de avance deben estar entre 0 y 1"):
        EVMCalculator.calculate_metrics(1000, 1.5, 0.5, 500)


class _Activity:
    def __init__(self, bac, planned_progress, actual_progress, actual_cost):
        self.bac = bac
        self.planned_progress = planned_progress
        self.actual_progress = actual_progress
        self.actual_cost = actual_cost


def test_project_metrics_empty():
    metrics = EVMCalculator.calculate_project_metrics([])
    assert metrics.pv == 0.0
    assert metrics.ev == 0.0
    assert metrics.cpi == 1.0
    assert metrics.spi == 1.0


def test_actual_progress_zero():
    metrics = EVMCalculator.calculate_metrics(1000, 0.5, 0.0, 500)
    assert metrics.ev == 0.0
    assert metrics.cv == -500.0
    assert metrics.cpi == 0.0
    assert metrics.status_cost == "Over Budget"


def test_project_metrics_consolidates_activities():
    activities = [
        _Activity(1000, 0.5, 0.4, 500),
        _Activity(1000, 0.5, 0.5, 500),
    ]
    metrics = EVMCalculator.calculate_project_metrics(activities)
    assert metrics.pv == 1000.0
    assert metrics.ev == 900.0
    assert metrics.cv == -100.0
    assert metrics.sv == -100.0
    assert metrics.cpi == 0.9
    assert metrics.spi == 0.9
