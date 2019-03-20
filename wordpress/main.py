import warnings
import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

try:
    import jieba.analyse
except Exception as e:
    print(e)

DISPLAY_BROSER = True

class WordPressAddArticle:
    def __init__(self, url, user, password, Key):
        self.uname = user
        self.upwd = password
        self.url = url
        self.key = Key
        if DISPLAY_BROSER:
            self.browser = webdriver.Chrome()
            self.browser.maximize_window()
        else:
            chrome_options=Options()
            chrome_options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(20)

    def __del__(self):
        self.error()
        self.browser.close()

    def __click(self, selector):
        self.browser.find_element_by_css_selector(selector).click()

    def __sendkeys(self, selector, sendkeys):
        self.browser.find_element_by_css_selector(selector).send_keys(sendkeys)

    def login(self):
        uname_selector = '#user_login'
        upwd_selector = '#user_pass'
        submit_selctor = '#wp-submit'
        self.browser.get(self.url)
        self.__sendkeys(uname_selector, self.uname)
        self.__sendkeys(upwd_selector, self.upwd)
        self.__click(submit_selctor)

    def pre_add(self):
        article_selector = '#menu-posts > a > div.wp-menu-name'
        warticle_selector = '#wpbody-content > div.wrap > a'
        self.__click(article_selector)
        self.__click(warticle_selector)

    def add_article(self, title, keyword, summary, L):
        title_selector = '#title'
        keyword_selector = '#aiosp_keywords_wrapper > div > span.aioseop_option_input > div.aioseop_option_div > input[type="text"]'
        save_selector = '#publish'
        sourcecode_selector = '#content-html'
        body_selector = '#content'
        summary_selector = '#aiosp_description_wrapper > div > span.aioseop_option_input > div.aioseop_option_div > textarea'
        column_selector = '#in-category-1598'
        self.__sendkeys(title_selector, f'{self.key}_{title}_{self.key}')
        try:
            self.__click(sourcecode_selector)
        except:
            pass
        for line in L:
            self.__sendkeys(body_selector, line)
            self.__sendkeys(body_selector, Keys.ENTER)
        self.__sendkeys(keyword_selector, f'{self.key},{keyword}')
        self.__sendkeys(summary_selector, summary)
        js = 'window.scrollTo(0,0)'
        self.browser.execute_script(js)
        self.__click(column_selector)
        self.__click(save_selector)
#publish
    def continue_add(self):
        continue_selector = '#wpbody-content > div.wrap > a'
        self.__click(continue_selector)
    
    def error(self):
        try:
            self.browser.switch_to_alert().accept()
        except:
            pass


def autokeyword(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    keys = jieba.analyse.extract_tags(content, topK=3, allowPOS=('ns', 'n', 'vn', 'v', 'i', 'l', 'nr', 'nt', 'nz'))
    return ','.join(keys)


def read_file(path1,Key):
    content_key = [f'{Key}规则',f'{Key}技巧',f'{Key}玩法',f'{Key}游戏',f'{Key}策略',f'{Key}必胜']
    with open(path1, 'r', encoding='utf-8') as f:
        L = ['<style>.acc_acc font-size: 14px;</style>']
        content_L = []
        index = 0
        for j in f.readlines():
            if len(j) < 4:
                continue
            content_L.append(j+content_key[index % 6])
            index += 1
        summary = content_L[0]
        for i in content_L:
            L.append(f'<span class="acc_acc">　　{i[:-1].strip()}</span><br class="acc_acc">')
    keys = autokeyword(path1)
    keyword = f'{keys}'
    return keyword, summary, L


def main(url, user, password, path, Key):
    wordpress = WordPressAddArticle(url, user, password, Key)
    print('正在初始化')
    wordpress.login()
    print('登录成功')
    wordpress.pre_add()
    print('选择栏目成功')
    result = [(i, os.stat(f'{path}\\{i}').st_mtime) for i in os.listdir(path)]
    total_doc = len(result)
    error_doc = 0
    success_doc = 0
    print(f'预计将发布{total_doc}篇文章')
    for i in sorted(result, key=lambda x: x[1], reverse=True):
        if i[0][-3:] == 'txt':
            title = i[0][:-4]
            path1 = f'{path}\\{i[0]}'
        else:
            continue
        try:
            print(f'读取文件:{path1}')
            keyword, summary, L = read_file(path1, Key)
            wordpress.add_article(title, keyword, summary, L)
            wordpress.continue_add()
        except Exception as e:
            error_doc += 1
            print(f'发布文章:{title} 失败')
            print(e)
            wordpress.error()
            wordpress.pre_add()
        else:
            success_doc += 1
            print(f'发布文章:{title} 成功,准备发布下一篇')
        finally:
            print(f'文章发布进度:{success_doc}/{total_doc},失败{error_doc}篇')
    print('发布文章结束')


