#this is locust file for load testing the API endpoints
#multiple users will be simulated to test the performance of the API
from locust import HttpUser, task, between
import random
import string

class PollsUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        username = "user_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        email = username + "@example.com"
        password = "123456789"

        self.client.post(
            "/api/register/",
            json={
                "username": username,
                "email": email,
                "password": password,
                "password2": password
            }
        )

        response = self.client.post(
            "/api/token/",
            json={"username": username, "password": password}
        )
        self.token = response.json()["access"]

    @task
    def get_questions(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/questions/", headers=headers)

    @task
    def get_choices(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/questions/1/choices/", headers=headers)
    
    @task
    def get_user_profile(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/api/profile/", headers=headers)
    
    @task
    def create_question(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.post(
            "/api/questions/",
            json={"text": "What is your favorite color?"},
            headers=headers
        )

# from locust import HttpUser, task, between

# class PollsUser(HttpUser):
#     wait_time = between(1, 3)
#     token = None

#     def on_start(self):
#         response = self.client.post(
#             "/api/token/",
#             json={"username": "rwrwz", "password": "123456789"}
#         )
#         self.token = response.json()["access"]

#     @task
#     def get_questions(self):
#         headers = {"Authorization": f"Bearer {self.token}"}
#         self.client.get("/api/questions/", headers=headers)

#     @task
#     def get_choices(self):
#         headers = {"Authorization": f"Bearer {self.token}"}
#         self.client.get("/api/questions/1/choices/", headers=headers)
