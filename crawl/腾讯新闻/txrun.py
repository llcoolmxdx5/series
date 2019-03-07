import os

from txconfig import keyword, path
from txcontent import main as contentmain
from txsave import main as savemain
from txtitle import main as titlemain

if __name__ == "__main__":
    for key in keyword:
        file_title = f'{path}\\腾讯新闻{key}title.csv'
        file_content = f'{path}\\腾讯新闻{key}content.csv'
        titlemain(key, file_title)
        contentmain(key, file_content)
        savemain(key, file_content)
        os.remove(file_title)
        os.remove(file_content)
