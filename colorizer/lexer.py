def load_transition_table(file_name: str) -> list:
  table = []
  with open(file_name, 'r') as file:
    for line in file:
      row = line.split(',')
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
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_POW = r"\^"
t_CHR = r"[a-zA-Z]"
t_LBR = r"\("
t_RBR = r"\)"
t_DOT = r"\."
t_SCI = r"[eE]"
t_BRK = " \n\t$"

def arithmetic_lexer(file_name: str) -> None:
  transition_table = load_transition_table("transition_tables/arithmetic_lexer.tbl")
  print_table(transition_table)

  table_size = len(transition_table)

  with open(file_name, 'r') as file:
    for line in file:
      s = line + '$'
      print(f"line = {line}")
      state = 0
      p = 0
      lexem = ''
      token = ''
      # print(f"table size = {table_size}")
      print(f"s[p] then = {s[p]}, state = {state}, p = {p} |||||||||||||||")
      while((s[p] != '$') or (s[p] == '$' and state != 0) and (state != 15)):
        c = s[p]
        print(f'checking "{c}"')
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
        elif c in t_CHR:
          col = 6
        elif c == t_LBR:
          col = 7
        elif c == t_RBR:
          col = 8
        elif c == t_DOT:
          col = 9
        elif c in t_SCI:
          col = 10
        elif c in t_BRK:
          col = 11
        else:
          col = 12
        
        state = int(transition_table[state][col])
        print(f'col = {col}, val = {state}')

        if state == 5:
          token = 'INT'
          state = 0
          p -= 1
        elif state == 6:
          token = 'RLN'
          state = 0
          p -= 1
        elif state == 7:
          token = 'SUM'
          # extract character
          lexem = s[p]
          state = 0
        elif state == 8:
          token = 'SUB' 
          state = 0
        elif state == 9:
          token = 'MUL'
          state = 0
          p -= 1
        elif state == 10:
          token = 'DIV'
          state = 0
          p -= 1
        elif state == 11:
          token = 'POW'
          state = 0
          p -= 1
        elif state == 12:
          token = 'VAR'
          state = 0
          p -= 1
        elif state == 13:
          token = 'LBR'
          state = 0
        elif state == 14:
          token = 'RBR'
          state = 0
        elif state == 15:
          token = 'ERR'
          p -= 1

        if lexem != '':
          print(f"{lexem} {token}")
  
        input(". . . ")
        lexem = ''
        p += 1

        if state != 0:
          lexem += c
          print(f"lexem = {lexem}")

def main():
  arithmetic_lexer("input_files/test.lex")

if __name__ == "__main__":
  main()