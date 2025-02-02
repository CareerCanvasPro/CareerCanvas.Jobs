from locust import HttpUser, task, between

class JobAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_jobs(self):
        self.client.get("/api/v1/jobs", 
            params={"page": 1, "limit": 10}
        )
    
    @task(1)
    def search_jobs(self):
        self.client.get("/api/v1/jobs", 
            params={
                "keyword": "python",
                "location": "Remote",
                "job_type": "FULL_TIME"
            }
        )
    
    @task(2)
    def get_job_details(self):
        self.client.get(f"/api/v1/jobs/{self.random_job_id()}")
    
    def random_job_id(self):
        return self.client.get("/api/v1/jobs").json()["items"][0]["id"]