from langchain_openai import ChatOpenAI
class LLM:
    @ staticmethod
    # def get_llm(model:str = "gpt-3.5-turbo", temperature : float = 0.0):
    def get_llm(model:str = "gpt-4.1", temperature : float = 0.0):
        llm = ChatOpenAI(temperature=temperature, model=model)
        return llm  