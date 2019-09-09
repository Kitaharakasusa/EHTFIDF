import jieba
import math
import re
import numpy as np
regex=re.compile('[%s]' % re.escape('[\s+\.\!\/_,$%^*(+\"\'“”’‘]+|[+——！，-。╮╯◇？、· 【〜～~@#￥%……&*（）]+?✌😉'))


def getEFTF(document):
    # 将所有文本看成一个整体的文档
    count = {}
    for word in document.split(' '):
        count[word] = count.get(word, 0) + 1
    TNAAW = 0   # 总词频数
    for key in count.keys():
        TNAAW += count[key]
    for key in count.keys():
        count[key] = count[key] / TNAAW

    return count


def getEFIDF(document):
    # 输入为分词后的列表列表
    weibo_list = document
    newlist = []
    for line in weibo_list:
        newline = []
        for word in line:
            newline.append(word)
        newlist.append(newline)

    for i, sentence in enumerate(weibo_list):
        for j, key in enumerate(sentence):
            NPD = 0
            for k in range(0, i):
                for word in weibo_list[k]:
                    if word == key:
                        NPD += 1
            TNPD = i
            if NPD == 0:
                NPD = 1
            # print(key)
            newlist[i][j] = {key: math.log((TNPD+1) / NPD) + 1}
    return newlist


def get_current_EFTFIDF():
    file = open('test.txt', 'r', encoding='utf-8')
    document = ''
    weibo_list = []
    for line in file:
        content = regex.sub("", line.replace('\n', ''))
        after_cut = ' '.join(jieba.cut(content))
        print(after_cut)
        document += after_cut + ' '
        line_list = after_cut.split(' ')
        print(line_list)
        weibo_list.append(line_list)
    print(weibo_list)
    TF = getEFTF(document)
    IDF = getEFIDF(weibo_list)
    print('TF', TF)
    print('IDF', IDF)

    for i, line in enumerate(IDF):
        for j, word in enumerate(line):
            pass
            # print(word.keys())
            index = list(word.keys())[0]
            IDF[i][j] = {index: word[index] * TF[index]}

    TF_IDF = IDF

def getTEAandEV(TF_IDF):
    TEA = set()
    all_list = []
    for line in TF_IDF:
        for word_dict in line:
            for key in word_dict.keys():
                all_list.append(word_dict[key])

    TEA.add(np.mean(all_list))



if __name__ == '__main__':
    get_current_EFTFIDF()
    # string = '香农在信息论中提出的信息熵定义为自信息的期望'
    #
    # result = ' '.join(jieba.cut(string))
    # # print(result)
    # getEFTF(result)