import re
import os
import requests
import htmlToPDF
from datetime import datetime
from bs4 import BeautifulSoup


class Scraper(object):
    def __init__(self, url) -> None:
        # Fix possible whitespaces errors
        self.url = url.strip()
        self.headers = {
            'Host': 'www.mobile.de',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cookie': 'sorting_e=""; show_qs_e=vhc%3Acar%2Cms1%3A25200_14_; _abck=A29FBBA04447D66FAF82AC5E995225EA~0~YAAQRggQAq2L9o2AAQAA3grAmAdeTWunTIqhlCsbISDOjoi8bFEfSzyl+WxbYc5DglHzL/Ckor43VXIKLZJaJOg/aVTvIuEW5d044z5vSRj4tfoWnquJQvQMfFVDDoZBjfRjGGi1fCFv3m3NAPQ/uHGFhp0t/gBnEIL0D/VF+UqEzsdPXCISCLBhL+HSSSyjRa+JwTLWnj5gzjQqoFa6v7VQYiW8I4YDVATfv3oNV+8WY67dsWih4GkDaYlgQfhpg3TFrNHEr4qlktl9kedOjR63MxWqSrrX0hJrEUaWYKuWzquODayDPw8FEhLhkaxM1tLGT33qfXSwKALFbStSwmHD3P9k//1d0yOLycEWvLbgLqBszPl2hDces7BrIzy4Izt4pJI7wM2qhhvnIMugJtxmr6UYSx0=~-1~-1~-1; bm_sz=521F24D458DC92A597605A8599F764C2~YAAQp+oWArq/1HOAAQAALixUmA/2dtKD0sEKJFQNeQatNCx5J3PzSjICeDXEvZa9XPL3ibOpbwRmjzZzZpuldKdgH5p57sg23lrAFOOCQngPqAEfPLLaliyk/LSC3EhKolqnU6kKG3fCTxRwuSfWs/mVVLbhM9MRXeJW3IB/M6i66Fy0DVLCa9Ebu5plR0x0uIuKnVGZWSIMPbh73iSNSsUO1u7JlqRqtLMiZxruYxp4EdNM5g2cdXgYZCcpn/asBptlAGvm/GjnHIpp1E9rZNIGKVGYc6ncSz2UGylcfPVVuw==~3225650~4342321; vi=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaWQiOiJiNDVmOGJmMC1mZDZiLTRiNTAtOWU0MC1hYmRjZDQ4MDY0ZDkiLCJpYXQiOjE2NTE4MjMwOTl9.i1Mo5x_AgHrcrUY43_Wmerj_KGovLBojbvoghnbnsLg; mobile.LOCALE=de; optimizelyEndUserId=oeu1651823096569r0.5312481568497365; visited=1; mdeConsentDataGoogle=1; mdeConsentData=CPYkDPWPYkDPWEyAHADECMCgAP_AAELAAAYgIsNd_X__bX9n-_7__ft0eY1f9_r3_-QzjhfNs-8F3L_W_L0X_2E7NF36tq4KuR4ku3bBIQNtHMnUTUmxaolVrzHsak2cpyNKJ7LkknsZe2dYGH9Pn9lD-YKZ7_5___f53z___9_-39z3_9f___d__-__-vjf_599n_v9fV_____________-_______8C84A4ACgAQAA0ACKAEwALYC8wCQkBAABYAFQAMgAcABEADIAHgARAAngBVAGGAP0BIgDJAGTgMuDQBQAmABcAOqAkQBk4iAIAEwA6oCRAGTioAgATAAuAKbAXmMgBABMAXmOgLAALAAqABkADgAIgAZAA8AB8AEQAJ4AVQAuABfADEAJgAYYA_QCLAJEAZIAycBlxCAUAAsADIAIgAmABVAC4AF8AMQCRAGTkoBgACwAMgAcABEADwAIgAVQAuABfADEAkQBk5SAmAAsACoAGQAOAAiABkADwAIgATwApABVAC-AGIAfoBFgEiAMkAZOAy4.YAAAAAAAD4AAAKcAAAAA; _ga=GA1.2.1824592379.1651823100; _gid=GA1.2.186741692.1651823100; _ga_2H40T2VTNP=GS1.1.1651828825.2.1.1651830167.0; ioam2018=0019f5046cda69a946274d1fd:1678434304777:1651823104777:.mobile.de:31:mobile:DE/ES/OB/S/P/D:noevent:1651830286721:sssfvb; iom_consent=0103ff03ff&1651823105397; _pubcid=c2cb941e-bb17-4ac5-b2e1-cebb14223731; cto_bundle=-ZMfdV9kMWFpbGZCWmhIejJZZVNjN2xPbjYzY21mZjdkVmQxU3p3OHdId2FlVW1HNGowWHp5RDAlMkJIRUNtTFJnT0EwUVhKd2h0JTJGS2FBakMlMkJlOGlYbVBlbTZuJTJCckwlMkJ4U1VlR2xGTVo0RXFXWXJ5Rk1FdTlXZkNseHV6U0hVS3pYYklYRU5xOWtxcHV2M1pxdGpWaWpSV2JmNWZnJTNEJTNE; cto_axid=x6mG858LHXc9na4WBHkYdsdWA_35tuiY; _clck=fsdy4i|1|f18|0; _clsk=6obze5|1651830164043|8|1|a.clarity.ms/collect; _uetsid=dfeb0740cd1011ec92ee71a685fb3d44; _uetvid=dfeb4d70cd1011ec942103db0d71c99a',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers',
        }

        if 'suchen.mobile.de' in self.url:
            self.__parseURL()

        self.request = requests.get(self.url, headers=self.headers)

    def __parseURL(self):
        urlES = '' +\
            'https://www.mobile.de/es/Veh%C3%ADculo/Vehiculo/' +\
            'vhc:car,dmg:false/pg:vipcar/{id}.html'

        self.url += '&'
        id = re.search('\d{9}', self.url)

        if id != None:
            id = id.group()
        self.url = urlES.format(id=id)

    def scrape(self):
        def images():
            images = soup.find_all('img')
            for n, im in enumerate(images):
                try:
                    url = im.attrs['src']
                    if 'https://img.classistatic.de/api/v1/mo-prod/images/' in url:
                        images[n] = url.replace('160.jpg', '1024.jpg')
                    else:
                        images[n] = None
                except:
                    images[n] = None

            images = [x for x in images if x != None]
            images = list(dict.fromkeys(images))

            return images

        def data():
            # Iterate and order all data
            tecnicData = soup.find_all('div', {'class': 'g-row'})
            title = re.search('(.*)', soup.find('h1').getText())
            rows = []
            data = {
                'title': title,
                'year': None,
                'transmission': None,
                'fuel': None,
                'km': None,
                'power': None,
                'c02': None,
                'images': images
            }

            patterns = {
                'year': '\d{2}\/\d{4}',
                'transmission': '(?<=Cambio)(.+)?',
                'fuel': '(?<=Combustible)(.+)?',
                'km': '\d+(?=\s+?km)',
                'power': '\d+(?=\s+?HP)',
                'c02': '\d+(?=\s+?g/km)'
            }
            # Find the text from each row
            for row in tecnicData:
                row = row.findChildren('span', recursive=False)
                if row != []:
                    row = ''.join(list(map(BeautifulSoup.getText, row)))
                    row = row.strip().replace('.', '').replace(',', '')
                    rows.append(row)

            # Get all re objects
            for row in rows:
                for key in data:
                    if data[key] == None:
                        data[key] = re.search(patterns[key], row)

            # Get re search result in a nice string format
            for key in data:
                if data[key] != None:
                    try:
                        data[key] = data[key].group().strip(
                        ).capitalize().replace('-', ' ')

                    except AttributeError as e:
                        pass

            return data

        def vendor():
            clientdata = {
                'location': None,
                'phone': None
            }

            patterns = {
                'location': '(?=[A-Z]{2}-\d{5})\s?(.+)',
                'phone': '(?=\+\d{2})(.+)'
            }

            clientTypes = ['Distribuidor', 'Empresa', 'Vendedor particular']
            for n, client in enumerate(clientTypes):
                div = soup.find('p', text=re.compile(client))
                if div != None:
                    div = div.parent.parent
                    paragraphs = list(
                        map(BeautifulSoup.getText, div.find_all('p')))[1:]
                    if n < 2:
                        clientdata['name'] = paragraphs[0]
                    else:
                        clientdata['name'] = 'Particular'
                    break

            for line in paragraphs:
                for key in clientdata:
                    if clientdata[key] == None:
                        clientdata[key] = re.search(patterns[key], line)

            for key in clientdata:
                if clientdata[key] != None:
                    try:
                        clientdata[key] = clientdata[key].group().strip().replace(
                            '\xa0', ' ')
                    except AttributeError:
                        pass
            return clientdata

        # Soup
        soup = BeautifulSoup(self.request.text, 'html.parser')

        images = images()

        data = data()
        data['vendedor'] = vendor()

        # Fix and parse strings
        data['title'] = re.sub('[^A-Za-z0-9\s-]+', '', data['title'])
        return data

    def pdf(self, title: str, pdf_folder: str):
        # Paths
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        file_html = os.path.join(pdf_folder, f'{now}_{title}.html')

        # Create html
        with open(file_html, 'w+') as file:
            file.write(self.request.text)

        return file_html
