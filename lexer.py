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
t_ABC = "abcdfghijklmnopqrstuvwxyzABCDFGHIJKLMNOPQRSTUVWXYZ"
t_DIG = "0123456789"
t_SUM = "+"
t_SUB = "-"
t_MUL = "*"
t_DIV = "/"
t_POW = "^"
t_ASN = "="
t_LBR = "("
t_RBR = ")"
t_Ee = "eE"
t_RETURN = "\n"
t_DOT = "."
t_CMT = "#"
t_BLANK = " \t$"
t_FLOOR = "_"
t_RESERVE = ["if", "else", "elif", "while", "for", "print", "return", "break", "continue", "const", "int", "float", "string", "bool", "True", "False", "and", "or", "not", "in", "input", "row", "column"]
t_END = "$"

# Function to print verbose messages (debugging)
def print_verbose(message: str) -> None:
  global verbose
  if verbose:
    print(message)

#verbose = True

# Function to implement the arithmetic lexer
def arithmetic_lexer(file_name: str) -> None:
  if not os.path.exists('output_files'):
    os.makedirs('output_files')

  transition_table = load_transition_table("transition_tables/updated_DFA.tbl")
  verbose and print_table(transition_table)

  # iteratively generate the output file (will be used for colorizer)
  output_file_name = file_name.split("/")[-1]
  output_file_name = output_file_name.split(".")[0]
  output_file_name = f"output_files/{output_file_name}.html"
  output_file = open(output_file_name, 'w')
  
  # read the input file and tokenize the lexemes
  with open(file_name, 'r') as file:
    output_file.write(hl.format_html(hl.load_theme("css_themes/vscode_classic.theme")))
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
      while((s[p] != '$') or (s[p] == '$' and state != 0) and (state != 24)):
        c = s[p]
        print_verbose(f'checking "{c}"')
        if c in t_ABC:
          col = 0
        elif c in t_DIG:
          col = 1
        elif c == t_SUM:
          col = 2
        elif c == t_SUB:
          col = 3
        elif c == t_MUL:
          col = 4
        elif c == t_DIV:
          col = 5
        elif c == t_POW:
          col = 6
        elif c == t_ASN:
          col = 7
        elif c == t_LBR:
          col = 8
        elif c == t_RBR:
          col = 9
        elif c in t_Ee:
          col = 10
        elif c in t_RETURN:
          col = 11
        elif c == t_DOT:
          col = 12
        elif c == t_CMT:
          col = 13
        elif c in t_BLANK:
          col = 14
        elif c == t_FLOOR:
          col = 15
        else:
          col = 16
        
        # update the state based on the transition table
        state = int(transition_table[state][col])
        print_verbose(f'col = {col}, val = {state}')
        if state == 18:
          token = 'CMT'
          state = 0
        elif state == 21:
          token = 'INT'
          state = 0
          p -= 1
        elif state in [19, 20]:
          token = 'RLN'
          state = 0
          p -= 1
        elif state == 10:
          token = 'SUM'
          lexem = s[p]
          state = 0
        elif state == 11:
          token = 'SUB'
          state = 0
        elif state == 12:
          token = 'MUL'
          lexem = s[p]
          state = 0
        elif state == 13:
          token = 'DIV'
          state = 0
        elif state == 14:
          token = 'POW'
          lexem = s[p]
          state = 0
        elif state == 15:
          token = 'ASN'
          lexem = s[p]
          state = 0
        elif state == 22:
          token = 'VAR'
          state = 0
          p -= 1
        elif state == 23:
          if lexem in t_RESERVE:
            token = 'RESERVE'
          else:
            token = 'VAR'
          state = 0
          p -= 1
        elif state == 16:
          token = 'LBR'
          lexem = s[p]
          state = 0
        elif state == 17:
          token = 'RBR'
          lexem = s[p]
          state = 0
        elif state == 24:
          token = 'ERR'

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

# --- Functions to process directories and files ---
def process_directory_sequencial(directory_path: str) -> None:
    directory = os.listdir(directory_path)
    for file in directory:
      file_path = os.path.join(directory_path, file)
      if file.endswith(".lex"):
        print(f"Processing file: {file}")
        arithmetic_lexer(file_path)

def process_file_parallel(file: str) -> None:
    tasks = []
    with ProcessPoolExecutor() as executor:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.lex'):
                    file_path = os.path.join(root, file)
                    tasks.append(executor.submit(arithmetic_lexer, file_path))
        for task in tasks:
            task.result()

def file_sequencial(file_path: str) -> None:
    arithmetic_lexer(file_path)

def main():
  directory_path = './input_files'
  process_directory_sequencial(directory_path)

if __name__ == "__main__":
  main()
