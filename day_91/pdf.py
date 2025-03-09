from PyPDF2 import PdfReader
import logging

# Detailed logging for the requests library for troubleshooting
logging.basicConfig(level=logging.DEBUG)

def extract_text_from_pdf(pdf_file):
    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PdfReader(file)

            # Extract text from each page
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

        return text

    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""