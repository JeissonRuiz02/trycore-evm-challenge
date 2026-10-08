from app.main import app

PROJECT_PAYLOAD = {"name": "Alpha", "description": "Demo"}
ACTIVITY_PAYLOAD = {
    "name": "Foundation",
    "bac": 1000.0,
    "planned_progress": 0.5,
    "actual_progress": 0.4,
    "actual_cost": 500.0,
}


def test_openapi_docs_are_published(client):
    swagger = client.get("/swagger-ui")
    assert swagger.status_code == 200
    redirect = client.get("/api-docs", follow_redirects=False)
    assert redirect.status_code in {307, 302}
    assert client.get("/openapi.json").status_code == 200
    paths = app.openapi()["paths"]
    assert "/projects" in paths
    assert "/projects/{project_id}" in paths
    assert "/projects/{project_id}/activities" in paths
    assert "/activities/{activity_id}" in paths


def test_post_projects(client):
    response = client.post("/projects", json=PROJECT_PAYLOAD)
    assert response.status_code == 201
    assert response.json()["name"] == "Alpha"


def test_get_projects(client):
    client.post("/projects", json=PROJECT_PAYLOAD)
    response = client.get("/projects")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_project_by_id(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert "metrics" in response.json()


def test_put_project(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    response = client.put(
        f"/projects/{project_id}",
        json={"name": "Beta", "description": None},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Beta"


def test_delete_project(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 204


def test_post_activity(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    response = client.post(
        f"/projects/{project_id}/activities",
        json=ACTIVITY_PAYLOAD,
    )
    assert response.status_code == 201
    assert "metrics" in response.json()


def test_get_activities(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    client.post(f"/projects/{project_id}/activities", json=ACTIVITY_PAYLOAD)
    response = client.get(f"/projects/{project_id}/activities")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_put_activity(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    activity_id = client.post(
        f"/projects/{project_id}/activities",
        json=ACTIVITY_PAYLOAD,
    ).json()["id"]
    response = client.put(
        f"/activities/{activity_id}",
        json={**ACTIVITY_PAYLOAD, "actual_progress": 0.5},
    )
    assert response.status_code == 200
    assert response.json()["actual_progress"] == 0.5


def test_delete_activity(client):
    project_id = client.post("/projects", json=PROJECT_PAYLOAD).json()["id"]
    activity_id = client.post(
        f"/projects/{project_id}/activities",
        json=ACTIVITY_PAYLOAD,
    ).json()["id"]
    response = client.delete(f"/activities/{activity_id}")
    assert response.status_code == 204
    assert client.get(f"/projects/{project_id}/activities").json() == []
