
import base64

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from src.utils.text_to_uri_data import text_to_uri_data


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

params = { 
  'landscape'       : False,
  'printBackground' : True ,

  # a4
  'paperWidth'      : 8.26,
  'paperHeight'     : 11.68,  

  # # margins
  # 'marginTop': 0.4,
  # 'marginBottom': 0.4,
  # 'marginLeft': 0.4,
  # 'marginRight': 0.4,
}

def _base64_encode(file):
  return base64.b64encode(file).decode('utf-8')

def printHtmlToPDF(text = '', *, 
                   base64_encoded = False,
                  ):
  service = Service()
  driver  = webdriver.Chrome(
    service = service, 
    options = chrome_options)
    
  driver.get(text_to_uri_data(text))
  
  pdfdata = driver.execute_cdp_cmd("Page.printToPDF", params)
  pdf     = base64.b64decode(pdfdata['data'])
  
  driver.quit()

  return pdf if not base64_encoded else _base64_encode(pdf)

