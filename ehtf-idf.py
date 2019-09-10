import jieba
import math
import re
import numpy as np
regex=re.compile('[%s]' % re.escape('[\s+\.\!\/_,$%^*(+\"\'“”’‘]+|[+——！，-。╮╯◇？、· 【〜～~@#￥%……&*（）]+?✌😉'))

TEA = []


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

    to_now_word_nums = {}

    for i, sentence in enumerate(weibo_list):
        for j, key in enumerate(sentence):
            NPD = 0
            if key in to_now_word_nums.keys():
                NPD += to_now_word_nums[key]
                nums = to_now_word_nums[key]
                to_now_word_nums[key] = nums+1
            else:
                to_now_word_nums[key] = 1
            # for k in range(0, i):
            #     for word in weibo_list[k]:
            #         if word in to_now_word_nums.keys():
            #         if word == key:
            #             NPD += 1
            TNPD = i
            if NPD == 0:
                NPD = 1
            # print(key)
            newlist[i][j] = {key: math.log((TNPD+1) / NPD) + 1}
    return newlist


def get_current_EFTFIDF():
    file = open('cont.txt', 'r', encoding='utf-8')
    document = ''
    weibo_list = []
    for line in file:
        if line != '\n':
            content = regex.sub("", line.replace('\n', ''))
            after_cut = ' '.join(jieba.cut(content))
            document += after_cut + ' '
            line_list = after_cut.split(' ')
            print(line_list)
            weibo_list.append(line_list)
    # print(document)
    # print(weibo_list)
    print('start get EFTF')
    TF = getEFTF(document)
    print('start get EFIDF')
    IDF = getEFIDF(weibo_list)
    print('idf finish')


    for i, line in enumerate(IDF):
        for j, word in enumerate(line):
            # print(word.keys())
            index = list(word.keys())[0]
            IDF[i][j] = {index: word[index] * TF[index]}

    TF_IDF = IDF
    return TF_IDF


def getTEAandEV():
    TF_IDF = get_current_EFTFIDF()
    all_list = []
    EV = {}

    for line in TF_IDF:
        for word_dict in line:
            # print(line)
            for key in word_dict.keys():

                if key in EV.keys():
                    # print(EV[key])
                    now_list = EV[key]
                    now_list.append(word_dict[key])
                    EV[key] = now_list
                else:
                    evlist = [word_dict[key]]
                    EV[key] = evlist
                all_list.append(word_dict[key])

    TEA.append(np.mean(all_list))

    return TEA, EV


def isRWDM():
    TEA, EV = getTEAandEV()

    TEVMA = TEA
    tea_len = 0
    if len(TEA) >= 3:
        TEVMA = TEA[-1] + TEA[-2] + TEA[-3]
        tea_len = 3
    else:
        for i in range(len(TEA)):
            tea_len += 1
            TEVMA += TEA[i]
    TEVMA = TEVMA / tea_len

    EVMA = 0
    evma_len = 0
    last_rwdm_and_value = []
    for key in EV.keys():
        if len(EV[key]) >= 3:
            EV_list = EV[key]
            EVMA = EV_list[-1] + EV_list[-2] + EV_list[-3]
            evma_len = 3
        else:
            for i in range(len(EV[key])):
                evma_len += 1
                EVMA += EV[key][i]
        EVMA = EVMA / evma_len
        if EVMA > TEVMA[0]:
            res = [key, EVMA]
            last_rwdm_and_value.append(res)

    return last_rwdm_and_value


if __name__ == '__main__':
    last_rwdm_and_value = isRWDM()
    print(sorted(last_rwdm_and_value, key=(lambda x: x[1])))
    # getTEAandEV()
    # get_current_EFTFIDF()
    # string = '香农在信息论中提出的信息熵定义为自信息的期望'
    #
    # result = ' '.join(jieba.cut(string))
    # # print(result)
    # getEFTF(result)