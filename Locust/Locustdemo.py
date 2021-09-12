from locust import HttpUser, TaskSet, task, User

class WebsiteTasks(HttpUser):
    def on_start(self):
        print("start locust")


class WebsiteUser(HttpUser):
    task_set = WebsiteTasks
    host = "https://debugtalk.com"
    min_wait = 1000
    max_wait = 5000