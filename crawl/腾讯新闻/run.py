from config import path, path1, keyword
from txtitle import main as titlemain

if __name__ == "__main__":
    for key in keyword:
        file_title = f'{path}\\腾讯新闻{key}title.csv'
        print(file_title)
        titlemain(key, file_title)
