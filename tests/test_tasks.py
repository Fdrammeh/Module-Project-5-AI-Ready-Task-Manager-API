# project/starter/tests/test_tasks.py
# Module 5 Project — Example test (starter)

def test_health_check(client):
    """Health check returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"



# TODO: Add more tests:
# - test_register_user
def test_register_user(client):
    response = client.post(
        "/register",
        json={
            "username": "Mira",
            "email": "mira@email.com",
            "password":"summer2026"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "Mira"
    assert data["email"] == "mira@email.com"

    #password should not be returned
    assert "password" not in data
    assert "hashed_password" not in data


# - test_login

def test_login(client):
    client.post(
        "/register",
        json={
            "username": "taskuser",
            "email": "taskuser@example.com",
            "password": "password123"
        }
    )
    response = client.post(
        "/token",
        data={
            "username": "taskuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


# - test_create_task_authenticated
def test_create_task_authenticated(client):
    #Register a user
    client.post(
        "/register",
        json={
            "username":"taskuser",
            "email": "taskuser@example.com",
            "password": "password123"
        }
    )
    #log in to get the JWT
    login_response = client.post(
        "/token",
        data={
            "username": "taskuser",
            "password": "password123"
        }
    )


    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/tasks/",
        json={
            "title": "Complete FastAPI assignment",
            "description": "Finish the authentication tests",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200 or response.status_code == 201

    data = response.json()

    assert data["title"] == "Complete FastAPI assignment"
    assert data["description"] == "Finish the authentication tests"
    assert data["completed"] is False

# - test_list_tasks_scoped_to_user
def test_list_tasks_scoped_to_user(client):
    """Users can only see their own tasks."""
#create user 1
    client.post(
        "/register",
        json={
            "username": "user1",
            "email": "user1@example.com",
            "password": "password123"
        }
    )
#log in user 1
    login1 = client.post(
        "/token",
        data={
            "username": "user1",
            "password": "password123"
        }
    )

    token1 = login1.json()["access_token"]

    #user 1 creates a task
    client.post(
        "/tasks/",
        json={
            "title": "User 1 Task",
            "description": "This belongs to User 1",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {token1}"
        }
    )

#create user 2
    client.post(
        "/register",
        json={
            "username": "user2",
            "email": "user2@example.com",
            "password": "password123"
        }
    )

#login user 2
    login2 = client.post(
        "/token",
        data={
            "username": "user2",
            "password": "password123"
        }
    )

    token2 = login2.json()["access_token"]
#user 2 creates a task
    client.post(
        "/tasks/",
        json={
            "title": "User 2 Task",
            "description": "This belongs to User 2",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {token2}"
        }
    )

#User 1 lists their task
    response = client.get(
        "/tasks/",
        headers={
            "Authorization": f"Bearer {token1}"
        }
    )

    assert response.status_code == 200

    tasks = response.json()

    # User 1 should see their own task
    assert len(tasks) == 1
    assert tasks[0]["title"] == "User 1 Task"

    # User 1 should NOT see User 2's task
    assert tasks[0]["title"] != "User 2 Task"

# - test_get_task_suggest

def test_get_task_suggest(client):
    """Authenticated user can get a suggestion for their task."""

    # Register a user
    client.post(
        "/register",
        json={
            "username": "suggestuser",
            "email": "suggest@example.com",
            "password": "password123"
        }
    )

    # Log in
    login_response = client.post(
        "/token",
        data={
            "username": "suggestuser",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Create a task
    task_response = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "description": "Practice authentication",
            "completed": False
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert task_response.status_code in [200, 201]

    task = task_response.json()
    task_id = task["id"]

    # Get the AI suggestion
    response = client.get(
        f"/tasks/{task_id}/suggest",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["task_id"] == task_id
    assert "suggestion" in data
