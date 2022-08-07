from aiohttp import ClientSession
from bs4 import BeautifulSoup
from numpy import outer
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from pipeit import Map
from typing import List, Tuple
import time
import re

class HjDictionary:

    def __init__(self):
        self.target = "https://dict.hjenglish.com/jp/jc/"

    def pre_activation(self, driver):
        driver.get(self.target + "漏れ無く")
        WebDriverWait(driver, 5, 0.1).until(lambda x: x.find_element(By.CSS_SELECTOR, "div.search-input-wrapper"))
        return True

    def find_sugesstions(self, outer_html: str) -> List[str]:
        soup = BeautifulSoup(outer_html, 'html.parser')
        return soup.find_all('li') | Map(lambda x:x.text) | list

    def post_selector(self, outer_html: str) -> str:
        has_url = re.search('="http.+?"', outer_html)
        while has_url:
            outer_html = outer_html[:has_url.start()] + outer_html[has_url.end():]
            has_url = re.search('="http.+?"', outer_html)
        return re.sub('class="([a-z]+)?', r'class="dictionary-\1', outer_html.replace('  ','').replace('\n',''))

    def find_explain(self, driver: 'selenium.webdriver', logger: 'Logger', word: str) -> Tuple[bool, str]:
        import time # _test
        loop_count = 0
        while word:
            loop_count += 1
            if loop_count >= 3:
                return False, "没有查询到相关词汇哦~~" 
            try:
                driver.get(self.target + word)
                WebDriverWait(driver, 5, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR, "section.content"))
                WebDriverWait(driver, 0.6, 0.2).until(lambda x: x.find_element(By.CSS_SELECTOR, "header.word-details-pane-header"))
                return True, self.post_selector(driver.find_element(By.CSS_SELECTOR, "header.word-details-pane-header").get_attribute('outerHTML'))
            except:
                try:
                    outer_html = driver.find_element(By.CSS_SELECTOR, "div.word-suggestions").get_attribute('outerHTML')
                    assert outer_html
                    sugesstions = self.find_sugesstions(outer_html)
                    assert len(sugesstions) > 0 and len(sugesstions[0]) > 0
                    word = sugesstions[0]
                    continue
                except:
                    try:
                        driver.find_element(By.CSS_SELECTOR, "div.word-notfound").get_attribute('outerHTML')
                    except:
                        return False, "没有查询到相关词汇哦~" 