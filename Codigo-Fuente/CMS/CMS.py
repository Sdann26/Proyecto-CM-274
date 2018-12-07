import hashlib
import array


class CountMinSketch(object):

    def __init__(self, m, d):
        """
        m es el tamanho de las tablas hash.
        d es la cantidad de tablas hash.
        Numeros mas grandes significan menos colisiones.
        """
        if not m or not d:
            raise ValueError("El tamanho (m) y la cantidad de funciones hash (d)"
                             " no deben ser 0")
        self.m = m
        self.d = d
        self.n = 0
        #Tabla hash
        self.tables = []
        for _ in xrange(d):
            #Creamos un array de tamanho m, todos en 0
            table = array.array("l", (0 for _ in xrange(m)))
            #Lo agregamos a la tabla hash
            self.tables.append(table)

    def _hash(self, x):
        #Se calcula el hash del elemento x
        #usamos Message-Digest Algorithm 5
        md5 = hashlib.md5(str(hash(x)))
        #Se hace un generador de tamanho d
        for i in xrange(self.d):
            md5.update(str(i))
            #El resultado esta restringido para el tamanho de la tabla m
            #y lo retorna
            yield int(md5.hexdigest(), 16) % self.m

    def add(self, x, value=1):
        """
        Cuenta del elemento `x` la candidad de apariciones `value`.
        por defecto el contador sera de uno en uno `value=1`
            sketch.add(x)
        """
        #El numero de elementos aumenta en 1
        self.n += value
        #Se aumentan en uno las posiciones que da el generador _hash()
        #en la tabla
        for table, i in zip(self.tables, self._hash(x)):
            table[i] += value

    def query(self, x):
        """
        Devuelve la cantidad de veces que el elemento `x` ha aparecido.
        siempre es una sobreestimacion del valor real.
        """
        #Se Busca el menor numero de las apariciones de cada hash para X
        return min(table[i] for table, i in zip(self.tables, self._hash(x)))

    def __getitem__(self, x):
        """
        Se hace el llamado de query()
        """
        return self.query(x)

    def __len__(self):
        """
        Retorna la cantidad de elementos ingresados.
        en el argumento de `add` podria ser distinto de 1.
        """
        return self.n
