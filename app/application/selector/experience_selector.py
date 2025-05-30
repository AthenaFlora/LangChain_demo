from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from application.selector.selector import Selector
from models.profile import Profile
from typing import Dict, List

class ExperienceSelector(Selector):
    def __init__(self, profile: Profile, temperature=0.0, model="gpt-3.5-turbo") -> None:
        super().__init__(temperature, model)
        self.experience_list = profile.experience

    def create_chain(self):
        class WorkExperienceGroup(BaseModel):
            """Grouped work experiences by category"""
            experiences: Dict[str, List[str]] = Field(
                description="Dictionary where keys are experience categories and values are lists of specific experiences"
            )
        parser = JsonOutputParser(pydantic_object=WorkExperienceGroup)
        prompt = PromptTemplate(
            template="""
            You are an helpful cv tailor.
            Given the following work experiences and job description, select 6-10 most relevant experiences and
            group them into 2-5 meaningful categories.

            Common categories include but are not limited to:
            - Software Development
            - Testing and CI/CD
            - Backend Development
            - Database Management
            - Cloud Technologies
            - Team Collaboration

            Job Description:
            {job_description}

            Work Experience:
            {experience_list}

            {format_instructions}

            Return only the JSON object with grouped experiences.
            """,
            input_variables=["job_description"],
            partial_variables={"format_instructions": parser.get_format_instructions(), "experience_list" : self.experience_list}
        )
        return prompt | self.llm | parser