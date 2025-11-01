from random import randint
from locust import HttpUser, task, between


class TestAPIHealth(HttpUser):
    wait_time = between(0, 0.2)

    @task(1)  # task weight of 1
    def api_health(self):
        self.client.get("/api/health/", name="Health-Endpoint")

    @task(10)  # task weight of 10
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
