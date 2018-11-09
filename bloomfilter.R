#BLOOMFILTER: 
library(digest)
library(magrittr)
library(gmp)
library(Rmpfr)

vbits <- function(x,m=1000,k=7){
  vec <- rep(FALSE,m)
  for (i in 1:k) {
    for (j in 1:length(x)) {
      hash <- digest(x[j], algo = "murmur32", serialize = FALSE, seed = i) %>%
        Rmpfr::mpfr(base = 16) %% 
        m %>%
        as.integer()
      
      vec[hash + 1] <- TRUE
    }
  }
  attributes(vec) <- list(m = m, k= k)
  
  return(vec)
}
  
vect <- vbits(c("Brenner", "jesus", "lisi", "Brian", "raul","juan", "rober", 
                  "josé","Maria", "marco", "susana","jordi"), m = 1000, k = 7)
#escojí estos nombres,donde entre ellos pueden ser personas maliciosas y otras no. y mediante este programa separamos(filtramos)
#A las personas buenas de las malas
#Así como El navegador web Google Chrome que solía usar un filtro Bloom para identificar URL maliciosas
#Otros ejemplos de estos son:
#Google BigTable, Apache HBase y Apache Cassandra, y Postgresql 
#usan filtros Bloom para reducir las búsquedas en el disco para filas o columnas no existentes

is_vect <- function(x, vbits){
  k <- attr(vbits,"k")
  m <- attr(vbits,"m")
  
  for (i in 1:k) {
    hash <- digest(x,algo="murmur32",serialize = FALSE, seed=i) %>%
      Rmpfr::mpfr(base = 16)%%
      m %>%
      as.integer()
    if(!vbits[hash + 1]){
      return(FALSE)
    }
  }
  return(TRUE)
}

is_vect("Julio",vect)
is_vect("Bruno",vect)
is_vect("jose",vect)
is_vect("Luis",vect)
is_vect("pepe",vect)
is_vect("juan",vect)
#y estos nombres son las personas a los que se quiere encontrar y ver si pertenecen dentro de la 
#base de datos previamente insertados como: vect <- vbits(c("Brenner", "jesus", "lisi", "Brian", "raul","juan", "rober", 
#"josé","Maria", "marco", "susana","jordi").
#notaremos que el único implicado dentro del conjunto de personas buscadas en la base de datos solo se encontró a juan





