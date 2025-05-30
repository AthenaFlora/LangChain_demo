from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from application.selector.selector import Selector

class CoverLetterSelector(Selector):
    def __init__(self, word_limit:int=250, temperature=0.0, model="gpt-3.5-turbo", option = "classic") -> None:
        super().__init__(temperature,model)
        self.word_limit = word_limit
        if option == "classic":
            self.cover_letter_style = "generate a cover letter as part of the job application. The cover letter should not contain any contact information (to or from) and only contain salutations and a body of four to five information dense lines using business causal language."
        elif option == "modern":
            self.cover_letter_style = """generate a message answering the question "Tell us about yourself?" as part of the job application. You should begin the message simply with "Hi, I'm <my name>, <a short tagline created for me>" and follow it up with one short information dense paragraph using business causal language."""
        else:
            raise ValueError(f'{option} shoulb be classic or modern')
        
    def create_chain(self):
        prompt = PromptTemplate(
            template="""
            You are a helpful CV assistant.
            Based on the provided job description and Resume, {cover_letter_style} You should highlight any overlap of technology, responsibility or domain present between the job listing and my experience while mentioning why I would be a good fit for the given role. You should use optimistic and affirmative language and end the message with a call to action. Be concise. keep word count within {word_limit}.
            ------------        
            Job Description:
            {job_description}
            ------------        
            Resume:
            {cv}
            ------------
            Excluding the salutation (e.g., ‘Dear Hiring Team’) and closing signature (e.g., ‘Best regards, [Name]’). Return only the main body content.
            """,
            
            input_variables=["job_description","cv"],
            partial_variables = {"word_limit" : self.word_limit, "cover_letter_style": self.cover_letter_style}
        )
        return prompt | self.llm | StrOutputParser()