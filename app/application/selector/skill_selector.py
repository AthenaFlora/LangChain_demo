from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from application.selector.selector import Selector
from models.profile import Profile
from typing import List

class SkillSelector(Selector):
    def __init__(self, profile: Profile, temperature=0.0, model="gpt-3.5-turbo") -> None:
        super().__init__(temperature,model)
        self.skills = profile.skills

    def create_chain(self):
        class Skills(BaseModel):
            skills : List[str] = Field(description="List of skills")
        parser = JsonOutputParser(pydantic_object=Skills)
        prompt = PromptTemplate(
            template="""
            You are a helpful CV assistant.
            Based on the provided job description and skills list, identify and prioritize 8-10 relevant skills. Just include skills in skills list.

            Job Description:
            {job_description}

            Skills:
            {skills}

            {format_instructions}

            Return only the JSON object containing the prioritized skill list.
            """,
            input_variables=["job_description"],
            partial_variables={"format_instructions": parser.get_format_instructions(), "skills": self.skills}
        )
        return prompt | self.llm | parser