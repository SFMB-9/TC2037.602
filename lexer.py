# Salvador Federico Milanés Braniff | A01029956
import highlighter as hl
import os
from concurrent.futures import ThreadPoolExecutor

global verbose
verbose = False

# Function to load a transition table from a .tbl file
def load_transition_table(file_name: str) -> list:
  table = []
  with open(file_name, 'r') as file:
    for line in file:
      row = line.split()
      # Convert string to int
      row = [int(i) for i in row]
      table.append(row)
  return table

# Function to print table data in a readable format
def print_table(table: list) -> None:
  # Print numbers so that they are aligned
  for row in table:
    for cell in row:
      print(f'{cell:2}', end=' ')
    print()

# Token definitions
t_DIG = "0123456789"
t_SUM = "+"
t_SUB = "-"
t_MUL = "*"
t_DIV = "/"
t_POW = "^"
t_ASN = "="
t_SCI = "eE"
t_CHR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
t_LBR = "("
t_RBR = ")"
t_DOT = "."
t_BRK = " \t"
t_NLN = "\n$"

# Function to print verbose messages (debugging)
def print_verbose(message: str) -> None:
  global verbose
  if verbose:
    print(message)

# verbose = True

# Function to implement the arithmetic lexer
if not os.path.exists('output_files'):
    os.makedirs('output_files')
def arithmetic_lexer(file_name: str) -> None:
  transition_table = load_transition_table("transition_tables/arithmetic_lexer.tbl")
  verbose and print_table(transition_table)

  # iteratively generate the output file (will be used for colorizer)
  output_file_name = file_name.split("/")[-1]
  output_file_name = output_file_name.split(".")[0]
  output_file_name = f"output_files/{output_file_name}.html"
  output_file = open(output_file_name, 'w')
  
  # read the input file and tokenize the lexemes
  with open(file_name, 'r') as file:
    output_file.write(hl.format_html(hl.load_theme("css_themes/avatar.theme")))
    print_verbose("_ _ _               _ _ _")
    print_verbose("      Start of file       ")
    for line in file:
      s = line + '$'
      print_verbose(f"line: {line}")
      state = 0
      p = 0
      lexem = ''
      token = ''
      
      # iterate through the string until the end of the line ($)
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
        elif c == t_ASN:
          col = 6
        elif c == t_LBR:
          col = 7
        elif c == t_RBR:
          col = 8
        elif c in t_SCI:
          col = 9
        elif c in t_CHR:
          col = 10
        elif c in t_BRK:
          col = 11
        elif c in t_NLN:
          col = 12
        elif c == t_DOT:
          col = 13
        else:
          col = 14
        
        # update the state based on the transition table
        state = int(transition_table[state][col])
        print_verbose(f'col = {col}, val = {state}')
        if state == 10:
          token = 'CMT'
          state = 0
          p -= 1 # Syntax for extracting a multi-character token.
        elif state == 11:
          token = 'INT'
          state = 0
          p -= 1
        elif state == 12:
          token = 'RLN'
          state = 0
          p -= 1
        elif state == 13:
          token = 'SUM'
          lexem = s[p]
          state = 0 # Syntax for extracting a single-character token.
        elif state == 14:
          token = 'SUB'
          state = 0
          p -= 1
        elif state == 15:
          token = 'MUL'
          lexem = s[p]
          state = 0
        elif state == 16:
          token = 'DIV'
          state = 0
        elif state == 17:
          token = 'POW'
          lexem = s[p]
          state = 0
        elif state == 18:
          token = 'ASN'
          lexem = s[p]
          state = 0
        elif state == 19:
          token = 'VAR'
          state = 0
          p -= 1
        elif state == 20:
          token = 'LBR'
          lexem = s[p]
          state = 0
        elif state == 21:
          token = 'RBR'
          lexem = s[p]
          state = 0
        elif state == 22:
          token = 'ERR'
          p -= 1

        if lexem != '' and token != '':
          print(f"{lexem} {token}")

          # Call the colorizer function
          formatted_token = hl.colorize(lexem, token)
          output_file.write(formatted_token + "\n")
          
          lexem = ''
          token = ''
          if col == 12:
            output_file.write("<br>")
  
        # ternary check if verbose is True to print loop by loop.
        verbose and input(". . . ")
        if s[p] != '$':
          p += 1

        if state != 0:
          lexem += c
          print_verbose(f"lexem = {lexem}")

    print_verbose("_ _ _ End of file _ _ _")
  output_file.close()
  return

# --- Function to process directories and files ---
def process_directory(directory: str) -> None:
  for root, _, files, in os.walk(directory):
    for file in files:
      if file.endswith(".lex"):
        file_path= os.path.join(root, file)
        arithmetic_lexer(file_path)

def process_directory_parallel(directory: str) -> None:
    tasks = []
    with ProcessPoolExecutor() as executor:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.lex'):
                    file_path = os.path.join(root, file)
                    tasks.append(executor.submit(arithmetic_lexer, file_path))
        for task in tasks:
            task.result()

def main():
  # send the route of the file to the lexers
  directories = ['input_files']
  for directory in directories:
    process_directory(directory)

if __name__ == "__main__":
  main()