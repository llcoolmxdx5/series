import requests

def main():
    '''
    先请求页面维持会话和取得页面隐藏字段token
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }
    session = requests.Session() #会话维持
    data = {
        'gotopage':'%2Fc4w96%2F',
        'dopost':'login',
        'adminstyle':'newdedecms',
        'userid':'charlice',
        'pwd':'charlice',
        'sm1':''
    }
    url = 'http://www.wlovet.com/c4w96/login.php'
    res = session.post(url, headers=headers, data=data)
    restext = res.text
    print(res.request.headers)
    print(restext)
    print(res.cookies)
    res = session.get('http://www.wlovet.com/c4w96/index.php')
    restext = res.text
    print(res.request.headers)
    print(restext)

def get_page(session):
    pass





if __name__ == "__main__":
    main()















