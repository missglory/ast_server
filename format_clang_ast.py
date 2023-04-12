symbols = ['|', '`', '-']

with open('document.ast') as f:
    for i, line in enumerate(f):
        line = line.rstrip('\n')
        for symbol in symbols:
            line = line.replace(symbol, ' ')
        parts = line.split()
        if parts:
            first_word = parts[0]
            leading_spaces = ' ' * (len(line) - len(line.lstrip()))
            quoted_part = "'{}'".format(' '.join(parts[1:]))
            output = f"{leading_spaces}{first_word} {quoted_part}"
            # print(i, output)
            print(output)