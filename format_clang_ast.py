import re
import sys

symbols = ['|', '`', '-']

last_line_begin = -666

with open('document.ast') as f:
    for i, line in enumerate(f):
        line = line.rstrip('\n')
        for symbol in symbols:
            line = line.replace(symbol, ' ')
        parts = line.split()
        quotes = line.split('\'')
        brackets = re.split('<|>', line)
        if len(brackets) > 1 and brackets[1].startswith("line"):
            comma_split = brackets[1].split()
            linepos = comma_split[0].split(':')[1]
            last_line_begin = int(linepos)
        if parts:
            first_word = parts[0]
            leading_spaces = ' ' * (len(line) - len(line.lstrip()))
            quoted_part = "{}".format(' '.join(parts[1:]))
            output = f"{leading_spaces}{first_word} {quoted_part}"
            # print(output)
            # print(i, len(quotes), last_line_begin, len(brackets), output)
            # sys.stdout.write(f'"{output}", ')
            print(f'"{output}_{last_line_begin}", ')