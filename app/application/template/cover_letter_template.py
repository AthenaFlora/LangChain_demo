from models.template.html_template import HtmlTemplate

class CoverletterTemplate(HtmlTemplate):
    def __init__(self, template_cover_letter_path:str) -> None:
        super().__init__(template_cover_letter_path)

    def overwrite_template(self, content, date):
        to_replace = self.template
        date_line = f'Date: {date}\n'
        to_replace = self.insert_end(to_replace=to_replace, div_id="contact-content", replace=date_line)
        self.replaced = self.replace_part( to_replace=to_replace, div_id="body-content", replace=content)
    
    def get_replaced_text(self) -> str | None:
        return self.replaced