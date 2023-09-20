import sys
import math
import os
import tokenize
from preprocess import removeSGML, tokenizeText, removeStopwords, stemWords

# thie code is not working for the output. I try to debug by my self and I found the problem is in the tokenized of the preprocess.py
# I try to debug for the preprocsee.py. Howvever, I did not find any problems. I also tried to used the tokenize package, hoever it is alos not working
# I came to many office hour and ask for gsi, they also do not how to deal with it
# Hustin help me to o througt line by line, and we did not find the bug


def indexDocument(cotent, doc_weight, query_weight, invertedIndex, docId):

    removesgml = removeSGML(cotent)
    tokenized = tokenizeText(removesgml)
    removestopwords = removeStopwords(tokenized)
    tokens = stemWords(removestopwords)

    # tokens = tokenize.generate_tokens(cotent)
    # print(tokens)
    if doc_weight is "tfc":
        for term in tokens:
            if term not in invertedIndex:
                invertedIndex[term] = []
                invertedIndex[term].append([docId, 1])
            elif invertedIndex[term][-1][0] == docId:
                invertedIndex[term][-1][1] += 1
            else:
                invertedIndex[term].append([docId, 1])
    return invertedIndex


def retrieveDocuments(query, invertedIndex, doc_weight, query_weight):

    # tokens_query = tokenize.generate_tokens(query)
    # print(tokens_query)

    removesgml = removeSGML(query)
    tokenized = tokenizeText(removesgml)
    removestopwords = removeStopwords(tokenized)
    tokens_query = stemWords(removestopwords)

    doc_set = set()
    for term in tokens_query:
        doc_list = invertedIndex.get(term, [])
        for doc_term in doc_list:
            doc_set.add(doc_term[0])

    que_dic = {}
    for term in tokens_query:
        if term not in que_dic:
            que_dic[term] = 1
        else:
            que_dic[term] += 1

    que_list = []
    if query_weight == "bfx":
        for term in que_dic:
            tf = que_dic[term]
            N = 1400.0
            if term in invertedIndex:
                n = len(invertedIndex[term])
                if n == 0:
                    tf = 0
                else:
                    tf = math.log10(N/n)
            que_list.append(tf)

    if query_weight == "tfx":
        for term in que_dic:
            tf = que_dic[term]
            N = 1400.0
            if term in invertedIndex:
                n = len(invertedIndex[term])
                if n == 0:
                    tf = 0
                else:
                    tf = math.log10(N/n)
            que_list.append(tf)

    doc_vec = {}
    if doc_weight == "bfx":
        for doc in doc_set:
            doc_weight = []
            for term in que_dic:
                tf = 0
                doc_list2 = invertedIndex.get(term, [])
                for doc_2 in doc_list2:
                    if doc_2[0] == doc:
                        tf = doc_2[1]
                N = 1400.0
                if term in invertedIndex:
                    n = len(invertedIndex[term])
                    if n == 0:
                        tf = 0
                    else:
                        tf = math.log10(N/n)
                    doc_weight.append(tf)

    if doc_weight == "tfc":
        for doc in doc_set:
            doc_weight = []
            for term in que_dic:
                tf = 0
                doc_list2 = invertedIndex.get(term, [])
                for doc_2 in doc_list2:
                    if doc_2[0] == doc:
                        tf = doc_2[1]
                N = 1400.0
                if term in invertedIndex:
                    n = len(invertedIndex[term])
                    if n == 0:
                        tf = 0
                    else:
                        tf = math.log10(N/n)
                doc_weight.append(tf)

            c = 0
            for i in range(len(que_dic)):
                c += doc_weight[i] * doc_weight[i]
            
            for j in range(len(doc_weight)):
                doc_weight[j] = doc_weight[j] / math.sqrt(c)

            doc_len = 0
            for k in range(len(doc_weight)):
                doc_len += doc_weight[k] * doc_weight[k]
            doc_len = math.sqrt(doc_len)

            que_len = 0
            for x in range(len(que_list)):
                que_len += que_list[x] * que_list[x]
            que_len = math.sqrt(que_len)

            inner = 0
            for y in range(len(que_list)):
                inner += que_list[y] * doc_weight[y]
            inner = inner / doc_len
            inner = inner / que_len
            doc_vec[doc] = inner

        sort_doc = sorted(
            doc_vec.items(), key=lambda value: value[1], reverse=True)

        return sort_doc


def main():
    doc_weight = sys.argv[1]
    query_weight = sys.argv[2]
    folder = sys.argv[3]
    test_file = sys.argv[4]

    # part A
    invertedIndex = {}
    docID = 1

    PATH = os.getcwd() + "/" + folder
    files = os.listdir(PATH)
    txt = ""
    for file in files:
        with open(os.path.join(PATH, file)) as f:
            data = f.read()
            invertedIndex = indexDocument(
                data, doc_weight, query_weight, invertedIndex, docID)
            docID += 1

    
    

    # part B
    with open('cranfield.reljudge', 'r', encoding='ISO-8859-1') as reljudge_file:
        reljudge_dic = {}
        for reljudge_line in reljudge_file.readline():
            reljudge_list = reljudge_line.split(" ")
            que_id = int(reljudge_list[0])
            doc_id = int(reljudge_list[1])
            if que_id not in reljudge_dic:
                reljudge_dic[que_id] = []
            reljudge_dic[que_id].append(doc_id)

    query_id = 1
    precision = 0
    recall = 0
    
    out = open("./cranfield.output.txt", "w+")
    with open(test_file, "r", ecoding='ISO-8859-1') as query_file:
        for query in query_file.readlines():
            reljudge_dic2 = retrieveDocuments(
                query, invertedIndex, doc_weight, query_weight)

            temp_count = 0.0
            for x, y in reljudge_dic:
                out.write(str(query_id) + " " +
                                  str(x) + " " + str(y) + "\n")
                if x in reljudge_dic(query_id):
                    temp_count += 1

            retrive = len(reljudge_dic2)
            relevant = len(reljudge_dic[query_id])
            precision += temp_count/retrive
            recall += temp_count/relevant
            query_id += 1

    recall /= 225.0
    precision /= 225.0

    # do the top N part
    
    topN = 500
    precision = 0
    recall = 0
    count = 0
    r_count = 0
    
    with open('cranfield.reljudge', 'r', encoding='ISO-8859-1') as f:  # open the file to
        for line in f:
            l = line.split(" ")
            qNum = int(l[0])
            while count < topN:  # to see whether the number is include in the N
                docID = int(l[1])
                if docID in reljudge_dic[qNum]:
                    r_count += 1
            count += 1

            precision += r_count / topN
            recall += r_count / len(reljudge_dic[qNum])

    recall /= 225.0
    precision /= 225.0

    ans = open("./cranfield.answers.txt", "w+")
    ans.write(topN, " recall: " + str(recall))
    ans.write(topN, " precision: " + str(precision))
    ans.write(" since I can not get the output, I try to discuss with my classmate and gsi from discussion, I choose the double bfx. From the calculation bfx is simple and the precision is high comapre to other methods ")


main()
