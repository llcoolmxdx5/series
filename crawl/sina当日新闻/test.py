''
from pyquery import PyQuery as pq

def parse(html):
    doc = pq(html)
    aes = doc('a').items()
    for a in aes:
        print(a.href)