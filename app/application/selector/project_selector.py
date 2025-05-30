from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from application.selector.selector import Selector
from models.profile import Profile
from typing import List

class ProjectSelector(Selector):
    def __init__(self, profile: Profile, temperature=0.0, model="gpt-3.5-turbo") -> None:
        super().__init__(temperature, model)
        self.projects = profile.projects

    def create_chain(self):
        class Projects(BaseModel):
            projects: List[str] = Field(description="List of project lines")
        parser = JsonOutputParser(pydantic_object=Projects)
        
        prompt = PromptTemplate(
            template="""
            You are a helpful CV assistant.
            Based on the provided job description, select 1-3 most relevant projects from the given projects list. 
            Notice, projects can be duplicated, for the same project, choose the most relevant one.
            Return the complete project lines. 

            Job Description:
            {job_description}

            Projects:
            {projects}

            {format_instructions}

            Return only the JSON object containing the complete project lines.

            Sample output format:
            {{"projects": [
                "**Hydesign Backend Service** Developed and maintained the backend for a browser-based 3D CAD platform.",
                "**AWS Infrastructure for Hydesign** Implemented cloud infrastructures for the 3D design platform."
            ]}}
            """,
            input_variables=["job_description"],
            partial_variables={"format_instructions": parser.get_format_instructions(),"projects":self.projects}
        )
        return prompt | self.llm | parser