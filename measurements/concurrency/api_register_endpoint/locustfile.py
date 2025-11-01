from random import randint
from locust import HttpUser, task, between


class TestAPIRegister(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def user_registration(self):
        id = randint(1, 1000000000)
        self.client.post(
            "/api/users/register/",
            json={
                "username": f"test-user-{id}",
                "password": f"test-password-{id}",
                "email": f"test-user-{id}@example.com"
            },
            name="Registration-Endpoint"
        )
