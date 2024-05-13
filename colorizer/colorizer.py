# import regular expression module
import re

# replace integers for 'AAAA'
pattern = r'\d+'

string = 'hello cruel 123 world 34157 other int'
repl = 'AAAA'

a = re.sub(pattern, repl, string)

print(a)

# Receive a token and replace it with an html snippet to define its color.
def colorize(lexem):
  return f'<font color="red">{lexem.group(0)}</font>'

b = re.sub(pattern, colorize, string)
print (b)

# Write to an html file
f2 = open('colorizer/colorized.html', 'wt')
f2.write(b)
f2.close()