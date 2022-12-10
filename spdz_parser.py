
class Var:
  def __init__(self, name):
    self.name = name
  
  def __str__(self):
    return self.name

class Num:
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return str(self.value)

class Op:
  def __init__(self, op):
    self.op = op

  def __str__(self):
    return self.op

class Expression:
  def __init__(self, left=None, right=None, op=None):
    self.left = left
    self.right = right
    self.op = op
    self.a = None
    self.b = None
    self.c = None
    self.shares = None


def tokenization(input):
  input_list = list(input)
  output_tokens = []
  while len(input_list) != 0:
    if input_list[0] == "(":
      output_tokens.append("(")
      input_list = input_list[1:]
    elif input_list[0] == ")":
      output_tokens.append(")")
      input_list = input_list[1:]
    elif input_list[0] in "0123456789":
      for i in range(1, len(input_list)):
        if input_list[i] not in "0123456789 ":
          index = i
          break
      output_tokens.append(Num(int("".join(filter(lambda x: x != " ", input_list[:index])))))
      input_list = input_list[index:]
    elif input_list[0] in "+^*-":
      output_tokens.append(Op(input_list[0]))
      input_list = input_list[1:]
    elif input_list[0] in "xy":
      for i in range(1, len(input_list)):
        if input_list[i] not in "0123456789 ":
          index = i
          break
      output_tokens.append(Var("".join(filter(lambda x: x != " ", input_list[:index]))))
      input_list = input_list[index:]
    else:
      input_list = input_list[1:]
  return output_tokens

def printTokens(tokens):
  for token in tokens:
    if type(token) is Var:
      print(token.name, end=" ")
    elif type(token) is Num:
      print(token.value, end=" ")
    elif type(token) is Op:
      print(token.op, end=" ")
    else:
      print(token, end=" ")


def parser_e(tokens):
  left = parser_e2(tokens)
  # print("e", left)
  exp = Expression()
  curr = exp
  while (len(tokens) > 0) and (type(tokens[0]) is Op) and (tokens[0].op in ["+", "-"]):
    op = tokens.pop(0)
    curr.left = left
    curr.op = op
    curr.right = Expression()
    last = curr
    curr = curr.right
    left = parser_e2(tokens)
    # print("e", left)
  if exp.left is None:
    return left
  elif curr.op is None:
    last.right = left

  return exp


def parser_e2(tokens):
  left = parser_e3(tokens)
  # print("e2", left)
  exp = Expression()
  curr = exp
  while (len(tokens) > 0) and (type(tokens[0]) is Op) and (tokens[0].op == "*"):
    op = tokens.pop(0)
    curr.left = left
    curr.op = op
    curr.right = Expression()
    last = curr
    curr = curr.right
    left = parser_e3(tokens)
    # print("e2", left)
  if exp.left is None:
    return left
  elif curr.op is None:
    last.right = left

  return exp

def parser_e3(tokens):
  left = parser_e4(tokens)
  exp = Expression()
  curr = exp
  while (len(tokens) > 0) and (type(tokens[0]) is Op) and (tokens[0].op == "^"):
    op = tokens.pop(0)
    curr.left = left
    curr.op = op
    curr.right = Expression()
    last = curr
    curr = curr.right
    left = parser_e4(tokens)
  if exp.left is None:
    return left
  elif curr.op is None:
    last.right = left

  return exp

def parser_e4(tokens):
  if (type(tokens[0]) is Var) or (type(tokens[0]) is Num):
    return tokens.pop(0)
  
  if tokens[0] == "(":
    tokens.pop(0)
  exp = parser_e(tokens)
  if tokens[0] == ")":
    tokens.pop(0)
  return exp
    
def printExp(exp):
  if (type(exp) is Var) or (type(exp) is Num):
    print(exp, end=" ")
  else:
    if type(exp.left) is Expression:
      print("(", end="")
      printExp(exp.left)
      print(")", end="")
    else:
      print(exp.left, end=" ")
    print(exp.op, end=" ")
    if type(exp.right) is Expression:
      print("(", end="")
      printExp(exp.right)
      print(")", end="")
    else:
      print(exp.right, end=" ")

if __name__ == '__main__':
  tokens = tokenization("")
  # printTokens(tokens)
  exp = parser_e(tokens)
  printExp(exp)
  
      
    