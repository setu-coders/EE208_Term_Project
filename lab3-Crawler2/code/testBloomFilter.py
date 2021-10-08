import bloomFilter
import random
import math
def readWordsFile(filename):
    # Open the file in read mode
    with open(filename, "r",encoding='utf-8') as file:
        allText = file.read()
        words = list(map(str, allText.split()))
        # print random string
        #print(random.choice(words))
        return words


def testBF(testSize,bitSize,words):

    falsePositiveCount = 0
    optimal_k = bloomFilter.get_optimal_k(bitSize,testSize)
    
    #print(f"Randomly choosing {(testSize)} words from {(len(words))} words")
    #print(f"BitarraySize: {(bitSize)}, k: {optimal_k}")

    myBF = bloomFilter.BloomFilter(size = bitSize, k = optimal_k)
    mySet = set()

    for i in range(testSize):
        currentword = random.choice(words)
        if myBF.find(currentword):
            if currentword not in mySet:
                falsePositiveCount += 1
        else:
            myBF.add(currentword)
            mySet.add(currentword)
    
    
    return falsePositiveCount / testSize

if __name__ == "__main__":
    N = 100
    tot = 0
    tSize = 5000
    bSize = 5 * tSize
    words = readWordsFile("words.txt")
    for testn in range(1,N+1):
        res = testBF(testSize=tSize,bitSize=bSize,words=words)
        print(f"test #{testn}, false positive rate: {res * 100}%")
        tot += res
    print(f"{N} tries, average {(tot / N * 100)} % false positive rate in {(tSize)} testset strings (chosen from {len(words)}), bitArray length:{bSize}")



