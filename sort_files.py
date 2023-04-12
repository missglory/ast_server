import sys

files = []
for file_name in sys.stdin:
    file_name = file_name.strip()

    with open(file_name) as f:
        lines = f.readlines()

    lines_count = len(lines)
    files.append((file_name, lines_count, lines))

files = sorted(files, key=lambda x: x[1])

for file_name, lines_count, lines in files:
    # sorted_lines = sorted(lines)
    print(f"{lines_count} {file_name}")
    # for line in sorted_lines:
        # print(line, end="")
