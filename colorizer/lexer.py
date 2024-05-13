table = [[1,6,7,8,0,8],[1,4,4,2,4,8],[3,8,8,8,8,8],[3,5,5,8,5,8]]

test_string = "125+243.56     +     97.042    +25"
s = test_string + '$'

ignored = " \n\t$"
digits = "0123456789"

state = 0
p = 0
lexem = ''
token = ''

while((s[p] != '$') or (s[p] == '$' and state != 0) and (state != 8)):
  c = s[p]
  if c in digits:
    col = 0
  elif c == '+':
    col = 1
  elif c == '-':
    col = 2
  elif c == '.':
    col = 3
  elif c in ignored:
    col = 4
  else:
    col = 5

  state = table[state][col]

  if state == 4:
    token = 'INT'
    print(lexem, token)
    lexem = ''
    state = 0
    p -= 1
  elif state == 5:
    token = 'RLN'
    print(lexem, token)
    lexem = ''
    state = 0
    p -= 1
  elif state == 6:
    token = 'SUM'
    print(s[p], token)
    lexem = ''
    state = 0
  elif state == 7:
    token = 'SUB'
    print(s[p], token)
    lexem = ''
    state = 0
  elif state == 8:
    token = 'ERR'
    print(lexem, token)
    
  p += 1

  if state != 0:
    lexem += c