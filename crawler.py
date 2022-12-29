from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from utils import Similarity

import requests
import time
import urllib.request
import os
import pandas as pd

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
        self.output_data_information = pd.DataFrame({'num': [], 'keywords' : [], 'url' : [], 'similarity' : []})
        
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
        
        # input the keyword to search box
        elem.send_keys(search_keyword)
        # Enter 입력
        elem.send_keys(Keys.RETURN) 
    
        self.get_images(search_keyword)
    
    def get_images(self, keywords):
        
        # scroll the page to bottom
        scroll_pause_time = 1
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
                except:
                    break
            last_height = new_height
            
        self.get_images_from_driver(keywords)

    def get_images_from_driver(self, keywords):
        try:
            images = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rg_i.Q4LuWd"))
            )
        finally:
            pass
        self.image_count = 0
        image_url = []
        criterion = Similarity()
        create_folder(self.output_dir)
        
        for image in images:
            try:
                image.click()
                time.sleep(1)
                element = self.driver.find_elements(By.CLASS_NAME, 'v4dQwb')
                
                if self.image_count == 0:
                    big_image = element[0].find_element(By.CLASS_NAME, 'n3VNCb')
                else:
                    big_image = element[1].find_element(By.CLASS_NAME, 'n3VNCb')
                try:
                    # The case link exists but response does not exist.
                    url = big_image.get_attribute("src")
                    response = requests.get(url)
                    image_url.append(url)
                    
                    time.sleep(1)
                    # if response was success, write the image on the local
                    similarity = 0
                    if response.status_code == 200:
                        time.sleep(1)
                        with open(f"{self.output_dir}/{keywords}{self.image_count+1}.jpg", "wb") as file:
                            file.write(response.content)
                            # check cosine similarity, and save the information in excel files
                            file.close()
                    try:
                        image_file_directory = f"{self.output_dir}/{keywords}{self.image_count+1}.jpg"
                        similarity = criterion.calculation(image_file_directory, keywords)
                    except Exception as error:
                        raise(error)
                        # print the option
                    finally:
                        self.print_intermediate_process(image_url, similarity)
                    # save the information in dataframe
                    
                    self.save_information(keywords, image_url, similarity)
                except:
                    pass
                
                if(self.image_count > self.maximum_image_count):
                    print(f"total {self.image_count - 1} was gathered")
                    break
            except:
                pass
            
        self.output_data_information.to_excel("data/output/information.xlsx")

    def print_intermediate_process(self, image_url, similarity):
        if(self.print_url_option):
            print(f"{self.image_count+1}th image url {'':3}:{'':3} {image_url[self.image_count]}")
            print(f"similarity {'':3}:{'':3}{similarity.item()*100}%.")

    def save_information(self, keywords, image_url, similarity):
        # df = df.append(more) -> df = pd.condat([df, more]) 바뀜!! 
        new_row = {
                        'num' : self.image_count + 1,
                        'keywords' : keywords,
                        'url' : image_url,
                        'similarity' : similarity.item()
                    }
        self.output_data_information = pd.concat([self.output_data_information,
                                                            pd.DataFrame.from_records([new_row])])
                    
        self.image_count += 1