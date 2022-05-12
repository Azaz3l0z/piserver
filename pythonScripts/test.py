import requests

data = {
    'url': 'https://suchen.mobile.de/fahrzeuge/details.html?id=344450133&damageUnrepaired=NO_DAMAGE_UNREPAIRED&isSearchRequest=true&pageNumber=1&ref=quickSearch&scopeId=C&action=topOfPage&top=1:1&searchId=07ba9742-1cee-470a-faca-61fdc933d4f5'
}

url = 'http://2.154.9.206/api/importarcoches'
r = requests.get(url, data=data)
print(r.text)
