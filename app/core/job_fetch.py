from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)

class JobFetchService(ABC):
    @abstractmethod
    def get_job_description(self, content: str, content_type : str) -> str:
        pass

class LinkedlnJobFetchService(JobFetchService):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.job_posting_path = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting"
    
    def get_job_description(self, content: str, content_type : str) -> str:
        if content_type == "url":
            job_id = self.extract_job_id
            return self.expand_job_description(job_id)
        elif content_type == "id":
            return content
        else:
            raise ValueError(f"Unknown content type {content}")
    
    def extract_job_id(self, url) -> str:
        match = re.search(r"currentJobId=(\d+)", url)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Could not extract job id from {url}")

    def expand_job_description(self, job_id) -> str:
        job_url = f"{self.job_posting_path}/{job_id}"

        response = requests.get(job_url, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # Get all description sections
        description_sections = soup.select(".show-more-less-html__markup")

        job_description = None
        for section in description_sections:
            # Filter out the collapsed one
            classes = section.get("class")
            if isinstance(classes, list) and "clamp-after" not in classes:
                job_description = section.get_text(separator="\n").strip()
                break

        if job_description is None:
            raise ValueError(f"Could not fetch job description from {job_url}")
        return job_description

class JobFetchFactory:
    @staticmethod
    def create_job_fetch_service( provider : str ) -> JobFetchService:
        if provider == "linkedln" :
            return LinkedlnJobFetchService()
        else:
            raise ValueError(f"Unknown provider type: {provider}")
            

