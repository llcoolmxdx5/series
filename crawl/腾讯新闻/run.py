from config import path, path1, keyword
from txtitle import main as titlemain
from txcontent import main as contentmain

if __name__ == "__main__":
    for key in keyword:
        file_title = f'{path}\\腾讯新闻{key}title.csv'
        file_content = f'{path}\\腾讯新闻{key}content.csv'
        titlemain(key, file_title)
        contentmain(key, file_content)
