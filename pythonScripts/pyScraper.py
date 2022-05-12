import os
import sys
import json
import scrapeScout as scout
import scrapeMobileDE as mobile


class SiteNotInDatabase(Exception):
    pass


if __name__ == "__main__":
    # Args
    url = sys.argv[1]
    pdf_path = sys.argv[2]

    # Chdir
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.abspath(os.path.dirname(sys.executable)))
    elif __file__:
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
    os.chdir(os.path.dirname(os.getcwd()))

    # # Make folders
    # folders = ['pdfs', 'html']
    # for folder in folders:
    #     path = os.path.join(os.getcwd(), 'files', folder)
    #     if not os.path.isdir(path):
    #         os.makedirs(path)

    ans = ''
    try:
        if 'mobile.de' in url:
            ans = mobile.main(url, pdf_path)
        elif 'autoscout24.es' in url:
            ans = scout.main(url, pdf_path)
        else:
            raise(SiteNotInDatabase)
    except SiteNotInDatabase:
        print(json.dumps({'Response': 'Site Not Found'}))

    else:
        print(json.dumps(ans, ensure_ascii=False))
