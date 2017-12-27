import math

def factorize(num):
  factors = []
  while num / 2 == math.floor(num / 2):
    num /= 2
    factors.append(2)
    if num == 1:
      break

  num_range = num
    
  for i in range(3, math.floor(num_range / 2) + 1, 2):
    if i > num:
      print('This shouldn''t happen...')
      break
    
    while num / i == math.floor(num / i):
      num /= i
      factors.append(i)
      if num == 1:
        break
      
    if num == 1:
      break
    
  return factors
