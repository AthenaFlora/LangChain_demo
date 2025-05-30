from abc import ABC, abstractmethod
from util.validate import Validate

class Template(ABC):
    def __init__(self, template_path:str):
        Validate.validate_file(template_path)
        with open(template_path, 'r') as f:
            self.template = f.read()
            self.replaced = None

    @abstractmethod
    def get_replaced_text(self) -> str | None:
        pass