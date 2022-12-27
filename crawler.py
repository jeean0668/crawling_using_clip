from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

def create_folder(name):
    if not os.path.isdir(f"{name}/"):
        os.makedirs(f"{name}/")
        
class GoogleImageCrawler():
    def __init__(self, keyword, output_dir = "data/output"):
        self.set_options()
        
    def set_options(self):
        
        options = webdriver.ChromeOptions()
        # ubuntu does not have window, so headless option must be defined.
        options.add_argument('--headless') # 
        options.add_argument('--no-sandbox')
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options, executable_path="/root/.wdm/drivers/chromedriver/linux64/108.0.5359/chromedriver")
        
    def search(self, keyword):
        # input keyword
        search_keyword = keyword
        # 검색창 탐색
        elem = self.driver.find_element_by_name("q")
        elem.send_keys(search_keyword)
        # Enter 입력
        elem.send_keys(Keys.RETURN) 
    
    
        # //*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
        
