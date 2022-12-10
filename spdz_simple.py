import math
import random
Q = 26569515 # Really simple Sophie Germain prime

def share(secret):
  share0 = random.randrange(secret)
  share1 = (secret - share0) % Q
  return share0, share1

def reconstruct(share0, share1):
  return (share0 + share1) % Q

def generate_mul_triple():
  a = random.randrange(Q)
  b = random.randrange(Q)
  c = (a * b) % Q
  return PrivateValue(a), PrivateValue(b), PrivateValue(c)

def generate_pows_triple(exponent):
  a = random.randrange(Q)
  return [ PrivateValue(pow(a, e, Q)) for e in range(1, exponent+1)]

def powPub(x, e):
  return PublicValue(pow(x.value, e, Q))

def powPri(x, triple):
  a = triple[0]
  v = x - a
  epsilon = v.reconstruct()
  res = powPub(epsilon, len(triple))
  for i in range(1, len(triple)+1):
    res += PublicValue(math.comb(len(triple), i) % Q) * powPub(epsilon, len(triple)-i) * triple[i-1]
  return res

class PublicValue:

  def __init__(self, value):
    self.value = value

  def __add__(self, y):
    if type(y) is PublicValue:
      return PublicValue((self.value + y.value) % Q)
    else:
      share0 = (self.value + y.share0) % Q
      share1 = y.share1
      return PrivateValue(None, share0, share1)

  def __sub__(self, y):
    if type(y) is PublicValue:
      return PublicValue((self.value - y.value) % Q)
    else:
      share0 = (self.value - y.share0) % Q
      share1 = y.share1
      return PrivateValue(None, share0, share1)

  def __mul__(self, y):
    if type(y) is PublicValue:
      return PublicValue((self.value * y.value) % Q)
    else:
      share0 = (self.value * y.share0) % Q
      share1 = (self.value * y.share1) % Q
      return PrivateValue(None, share0, share1)


class PrivateValue:

  def __init__(self, value, share0=None, share1=None):
    if value is not None:
      self.share0, self.share1 = share(value)
    else:
      self.share0 = share0
      self.share1 = share1

  def reconstruct(self):
    return PublicValue(reconstruct(self.share0, self.share1))
  
  def __add__(self, y):
    if type(y) is PublicValue:
      share0 = (self.share0 + y.value) % Q
      share1 = self.share1
      return PrivateValue(None, share0, share1)
    else:
      share0 = (self.share0 + y.share0) % Q
      share1 = (self.share1 + y.share1) % Q
      return PrivateValue(None, share0, share1)

  def __sub__(self, y):
    if type(y) is PublicValue:
      share0 = (self.share0 - y.value) % Q
      share1 = self.share1
      return PrivateValue(None, share0, share1)
    else:
      share0 = (self.share0 - y.share0) % Q
      share1 = (self.share1 - y.share1) % Q
      return PrivateValue(None, share0, share1)

  def __mul__(self, y):
    if type(y) is PublicValue:
      share0 = (self.share0 * y.value) % Q
      share1 = (self.share1 * y.value) % Q
      return PrivateValue(None, share0, share1)
    else:
      a, b, c = generate_mul_triple()
      beta = (y - b).reconstruct()
      alpha = (self - a).reconstruct()
      return (alpha * beta + alpha * b + beta * a + c)


if __name__ == '__main__':

  x = PrivateValue(10)
  pow_triples = generate_pows_triple(3)
  x_trip = powPri(x, pow_triples).reconstruct()
  print(x_trip.value)