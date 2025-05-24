import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMInterface:
    def __init__(self, config_path: str = "app/config/settings.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # Verify API key is set
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.llm = ChatOpenAI(
            model=self.config["llm"]["model"],
            temperature=self.config["llm"]["temperature"],
            max_retries=3,
        )

    def generate_cv(
        self, profile_data: dict, job_data: dict, tone: str = "professional"
    ) -> str:
        """Generate a CV based on profile and job data."""
        try:
            tone_style = self.config["tone_styles"].get(tone, "professional")

            prompt = ChatPromptTemplate.from_template(
                """
            Create a professional CV based on the following information:

            Profile Information:
            {profile_content}

            Job Description:
            {job_content}

            Tone Style: {tone_style}

            Please format the CV in Markdown and ensure it highlights relevant experience 
            and skills that match the job requirements.
            """
            )

            formatted_prompt = prompt.format(
                profile_content=profile_data["raw_content"],
                job_content=job_data["raw_content"],
                tone_style=tone_style,
            )

            response = self.llm.predict(formatted_prompt)
            logger.info("Successfully generated CV")
            return response

        except Exception as e:
            logger.error(f"Error generating CV: {str(e)}")
            raise

    def generate_cover_letter(
        self, profile_data: dict, job_data: dict, tone: str = "professional"
    ) -> str:
        """Generate a cover letter based on profile and job data."""
        try:
            tone_style = self.config["tone_styles"].get(tone, "professional")

            prompt = ChatPromptTemplate.from_template(
                """
            Create a compelling cover letter based on the following information:

            Profile Information:
            {profile_content}

            Job Description:
            {job_content}

            Tone Style: {tone_style}

            Please write a personalized cover letter in Markdown format that connects 
            the candidate's experience with the job requirements and demonstrates enthusiasm 
            for the role.
            """
            )

            formatted_prompt = prompt.format(
                profile_content=profile_data["raw_content"],
                job_content=job_data["raw_content"],
                tone_style=tone_style,
            )

            response = self.llm.predict(formatted_prompt)
            logger.info("Successfully generated cover letter")
            return response

        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}")
            raise
