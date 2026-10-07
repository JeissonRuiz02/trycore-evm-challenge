PROJECT_PAYLOAD = {"name": "Alpha", "description": "Demo project"}
ACTIVITY_PAYLOAD = {
    "name": "Foundation",
    "bac": 1000.0,
    "planned_progress": 0.5,
    "actual_progress": 0.4,
    "actual_cost": 500.0,
}


def test_activity_includes_metrics_on_create_and_update(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    created = client.post(
        f"/projects/{project_id}/activities",
        json=ACTIVITY_PAYLOAD,
    )
    assert created.status_code == 201
    metrics = created.json()["metrics"]
    assert metrics["pv"] == 500.0
    assert metrics["ev"] == 400.0
    assert metrics["cv"] == -100.0
    assert metrics["sv"] == -100.0
    assert metrics["cpi"] == 0.8
    assert metrics["spi"] == 0.8
    assert metrics["eac"] == 1250.0
    assert metrics["vac"] == -250.0
    assert metrics["status"]["cost"] == "Over Budget"
    assert metrics["status"]["schedule"] == "Behind Schedule"

    activity_id = created.json()["id"]
    updated = client.put(
        f"/activities/{activity_id}",
        json={**ACTIVITY_PAYLOAD, "actual_progress": 0.5, "actual_cost": 500.0},
    )
    assert updated.status_code == 200
    assert updated.json()["metrics"]["cpi"] == 1.0
    assert updated.json()["metrics"]["status"]["cost"] == "Under Budget"


def test_project_detail_includes_consolidated_metrics(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    empty_detail = client.get(f"/projects/{project_id}")
    assert empty_detail.status_code == 200
    empty_metrics = empty_detail.json()["metrics"]
    assert empty_metrics["pv"] == 0.0
    assert empty_metrics["cpi"] == 1.0

    client.post(f"/projects/{project_id}/activities", json=ACTIVITY_PAYLOAD)
    client.post(
        f"/projects/{project_id}/activities",
        json={
            "name": "Structure",
            "bac": 1000.0,
            "planned_progress": 0.5,
            "actual_progress": 0.5,
            "actual_cost": 500.0,
        },
    )

    detail = client.get(f"/projects/{project_id}")
    assert detail.status_code == 200
    metrics = detail.json()["metrics"]
    assert metrics["pv"] == 1000.0
    assert metrics["ev"] == 900.0
    assert metrics["cv"] == -100.0
    assert metrics["cpi"] == 0.9
    assert metrics["spi"] == 0.9
    assert metrics["status"]["cost"] == "Over Budget"
