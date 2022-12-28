from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
import time
import urllib.request
import os

def create_folder(name):
    if not os.path.isdir(f"{name}/"):
        os.makedirs(f"{name}/")
        
class GoogleImageCrawler():
    def __init__(self, output_dir = "data/output", url_option = True,
                 maximum_image_count = 100):
        self.set_options()
        self.print_url_option = url_option
        self.output_dir = output_dir
        self.image_count = 0
        self.maximum_image_count = maximum_image_count
        
    def set_options(self):
        
        options = webdriver.ChromeOptions()
        # ubuntu does not have window, so headless option must be defined.
        options.add_argument('--headless') # 
        options.add_argument('--no-sandbox')
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options, executable_path="/root/.wdm/drivers/chromedriver/linux64/108.0.5359/chromedriver")
        self.driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
        
    def search(self, keyword):
        # input keyword
        search_keyword = keyword
        
        # 검색창 탐색(4.3.0 이 후 버전으로는 아래와 같이 실행)
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
        finally:
            pass
        
        elem.send_keys(search_keyword)
        # Enter 입력
        elem.send_keys(Keys.RETURN) 
    
        self.get_images(elem, search_keyword)
    
    def get_images(self, elem, keywords):
        try:
            images = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rg_i.Q4LuWd"))
            )
        finally:
            pass
        
        self.image_count = 0
        image_url = []
        for image in images:
            try:
                image.click()
                time.sleep(1)
                element = self.driver.find_elements(By.CLASS_NAME, 'v4dQwb')
                
                if self.image_count == 0:
                    big_image = element[0].find_element(By.CLASS_NAME, 'n3VNCb')
                else:
                    big_image = element[1].find_element(By.CLASS_NAME, 'n3VNCb')
                image_url.append(big_image.get_attribute("src"))
                
                if(self.print_url_option):
                    print(f"{self.image_count+1}th image url {'':3}:{'':3} {image_url[self.image_count]}")
                response = requests.get(image_url[self.image_count])
                
                # if response was success, write the image on the local
                create_folder(self.output_dir)
                if response.status_code == 200:
                    with open(f"{self.output_dir}/{keywords}{self.image_count+1}.jpg", "wb") as file:
                        file.write(response.content)
                self.image_count += 1
                
                if(self.image_count > self.maximum_image_count):
                    print(f"total {self.image_count} was gathered")
                    break
                
            except:
                pass
        # //*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img
        
# /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[18]

#*[@id="islrg"]/div[1]/div[36]/a[1]/div[1]/img
#*[@id="islrg"]/div[1]/div[38]/a[1]/div[1]/img
#*[@id="islrg"]/div[1]/div[40]/a[1]/div[1]/img
#*[@id="islrg"]/div[1]/div[6]/a[1]/div[1]/img
#*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img
#*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img
#*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img
#*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img
# *[@id="islrg"]/div[1]/div[153]/a[1]/div[1]/img
# *[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img