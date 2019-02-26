import pymysql
import warnings
from time import time
# 数据库配置
HOST = 'localhost'
USER = 'root'
PASSWORD = '1342a4b5e9'
PORT = 3306
DB = 'dedecmsv57utf8sp2'
# 参数设置
aid = 8
typeid = 5

warnings.filterwarnings("ignore") # 去掉警告
# 连接数据库
db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=PORT, db=DB)
cursor = db.cursor()

def insert_dede(title, body):
    '''
    插入文章标题对应的表
    :param title: 文章标题
    :param body: 文章内容
    '''
    global aid
    if judge_duplicate(title):
        return
    t = int(time())
    sql_1 = f'INSERT INTO dede_archives(id, typeid, sortrank, ismake, title, pubdate, senddate, weight) VALUES \
           ({aid}, {typeid}, {t}, 1, "{title}", {t}, {t-100}, 1)'
    sql_2 = f'INSERT INTO dede_addonarticle(aid, typeid, body) VALUES ({aid}, {typeid}, "{body}")'
    sql_3 = f'INSERT INTO dede_arctiny(id, typeid, senddate, sortrank, mid) VALUES ({aid}, {typeid}, {t}, {t-100}, 1)'
    try:
        cursor.execute(sql_1)
        try:
            cursor.execute(sql_2)
            db.commit()
        except Exception as e:
            print(e)
            cursor.execute(f'DELETE FROM dede_archives WHERE (id={aid})')
            db.commit()
            return
        cursor.execute(sql_3)
        db.commit()
        aid += 1
    except:
        db.rollback()


def select_aid():
    '''
    查询文章应该从哪插入数据库
    '''
    global aid
    sql = f'SELECT MAX(id) FROM dede_archives where typeid={typeid};'
    cursor.execute(sql)
    aid = cursor.fetchone()[0] + 1
    print(aid)

def close_db():
    db.close

def main():
    select_aid()
    insert_dede('title1', 'aDASDAS')
    db.close()

def judge_duplicate(title):
    sql = f'SELECT id FROM dede_archives WHERE title="{title}";'
    cursor.execute(sql)
    m = cursor.fetchone()
    if m:
        return False
    else:
        return True

select_aid()

if __name__ == "__main__":
    main()
