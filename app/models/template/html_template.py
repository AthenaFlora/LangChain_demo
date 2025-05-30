from bs4 import BeautifulSoup, Tag
from models.template.template import Template
from util.validate import Validate
class HtmlTemplate(Template):
    def __init__(self, template_path:str):
        Validate.validate_extension(template_path, ".html")
        super().__init__(template_path=template_path)

    @staticmethod
    def replace_part(to_replace: str, div_id: str, replace: str) -> str:
        """
        Replaces the inner HTML of a <div> with the given ID.
        """
        soup = BeautifulSoup(to_replace, 'html.parser')
        target_div = soup.find('div', id=div_id)

        if not isinstance(target_div, Tag):
            raise ValueError(f"Could not find a valid <div> with id='{div_id}'.")

        # Convert paragraphs from plain text (\n\n) to <p>...</p>
        paragraphs = [p.strip() for p in replace.strip().split('\n\n') if p.strip()]
        for para in paragraphs:
            p_tag = soup.new_tag("p")
            p_tag.string = para
            target_div.append(p_tag)

        return str(soup)
    
    @staticmethod
    def insert_end(to_replace: str, div_id: str, replace: str) -> str:
        """
        Inserts the 'replace' HTML string just before the closing </div> of the div with the given ID.
        """
        soup = BeautifulSoup(to_replace, 'html.parser')
        target_div = soup.find('div', id=div_id)

        if not isinstance(target_div, Tag):
            raise ValueError(f"Could not find a valid <div> with id='{div_id}'.")

        # Parse the replacement content
        new_content = BeautifulSoup(replace, 'html.parser')
        
        # Insert each element at the end of the div
        for element in new_content.contents:
            target_div.append(element)

        return str(soup)


    def get_replaced_text(self) -> str | None:
        return self.replaced