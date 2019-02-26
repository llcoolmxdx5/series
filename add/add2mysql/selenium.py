import time
import requests
from selenium import webdriver
# from PIL import Image
# import tesserocr

browser = webdriver.Chrome()
browser.get('https://28835533.com/Register')
browser.maximize_window()
time.sleep(5)
try:
    closed = browser.find_element_by_css_selector('#marquee > footer > span')
    closed.click()
except:
    pass


def register(uname,upwd,cupwd,cash_pwd,real_name,sex):
    '''
    自动填入数据进行注册
    '''
    user_name = browser.find_element_by_css_selector('#articles > div.ng-scope > form > fieldset:nth-child(1) > div:nth-child(3) > div.control-div > input')
    user_name.send_keys(uname) #用户名

    user_pwd = browser.find_element_by_css_selector('#articles > div.ng-scope > form > fieldset:nth-child(1) > div:nth-child(4) > div.control-div > input')
    user_pwd.send_keys(upwd) #用户密码
    time.sleep(1)
    user_config = browser.find_element_by_css_selector('#articles > div.ng-scope > form > fieldset:nth-child(1) > div:nth-child(5) > div.control-div > input')
    user_config.send_keys(cupwd) #确认密码

    user_cash_pwd = browser.find_element_by_css_selector('#articles > div.ng-scope > form > fieldset:nth-child(1) > div:nth-child(6) > div.control-div > input')
    user_cash_pwd.send_keys(cash_pwd) #取款密码

    user_real_name = browser.find_element_by_css_selector('#fieldset-more-option > div:nth-child(2) > div.control-div > input')
    user_real_name.send_keys(real_name) #真实姓名

    if sex=='man':
        user_sex = browser.find_element_by_css_selector('#fieldset-more-option > div:nth-child(3) > div > label:nth-child(1) > input')
    elif sex=='women':
        user_sex = browser.find_element_by_css_selector('#fieldset-more-option > div:nth-child(3) > div > label:nth-child(2) > input')
    user_sex.click() #选择性别
    time.sleep(1)
    # 验证码
    vertify_code = browser.find_element_by_css_selector('#checkcode-input-group > input')
    vertify_code.click()
    # code = vertificate_code()
    
    time.sleep(1)
    # vertify_code.send_keys(code)
    time.sleep(20)

    submit = browser.find_element_by_css_selector('#btn-submit')
    submit.click() #提交注册

    time.sleep(2)
    ok = browser.find_element_by_css_selector('body > div.modal.fade.custom-modal.in > div > div > div.cms-modal-footer.ng-scope > button.btn.btn-confirm')
    ok.click()
    time.sleep(5)
# checkcode-input-group > span > img

# def vertificate_code():
#     '''
#     验证码识别
#     '''
#     browser.save_screenshot('D:\\aa.png')
#     img = browser.find_element_by_css_selector('#checkcode-input-group > span > img')
#     location = img.location
#     size = img.size
#     rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height']))
#     i = Image.open("D://aa.png")
#     frame4 = i.crop(rangle)
#     frame4.save('d://frame4.png')
#     qq = Image.open('d://frame4.png')
#     code = tesserocr.image_to_text(qq).strip()
#     print(code)
#     return code

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
# }

# url = '/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAASACgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD1a8v7XTohLfXcFtGTtDzyKgY+mT34qte63Z2WhzawJRc2cUZffbkOJB04I4zn8P6c9rlpe23j7Sdamtp7rTYYHi/cRNK0MhB+bYoJ54GQO30rKsNL16Hw34nmsrLYL+4aS0s7mMZ2EkMSjcAkdFI7dOleYoLlvf8Aq9rfqbOrJT5bf1a9/wBPU39P8XTTajplpfWCQf2lbG4tpIbjzRgDcQ/yrtOPTIrUTxNockixx63pruxAVVu4yWJ7DnrXFaFof2LxDYSaDY30NpLC39oLfWpQRZUD5GdQdxPUKSDgdhx0SeHNHi1O1trTSbICxVZZZlgTzCw/1a7sZ3cFj9B/eq5xgn/Xn/XmRTnVa/rsv+D6Gyus6a199hXUrNrwMV+zidPMJ7jbnORRXmrmO4uLGD/hF/ENnp1jeG4iggsWdpGzncZGb5Qe6gH688FNULrr/XzJlimna39fcetUUUVgdgVi+G2Lw6i7Esx1G4BY8kgPgfkAB9AKKKcevp+qJl09f0ZtUUUUij//2Q=='
# import base64

# res = requests.get(url=url, headers=headers)
# imgdata=base64.b64decode(url)
# with open('D://1.png', 'wb') as f:
#     f.write(imgdata)
# qq = Image.open('d://1.png')
# code = tesserocr.image_to_text(qq).strip()
# print(code)
if __name__ == "__main__":
    register('pythontest124', 'a123456', 'a123456', 123456, '算法', 'man')





