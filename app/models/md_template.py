from abc import ABC, abstractmethod
from util.validate import Validate

class MdTemplate(ABC):
    def __init__(self, template_path:str):
        Validate.validate_file(template_path)
        Validate.validate_md_format(template_path)
        with open(template_path, 'r') as f:
            self.template = f.read()
            self.replaced = None
    
    @staticmethod
    def replace_part(start: str, end: str, to_replace: str, replace: str) -> str:
        start_pos = to_replace.find(start)
        if start_pos == -1:
            raise Exception(f"Start marker '{start}' not found")

        end_pos = to_replace.find(end, start_pos + len(start))
        if end_pos == -1:
            raise Exception(f"End marker '{end}' not found")

        return (
            to_replace[:start_pos + len(start)] +
            replace +
            to_replace[end_pos:]
        )

    @staticmethod
    def insert_before(marker: str, to_replace: str, replace: str) -> str:
        pos = to_replace.find(marker)
        if pos == -1:
            raise Exception(f"Marker '{marker}' not found")
        return to_replace[:pos] + replace + to_replace[pos:]

    @staticmethod
    def get_next_line(known_line:str, content:str) -> str | None:
        lines = content.split('\n')
        try:
            idx = lines.index(known_line)
            return lines[idx + 1] if idx + 1 < len(lines) else None
        except ValueError:
            return None
    
    @abstractmethod
    def get_replaced_text(self) -> str | None:
        pass
            