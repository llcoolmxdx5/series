''
import requests
res = requests.get("http://www.guangyukeji.com")
res.encoding = 'gb2312'
print(res.text)