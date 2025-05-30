import logging
from pathlib import Path
from dotenv import load_dotenv
import asyncio

from application.builder.cv_builder import CvBuilder
from application.selector.education_selector import EducationSelector
from application.selector.experience_selector import ExperienceSelector
from application.selector.project_selector import ProjectSelector
from application.selector.relevant_selector import RelevantSelector
from application.selector.skill_selector import SkillSelector
from application.selector.summary_selector import SummaryCreator
from models.profile import Profile
from core.job_fetch import JobFetchFactory 
from models.context import Context

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Generator:
    def __init__(self, job_source, job_source_type):
        self.job_fetch = JobFetchFactory.create_job_fetch_service("linkedln")
        self.output_dir = Path("app/data/output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.job_fetch_service = JobFetchFactory.create_job_fetch_service("linkedln")
        self.job = self.job_fetch_service.get_job(content=job_source, content_type=job_source_type)

    async def generate_documents(self):
        """
        Generate CV and cover letter based on profile and job description.
        """
        try:
            is_relevant = RelevantSelector().create_chain().invoke({"job_description":self.job.description})
            
            context = Context()
            if is_relevant:
                await self._generate_cv(context)

        except Exception as e:
            logger.error(f"Error generating documents: {str(e)}")
            raise
        
    async def _generate_cv(self, context):
        profile = Profile("app/data/profiles/my_profile.json")
        selectors = [SummaryCreator(), SkillSelector(profile), ExperienceSelector(profile), ProjectSelector(profile), EducationSelector(profile)]
        cv_builder = CvBuilder( job = self.job, selectors= selectors, context=context)
        await cv_builder.create_cv_content()
        output_cv = cv_builder.export_cv_md()
        logger.info(f"Generated documents saved to {output_cv}")

async def main():
    try:
        generator = Generator(job_source='https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3733041803', job_source_type='url')
        await generator.generate_documents()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
