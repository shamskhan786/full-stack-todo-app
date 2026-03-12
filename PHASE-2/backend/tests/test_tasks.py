"""Tests for all task API endpoints (US1, US2, US3)."""

from uuid import uuid4

# Must match conftest.py values
TEST_USER_ID = "11111111-1111-1111-1111-111111111111"
OTHER_USER_ID = "22222222-2222-2222-2222-222222222222"

# ──────────────────────────────────────────────
# US1: Create and List Tasks
# ──────────────────────────────────────────────


class TestCreateTask:
    """T017: POST /api/{user_id}/tasks — success cases."""

    def test_create_task_success(self, client):
        response = client.post(
            f"/api/{TEST_USER_ID}/tasks",
            json={"title": "Buy groceries", "description": "Milk, eggs"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["success"] is True
        assert body["data"]["title"] == "Buy groceries"
        assert body["data"]["description"] == "Milk, eggs"
        assert body["data"]["is_completed"] is False
        assert body["data"]["completed_at"] is None
        assert body["data"]["user_id"] == TEST_USER_ID
        assert body["data"]["id"] is not None
        assert body["data"]["created_at"] is not None
        assert body["data"]["updated_at"] is not None

    def test_create_task_title_only(self, client):
        response = client.post(
            f"/api/{TEST_USER_ID}/tasks",
            json={"title": "Simple task"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["data"]["title"] == "Simple task"
        assert body["data"]["description"] is None


class TestCreateTaskValidation:
    """T018: POST validation — empty title, long title."""

    def test_create_task_empty_title(self, client):
        response = client.post(
            f"/api/{TEST_USER_ID}/tasks",
            json={"title": ""},
        )
        assert response.status_code == 422
        body = response.json()
        assert body["success"] is False
        assert body["code"] == "VALIDATION_ERROR"

    def test_create_task_missing_title(self, client):
        response = client.post(
            f"/api/{TEST_USER_ID}/tasks",
            json={"description": "no title"},
        )
        assert response.status_code == 422

    def test_create_task_title_too_long(self, client):
        response = client.post(
            f"/api/{TEST_USER_ID}/tasks",
            json={"title": "x" * 501},
        )
        assert response.status_code == 422


class TestListTasks:
    """T019: GET /api/{user_id}/tasks — list and isolation."""

    def test_list_tasks_empty(self, client):
        response = client.get(f"/api/{TEST_USER_ID}/tasks")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"] == []

    def test_list_tasks_returns_only_user_tasks(self, client):
        from src.dependencies import verify_jwt
        from src.main import app

        # Create tasks for main user
        client.post(f"/api/{TEST_USER_ID}/tasks", json={"title": "Task A"})
        client.post(f"/api/{TEST_USER_ID}/tasks", json={"title": "Task B"})

        # Switch to other user and create a task
        app.dependency_overrides[verify_jwt] = lambda: {"sub": OTHER_USER_ID}
        client.post(f"/api/{OTHER_USER_ID}/tasks", json={"title": "Other task"})

        # Switch back to main user and list tasks
        app.dependency_overrides[verify_jwt] = lambda: {"sub": TEST_USER_ID}
        response = client.get(f"/api/{TEST_USER_ID}/tasks")
        body = response.json()
        assert len(body["data"]) == 2
        titles = [t["title"] for t in body["data"]]
        assert "Task A" in titles
        assert "Task B" in titles
        assert "Other task" not in titles

    def test_list_tasks_user_id_mismatch(self, client):
        other_id = str(uuid4())
        response = client.get(f"/api/{other_id}/tasks")
        assert response.status_code == 403


class TestAuthFailure:
    """T020: Auth failure — no JWT returns 401."""

    def test_create_task_no_auth(self, client_no_auth):
        response = client_no_auth.post(
            f"/api/{TEST_USER_ID}/tasks",
            json={"title": "Should fail"},
        )
        assert response.status_code in (401, 403)

    def test_list_tasks_no_auth(self, client_no_auth):
        response = client_no_auth.get(f"/api/{TEST_USER_ID}/tasks")
        assert response.status_code in (401, 403)


# ──────────────────────────────────────────────
# US2: View, Update, and Delete a Single Task
# ──────────────────────────────────────────────


class TestGetSingleTask:
    """T023: GET /api/{user_id}/tasks/{id}."""

    def test_get_task_success(self, client):
        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks", json={"title": "Find me"}
        )
        task_id = create_resp.json()["data"]["id"]

        response = client.get(f"/api/{TEST_USER_ID}/tasks/{task_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["title"] == "Find me"
        assert body["data"]["id"] == task_id

    def test_get_task_not_found(self, client):
        fake_id = str(uuid4())
        response = client.get(f"/api/{TEST_USER_ID}/tasks/{fake_id}")
        assert response.status_code == 404

    def test_get_task_cross_user(self, client):
        from src.dependencies import verify_jwt
        from src.main import app

        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks", json={"title": "Private"}
        )
        task_id = create_resp.json()["data"]["id"]

        # Switch to other user
        app.dependency_overrides[verify_jwt] = lambda: {"sub": OTHER_USER_ID}
        response = client.get(
            f"/api/{OTHER_USER_ID}/tasks/{task_id}"
        )
        assert response.status_code == 404

        # Restore main user
        app.dependency_overrides[verify_jwt] = lambda: {"sub": TEST_USER_ID}


class TestUpdateTask:
    """T024: PUT /api/{user_id}/tasks/{id}."""

    def test_update_task_success(self, client):
        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks",
            json={"title": "Old title", "description": "Old desc"},
        )
        task_id = create_resp.json()["data"]["id"]

        response = client.put(
            f"/api/{TEST_USER_ID}/tasks/{task_id}",
            json={"title": "New title", "description": "New desc"},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["title"] == "New title"
        assert body["data"]["description"] == "New desc"

    def test_update_task_validation(self, client):
        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks", json={"title": "Valid"}
        )
        task_id = create_resp.json()["data"]["id"]

        response = client.put(
            f"/api/{TEST_USER_ID}/tasks/{task_id}",
            json={"title": ""},
        )
        assert response.status_code == 422

    def test_update_task_not_found(self, client):
        fake_id = str(uuid4())
        response = client.put(
            f"/api/{TEST_USER_ID}/tasks/{fake_id}",
            json={"title": "Nope"},
        )
        assert response.status_code == 404


class TestDeleteTask:
    """T025: DELETE /api/{user_id}/tasks/{id}."""

    def test_delete_task_success(self, client):
        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks", json={"title": "Delete me"}
        )
        task_id = create_resp.json()["data"]["id"]

        response = client.delete(f"/api/{TEST_USER_ID}/tasks/{task_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True

        # Verify deleted
        get_resp = client.get(f"/api/{TEST_USER_ID}/tasks/{task_id}")
        assert get_resp.status_code == 404

    def test_delete_task_not_found(self, client):
        fake_id = str(uuid4())
        response = client.delete(f"/api/{TEST_USER_ID}/tasks/{fake_id}")
        assert response.status_code == 404


# ──────────────────────────────────────────────
# US3: Mark Task as Complete
# ──────────────────────────────────────────────


class TestCompleteTask:
    """T029: PATCH /api/{user_id}/tasks/{id}/complete."""

    def test_complete_task_success(self, client):
        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks", json={"title": "Finish me"}
        )
        task_id = create_resp.json()["data"]["id"]

        response = client.patch(
            f"/api/{TEST_USER_ID}/tasks/{task_id}/complete"
        )
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["is_completed"] is True
        assert body["data"]["completed_at"] is not None

    def test_complete_task_idempotent(self, client):
        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks", json={"title": "Twice"}
        )
        task_id = create_resp.json()["data"]["id"]

        client.patch(f"/api/{TEST_USER_ID}/tasks/{task_id}/complete")
        response = client.patch(
            f"/api/{TEST_USER_ID}/tasks/{task_id}/complete"
        )
        assert response.status_code == 200
        assert response.json()["data"]["is_completed"] is True

    def test_complete_task_not_found(self, client):
        fake_id = str(uuid4())
        response = client.patch(
            f"/api/{TEST_USER_ID}/tasks/{fake_id}/complete"
        )
        assert response.status_code == 404

    def test_complete_task_cross_user(self, client):
        from src.dependencies import verify_jwt
        from src.main import app

        create_resp = client.post(
            f"/api/{TEST_USER_ID}/tasks", json={"title": "Mine"}
        )
        task_id = create_resp.json()["data"]["id"]

        # Switch to other user
        app.dependency_overrides[verify_jwt] = lambda: {"sub": OTHER_USER_ID}
        response = client.patch(
            f"/api/{OTHER_USER_ID}/tasks/{task_id}/complete"
        )
        assert response.status_code == 404

        # Restore main user
        app.dependency_overrides[verify_jwt] = lambda: {"sub": TEST_USER_ID}
