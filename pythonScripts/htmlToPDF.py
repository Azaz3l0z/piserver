import os
import sys
import weasyprint


def htmlToPDF(html_path: str):
    html_path = html_path.replace('"', '')
    pdf_path = html_path.replace('.html', '.pdf')

    with open(html_path, 'r+') as file:
        html = file.read()
    os.remove(html_path)
    weasyprint.HTML(string=html.encode(
        'utf-8')).write_pdf(pdf_path)


if __name__ == '__main__':
    htmlToPDF(sys.argv[1])
