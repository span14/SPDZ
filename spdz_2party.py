import json
from spdz_parser import *
from spdz_trusted import *
import sys


# Parse expressions
with open("expression.conf", "r") as f:
  raw_expression = f.readlines()[0].strip()
  print(raw_expression)

tokens = tokenization(raw_expression)
exp = parser_e(tokens)

# Simulation Purpose
# Check missing party inputs
with open("party_x.json", "r") as f:
  input_x = json.load(f)
with open("party_y.json", "r") as f:
  input_y = json.load(f)
for token in tokens:
  if type(token) is Var:
    if "x" in token.name:
      if input_x.get(token.name) is None:
        print("Missing input:", token.name)
        sys.exit(1)
    if "y" in token.name:
      if input_y.get(token.name) is None:
        print("Missing input:", token.name)
        sys.exit(1)

# Trusted setup for exponential as well as multiplication function
# share0 belongs to party x and share1 belongs to party y
generate_triples(exp)


# Generate shares to the other party
# index 0 belongs to party x and index 1 belongs to party y
shares_x = {}
for x in input_x:
  shares_x[x] = share(input_x[x])

shares_y = {}
for y in input_y:
  shares_y[y] = share(input_y[y])

# Compute shares in the expression
def evaluate(exp, shares_x, shares_y):
  if type(exp) is Var:
    if "x" in exp.name:
      exp.x = shares_x[exp.name][0]
      exp.y = shares_x[exp.name][1]
    else:
      exp.x = shares_y[exp.name][0]
      exp.y = shares_y[exp.name][1]
  elif type(exp) is Num:
    exp.x = exp.share[0]
    exp.y = exp.share[1]
  else:
    evaluate(exp.left, shares_x, shares_y)
    evaluate(exp.right, shares_x, shares_y)
    if exp.op.op == "+":
      exp.x = (exp.left.x + exp.right.x) % Q
      exp.y = (exp.left.y + exp.right.y) % Q
    else:
      # Simulate reconstruction of (y-b) and (x-a)
      x_a = reconstruct((exp.left.x-exp.a.share0) % Q, (exp.left.y-exp.a.share1) % Q)
      y_b = reconstruct((exp.right.x-exp.b.share0) % Q, (exp.right.y-exp.b.share1) % Q)
      x_a_y_b = share(x_a * y_b)
      exp.x = ((x_a * exp.b.share0) % Q + (y_b * exp.a.share0) % Q + exp.c.share0 + x_a_y_b[0]) % Q
      exp.y = ((x_a * exp.b.share1) % Q + (y_b * exp.a.share1) % Q + exp.c.share1 + x_a_y_b[1]) % Q

evaluate(exp, shares_x, shares_y)

# Reconstruct the computation
print(reconstruct(exp.x, exp.y))

    


  
