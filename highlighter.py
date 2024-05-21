def load_theme(file_name):
    theme = {}
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments

            try:
                key, value = line.split(' = ')
                token_name = key.strip()
                attrs_dict = eval(value.strip())  # Convert attribute string to dictionary
                theme[token_name] = attrs_dict
            except ValueError as e:
                print(f"Error parsing theme line: {line} - {e}")

    return theme

def format_html(theme):
    html = '<html><head><style>'
    for token, attrs in theme.items():
        css = ''
        for attr, value in attrs.items():
            css += f'{attr}: {value}; '
        if token == 'body':
            html += f'body {{{css}}}'
        else:
            html += f'.{token} {{{css}}}'
    html += '</style></head><body>'
    return html

# Receive a token and replace it with an html snippet to define its color.
def colorize(lexem, token):
    # remove spaces from the token
    token = token.replace(' ', '')
    return f'<span class="{token}">{lexem}</span>'