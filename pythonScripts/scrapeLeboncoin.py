import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path='chromedriver', options=options)

url = "https://www.leboncoin.fr/voitures/2182521551.htm"
driver.get("https://www.leboncoin.fr")
driver.get(url)

time.sleep(100)
