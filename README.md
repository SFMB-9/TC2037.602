# TC2037.602
> Repository for the Lexer & Html Formatter

© Salvador Federico Milanés Braniff | Eduardo Porto Morales | Valeria Tapia

This repository contains a Python implementation of a Lexer and HTML Formatter using a DFA (Deterministic Finite Automaton) represented by a transition table implemented as a list of lists. The Lexer processes input tokens according to predefined rules and generates HTML output with syntax-highlighted code.

## Purpose
The main goal of this project is to implement a Lexer capable of analyzing input files in the .lex format, tokenizing them using a DFA-based approach, and producing HTML output that visually highlights the syntax of the input code.

## Project Structure
```python
TC2037.602
│
├── css_themes/              # Predefined CSS themes for syntax highlighting
│
├── input_files/             # Sample input files (.lex) for the lexer
│   ├── sample.lex
│   ├── comments.lex
│   └── test.lex
│
├── output_files/            # Output directory for generated HTML files
│
├── transition_tables/       # Reference transition tables for the lexer
│
└── lexer.py                 # Main script for the lexer and HTML formatter
```


## Prerequisites
- __Python 3.11__ or later must be installed on your systyem to run the lexer.

## Usage
1. Clone the repository:
    ```bash
    git clone https://github.com/SFMB-9/TC2037.602
    cd TC2037.602
    ```

2. Run the lexer

    Execute the main script `lexer.py` using Python:
    ```bash
    python lexer.py
    ```
    This will process the input files from the `input_files` directory, generate syntax-highlighted HTML output files in the `output_files` directory, and apply predefined CSS themes from the `css_themes` directory.

3. View Output
   
    After running the lexer, check the `output_files` directory for the generated HTML files corresponding to the processed `.lex` input files.

## Additional Notes
- Modify the `verbose` variable in `lexer.py` to enable detailed token identification during execution.
- Explore the `css_themes` directory to customize or add new CSS themes for syntax highlighting.
- Refer to the `transition_tables` directory for referenceable transition tables used by the lexer.
  
Feel free to explore and utilize this lexer and HTML formatter project for processing lex code files and generating syntax-highlighted HTML output. Customize and extend the functionality as needed for your requirements.