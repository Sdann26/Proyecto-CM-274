from bitarray import bitarray
from hashlib import sha1
from math import ceil
from math import log
from math import pow
from sys import getsizeof

def get_SHA1_bin(elemento):
    """
    Retorna el hash 'Secure Hash Algorithm - 1' de un elemento
    """
    hash_s = sha1()
    hash_s.update(elemento)
    return bin(long(hash_s.hexdigest(),16))[2:].zfill(160)

def get_index(binString,endIndex=160):
    """
    Devuelve la posicion del primer bit 1
    desde la izquierda del elemento hasta el final 'endIndex'
    """
    res = -1
    try:
        res = binString.index('1')+1
    except(ValueError):
        res = endIndex
    return res

class HyperLogLog(object):
    """
    Implementacion HyperLogLog
    """

    def __init__(self, maxCardinality, error_rate):
        """
        Implementamos los datos iniciales
        hace una estimacion de los valores unicos ingresados con un porcentaje
        de error.
        """
        #Algunos valores preestablecidos para alfa
        self.__ALPHA16=0.673
        self.__ALPHA32=0.697
        self.__ALPHA64=0.709

        if not (0 < error_rate < 1):
            raise ValueError("Error_Rate debe estar entre 0 y 1.")
        if not maxCardinality > 0:
            raise ValueError("El numero de carninales debe ser > 0")

        self._maxCardinality = maxCardinality
        self._k = int(round(log(pow(1.04/error_rate,2),2)))
        self._bucketNumber = 1<<self._k
        self._bucketSize = self._wordSizeCalculator(self._maxCardinality)
        self._bucketList =[0 for _ in xrange(self._bucketNumber)]
        self._alpha = self.__getALPHA(self._bucketNumber)


    def __getALPHA(self,m):
        if m <=16:
            return self.__ALPHA16
        elif m<=32:
            return self.__ALPHA32
        elif m<=64:
            return self.__ALPHA64
        else:
            return 0.7213/(1+1.079/float(m))

    def add(self,item):
        """
        anhadimos un elemento al HyperLogLog
        """
        binword = get_SHA1_bin(item)
        pos = int(binword[:self._k],2)
        #Retrives the position of leftmost 1
        aux = get_index(binword[self._k:],160-self._k)
        # Sets its own register value to maximum value seen so far
        self._bucketList[pos] = max(aux,self._bucketList[pos])



    def getNumberEstimate(self):
        """
        Devuelve la estimacion de valores unicos
        """
        m = self._bucketNumber
        raw_e = self._alpha*pow(m,2)/sum([pow(2,-x) for x in self._bucketList])
        if raw_e <= 5/2.0*m:
            v = self._bucketList.count(0)
            if v!=0:
                return m*log(m/float(v),2)
            else:
                return raw_e
        elif raw_e <= 1/30.0*2**160:
            return raw_e
        else:
            return -2**160*log(1-raw_e/2.0**160,2)

    def __sizeof__(self):
        return self._bucketNumber* self._bucketSize

    def _wordSizeCalculator(self,Nmax):
        """
        Devuelve la estimacion del tamanho de memoria, que usan el cardinal maximo como argumento
        """
        return int(ceil(log(log(Nmax,2),2)))
