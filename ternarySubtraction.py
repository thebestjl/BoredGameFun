import math

def toTernary(num):
  result = []
  val = num
  while (val >= 1):
    result.insert(0, val % 3)
    val = math.floor(val / 3)
    
  return result
  
def toBalancedTernary(tern):
  carry = 0
  result = []
  for i in range(len(tern) - 1, -1, -1):
    result.insert(0, tern[i] + carry + 1)
    
    if result[0] > 2:
      carry = 1
      
    else:
      carry = 0
      
    result[0] = result[0] % 3
    result[0] -= 1
    
  if carry == 1:
    result.insert(0, carry)
    
  return result

def subtractTern(t1, t2):
  l_t1 = len(t1)
  l_t2 = len(t2)
  dif = abs(l_t1 - l_t2)
  result = []

  if (l_t1 > l_t2):
    for i in range(l_t1 - 1, dif - 1, -1):
      result.insert(0, t1[i] + t2[i - dif])
      
    for i in range(dif - 1, -1, -1):
      result.insert(0, t1[i])

  elif (l_t2 > l_t1):
    for i in range(l_t2 - 1, dif - 1, -1):
      result.insert(0, t1[i - dif] + t2[i])
      
    for i in range(dif):
      result.insert(0, t2[i])

  else:
    for i in range(l_t1 - 1, dif - 1, -1):
      result.insert(0, t1[i] + t2[i])

  result = fixTernary(result)
  
  return result
  
def fixTernary(result):
  carry = 0
  for i in range(len(result) - 1, -1, -1):
    result[i] += carry
    
    if result[i] < -1:
      carry = -1
      
      if result[i] == -2:
        result[i] = 1
        
      else:
        result[i] = 0
    
    elif result[i] > 1:
      carry = 1
      
      if result[i] == 2:
        result[i] = -1
        
      else:
        result[i] = 0
    
    else:
      carry = 0
  
  if carry != 0:
    result.insert(0, carry)
    
  return result
  
  
def negTernary(tern):
  neg = []
  for i in range(len(tern)):
    neg.append(tern[i] * -1)

  return neg

def restoreTern(tern):
  borrow = 0
  result = []
  for i in range(len(tern) - 1, -1, -1):
    result.insert(0, tern[i] + 1)
    result[0] = result[0] - borrow - 1
    
    if (result[0] < 0):
      borrow = 1
      
    else:
      borrow = 0
    result[0] = result[0] % 3
    
  return result
  
def toDecimalFromTern(tern):
  num = 0
  for i in range(len(tern)):
    num += math.pow(3, len(tern) - 1 - i) * tern[i]
    
  return num
  
def subtraction(n, m):
  t1 = toTernary(n)
  t2 = toTernary(m)
  
  tb1 = toBalancedTernary(t1)
  tb2 = toBalancedTernary(t2)
  
  ntb2 = negTernary(tb2)
  st = subtractTern(tb1, ntb2)
  
  rt = restoreTern(st)
  num = toDecimalFromTern(rt)
  
  print_results([n, m, t1, t2, tb1, tb2, ntb2, st, rt, num])
  
def print_results(results):
  print('Expected result: ', results[0] - results[1])
  print('In ternary: ', results[2], results[3])
  print('In balanced ternary: ', results[4], results[5])
  print('Negative second arg: ', results[4], results[6])
  print('After subtraction: ', results[7])
  print('Back to standard ternary: ', results[8])
  print('Restored decimal value: ', results[9])

  