import re
import requests
url = 'https://www.baidu.com/link?url=Hw7rAhLLT11B1U0XdvXYH_1SoBZm1EA1M-lLKMVfqXY9biy-2pwZTIwNcTCUPGzmM90ccsOIypCNmHhY73013q&wd=&eqid=f3ac412e0000fcd8000000065c7cbca6'
headers = {'User-Agent': "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}
res =  requests.get(url, headers=headers)
print(res.text)
regxp = r"<META.*?URL='https://news.qq.com/a/(.*?)/(.*?)\.htm'.*?>"
result = re.findall(regxp, res.text ,re.S)
# res = requests.get(result, headers=headers)
# print(res.text[:1000]) # gb2312 #Cnt-Main-Article-QQ > p
# https://new.qq.com/cmsn/20160804/20160804002185
# https://news.qq.com/a/20160804/002185.htm
url = f'https://new.qq.com/cmsn/{result[0][0]}/{result[0][0]+result[0][1]}'
print(url)
res =  requests.get(url, headers=headers)
print(res.text)
#login-box > div.login-main > form > dl > dd:nth-child(2) > input[type="text"]