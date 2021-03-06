import os
import time
import warnings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from config import AUTO_KEYWORD, CONFIRM_KEYSUMM, DISPLAY_BROSER, FONT_SIZE, AUTO_SUMMARY

try:
    import jieba.analyse
except Exception as e:
    print(e)


warnings.filterwarnings("ignore")


class DedeAddArticle:
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
        self.browser.implicitly_wait(20)
    
    def exit(self):
        self.browser.close()
    
    def __click(self, selector):
        self.browser.find_element_by_css_selector(selector).click()
    
    def __sendkeys(self, selector, sendkeys):
        self.browser.find_element_by_css_selector(selector).send_keys(sendkeys)

    def login(self):
        uname_selector = '#login-box > div.login-main > form > dl > dd:nth-child(2) > input[type="text"]'
        upwd_selector = '#login-box > div.login-main > form > dl > dd:nth-child(4) > input'
        submit_selctor = '#login-box > div.login-main > form > dl > dd:nth-child(6) > button'
        self.browser.get(self.url)
        self.__sendkeys(uname_selector, self.uname)
        self.__sendkeys(upwd_selector, self.upwd)
        # time.sleep(20)
        self.__click(submit_selctor)
    
    def error(self):
        self.browser.switch_to_default_content()
    
    def column(self):
        time.sleep(10)
        maincolumn_selector = f'body > table > tbody > tr:nth-child(4) > td > table:nth-child({self.maincolumn}) > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > a:nth-child(2)'
        webcolumn_selector = '#items1_1 > ul > li:nth-child(1) > div > div.fllct > a'
        add_selector = 'body > table > tbody > tr > td > table > tbody > tr > td > input:nth-child(1)'
        self.browser.switch_to_frame('menufra')
        self.__click(webcolumn_selector)
        self.browser.switch_to.default_content()
        self.browser.switch_to_frame('main')
        if int(self.subcolumn_selector):
            self.select_subcolumn()
        else:
            self.__click(maincolumn_selector)
        self.__click(add_selector)
    
    def select_subcolumn(self):
        maincolumn_expand_selector = f'body > table > tbody > tr:nth-child(4) > td > table:nth-child({self.maincolumn}) > tbody > tr:nth-child(1) > td:nth-child(1) > img'
        subcolumn_selector = f'#suns{self.maincolumn_id} > table > tbody > tr:nth-child({str(int(self.subcolumn)*2 -1)}) > td > table > tbody > tr > td:nth-child(1) > a:nth-child(3)'
        try:
            self.__click(subcolumn_selector)
        except:
            self.__click(maincolumn_expand_selector)
            self.__click(subcolumn_selector)

    def add_article(self, title, keyword, summary, L, img_L, tag=''):
        title_selector = '#title'
        tag_selector = '#tags'
        keyword_selector = '#keywords'
        save_selector = 'body > form > table:nth-child(8) > tbody > tr > td:nth-child(2) > input'
        sourcecode_selector = '#cke_8' 
        body_selector = '#cke_contents_body > textarea'
        summary_selector = '#description'
        self.__sendkeys(title_selector, title)
        self.__sendkeys(tag_selector, tag)
        self.__sendkeys(keyword_selector, keyword)
        self.__sendkeys(summary_selector, summary)
        self.__click(sourcecode_selector)
        for line in L:
            self.__sendkeys(body_selector, line)
            self.__sendkeys(body_selector, Keys.ENTER)
        self.__click(save_selector)

    def continue_add(self):
        continue_selector = 'body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > div > a:nth-child(1) > u'
        self.__click(continue_selector)
    
    def add_img(self, imgpath):
        sourcecode_selector = '#cke_8'
        # img_selector = '#cke_27'
        # imgupload_selector = '#cke_dialog_tabs_84 > #cke_Upload_143'
        file_selector = 'body > form > input[type="file"]'
        upload2server_selector = '#cke_140_labelifame'
        imgconfirm_selector = '#cke_172_label'
        # body_selector = '#cke_contents_body > textarea'
        # imgerror_selector = '#cke_dialog_close_button_84'
        error_selector = '#cke_dialog_close_button_84'
        js1 = 'document.getElementById("cke_27").click();'
        js2 = 'var tabs = document.getElementById("cke_dialog_tabs_84");tabs.children[2].click()'
        try:
            self.__click(sourcecode_selector) # 1
            # self.__click(img_selector) # 2
            self.browser.execute_script(js1)
            self.browser.execute_script(js2)
            # self.__click(imgupload_selector) # 3
            self.browser.switch_to_frame('cke_138_fileInput') # 4
            self.__sendkeys(file_selector, imgpath)
            self.__click(upload2server_selector) # 5
            self.browser.switch_to.parent_frame()
            self.__click(imgconfirm_selector) # 6
            self.__click(sourcecode_selector) # 7
        except:
            print(f'添加图片:{imgpath} 失败')
            self.browser.switch_to.default_content()
            self.browser.switch_to_frame('main')
            self.__click(error_selector)


def autokeyword(path):
    with open(path) as f:
        content = f.read()
    keys = jieba.analyse.extract_tags(content, topK=3, allowPOS=('ns', 'n', 'vn', 'v', 'i', 'l', 'nr', 'nt', 'nz'))
    return ','.join(keys)


def read_file(path1): 
    img_L = []
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
    return keyword, summary, L, img_L


def main(url, user, password, maincolumn, subcolumn_selector, maincolumn_id, subcolumn, path):
    dede = DedeAddArticle(url, user, password, maincolumn, subcolumn_selector, maincolumn_id, subcolumn)
    print('正在初始化')
    dede.login()
    print('登录成功')
    dede.column()
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
            keyword, summary, L, img_L = read_file(path1)
            dede.add_article(title, keyword, summary, L, img_L)
            dede.continue_add()
        except Exception as e:
            error_doc += 1
            print(f'发布文章:{title} 失败')
            print(e)
            dede.error()
            dede.column()
        else:
            success_doc += 1
            print(f'发布文章:{title} 成功,准备发布下一篇')
        finally:
            print(f'发布文章进度:{success_doc}/{total_doc},失败{error_doc}篇')
    print('发布文章结束')
    dede.exit()
