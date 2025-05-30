from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from application.selector.selector import Selector

class SummaryCreator(Selector):
    def __init__(self, word_limit:int=70, temperature=0.0, model="gpt-3.5-turbo") -> None:
        super().__init__(temperature,model)
        self.word_limit = word_limit

    def create_chain(self):
        prompt = PromptTemplate(
            template="""
            You are a helpful CV assistant.
            Based on the provided job description and profile, create a summary within {word_limit} words.
            
            Job Description:
            {job_description}
            
            profile:
            {selected_profile}

            Just reture summary text.
            """,
            input_variables=["job_description","selected_profile"],
            partial_variables = {"word_limit" : self.word_limit}
        )
        return prompt | self.llm | StrOutputParser()