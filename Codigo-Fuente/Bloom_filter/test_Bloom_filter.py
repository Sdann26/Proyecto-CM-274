from Bloom_filter import BloomFilter
from random import shuffle

n = 20 #numero de elementos que se anhadiran
p = 0.05 #probabilidad de falso positivo

bloomf = BloomFilter(n,p)
print("Tamanho de bits del vector:{}".format(bloomf.size))
print("Probabilidad de falso positivo:{}".format(bloomf.prob_fp))
print("Numero de funciones hash:{}".format(bloomf.hash_count))

# elementos a anhadir
elementos_presentes = ['hola','avion','sugerencia','optimismo','CM274',
				'persona','cuerda','sujeto','auto','tren','linterna',
				'coherente','agregado','paz','colores','comedia',
				'dientes','pelota','amable','generosidad','genial']

# elementos no anhadidos para prueba
elementos_nopresentes = ['salud','fiesta','suceso','pelea','guitarra',
			'viaje','apacible','ventaja','google','estatua',
			'trabajador','desfile']

#anhadiremos los elementos a la lista
for item in elementos_presentes:
	bloomf.add(item)

shuffle(elementos_presentes)
shuffle(elementos_nopresentes)

test_elementos = elementos_presentes[:10] + elementos_nopresentes
shuffle(test_elementos)
for word in test_elementos:
	if bloomf.check(word):
		if word in elementos_nopresentes:
			print("'{}' es un falso positivo".format(word))
		else:
			print("'{}' probablemente esta en la lista".format(word))
	else:
		print("'{}' No esta en la lista".format(word))
