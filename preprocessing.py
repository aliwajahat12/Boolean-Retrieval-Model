import string
import nltk
import re
import json

from nltk.stem import PorterStemmer
porter = PorterStemmer()
overallPosIndex = {}


def main():

    stopwordsFile = open("./Stopword-List.txt", "r", encoding='utf8')
    stopwords = stopwordsFile.read()

    universalSet = set()

    for i in range(1, 51):
        f = open("./ShortStories/" + str(i) + ".txt", "r", encoding='utf8')

        universalSet.add(i)

        fileContents = f.read()
        f.close()
        # print("With: ", len(fileContents))
        fileContents = re.sub(r'[^\w\s]', '', fileContents)

        fileContents = fileContents.lower().split()

        # contentWithoutStopWords = [word for word in fileContents if word.lower() not in stopwords ]
        contentWithoutStopWords = fileContents

        results = contentWithoutStopWords
        for j in range(len(results)):
            results[j] = porter.stem(results[j])
        # print("Without: ", len(results))

        posIndex = {}
        for j in range(len(results)):
            results[j] = results[j].lower()
            if results[j] not in stopwords:
                if posIndex.get(results[j]) == None:
                    posIndex[results[j]] = {j}
                else:
                    posIndex[results[j]].add(j)

        # print(posIndex)

        for key, value in posIndex.items():
            if overallPosIndex.get(key) == None:
                overallPosIndex[key] = {str(i): list(value)}
            else:
                # overallPosIndex[key].add({str(i) : list(value)})
                overallPosIndex[key][str(i)] = list(value)

    f = open("./positionalIndexJSON.json", "w")
    json.dump(overallPosIndex, f)
    f.close()
    f = open("./universalSet.txt", "w")
    for val in universalSet:
        f.write(str(val)+'\n')
    f.close()


if __name__ == "__main__":
    main()
