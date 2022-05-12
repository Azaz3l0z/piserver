import os
import sys
import weasyprint


def htmlToPDF(html_path: str, pdf_path: str):
    with open(html_path, 'r+') as file:
        html = file.read()
    os.remove(html_path)
    weasyprint.HTML(string=html.encode(
        'utf-8')).write_pdf(pdf_path)
