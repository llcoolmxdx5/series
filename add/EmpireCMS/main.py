import warnings
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from config import AUTO_KEYWORD, CONFIRM_KEYSUMM, DISPLAY_BROSER, FONT_SIZE, AUTO_SUMMARY

try:
    import jieba.analyse
except Exception as e:
    print(e)


class EmpireAddArticle:
    def __init__(self, url, user, password, maincolumn, subcolumn_selector, maincolumn_id, subcolumn):
        self.uname = user
        self.upwd = password
        self.url = url
        self.maincolumn = maincolumn
        self.subcolumn_selector = subcolumn_selector
        self.maincolumn_id = maincolumn_id
        self.subcolumn = subcolumn
        if DISPLAY_BROSER:
            self.browser = webdriver.Chrome()
            self.browser.maximize_window()
        else:
            chrome_options=Options()
            chrome_options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(10)

    def __del__(self):
        self.browser.close()
    
    def __click(self, selector):
        self.browser.find_element_by_css_selector(selector).click()
    
    def __sendkeys(self, selector, sendkeys):
        self.browser.find_element_by_css_selector(selector).send_keys(sendkeys)
    
    def login(self):
        # 已完成
        uname_selector = 'body > table:nth-child(2) > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > input'
        upwd_selector = 'body > table:nth-child(2) > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > input'
        submit_selctor = 'body > table:nth-child(2) > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(6) > td:nth-child(2) > input[type="image"]'
        self.browser.get(self.url)
        self.__sendkeys(uname_selector, self.uname)
        self.__sendkeys(upwd_selector, self.upwd)
        # time.sleep(20)
        self.__click(submit_selctor)

    def column(self):
        time.sleep(10)
        maincolumn_selector = f'#pr{"主栏目id"} > a'
        subcolumn_selector = f'#pr{"子栏目id"} > a'
        add_selector = 'body > table.tableborder > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(1) > div > input[type="button"]'
        self.browser.switch_to_frame('left')
        if int(self.subcolumn_selector):
            self.__click(maincolumn_selector)
        self.__click(subcolumn_selector)
        self.browser.switch_to.default_content()
        self.browser.switch_to_frame('main')
        self.__click(add_selector)

    def add_article(self, title, keyword, summary, L, img_L, subtitle=''):
        title_selector = '#baseinfo > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > input[type="text"]:nth-child(1)'
        subtitle_selector = '#ftitle'
        keyword_selector = '#baseinfo > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > input[type="text"]'
        save_selector = 'body > form > table > tbody > tr > td:nth-child(2) > input[type="submit"]:nth-child(1)'
        sourcecode_selector = '#cke_16' 
        body_selector = '#cke_1_contents > textarea'
        summary_selector = '#smalltext'
        self.__sendkeys(title_selector, title)
        self.__sendkeys(subtitle_selector, subtitle)
        self.__sendkeys(keyword_selector, keyword)
        self.__sendkeys(summary_selector, summary)
        self.__click(sourcecode_selector)
        for line in L:
            self.__sendkeys(body_selector, line)
            self.__sendkeys(body_selector, Keys.ENTER)
        self.__click(save_selector)


def main():
    pass


