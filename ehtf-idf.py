import jieba
import math


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
    print(count)
    return count


def getEFIDF(document):
    # 输入为分词后的列表列表
    weibo_list = document
    newlist = []
    for line in weibo_list:
        newlist.append(line)

    for i, sentence in enumerate(weibo_list):
        for j, key in enumerate(sentence):
            NPD = 0
            for j in range(0, i):
                for word in weibo_list[j]:
                    if word == key:
                        NPD += 1
            TNPD = i
            if NPD == 0:
                NPD = 1
            print(key)
            newlist[i][j] = {key: math.log((TNPD+1) / NPD) + 1}
    return weibo_list


def get_current_EFTFIDF():
    file = open('test.txt', 'r', encoding='utf-8')
    document = ''
    weibo_list = []
    for line in file:
        after_cut = ' '.join(jieba.cut(line.replace('\n', '')))
        document += after_cut
        line_list = after_cut.split(' ')
        weibo_list.append(line_list)
    TF = getEFTF(document)
    IDF = getEFIDF(weibo_list)
    print(TF)
    print(IDF)


if __name__ == '__main__':
    get_current_EFTFIDF()
    # string = '香农在信息论中提出的信息熵定义为自信息的期望'
    #
    # result = ' '.join(jieba.cut(string))
    # # print(result)
    # getEFTF(result)