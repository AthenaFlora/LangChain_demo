import requests
from bs4 import BeautifulSoup
from pathlib import Path
import yaml
import logging
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobParser:
    def __init__(self, config_path: str = "app/config/settings.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.embedder = SentenceTransformer(self.config['embeddings']['model'])
        self.jobs_dir = Path(self.config['paths']['jobs'])

    def parse_job_description(self, text: str) -> dict:
        """Parse raw job description text."""
        try:
            # Basic implementation - just create embeddings and store text
            parsed_job = {
                'raw_content': text,
                'embedding': self.get_embedding(text)
            }
            
            logger.info("Successfully parsed job description")
            return parsed_job
        
        except Exception as e:
            logger.error(f"Error parsing job description: {str(e)}")
            raise

    def scrape_linkedin_job(self, url: str) -> dict:
        """Scrape job description from LinkedIn URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # Note: This is a basic implementation and might need adjustment
            # based on LinkedIn's actual structure
            job_description = soup.find('div', {'class': 'description'})
            
            if job_description:
                return self.parse_job_description(job_description.text)
            else:
                raise ValueError("Could not find job description in LinkedIn page")
        
        except Exception as e:
            logger.error(f"Error scraping LinkedIn job: {str(e)}")
            raise

    def get_embedding(self, text: str) -> list:
        """Generate embeddings for the text content."""
        try:
            return self.embedder.encode(text).tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []

    def save_job(self, job_data: dict, filename: str):
        """Save job data to file."""
        try:
            job_path = self.jobs_dir / filename
            with open(job_path, 'w', encoding='utf-8') as f:
                yaml.dump(job_data, f)
            logger.info(f"Successfully saved job data to {filename}")
        except Exception as e:
            logger.error(f"Error saving job data: {str(e)}")
            raise 