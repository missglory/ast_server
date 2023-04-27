#!python
import re
import curses
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

def find_closing_bracket(content, start_line):
    count = 0
    for i in range(start_line, len(content)):
        line = content[i]
        count += line.count('{')
        count -= line.count('}')
        if count <= 0:
            return i
    return len(content) - 1

def main(stdscr, regex_input, file_path):
    # Clear the screen and initialize variables
    stdscr.clear()
    stdscr.refresh()

    # Read file and find matches
    with open(file_path, 'r') as f:
        content = f.readlines()

    pattern = re.compile(regex_input)
    new_content = []

    i = 0
    while i < len(content):
        line = content[i]
        match = pattern.search(line)
        closing_bracket = find_closing_bracket(content, i)

        if match:
            stdscr.clear()  # Clear previous output
            to_print = 0
            lines_left = closing_bracket - i + 1
            while lines_left > 0:
                stdscr.addstr(to_print, 0, f"Match found: {line.strip()}")
                lines_left -= 1
                to_print += 1
            stdscr.addstr(to_print + 1, 0, "Comment out this method? (y/n):")
            stdscr.refresh()

            while True:
                ch = stdscr.getch()
                if ch in [ord('y'), ord('Y'), ord('n'), ord('N')]:
                    break

            if ch in [ord('y'), ord('Y')]:
                method_lines = content[i:closing_bracket+1]
                highlighted_code = highlight(''.join(method_lines), get_lexer_by_name('cpp'), TerminalFormatter())
                new_content.append('/*\n')
                new_content.extend(highlighted_code.splitlines())
                new_content.append(' */\n')
                i = closing_bracket + 1
            else:
                new_content.append(line)
                i += 1
        else:
            new_content.append(line)
            i += 1

    # Write modified content back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_content)

    stdscr.addstr(2, 0, "File updated. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python comment_out_cpp.py <regex_pattern> <file_path>")
        sys.exit(1)

    regex_input = sys.argv[1]
    file_path = sys.argv[2]

    curses.wrapper(main, regex_input, file_path)
