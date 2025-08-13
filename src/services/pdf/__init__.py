
import base64
import contextlib
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

@contextlib.contextmanager
def _chrome_driver_context(options):
  service = Service()
  driver  = None
  
  try:
    driver = webdriver.Chrome(service = service, options = options)
    yield driver

  finally:
    if driver is not None:
      driver.quit()
      service.stop()


def _base64_encode(file):
  return base64.b64encode(file).decode('utf-8')


def printHtmlToPDF(text = '', *, 
                   base64_encoded = False,
                  ):
  global chrome_options
  global params

  with _chrome_driver_context(chrome_options) as driver:
    driver.get(text_to_uri_data(text))
    pdfdata = driver.execute_cdp_cmd("Page.printToPDF", params)
    pdf     = base64.b64decode(pdfdata['data'])

  return pdf if not base64_encoded else _base64_encode(pdf)

