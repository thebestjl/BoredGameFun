class InfiniteError(Exception):
    pass

import math
def wackyDivision(num, den, tol, incrementor):
  i = 0
  val = 1
  val_prev = val
  multiply = True
  div = 2
  if (num < den):
    multiply = False
    t_num = num
    num = den
    den = t_num
  
  b_upper = num + (num * tol)
  b_lower = num - (num * tol)
  mult_ind = 0
  av_ind = 0
  while (val * den > b_upper or val * den < b_lower):
    
    if val * den > num:
      av_ind += 1
      if (val == (val + val_prev) / div):
        if multiply:
          raise InfiniteError('Infinite loop detected during multiplication. \n\tValue was: ' + str(val) + '\n\tPrev value was: ' + str(val_prev) + '\n\tDivisor was: ' + str(div) + '\n\tMultiplier was ' + str(incrementor) + '\n\tNumerator was: ' + str(num) + '\n\tDenominator was: ' + str(den) + '\n\tTolerance was: ' + str(tol) + ' with upper bound: ' + str(b_upper) + ' lower bound: ' + str(b_lower) + '\nSucks to suck!')
        else:
          raise InfiniteError('Infinite loop detected during divison. \n\tValue was: ' + str(val) + '\n\tPrev value was: ' + str(val_prev) + '\n\tDivisor was: ' + str(div) + '\n\tMultiplier was ' + str(incrementor) + '\n\tNumerator was: ' + str(num) + '\n\tDenominator was: ' + str(den) + '\n\tTolerance was: ' + str(tol) + '\n\t\twith upper bound: ' + str(b_upper) + '\n\t\tlower bound: ' + str(b_lower) + '\nSucks to suck!')
      val = (val + val_prev) / 2
      
    else:
      mult_ind += 1
      val_prev = val
      val *= incrementor
    i += 1
  
  if not multiply:
    val = 1 / val
  return [val, incrementor, i, mult_ind, av_ind]
  

def findWackyDivisionMin(num, den, tol, lo, hi = None):
  res = []
  if hi == None:
    hi = lo
  if (num < den and lo == 2):
    raise ValueError('Cannot calculate with multiplier of 2 when dividing.')
  for i in range(lo, hi + 1):
    res.append(wackyDivision(num, den, tol, i))
  return res
  
def customTol(num, den, pad = 1):
  if (pad < 1):
    raise ValueError('padding should be at least one.')
  if pad != 1 and (pad % 10) != 0:
    print('padding should be a multiple of 10, but do you, man.')
  
  return min(1/num, 1/den) * 1/pad

def perc_diff(act, calc):
  if (act == 0 and calc == 0):
    return 0
  else:
    a = abs(act - calc)
    b = (act + calc) / 2
    return a / b * 100

def perc_err(num, den, res):
  if (num == 0 and den == 0):
    return 0
  else:
    a = num / den 
    return abs((a - res) / a) * 100
  
def print_stats(num, den, res, tol):
  tol *= 100
  p_e = perc_err(num, den, res)
  p_d = perc_diff(num / den, res)
  p_de = perc_diff(tol, p_e)
  print('percent difference: ' + str(p_d))
  print('percent error: ' + str(p_e))
  print('tolerance: ' + str(t))
  print('percent difference in error/tolerance: ' + str(p_de))
  print('remember, smaller is better for percent difference and error, and bigger is better for the percent error between the two!')
  print('and also, arbitrary statistics are arbitary. :-/')
    
def find_min(orig):
  temp = orig[0]
  print (len(orig))
  for x in range(0, len(orig)):
    if orig[x][2] < temp[2]:
      temp = orig[x]
  return temp
  
def print_res(result, orig = None):
  if orig != None:
    print('list of full results:\n')
    for lst in orig:
      print(lst)
    print('results contained ' + str(len(result)) + ' items')
  print('result: ' + str(result[0]))
  print('incrementor: ' + str(result[1]))
  print('iterations: ' + str(result[2]))
  print('incremented ' + str(result[3]) + ' times.')
  print('averaged ' + str(result[4]) + ' times.')
  
 def insertionSort(alist):
  temp = alist[0 : len(alist)]
  for i in range(1, len(temp)):

    currentvalue = temp[i]
    position = i

    while (position > 0) and (temp[position - 1][2] > currentvalue[2]):
      temp[position] = temp[position - 1]
      position = position - 1

    temp[position] = currentvalue
  
  return temp[0:10]
  

n = 1.5
d = math.sqrt(9999)
t = customTol(n, d, 15)
results = findWackyDivisionMin(n, d, t, 4, 10001)
m = find_min(results)

print_res(m)
print_stats(n, d, m[0], t)
