import csv
import os
import time
import warnings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from config import *

warnings.filterwarnings("ignore")

class DedeAddArticle:
    def __init__(self):
        self.uname = UESR
        self.upwd = PASSWORD
        self.url = BACKADD
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

    def login(self):
        '''
        此实例方法用于处理登录账户
        '''
        uname_selector = '#login-box > div.login-main > form > dl > dd:nth-child(2) > input[type="text"]'
        upwd_selector = '#login-box > div.login-main > form > dl > dd:nth-child(4) > input'
        submit_selctor = '#login-box > div.login-main > form > dl > dd:nth-child(6) > button'
        self.browser.get(self.url)
        user_name = self.browser.find_element_by_css_selector(uname_selector)
        user_name.send_keys(self.uname) #用户名
        user_pwd = self.browser.find_element_by_css_selector(upwd_selector)
        user_pwd.send_keys(self.upwd) #用户密码
        submit = self.browser.find_element_by_css_selector(submit_selctor)
        submit.click() # 登录
    
    def column(self):
        '''
        选择栏目
        '''
        time.sleep(10)
        maincolumn_selector = f'body > table > tbody > tr:nth-child(4) > td > table:nth-child({MAINCOLUMN}) > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > a:nth-child(2)'
        self.browser.switch_to_frame('menufra')
        webcolumn = self.browser.find_element_by_css_selector('#items1_1 > ul > li:nth-child(1) > div > div.fllct > a')
        webcolumn.click()
        self.browser.switch_to.default_content()
        self.browser.switch_to_frame('main')
        if SUBCOLUMN_SELECTOR:
            self.subcolumn()
        else:
            maincolumn = self.browser.find_element_by_css_selector(maincolumn_selector)
            maincolumn.click()
    
    def subcolumn(self):
        maincolumn_expand_selector = f'body > table > tbody > tr:nth-child(4) > td > table:nth-child({MAINCOLUMN}) > tbody > tr:nth-child(1) > td:nth-child(1) > img'
        subcolumn_selector = f'#suns{MAINCOLUMN_ID} > table > tbody > tr:nth-child({str(SUBCOLUMN*2 -1)}) > td > table > tbody > tr > td:nth-child(1) > a:nth-child(3)'
        maincolumn_expand_botton = self.browser.find_element_by_css_selector(maincolumn_expand_selector)
        maincolumn_expand_botton.click()
        subcolumn_botton = self.browser.find_element_by_css_selector(subcolumn_selector)
        subcolumn_botton.click()

    def add_article(self, title, body, tag='', keyword=''):
        '''
        添加文章
        '''
        title_selector = '#title'
        tag_selector = '#tags'
        keyword_selector = '#keywords'
        save_selector = 'body > form > table:nth-child(8) > tbody > tr > td:nth-child(2) > input'
        add_botton = self.browser.find_element_by_css_selector('body > table > tbody > tr > td > table > tbody > tr > td > input:nth-child(1)')
        add_botton.click()
        title_input = self.browser.find_element_by_css_selector(title_selector)
        title_input.send_keys(title)
        tag_input = self.browser.find_element_by_css_selector(tag_selector)
        tag_input.send_keys(tag)
        keyword_input = self.browser.find_element_by_css_selector(keyword_selector)
        keyword_input.send_keys(keyword)
        self.browser.switch_to_frame(self.browser.find_element_by_xpath('//iframe[contains(@allowtransparency,"true")]'))
        body_input = self.browser.find_element_by_class_name('cke_show_borders')
        body_input.click()
        body_input.send_keys(body)
        self.browser.switch_to.parent_frame()
        save_botton = self.browser.find_element_by_css_selector(save_selector)
        save_botton.click()

    def continue_add(self):
        continue_selector = 'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > div > a:nth-child(1) > u'
        continue_botton = self.browser.find_element_by_css_selector(continue_selector)
        continue_botton.click()
            

def read_file(path1): 
    list2 = os.listdir(path1)
    for i in list2:
        if i[-3:] == 'txt':
            title = i[:-4]
            path2 = path1 + '\\' + i
    with open(path2, 'r') as f:
        body = f.read()
    return title, body


def main():
    dede = DedeAddArticle()
    print('正在初始化')
    dede.login()
    print('登录成功')
    dede.column()
    print('选择栏目成功')
    for i in os.listdir(PATH):
        try:
            path1 = PATH + i
            print(f'读取路径{path1}')
            title, body = read_file(path1)
            dede.add_article(title, body)
            print(f'添加文章:{title}成功,准备添加下一篇')
            dede.continue_add()
        except Exception as e:
            with open('error.txt', 'a+', 'gb18030') as f:
                f.write(i+e)
            print('出现错误已记录')
    print('添加文章结束')
