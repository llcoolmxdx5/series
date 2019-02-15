with open('./similarword.txt', 'r', encoding='utf-8') as fr:
    word_dict = {}
    try:
        while True:
            s = fr.readline()[:-1]
            l1 = s.split(' ')
            word_dict[l1[0]] = l1[1]
    except:
        pass
    result = word_dict.get('人', '')
    if result:
        print(result)
    