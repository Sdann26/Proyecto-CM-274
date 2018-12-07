#Codigo python del programa Blomm-filter
#Es necesario instalar los siguientes modulos
#pip install mmh3
#pip install bitarray
import math
import mmh3
from bitarray import bitarray

class BloomFilter(object):
    #Esta es la clase del Bloom Filter

    def __init__(self, items_count,prob_fp):
        #Creamos los primeros parametros del filtro
        # Probabilidad de un falso positivo
        self.prob_fp = prob_fp

        # Cantidad de elementos en el vector
        self.size = self.get_size(items_count,prob_fp)

        # numeros de funciones hash que usaremos
        self.hash_count = self.get_hash_count(self.size,items_count)

        # Tamanho de bits del vector
        self.bit_array = bitarray(self.size)

        # inicializa todos los bits en 0
        self.bit_array.setall(0)

    def add(self, item):
        #anhade un elemento al filtro
        digests = []
        for i in range(self.hash_count):
            # Creamos un digest para el elemento actual.
            # trabajaremos con distintos numeros generadores en mmh3.hash()
            # cada numero generador hara un digest diferente.
            digest = mmh3.hash(item,i) % self.size
            #anhadimos el elemento al final de la lista
            digests.append(digest)
            # Cambiamos el estado de la posicion del digest
            self.bit_array[digest] = True

    def check(self, item):
        #Hacemos la busqueda de un elemento en el filtro
        for i in range(self.hash_count):
            digest = mmh3.hash(item,i) % self.size
            if self.bit_array[digest] == False:
                # si alguno de los bits analizados es falso
                # entonces el elemento no esta en la lista
                return False
        #Si todos los bits analizados son verdaderos, entonces
        #es posible que el elemento este en la lista.
        return True

    def get_size(self,n,p):
        #Retorna el tamanho del vector(m) bit usandose la formula:
        #m = -(n * lg(p)) / (lg(2)^2)
        #n : int, numero de elementos que guardara el filtro
        #p : float, probabilidad de un falso positivo en decimales
        m = -(n * math.log(p))/(math.log(2)**2)
        return int(m)

    def get_hash_count(self, m, n):
        #Retorna la funcion(k) del hash usando la siguiente formula
        #k = (m/n) * lg(2)
        #m : int, tamanho de bits del vector
        #n : int, numero de items que se pueden almacenar en el filtro
        k = (m/n) * math.log(2)
        return int(k)
