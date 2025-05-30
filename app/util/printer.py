import logging
import pdfkit
from pathlib import Path

logger = logging.getLogger(__name__)
class PdfPrinter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def export_html_to_pdf(html_file: str, output_pdf_path: str):
        """
        Converts an HTML file to a PDF using pdfkit + wkhtmltopdf.
        
        :param html_file: Input HTML file.
        :param output_pdf_path: Path to save the resulting PDF.
        """
        try:
            pdfkit.from_string(html_file, output_pdf_path)
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")