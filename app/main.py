import logging
import os
from pathlib import Path

from core.job_parser import JobParser
from core.llm_interface import LLMInterface
from core.profile_loader import ProfileLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CVGenerator:
    def __init__(self):
        self.profile_loader = ProfileLoader()
        self.job_parser = JobParser()
        self.llm_interface = LLMInterface()

        # Ensure output directory exists
        self.output_dir = Path("app/data/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_documents(
        self,
        profile_file: str,
        job_description: str,
        tone: str = "professional",
        is_job_url: bool = False,
    ) -> tuple:
        """
        Generate CV and cover letter based on profile and job description.

        Args:
            profile_file (str): Name of the profile markdown file
            job_description (str): Job description text or LinkedIn URL
            tone (str): Tone style for generation (original/precise/professional)
            is_job_url (bool): Whether job_description is a LinkedIn URL

        Returns:
            tuple: (cv_path, cover_letter_path)
        """
        try:
            # Load profile
            profile_data = self.profile_loader.load_profile(profile_file)

            # Parse job description
            if is_job_url:
                job_data = self.job_parser.scrape_linkedin_job(job_description)
            else:
                job_data = self.job_parser.parse_job_description(job_description)

            # Generate documents
            cv_content = self.llm_interface.generate_cv(profile_data, job_data, tone)
            cover_letter_content = self.llm_interface.generate_cover_letter(
                profile_data, job_data, tone
            )

            # Save documents
            timestamp = Path(profile_file).stem
            cv_path = self.output_dir / f"cv_{timestamp}.md"
            cover_letter_path = self.output_dir / f"cover_letter_{timestamp}.md"

            cv_path.write_text(cv_content)
            cover_letter_path.write_text(cover_letter_content)

            logger.info(f"Generated documents saved to {self.output_dir}")
            return str(cv_path), str(cover_letter_path)

        except Exception as e:
            logger.error(f"Error generating documents: {str(e)}")
            raise


def main():
    """Example usage of the CV Generator."""
    try:
        generator = CVGenerator()

        # Example profile and job description
        profile_file = "example_profile.md"
        job_description = """
        Software Engineer Position
        Requirements:
        - 3+ years of Python development
        - Experience with AI/ML
        - Strong communication skills
        """

        cv_path, cover_letter_path = generator.generate_documents(
            profile_file=profile_file,
            job_description=job_description,
            tone="professional",
        )

        print(f"Generated CV: {cv_path}")
        print(f"Generated Cover Letter: {cover_letter_path}")

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
