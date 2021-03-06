import warnings
import time
import os
import random
import sys
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

try:
    import jieba.analyse
except Exception as e:
    print(e)

DISPLAY_BROSER = True

class WordPressAddArticle:
    def __init__(self, url, user, password):
        self.uname = user
        self.upwd = password
        self.url = url
        self.index = 0
        self.tags = [row.split(',')[0] for row in open(sys.path[0]+r'\tags.csv', 'r', encoding='gb18030')]
        if DISPLAY_BROSER:
            self.browser = webdriver.Chrome()
            self.browser.maximize_window()
        else:
            chrome_options=Options()
            chrome_options.add_argument('--headless')
            self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.implicitly_wait(20)

    def wp_exit(self):
        # self.browser.close()
        self.browser.quit()

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
        self.error()
        time.sleep(2)
        self.__click(warticle_selector)

    def get_link(self):
        random.shuffle(self.tags)
        path = f'{sys.path[0]}\\urls'
        urls_path = os.listdir(path)
        random.shuffle(urls_path)
        path1 = f'{path}\\{urls_path[0]}'
        with open(path1, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            L = []
            for row in reader:
                L.append(row[0])
            random.shuffle(L)
        return f'<a href="{L[0]}" rel="nofollow"  target="_blank">{self.tags[0]}</a>'

    def add_article(self, title, keyword, summary, L, key):
        title_selector = '#title'
        keyword_selector = '#aiosp_keywords_wrapper > div > span.aioseop_option_input > div.aioseop_option_div > input[type="text"]'
        save_selector = '#publish'
        sourcecode_selector = '#content-html'
        body_selector = '#content'
        summary_selector = '#aiosp_description_wrapper > div > span.aioseop_option_input > div.aioseop_option_div > textarea'
        column_selector = '#in-popular-category-1598'
        tag_selector = '#new-tag-post_tag'
        self.__sendkeys(title_selector, f'{key}{title}_{key}')
        try:
            self.__click(sourcecode_selector)
        except:
            pass
        num = len(L)
        i = 0
        for line in L:
            if i == num // 2:
                self.__sendkeys(body_selector, f'{self.get_link()}{line}')
            else:
                self.__sendkeys(body_selector, line)
            self.__sendkeys(body_selector, Keys.ENTER)
            i += 1
        self.__sendkeys(keyword_selector, keyword)
        self.__sendkeys(summary_selector, summary)
        # self.__sendkeys(tag_selector, self.tags[self.index % len(self.tags)])
        random.shuffle(self.tags)
        self.__sendkeys(tag_selector, self.tags[0])
        js = 'window.scrollTo(0,0)'
        self.browser.execute_script(js)
        time.sleep(2)
        self.__click(column_selector)
        self.__click(save_selector)
        self.index += 1
        time.sleep(2)
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

add = [row.split(',')[0] for row in open(sys.path[0]+r'\add.csv', 'r', encoding='gb18030')]

def read_file(path1):
    global add
    L = ['乐都城','hg8868']
    random.shuffle(L)
    title_key = L[0]
    with open(path1, 'r', encoding='utf-8') as f:
        # <script>document.title = document.title.substring(0,document.title.length-20);</script>
        L = ['',
             '<style>.acc_acc font-size: 14px;</style>']
        content_L = []
        for j in f.readlines():
            if len(j) < 10:
                continue
            content_L.append(j[:-1].strip())
        while len(content_L) < 8:
            random.shuffle(add)
            content_L = content_L + add[:8-len(content_L)]
        summary = content_L[0]
        random.shuffle(content_L)
        for i in content_L:
            L.append(f'<span class="acc_acc">　　{i.strip()}</span><br class="acc_acc">')
    keys = autokeyword(path1)
    keyword = f'{title_key},{keys}'
    return keyword, summary, L, title_key

def main(url, user, password, path):
    wordpress = WordPressAddArticle(url, user, password)
    print('正在初始化')
    wordpress.login()
    print('登录成功')
    wordpress.pre_add()
    print('选择栏目成功')
    result = [(i, os.stat(f'{path}\\{i}').st_mtime) for i in os.listdir(path)]
    total_doc = len(result)
    error_doc = 0
    success_doc = 0
    if total_doc == 0:
        raise AssertionError("文章发布结束!")
    print(f'预计将发布{total_doc}篇文章')
    for i in sorted(result, key=lambda x: x[1], reverse=True):
        if i[0][-3:] == 'txt':
            title = i[0][:-4]
            path1 = f'{path}\\{i[0]}'
        else:
            continue        
        try:
            print(f'读取文件:{path1}')
            keyword, summary, L, Key = read_file(path1)
            wordpress.add_article(title, keyword, summary, L, Key)
            wordpress.continue_add()
        except:
            error_doc += 1
            print(f'发布文章:{title} 失败')
            try:
                wordpress.pre_add()
            except:
                wordpress.wp_exit()
                time.sleep(30)
                raise ArithmeticError
        else:
            success_doc += 1
            print(f'发布文章:{title} 成功,准备发布下一篇')
        finally:
            print(f'文章发布进度:{success_doc}/{total_doc},失败{error_doc}篇')
            os.remove(path1)


if __name__ == "__main__":
    m = read_file(r'D:\新建文件夹\2019-03-15\现场实录国务院总理李克强回答中外记者提问.txt')
    print(m)
