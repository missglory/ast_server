#!/home/mg/miniconda3/bin/python
import re
import curses
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
from colorama import init, Fore, Style

# init()

def find_closing_bracket(content, start_line):
    count = 0
    for i in range(start_line, len(content)):
        line = content[i]
        count += line.count('{')
        count -= line.count('}')
        if count <= 0:
            return i
    return len(content) - 1

def find_closing_semicolon(content, start_line):
    for i in range(start_line, len(content)):
        line = content[i]
        if ';' in line:
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

        if match:
            closing_bracket = find_closing_bracket(content, i + 1)
            closing_semicolon = find_closing_semicolon(content, i + 1)
            stdscr.clear()  # Clear previous output
            method_lines = content[i:min(closing_bracket, closing_semicolon)]
            # if '{' in line:
            # else:
            #     method_lines = content[i:closing_semicolon+1]

            stdscr.addstr(0, 0, f"{Fore.YELLOW}Match found:\n")
            # for i, ln in enumerate(method_lines):
            #     stdscr.addstr(i, 0, f"{line.strip()}{Style.RESET_ALL}\n")

            highlighted_code = highlight('\n'.join(method_lines), get_lexer_by_name('cpp'), TerminalFormatter())
            stdscr.addstr(1, 0, highlighted_code)
            stdscr.refresh()

            stdscr.addstr(len(method_lines) + 1, 0, "Comment out this method/declaration? (y/n):")
            stdscr.refresh()

            while True:
                ch = stdscr.getch()
                if ch in [ord('y'), ord('Y'), ord('n'), ord('N')]:
                    break

            if ch in [ord('y'), ord('Y')]:
                new_content.append('/*\n')
                new_content.extend(method_lines)
                new_content.append(' */\n')

            if '{' in line:
                i = closing_bracket + 1
            else:
                i = closing_semicolon + 1
        else:
            new_content.append(line)
            i += 1

    # Write modified content back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_content)

    stdscr.addstr(3, 0, "File updated. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python comment_out_cpp.py <regex_pattern> <file_path>")
        sys.exit(1)

    regex_input = sys.argv[1]
    file_path = sys.argv[2]

    curses.wrapper(main, regex_input, file_path)
import re
import curses
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
from colorama import init, Fore, Style

init(autoreset=True)

def find_closing_bracket(content, start_line):
    count = 0
    for i in range(start_line, len(content)):
        line = content[i]
        count += line.count('{')
        count -= line.count('}')
        if count <= 0:
            return i
    return len(content) - 1

def find_closing_semicolon(content, start_line):
    for i in range(start_line, len(content)):
        line = content[i]
        if ';' in line:
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

        if match:
            stdscr.clear()  # Clear previous output
            stdscr.addstr(0, 0, f"{Fore.YELLOW}Match found: {line.strip()}{Style.RESET_ALL}\n")

            if '{' in line:
                closing_bracket = find_closing_bracket(content, i + 1)
                method_lines = content[i:closing_bracket+1]
            else:
                closing_semicolon = find_closing_semicolon(content, i + 1)
                method_lines = content[i:closing_semicolon+1]

            highlighted_code = highlight(''.join(method_lines), get_lexer_by_name('cpp'), TerminalFormatter())
            stdscr.addstr(1, 0, highlighted_code)
            stdscr.refresh()

            stdscr.addstr(2, 0, "Comment out this method/declaration? (y/n):")
            stdscr.refresh()

            while True:
                ch = stdscr.getch()
                if ch in [ord('y'), ord('Y'), ord('n'), ord('N')]:
                    break

            if ch in [ord('y'), ord('Y')]:
                new_content.append('/*\n')
                new_content.extend(method_lines)
                new_content.append(' */\n')
            else:
                new_content.extend(method_lines)

            if '{' in line:
                i = closing_bracket + 1
            else:
                i = closing_semicolon + 1
        else:
            new_content.append(line)
            i += 1

    # Write modified content back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_content)

    stdscr.addstr(3, 0, "File updated. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python comment_out_cpp.py <regex_pattern> <file_path>")
        sys.exit(1)

    regex_input = sys.argv[1]
    file_path = sys.argv[2]

    curses.wrapper(main, regex_input, file_path)
