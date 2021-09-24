from Bitarray import Bitarray
class BloomFilter:
    def __init__(self,size,k):
        self.size = size
        self.k = k
        self.bits = Bitarray(size)
    
    def add(self,str):
        for i in range(self.k):
            pass
