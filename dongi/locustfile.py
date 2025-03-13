from locust import HttpUser, task, between

class DjangoLoadTest(HttpUser):
    # wait_time = between(1, 2)

    @task(1)
    def load_home_page(self):
        self.client.get("/api/v1/apps/users/")