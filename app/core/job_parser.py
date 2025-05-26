import requests
from bs4 import BeautifulSoup
from pathlib import Path
import yaml
import logging
from infras.embedding.embedding import EmbeddingFactory

logger = logging.getLogger(__name__)

class JobParser:
    def __init__(self, config_path: str = "app/config/settings.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize embedding service based on config
        service_type = self.config['embeddings'].get('service_type', 'local')
        model_name = self.config['embeddings']['models'].get(service_type)
        self.embedder = EmbeddingFactory.create_embedding_service(
            service_type=service_type,
            model_name=model_name
        )
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

    def get_embedding(self, text: str) -> list:
        """Generate embeddings for the text content."""
        try:
            return self.embedder.generate_embedding(text)
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