from locust import HttpUser, task, between


class RecruitmentUser(HttpUser):

    wait_time = between(1, 2)

    @task
    def login(self):
        self.client.post(
            "/login/",
            json={
                "username": "Rayana121",
                "password": "password1234"
            }
        )

    @task
    def job_list(self):
        self.client.get(
            "/jobs/",
            headers={
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg1MzIyNDc1LCJpYXQiOjE3ODUzMjE1NzUsImp0aSI6ImVmZTdjY2I1ZDY1YzQwN2NhNjVlYmMzNzlmMTg0NTNlIiwidXNlcl9pZCI6IjUifQ.KVG2o6F6q3UlEXf_VEssefT6sQGoS1x8tyOpbac0380"
            }
        )