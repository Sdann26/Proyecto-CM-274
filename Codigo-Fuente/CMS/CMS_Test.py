from CMS import CountMinSketch
from random import shuffle

m=20
d=4

CountMS=CountMinSketch(m,d)
print("Tamanho de la tabla:{}".format(CountMS.m))
print("Numero de hash:{}".format(CountMS.d))

CountMS.add('Hola')
CountMS.add('Hola')
CountMS.add('Hi')
print("el numero de veces que aparece Hola es {}".format(CountMS.__getitem__('Hola')))
print("Numero de elementos ingresados:{}".format(CountMS.__len__()))
