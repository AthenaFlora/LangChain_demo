from abc import ABC, abstractmethod
from infras.llm import LLM
from langchain_core.runnables import Runnable

class Selector(ABC):
    def __init__(self, temperature, model) -> None:
        self.llm = LLM.get_llm(temperature=temperature, model=model)

    @abstractmethod
    def create_chain(self) -> Runnable:
        pass