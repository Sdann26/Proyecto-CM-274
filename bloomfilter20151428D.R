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
  
vect <- vbits(c("Brenner", "Bustillos", "Robles", "Brian", "20151428D",
                              "123456"), m = 1000, k = 7)


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

is_vect("B",vect)
is_vect("Brian",vect)
is_vect("Bren",vect)







