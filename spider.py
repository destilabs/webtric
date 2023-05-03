import argparse
import os
import time

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from tools.helpers import get_text_by_selector
from tools.loaders import load_config
from tools.setups import get_local_safe_setup, get_safe_setup


class Spider:
    def __init__(self, driver, config):
        self.__driver = driver
        self.__config = config
    
    def parse(self, url: str) -> pd.DataFrame:
        """
            Scrapes a website from url using predefined config, returns DataFrame
            parameters:
                url: string
            
            returns:
                pandas Dataframe
        """
        self.__driver.get(url)
  
        WebDriverWait(self.__driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, self.__config['container_class']))
        )

        try:    
            items = self.__driver.find_elements(By.CLASS_NAME, self.__config['items_class'])
        except NoSuchElementException:
            with open('page_source.html', 'w') as f:
                f.write(self.__driver.page_source)
        
            candidates = self.__find_textual_elements(self.__driver)
            print(f'No items found, but following candidates were found: {candidates}. Try to use one of them as items_class in config.json')
        
        if len(items) == 0:
            candidates = self.__find_textual_elements(self.__driver)
            print(f'No items found, but following candidates were found: {candidates}. Try to use one of them as items_class in config.json')

        items_content = [
            [get_text_by_selector(div, selector) for selector in self.__config['data_selectors']]
            for div in items]
        
        df = pd.DataFrame(items_content, columns = self.__config['data_column_titles'])

        if df.shape[0] == 0:
            candidates = self.__find_textual_elements(items[0])
            print(f'No items found, but following candidates were found: {candidates}. Try to use one of them as items_class in config.json')

        return df 

    def parse_pages(self, url: str):
        """
            Scrapes a website with pagination from url using predefined config, yields list of pandas DataFrames
            parameters:
                url: string
        """
        pagination_config = self.__config['pagination']        
        
        for i in tqdm(range(1, pagination_config['crawl_pages'] + 1)):
            yield self.parse(url.replace("$p$", str(i)))

            time.sleep(int(pagination_config['delay']/1000))      


    def __find_textual_elements(self, container) -> list:
        """
            Finds all elements with text on a page
            returns:
                list of selenium elements
        """
        return container.find_elements(By.XPATH, "//*[text()]")

def scrape(args): 
    config = load_config(args.config)

    pagination_config = config['pagination']
    url = config['url']

    if args.mode == 'local':
        driver = get_local_safe_setup()
    else:
        driver = get_safe_setup()

    spider = Spider(driver, config)

    os.makedirs(os.path.dirname(args.output), exist_ok = True)

    try:
        if pagination_config['crawl_pages'] > 0:
            data = spider.parse_pages(url)
            df = pd.concat(list(data), axis = 0)
        else:
            df = spider.parse(url)
        
        df.to_csv(args.output, index = False)
    except Exception as e:
        print(f'Parsing failed due to {str(e)}')
    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Configuration of spider learning', required=True)
    parser.add_argument('-o', '--output', help='Output file path', required=True)
    parser.add_argument('-m', '--mode', default='true', help='Which driver to use', choices=['local', 'remote'], required=True)
    args = parser.parse_args()

    scrape(args)