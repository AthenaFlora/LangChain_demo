from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from application.selector.selector import Selector

class RelevantSelector(Selector):
    def __init__(self, exclude_criterias:str = '''German for communication \n Programming language is C/C++ \n Frontend \n JavaScript''',
                 temperature=0.0, 
                 model="gpt-3.5-turbo") -> None:
        super().__init__(temperature, model)
        self.exclude_criterias = exclude_criterias

    def create_chain(self):
        class RelevantResponse(BaseModel):
            is_relevant: bool = Field(description="Whether relevant")  
        parser = JsonOutputParser(pydantic_object=RelevantResponse)
        prompt = PromptTemplate(
            template="""
            Job filter agent: Given a job description and exclusion criteria, return True if the job is relevant, otherwise False.
            
            Job Description:
            {job_description}

            Exclusion criteria:
            {exclude_criterias}
            
            {format_instructions}

            Return only the JSON object with the boolean decision.
            """,
            input_variables=["job_description"],
            partial_variables={"format_instructions": parser.get_format_instructions(),
                               "exclude_criterias": self.exclude_criterias}
        )
        return prompt | self.llm | parser 