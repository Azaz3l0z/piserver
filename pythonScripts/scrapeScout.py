import re
import os
import json
import requests
import htmlToPDF
from datetime import datetime
from bs4 import BeautifulSoup


class Scraper(object):
    def __init__(self, url) -> None:
        self.url = url.strip()
        self.request = requests.get(url)

    def scrape(self):
        data = {}
        soup = BeautifulSoup(self.request.text, 'html.parser')
        scriptJSON = soup.find(
            'script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
        scriptJSON = json.loads(scriptJSON.decode_contents())
        details = scriptJSON['props']['pageProps']['listingDetails']

        # Data return values
        data['title'] = ' '.join([details['vehicle'].get('make'), details['vehicle'].get(
            'model'), details['vehicle'].get('modelVersionInput')])
        data['year'] = details['vehicle'].get('firstRegistrationDate')
        data['transmission'] = details['vehicle'].get('transmissionType')
        data['fuel'] = details['vehicle']['fuelCategory']['formatted']
        data['km'] = details['vehicle'].get('mileageInKmRaw')
        data['power'] = details['vehicle'].get('rawPowerInHp')
        data['c02'] = details['vehicle']['co2emissionInGramPerKm']['formatted']
        data['images'] = [x[:x.find('.jpg')+len('.jpg')]
                          for x in details['images']]
        data['vendedor'] = {
            'name': details['seller'].get('companyName'),
            'location': ' '.join([details['location'][x]
                                  for x in details['location']
                                  if details['location'][x]]),
            'phone': details['seller']['phones'][0]['callTo']
            if details['seller']['phones'] != [] else ""
        }

        # Fix and parse string
        data['title'] = re.sub('[^A-Za-z0-9\s-]+', '', data['title'])

        for k, v in data.items():
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    if v2 == None:
                        data[k][k2] = ""

            else:
                if k == None:
                    data[k] = ""

        return data

    def pdf(self, title: str, pdf_folder: str):
        # Paths
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        file_html = os.path.join(pdf_folder, f'{now}_{title}.html')

        html = self.request.text
        html = re.sub(r'(?i)(color)', '', html)
        with open(file_html, 'w+') as file:
            file.write(html)

        return file_html
