from spdz_parser import *
from spdz_simple import *


def generate_triples(exp):
  if type(exp) is Num:
    exp.share = share(exp.value)
  elif type(exp) is Var: return
  else:
    generate_triples(exp.left)
    generate_triples(exp.right)
    if exp.op.op == "*":
      a, b, c = generate_mul_triple()
      exp.a = a
      exp.b = b
      exp.c = c
    elif exp.op.op == "^":
      if type(exp.right) is Num:
        exp.shares = generate_pows_triple(exp.right.value) 