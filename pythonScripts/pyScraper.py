import os
import sys
import json
import scrapeScout as scout
import scrapeMobileDE as mobile
import htmlToPDF as downloadPDF

from multiprocessing import Process


class SiteNotInDatabase(Exception):
    pass


if __name__ == "__main__":
    # Args
    url = sys.argv[1].replace('"', '')
    pdf_path = '../files'

    # Chdir
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.abspath(os.path.dirname(sys.executable)))
    elif __file__:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    os.chdir(os.path.dirname(os.getcwd()))

    pdf_path = os.path.join(os.getcwd(), 'files')

    ans = ''
    try:
        if 'mobile.de' in url:
            scrpr = mobile.Scraper(url)
            data = scrpr.scrape()
            pdf = scrpr.pdf(data['title'], pdf_path)

        elif 'autoscout24' in url:
            scrpr = scout.Scraper(url)
            data = scrpr.scrape()
            pdf = scrpr.pdf(data['title'], pdf_path)

        else:
            raise(SiteNotInDatabase)

        data['pdf'] = pdf

    except SiteNotInDatabase:
        print(json.dumps({'Response': 'Site Not Found'}))

    else:
        print(json.dumps(data, ensure_ascii=False))
