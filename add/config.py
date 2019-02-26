DISPLAY_BROSER = True # 控制是否显示浏览器界面 True OR False
                       # 不显示时减少对电脑性能和带宽的影响,速度会更快

FONT_SIZE = 14 # 字号默认为14px

CONFIRM_KEYSUMM = False # 控制读取文本第一行为关键词, 第二行为摘要 True OR False
                       # 为False时全文本内容为文章内容

AUTO_KEYWORD = False # 控制开启自动关键词功能 True OR False
                     # 启用该功能须在命令行中输入 pip install jieba 显示successfully即成功安装
                     # 自动生成的关键词会加在手动填写的关键词后

AUTO_SUMMARY = False # 控制开启自动摘要功能 True OR False
                     # 此功能为True时须保证 CONFIRM_KEYSUMM = False
                     # 此功能作用为自动读取文本第一行为文章摘要 若第一行为空则为接下来不为空的一行
