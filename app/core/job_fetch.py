from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import logging
import re
from models.job import Job

logger = logging.getLogger(__name__)

class JobFetchService(ABC):
    @abstractmethod
    def get_job(self, content: str, content_type : str) -> Job:
        pass

class LinkedlnJobFetchService(JobFetchService):
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.job_posting_path = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting"
    
    def get_job(self, content: str, content_type : str) -> Job:
        self._set_job_url(content, content_type)
        return self._get_job_info()
    
    def _set_job_url(self, content: str, content_type : str):
        if content_type == 'url' or "url":
            self.job_id = self._extract_job_id(content)
        elif content_type == 'id' or "id":
            self.job_id = content
        else:
            raise ValueError(f"Unknown content type {content}")
        self.job_url = f"{self.job_posting_path}/{self.job_id}"

    def _extract_job_id(self, url) -> str:
        match = re.search(r"currentJobId=(\d+)", url)
        if match:
            return match.group(1)
        else:
            raise ValueError(f"Could not extract job id from {url}")

    def _expand_job_description(self, soup) -> str:
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
            raise ValueError(f"Could not fetch job description from {self.job_url}")
        return job_description
    
    def _get_job_info(self) -> Job:        
        response = requests.get(self.job_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        description = self._expand_job_description(soup)
        
        title_tag = soup.find("h2", class_="topcard__title")
        company_tag = soup.find("a", class_="topcard__org-name-link")
        company_alt_tag = soup.find("span", class_="topcard__flavor")
        post_date_tag = soup.find("span", class_="posted-time-ago__text")

        title = title_tag.get_text(strip=True) if title_tag else None

        # Prefer company_tag if available, else fallback to company_alt_tag
        if company_tag:
            company = company_tag.get_text(strip=True)
        elif company_alt_tag:
            company = company_alt_tag.get_text(strip=True)
        else:
            company = None

        post_date = post_date_tag.get_text(strip=True) if post_date_tag else None

        return Job({
            "url": self.job_url,
            "id": self.job_id,
            "title": title,
            "company": company,
            "post_date": post_date,
            "description": description
        })

class JobFetchFactory:
    @staticmethod
    def create_job_fetch_service( provider : str ) -> JobFetchService:
        if provider == "linkedln" :
            return LinkedlnJobFetchService()
        else:
            raise ValueError(f"Unknown provider type: {provider}")
            

