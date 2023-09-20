import os
import math


def trainBigramLanguageModel(string):
    list = string.split()
    s = "".join(list)
    d1 = {}
    d2 = {}

    for i in range(len(s)):
        t = s[i]
        if t not in d1:
            d1[t] = s.count(t)

    v = len(d1)

    for i in range(len(s)-1):
        t = s[i:i+2]
        if t not in d2:
            d2[t] = s.count(t)
    return (d1, d2, v)


def identifyLanguage(input_str, list_of_str, list_of_dic_uni, list_of_dic_bi):
    list = input_str.split()
    s = "".join(list)
    v_1 = len(list_of_dic_uni)
    list_p = []
    for train in range(0, 3):
        probaility_total = 1

        for i in range(len(s)-1):
            if s[i]+s[i+1] not in list_of_dic_bi[train]:
                numerator = 1
            else:
                numerator = list_of_dic_bi[train][s[i]+s[i+1]]+1
            if s[i] not in list_of_dic_uni[train]:
                denominator = 1
            else:
                denominator = list_of_dic_uni[train][s[i]]+v_1
            p = math.log(numerator/denominator)
            probaility_total = probaility_total*p
        list_p.append(probaility_total)
    language = sorted(zip(list_p, list_of_str), key=lambda x: x[0])
    return language[0][1]


def main():
    ans = open("./languageIdentification.answers.txt", "w+")
    out = open("./languageIdentification.output", "w+")

    PATH = "/Users/chengqingyun/Desktop/training/"
    files = os.listdir(PATH)
    list_of_dic_uni = []
    list_of_dic_bi = []
    list_v = list()
    for file in files:

        with open(os.path.join(PATH, file), encoding='iso-8859-1') as f:
            data = f.read()
            a, b, c = trainBigramLanguageModel(data)
            list_of_dic_uni.append(a)
            list_of_dic_bi.append(b)
            list_v.append(c)

    PATH2 = "/Users/chengqingyun/Desktop/test/"
    files = os.listdir(PATH2)
    for file in files:
        with open(os.path.join(PATH2, file), encoding='iso-8859-1') as f:
            count = 0
            list_o = []
            lines = f.readlines()
            for line in lines:
                language = identifyLanguage(line, ["English", "French", "Italian"],
                                            list_of_dic_uni, list_of_dic_bi)
                count += 1
                out.write(str(count) + " "+language+'\n')
                list_o.append(language)

    PATH3 = "/Users/chengqingyun/Desktop/solution/"
    files = os.listdir(PATH3)
    for file in files:
        with open(os.path.join(PATH3, file), encoding='iso-8859-1') as f:
            list_s = []
            correct = 0
            count_1 = 0
            solution = f.readlines()
            for i in solution:
                if i.split()[1] == list_o[count_1]:
                    correct += 1
                count_1 += 1
            ans.write(str(correct*100/300))

main()
