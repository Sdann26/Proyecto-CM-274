
from HLL import HyperLogLog
from HLL import get_SHA1_bin

a = HyperLogLog(2000000,0.05)
b = HyperLogLog(2000000,0.05)
c = HyperLogLog(2000000,0.05)

for i in xrange(100000):
    a.add(str(i))
for i in xrange(1500):
    b.add(str(i))
for i in xrange(100000,200000):
    c.add(str(i))

print "1-100000 elementos aleatorios ingresados - Conteo estimado: ", a.getNumberEstimate()
print "1500 elementos aleatorios ingresados - Conteo estimado: ", b.getNumberEstimate()
print "100000-200000 elementos aleatorios ingresados - Conteo estimado: ", c.getNumberEstimate()
