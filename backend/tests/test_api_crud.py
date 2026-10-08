from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.activity import Activity

PROJECT_PAYLOAD = {"name": "Alpha", "description": "Demo project"}
ACTIVITY_PAYLOAD = {
    "name": "Foundation",
    "bac": 1000.0,
    "planned_progress": 0.5,
    "actual_progress": 0.4,
    "actual_cost": 500.0,
}


def test_create_and_list_projects(client):
    created = client.post("/projects", json=PROJECT_PAYLOAD)
    assert created.status_code == 201
    body = created.json()
    assert body["name"] == "Alpha"
    assert body["id"]

    listed = client.get("/projects")
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_get_update_and_delete_project(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]

    fetched = client.get(f"/projects/{project_id}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Alpha"

    updated = client.put(
        f"/projects/{project_id}",
        json={"name": "Beta", "description": "Updated"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Beta"

    deleted = client.delete(f"/projects/{project_id}")
    assert deleted.status_code == 204
    assert client.get(f"/projects/{project_id}").status_code == 404


def test_project_not_found(client):
    missing = uuid4()
    assert client.get(f"/projects/{missing}").status_code == 404
    assert (
        client.put(
            f"/projects/{missing}",
            json=PROJECT_PAYLOAD,
        ).status_code
        == 404
    )
    assert client.delete(f"/projects/{missing}").status_code == 404


def test_create_list_update_and_delete_activity(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]

    created = client.post(
        f"/projects/{project_id}/activities",
        json=ACTIVITY_PAYLOAD,
    )
    assert created.status_code == 201
    activity = created.json()
    assert activity["project_id"] == project_id
    activity_id = activity["id"]

    listed = client.get(f"/projects/{project_id}/activities")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.put(
        f"/activities/{activity_id}",
        json={**ACTIVITY_PAYLOAD, "name": "Structure", "actual_progress": 0.6},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Structure"
    assert updated.json()["actual_progress"] == 0.6

    deleted = client.delete(f"/activities/{activity_id}")
    assert deleted.status_code == 204
    assert client.get(f"/projects/{project_id}/activities").json() == []


def test_list_activities_returns_404_when_project_missing(client):
    response = client.get(f"/projects/{uuid4()}/activities")
    assert response.status_code == 404
    assert response.json()["detail"] == "Proyecto no encontrado"


def test_create_activity_returns_404_when_project_missing(client):
    response = client.post(
        f"/projects/{uuid4()}/activities",
        json=ACTIVITY_PAYLOAD,
    )
    assert response.status_code == 404


def test_activity_not_found(client):
    missing = uuid4()
    assert (
        client.put(
            f"/activities/{missing}",
            json=ACTIVITY_PAYLOAD,
        ).status_code
        == 404
    )
    assert client.delete(f"/activities/{missing}").status_code == 404


def test_activity_progress_validation(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    response = client.post(
        f"/projects/{project_id}/activities",
        json={**ACTIVITY_PAYLOAD, "planned_progress": 1.5},
    )
    assert response.status_code == 422


def test_delete_project_removes_activities(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    activity_id = client.post(
        f"/projects/{project_id}/activities",
        json=ACTIVITY_PAYLOAD,
    ).json()["id"]

    assert client.delete(f"/projects/{project_id}").status_code == 204
    assert client.get(f"/projects/{project_id}/activities").status_code == 404
    assert (
        client.put(
            f"/activities/{activity_id}",
            json=ACTIVITY_PAYLOAD,
        ).status_code
        == 404
    )


def test_sqlite_rejects_activity_without_project(db_session):
    orphan = Activity(
        name="Orphan",
        bac=100.0,
        planned_progress=0.1,
        actual_progress=0.1,
        actual_cost=10.0,
        project_id=uuid4(),
    )
    db_session.add(orphan)
    with pytest.raises(IntegrityError):
        db_session.commit()
