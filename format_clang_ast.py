import re
import sys

symbols = ['|', '`', '-']

last_line_begin = 0

original_lines = []

with open(r"document.cc", 'r') as fp:
    original_lines = fp.readlines()

print("""
{
	"DOCUMENT": {
    "deps": [
""")

line_stack = [{
    "node": "DOCUMENT",
    "lvl": -1,
    "line": 0
}]

def first_letter(s):
    m = re.search(r'[a-z]', s, re.I)
    if m is not None:
        return m.start()
    raise Exception("No letter found")
    return -1

def get_last_line(brackets, stac):
    if len(brackets) > 1 and brackets[1].startswith("line"):
        comma_split = brackets[1].split()
        linepos = comma_split[0].split(':')[1]
        return int(linepos)
    return stac[len(stac)-1]["line"]

def last(arr):
    return arr[len(arr)-1]

with open('document.ast') as f:
    f_lines = f.readlines()
    for i, line in enumerate(f_lines):
        line = line.rstrip('\n')
        for symbol in symbols:
            line = line.replace(symbol, ' ')
        parts = line.split()
        quotes = line.split('\'')
        brackets = re.split('<|>', line)
        fl = first_letter(line)
        # if len(brackets) > 1 and brackets[1].startswith("line"):
        #     comma_split = brackets[1].split()
        #     linepos = comma_split[0].split(':')[1]
        #     last_line_begin = int(linepos)
        while last(line_stack)["lvl"] >= fl:
            line_stack.pop()
        line_stack.append({
            "node": line,
            "lvl": fl,
            "line": get_last_line(brackets, line_stack)
				})
        if parts:
            first_word = parts[0]
            leading_spaces = ' ' * (len(line) - len(line.lstrip()))
            quoted_part = "{}".format(' '.join(parts[1:]))
            output = f"{leading_spaces}{first_word} {quoted_part}".replace(r'"', r'\"')
            # print(output)
            # print(i, len(quotes), last_line_begin, len(brackets), output)
            # sys.stdout.write(f'"{output}", ')
            fmt = (original_lines[last(line_stack)["line"]]).replace(r'"', r'\"').replace("\n", "")
            sys.stdout.write(f'"{output}____{fmt}"')
            if i < len(f_lines) - 1:
              sys.stdout.write(",\n")


sys.stdout.write("]}}")