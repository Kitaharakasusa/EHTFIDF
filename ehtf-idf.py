import jieba
import math

def getEFTF(document):
    count = {}
    for word in document.split(' '):
        count[word] = count.get(word, 0) + 1
    TNAAW = 0   # 总词频数
    for key in count.keys():
        TNAAW += count[key]
    for key in count.keys():
        count[key] = count[key] / TNAAW
    print(count)

def getEFIDF()


if __name__ == '__main__':
    string = '香农在信息论中提出的信息熵定义为自信息的期望'
    result = ' '.join(jieba.cut(string))
    # print(result)
    getEFTF(result)