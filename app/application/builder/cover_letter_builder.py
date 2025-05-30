from application.selector.cover_letter_selector import CoverLetterSelector
from application.template.cover_letter_template import CoverletterTemplate
from models.context import Context
from models.job import Job
from util.printer import PdfPrinter
from util.validate import Validate

class CoverLetterBuilder:
    def __init__(self, cv:str, 
                 job: Job, 
                 context: Context, 
                 selector: CoverLetterSelector = CoverLetterSelector(option="classic"), 
                 template = CoverletterTemplate("app/data/templates/cover_letter_template.html")) -> None:
        self.cv = cv
        self.job = job
        self.selector = selector
        self.template = template
        self.context = context

    def create_cover_letter(self):
        chain = self.selector.create_chain()
        input = {
            "job_description": self.job.description,
            "cv": self.cv,
        }
        self.content = chain.invoke(input)
        self.template.overwrite_template(self.content, self.context.today)

    def export_pdf(self):
        replaced = self.template.get_replaced_text()
        if replaced is None:
            raise Exception("Cover letter is not created yet, call <create_cover_letter> first")
       
        cover_letter_file = "app/data/output/" + Validate.sanitize_filename(f"cover_letter_{self.job.company}_{self.job.title}_{self.context.today}.pdf").lower()
        PdfPrinter.export_html_to_pdf(replaced, cover_letter_file)
        return cover_letter_file