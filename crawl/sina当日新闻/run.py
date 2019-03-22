import sys
import os
from datetime import datetime, timedelta

from sinatitle import main as titlemain
from sinacontent import main as contentmain
from sinasave import main as savemain


now_date = datetime.today().day() - timedelta(days=1)
result_path = f'D:\\sina\\{now_date}'

path = sys.path[0]
file_title = f'{path}\\新浪新闻{now_date}title.csv'
file_content = f'{path}\\新浪新闻{now_date}content.csv'

if __name__ == "__main__":
    titlemain(now_date, file_title)
    contentmain(file_title, file_content)
    savemain(now_date, file_content, result_path)
    # os.remove(file_title)
    # os.remove(file_content)
