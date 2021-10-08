# -*-coding:utf-8-*-
from Bitarray import Bitarray
from BKDRHash import BKDRHash_withseed
import math
def get_optimal_k(m,n):      # m: bitset length   n:  total number of words(urls)
    return max(1,math.ceil(math.log(2) * m / n))        

def genBKDRhashseeds(k):
    seeds = [31,131]
    for i in range(2,k):
        seeds.append(seeds[i-1] * 10 + 1 + 2 * ((i + 1) % 2))
    return seeds

class BloomFilter:
    def __init__(self,size,k):  # 指定bitArray长度和k
        self.size = size
        self.k = k
        self.hashseeds = genBKDRhashseeds(k)
        print("BKDRseeds:",self.hashseeds)
        self.bits = Bitarray(size)

    def add(self,str):
        if self.find(str):  #已经存在了，不要再往里加
            return
        
        for i in range(self.k):
            setbit = BKDRHash_withseed(str,self.hashseeds[i]) % self.size   # 将hash结果映射到0～k-1
            #print(i,setbit)
            self.bits.set(setbit)
    
    def find(self,str):
        for i in range(self.k):
            getbit = BKDRHash_withseed(str,self.hashseeds[i]) % self.size   # 将hash结果映射到0～k-1
            if not self.bits.get(getbit):  # 有一bit不匹配，字符串一定不在bloomfilter中
                return False
        return True         #全部bit匹配，字符串可能在set里
