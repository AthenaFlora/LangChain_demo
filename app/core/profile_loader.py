from pathlib import Path
import markdown
import yaml
import logging
from infras.embedding.embedding import EmbeddingFactory

logger = logging.getLogger(__name__)

class ProfileLoader:
    def __init__(self, config_path: str = "app/config/settings.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize embedding service based on config
        service_type = self.config['embeddings'].get('service_type', 'openai')
        model_name = self.config['embeddings']['models'].get(service_type)
        self.embedder = EmbeddingFactory.create_embedding_service(
            service_type=service_type,
            model_name=model_name
        )
        self.profiles_dir = Path(self.config['paths']['profiles'])

    def load_profile(self, filename: str) -> dict:
        """Load and parse a markdown profile file."""
        try:
            profile_path = self.profiles_dir / filename
            with open(profile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert markdown to HTML then to text
            html = markdown.markdown(content)
            
            # Extract sections (basic implementation)
            sections = {
                'raw_content': content,
                'html_content': html,
                'embedding': self.get_embedding(content)
            }
            
            logger.info(f"Successfully loaded profile: {filename}")
            return sections
        
        except Exception as e:
            logger.error(f"Error loading profile {filename}: {str(e)}")
            raise

    def get_embedding(self, text: str) -> list:
        """Generate embeddings for the text content."""
        try:
            return self.embedder.generate_embedding(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []

    def list_profiles(self) -> list:
        """List all available profile files."""
        return [f.name for f in self.profiles_dir.glob("*.md")]