from locust import HttpUser, task, between


class RecruitmentUser(HttpUser):

    wait_time = between(1, 2)

    @task
    def login(self):
        self.client.post(
            "/login/",
            json={
                "username": "your_username",
                "password": "your_password"
            }
        )

    @task
    def job_list(self):
        self.client.get(
            "/jobs/",
            headers={
                "Authorization": "Bearer YOUR_ACCESS_TOKEN"
            }
        )