
#
# Utilities
#

hex_with_alpha <- function(hex, alpha){
  # NB: assumes white background
  
  # hex -> rgb
  rgb_col <- col2rgb(hex)
  r <- rgb_col[1,]
  g <- rgb_col[2,]
  b <- rgb_col[3,]
  
  new_hex <- rgb(
    (1 - alpha) * 255 + alpha * r, 
    (1 - alpha) * 255 + alpha * g, 
    (1 - alpha) * 255 + alpha * b, 
    maxColorValue = 255
  )
  
  return(new_hex)
}

gaussian_mean_95_ci <- function(sample) {
  n <- length(sample)
  sample_std <- sd(sample)
  return(1.96 * sample_std / sqrt(n))
}
