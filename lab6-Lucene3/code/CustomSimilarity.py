from org.apache.pylucene.search.similarities import PythonSimilarity, PythonClassicSimilarity
import math
class SimpleSimilarity1(PythonClassicSimilarity):

    def lengthNorm(self, numTerms):
        return 1 / math.sqrt(numTerms)

    def tf(self, freq):
        return math.sqrt(freq)

    def sloppyFreq(self, distance):
        return 1 / (distance + 1)

    def idf(self, docFreq, numDocs):
        return math.log2((numDocs + 1) / (docFreq + 1))

    def idfExplain(self, collectionStats, termStats):
        return Explanation.match(1.0, "inexplicable", [])

class SimpleSimilarity2(PythonClassicSimilarity):

    def lengthNorm(self, numTerms):
        return 1 / math.sqrt(numTerms)

    def tf(self, freq):
        return math.log2(freq + 1)

    def sloppyFreq(self, distance):
        return 1 / (distance + 1)

    def idf(self, docFreq, numDocs):
        return math.log2((numDocs - docFreq) / (docFreq) + 1)

    def idfExplain(self, collectionStats, termStats):
        return Explanation.match(1.0, "inexplicable", [])