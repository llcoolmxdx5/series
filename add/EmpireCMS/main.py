import warnings
import time
import os

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
        uname_selector = 'body > table:nth-child(2) > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > input'
        upwd_selector = 'body > table:nth-child(2) > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > input'
        submit_selctor = 'body > table:nth-child(2) > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(6) > td:nth-child(2) > input[type="image"]'
        self.browser.get(self.url)
        self.__sendkeys(uname_selector, self.uname)
        self.__sendkeys(upwd_selector, self.upwd)
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

    def add_article(self, title, keyword, summary, L, subtitle=''):
        title_selector = '#baseinfo > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr:nth-child(1) > td > input[type="text"]:nth-child(1)'
        subtitle_selector = '#ftitle'
        keyword_selector = '#baseinfo > table:nth-child(3) > tbody > tr:nth-child(3) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > input[type="text"]'
        save_selector = 'body > form > table > tbody > tr > td:nth-child(2) > input[type="submit"]:nth-child(1)'
        sourcecode_selector = '#xToolbar > table:nth-child(1) > tbody > tr > td:nth-child(2) > div > table > tbody > tr > td.TB_Button_Text' 
        body_selector = '#xEditingArea > textarea'
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

    def continue_add(self):
        # todo
        continue_selector = 'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > div > a:nth-child(1) > u'
        self.__click(continue_selector)

    def error(self):
        self.browser.switch_to_default_content()


def autokeyword(path):
    with open(path) as f:
        content = f.read()
    keys = jieba.analyse.extract_tags(content, topK=3, allowPOS=('ns', 'n', 'vn', 'v', 'i', 'l', 'nr', 'nt', 'nz'))
    return ','.join(keys)


def read_file(path1):
    with open(path1, 'r') as f:
        if CONFIRM_KEYSUMM:
            keyword = f.readline()[:-1]
            summary = f.readline()[:-1]
        else:
            keyword = ''
            summary = ''
        L = [f'<style>.acc_acc {{font-size: {FONT_SIZE}px;}}</style>']
        content_L = []
        for j in f.readlines():
            if len(j) < 4:
                continue
            content_L.append(j)
        if AUTO_SUMMARY and len(summary) < 2:
            summary = content_L[0]
        for i in content_L:
            L.append(f'<span class="acc_acc">　　{i[:-1].strip()}</span><br class="acc_acc">')
            L.append(f'<span class="acc_acc">　　</span><br class="acc_acc">')
    if AUTO_KEYWORD:
        keys = autokeyword(path1)
        if CONFIRM_KEYSUMM:
            keyword = f'{keyword},{keys}'
        else:
            keyword = keyword + keys
    return keyword, summary, L


def main(url, user, password, maincolumn, subcolumn_selector, maincolumn_id, subcolumn, path):
    empire = EmpireAddArticle(url, user, password, maincolumn, subcolumn_selector, maincolumn_id, subcolumn)
    print('正在初始化')
    empire.login()
    print('登录成功')
    empire.column()
    print('选择栏目成功')
    path = f'{path}\\'
    for i in os.listdir(path):
        if i[-3:] == 'txt':
            title = i[:-4]
            path1 = path + i
        else:
            continue
        try:
            print(f'读取文件:{path1}')
            keyword, summary, L = read_file(path1)
            empire.add_article(title, keyword, summary, L)
            print(f'添加文章:{title} 成功,准备添加下一篇')
            # empire.continue_add()
        except Exception as e:
            print(e)
            empire.error()
            empire.column()
    print('添加文章结束')


