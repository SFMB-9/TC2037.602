def load_transition_table(file_name: str) -> list:
  table = []
  with open(file_name, 'r') as file:
    for line in file:
      row = line.split()
      # Convert string to int
      row = [int(i) for i in row]
      table.append(row)
  return table

def print_table(table: list) -> None:
  # Print numbers so that they are aligned
  for row in table:
    for cell in row:
      print(f'{cell:2}', end=' ')
    print()

t_DIG = "0123456789"
t_SUM = "+"
t_SUB = "-"
t_MUL = "*"
t_DIV = "/"
t_POW = "^"
t_EQS = "="
t_SCI = "eE"
t_CHR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
t_LBR = "("
t_RBR = ")"
t_DOT = "."
t_BRK = " \t\n$"

verbose = True
# verbose = False
def print_verbose(message: str) -> None:
  if verbose:
    print(message)

def arithmetic_lexer(file_name: str) -> None:
  transition_table = load_transition_table("transition_tables/arithmetic_lexer.tbl")
  print_table(transition_table)

  with open(file_name, 'r') as file:
    for line in file:
      s = line + '$'
      print_verbose(f"line = {line}")
      state = 0
      p = 0
      lexem = ''
      token = ''
      print_verbose(f"s[p] then = {s[p]}, state = {state}, p = {p} |||||||||||||||")
      while((s[p] != '$') or (s[p] == '$' and state != 0) and (state != 15)):
        c = s[p]
        print_verbose(f'checking "{c}"')
        if c in t_DIG:
          col = 0
        elif c == t_SUM:
          col = 1
        elif c == t_SUB:
          col = 2
        elif c == t_MUL:
          col = 3
        elif c == t_DIV:
          col = 4
        elif c == t_POW:
          col = 5
        elif c == t_EQS:
          col = 6
        elif c == t_LBR:
          col = 8
        elif c == t_RBR:
          col = 9
        elif c == t_DOT:
          col = 10
        elif c in t_SCI:
          print(f"sci = {c}")
          col = 11
        elif c in t_CHR:
          col = 7
        elif c in t_BRK:
          col = 12
        else:
          col = 13
        
        state = int(transition_table[state][col])
        print_verbose(f'col = {col}, val = {state}')

        if state == 6:
          token = 'INT'
          state = 0
          p -= 1
        elif state == 7:
          token = 'RLN'
          state = 0
          p -= 1
        elif state == 8:
          token = 'SUM'
          lexem = s[p]
          state = 0
        elif state == 9:
          token = 'SUB'
          lexem = s[p]
          state = 0
        elif state == 10:
          token = 'MUL'
          lexem = s[p]
          state = 0
        elif state == 11:
          token = 'DIV'
          lexem = s[p]
          state = 0
        elif state == 12:
          token = 'POW'
          lexem = s[p]
          state = 0
        elif state == 13:
          token = 'EQS'
          lexem = s[p]
          state = 0
        elif state == 14:
          token = 'VAR'
          state = 0
          p -= 1
        elif state == 15:
          token = 'LBR'
          lexem = s[p]
          state = 0
        elif state == 16:
          token = 'RBR'
          lexem = s[p]
          state = 0
        elif state == 17:
          token = 'ERR'
          p -= 1

        if lexem != '' and token != '':
          print(f"{lexem} {token}")
          lexem = ''
          token = ''
  
        # ternary check if verbose is True
        verbose and input(". . . ")
        if s[p] != '$':
          p += 1

        if state != 0:
          lexem += c
          print_verbose(f"lexem = {lexem}")

def main():
  arithmetic_lexer("input_files/test.lex")

if __name__ == "__main__":
  main()