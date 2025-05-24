from pathlib import Path
import markdown
from sentence_transformers import SentenceTransformer
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfileLoader:
    def __init__(self, config_path: str = "app/config/settings.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.embedder = SentenceTransformer(self.config['embeddings']['model'])
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
            return self.embedder.encode(text).tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []

    def list_profiles(self) -> list:
        """List all available profile files."""
        return [f.name for f in self.profiles_dir.glob("*.md")] 