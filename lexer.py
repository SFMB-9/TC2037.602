# Salvador Federico Milanés Braniff | A01029956
import highlighter as hl
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

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
t_LBR = "("
t_RBR = ")"
t_DTS = ":"
t_HSH = "#"
t_E = "eE"
t_FUN = ["print", "input", "len", "range", "abs", "round", "max", "min", "sum", "sorted", "reversed", "zip", "enumerate", "map", "filter", "reduce"]
t_CON = ["if", "elif", "else","while", "for", "in", "break", "continue", "return"]
t_TYP = ["int", "float", "str", "bool"]
t_BOL = ["True", "False"]
t_LGO = ["and", "or", "not"]
t_CHR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
t_DOT = "."
t_SPC = " "
t_TAB = "\t"
t_QTS = "\""
t_NLN = "\n$"

# Function to print verbose messages (debugging)
def print_verbose(message: str) -> None:
  global verbose
  if verbose:
    print(message)

# verbose = True

# Function to implement the arithmetic lexer

def arithmetic_lexer(file_path: str, transition_table: list) -> None:
  if not os.path.exists('output_files'):
    os.makedirs('output_files')

  # iteratively generate the output file (will be used for colorizer)
  file_path = file_path.split("/")[-1]
  file_name = file_path.split("\\")[-1]
  output_file_name = file_name.split(".")[0]
  output_file_name = f"output_files/{output_file_name}.html"
  output_file = open(output_file_name, 'w')
  
  # read the input file and tokenize the lexemes
  with open(file_path, 'r') as file:
    output_file.write(hl.format_html(hl.load_theme("css_themes/vscode_classic.theme")))
    print_verbose("_ _ _               _ _ _")
    print_verbose(f"     {file_name}")
    
    for line in file:
      s = line + '$'
      print_verbose(f"line: {line}")
      # if line starts with spaces, tabs or newlines, replace them with &nbsp;
      if line[0] in t_NLN:
        output_file.write("<br>")
      elif line[0] in t_SPC:
        output_file.write("<br>&nbsp&nbsp")
      state = 0
      p = 0
      lexem = ''
      token = ''
      
      # iterate through the string until the end of the line ($)
      while((s[p] != '$') or (s[p] == '$' and state != 0) and (state != 29)):
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
        elif c == t_DTS:
          col = 9
        elif c == t_HSH:
          col = 10
        elif c in t_SPC or c == t_TAB:
          col = 11
        elif c in t_NLN:
          col = 12
        elif c in t_E:
          col = 13
        elif c in t_CHR:
          col = 14
        elif c == t_DOT:
          col = 15
        elif c == t_QTS:
          col = 16
        else:
          col = 17
        
        # update the state based on the transition table
        state = int(transition_table[state][col])
        print_verbose(f'col = {col}, val = {state}')
        if state == 11:
          token = 'CMT'
          state = 0
          p -= 1 # Syntax for extracting a multi-character token.
        elif state == 12:
          token = 'INT'
          state = 0
          p -= 1
        elif state == 13:
          token = 'RLN'
          state = 0
          p -= 1
        elif state == 14:
          token = 'SUM'
          lexem = s[p]
          state = 0 # Syntax for extracting a single-character token.
        elif state == 15:
          token = 'SUB'
          state = 0
          p -= 1
        elif state == 16:
          token = 'MUL'
          lexem = s[p]
          state = 0
        elif state == 17:
          token = 'DIV'
          state = 0
        elif state == 18:
          token = 'POW'
          lexem = s[p]
          state = 0
        elif state == 19:
          token = 'ASN'
          lexem = s[p]
          state = 0
        elif state == 20:
          token = 'LGO'
          state = 0
          p -= 1
        elif state == 21:
          token = 'CON'
          state = 0
          p -= 1
        elif state == 22:
          token = 'BOL'
          state = 0
          p -= 1
        elif state == 23:
          if lexem in t_FUN:
            token = 'FUN'
          elif lexem in t_CON:
            token = 'CON'
          elif lexem in t_TYP:
            token = 'TYP'
          elif lexem in t_BOL:
            token = 'BOL'
          elif lexem in t_LGO:
            token = 'LGO'
          else:
            token = 'VAR'
          state = 0
          p -= 1
        elif state == 24:
          token = 'LBR'
          lexem = s[p]
          state = 0
        elif state == 25:
          token = 'RBR'
          lexem = s[p]
          state = 0
        elif state == 26:
          token = 'DTS'
          lexem = s[p]
          state = 0
        elif state == 27:
          token = 'QTS'
          lexem = s[p]
          state = 0
        elif state == 28:
          token = 'STR'
          lexem = s[p]
          state = 0
        elif state == 29:
          token = 'ERR'

        if lexem != '' and token != '':
          print(f"{lexem} {token}")

          # Call the colorizer function
          formatted_token = hl.colorize(lexem, token)
          output_file.write(formatted_token)
          
          lexem = ''
          token = ''
          if col == 12: # If the character is a newline, print a line break.
            output_file.write("<br>")
        
        if col == 11: # If the character is a space
          output_file.write(" ")
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

# --- Functions to process directories and files ---
def process_directory_sequential(directory_path: str, transition_table: list) -> None:
    directory = os.listdir(directory_path)
    for file in directory:
      file_path = os.path.join(directory_path, file)
      if file.endswith(".lex"):
        print(f"Processing file: {file}")
        arithmetic_lexer(file_path, transition_table)

def process_file_parallel(file: str) -> None:
    tasks = []
    directory = os.path.dirname(file)
    with ProcessPoolExecutor() as executor:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.lex'):
                    file_path = os.path.join(root, file)
                    tasks.append(executor.submit(arithmetic_lexer, file_path))
        for task in tasks:
            task.result()

def file_sequential(file_path: str) -> None:
    arithmetic_lexer(file_path)

def main():
  # Call the arithmetic lexer function with an example input file
  transition_table = load_transition_table("transition_tables/python_lexer.tbl")
  verbose and print_table(transition_table)
  process_directory_sequential("input_files", transition_table)

if __name__ == "__main__":
  main()
