from cnserchtitle import main as titlemain
from cnserchcontent import main as contentmain
from img_save import main as savemain
from config import keyword, path

if __name__ == "__main__":
    titlemain()
    for key in keyword:
        file_content = file_content = path + '\\' + key + 'content.csv'
        print(file_content)
        contentmain(key, file_content)
        savemain(file_content)







