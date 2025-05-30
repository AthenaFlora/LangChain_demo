from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from application.selector.selector import Selector
from models.profile import Profile

class EducationSelector(Selector):
    def __init__(self, profile: Profile, temperature=0.0, model="gpt-3.5-turbo") -> None:
        super().__init__(temperature, model)
        self.detailed_education = profile.detailed_education
        self.simple_education = profile.simple_education
    
    def select_education(self, show_detailed_education)->str:
        if(show_detailed_education['show_ed_details']):
            return self.detailed_education
        else:
            return self.simple_education

    def create_chain(self):
        class EducationResponse(BaseModel):
            show_ed_details: bool = Field(description="Whether to show detailed education info")  
        parser = JsonOutputParser(pydantic_object=EducationResponse)
        prompt = PromptTemplate(
            template="""
            You are a helpful CV assistant.
            Based on the provided job description, determine if it falls in below categories:
            
            - Graduate positions value detailed education information like courses
            - Academic positions

            Job Description:
            {job_description}
            
            {format_instructions}
            
            Return only the JSON object with the boolean decision.
            """,
            input_variables=["job_description"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        postprocessor = RunnableLambda(self.select_education)
        return prompt | self.llm | parser | postprocessor