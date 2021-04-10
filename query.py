from nltk.stem import PorterStemmer
import json
import re

porter = PorterStemmer()


def main(query):

    # universal Set
    universalSetFile = open("./universalSet.txt", "r", encoding='utf8')
    universalList = universalSetFile.read()
    universalList = universalList.split()
    universalSet = set()
    for val in universalList:
        universalSet.add(int(val))
    universalSet = set(universalSet)

    # query = input('Enter Query: ')

    query = query.lower().split()
    for j in range(len(query)):
        if query[j] != 'and' and query[j] != 'or':
            query[j] = porter.stem(query[j])

    with open('./positionalIndexJSON.json') as f:
        posIndex = json.load(f)

    wordStack = []
    i = 0
    length = len(query)
    while i < length:
        if query[i] != 'and' and query[i] != 'or' and query[i] != 'not' and '/' not in query[i]:
            docNums = posIndex[query[i]].keys()
            docNums = list(map(int, docNums))
            wordStack.append(set(docNums))
            i += 1
        else:
            if i+1 < length and query[i+1] == 'not' and '/' not in query[i]:
                t2 = posIndex[query[i+2]].keys()
                t2 = set(list(map(int, t2)))
                t2 = universalSet.difference(t2)
            elif i+1 < length and '/' not in query[i]:
                t2 = posIndex[query[i+1]].keys()
                t2 = set(list(map(int, t2)))
            # print("t2: ", t2)
            if query[i] == 'and':
                t1 = wordStack.pop()
                result = t1.intersection(t2)
                wordStack.append(result)
                # i += 2
            elif query[i] == 'or':
                t1 = wordStack.pop()
                # t2 = posIndex[query[i+1]].keys()
                # t2 = set(list(map(int, t2)))
                result = t1.union(t2)
                wordStack.append(result)
                # i += 2
            elif query[i] == 'not':
                # t2 = posIndex[query[i+1]].keys()
                # t2 = set(list(map(int, t2)))
                result = universalSet.difference(t2)
                wordStack.append(result)
                # i += 2
            else:
                tokenize = query[i].split('/')
                num = int(tokenize[1])
                num += 1
                t1 = wordStack.pop()
                t1 = set(list(map(int, t1)))
                t2 = wordStack.pop()
                t2 = set(list(map(int, t2)))
                comman = t1.intersection(t2)
                result = set()
                for word in comman:
                    positionsIn1 = posIndex[query[i-1]][str(word)]
                    positionsIn2 = posIndex[query[i-2]][str(word)]
                    for pos1 in positionsIn1:
                        for pos2 in positionsIn2:
                            if pos1-pos2 == num or pos2-pos1 == num:
                                result.add(word)
                # print(result)
                wordStack.append(result)
            if '/' in query[i]:
                i+=1
            elif i+1 < length and query[i+1] == 'not':
                i += 3
            else:
                i += 2

    return wordStack.pop()
    # print("Anwser: ", wordStack.pop())


# if __name__ == "__main__":
#     main()
