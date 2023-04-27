#!/home/mg/miniconda3/bin/python
import re
import curses
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter
from colorama import init, Fore, Style

init()

def find_closing_bracket(content, start_line):
    count = 0
    for i in range(start_line, len(content)):
        line = content[i]
        count += line.count('{')
        count -= line.count('}')
        if count <= 0:
            return i
    return len(content) - 1

def find_symbol(content, start_line, symbol=';'):
    for i in range(start_line, len(content)):
        line = content[i]
        if symbol in line:
            return i
    return len(content) - 1

def print_with_color(stdscr, line, match_regex = None, colorize=True):
    highlighted_line = line
    if colorize: highlighted_line = highlight(line, get_lexer_by_name('cpp'), Terminal256Formatter(style='native')).strip()
    parts = re.split(r'\x1b\[[0-9;]*m', highlighted_line)  # Split highlighted line by escape sequences
    color_sequence_parts = re.findall(r'\x1b\[[0-9;]*m', highlighted_line)  # Find color sequences
    color_sequence_index = 0

    for part in parts:
        if color_sequence_index < len(color_sequence_parts):
            color_code = color_sequence_parts[color_sequence_index]
            color_pair = get_color_pair(color_code)
            color_sequence_index += 1
        if match_regex is not None and not match_regex == '' and not colorize and re.search(match_regex, part):
             part = Fore.LIGHTGREEN_EX + part + Style.RESET_ALL
        if len(re.findall(r'\x1b\[[0-9;]*m', part)) > 0:
            print_with_color(stdscr, part, None, False)
        else: stdscr.addstr(part, color_pair)

def get_color_pair(color_code):
    # Remove escape sequence characters
    color_code = color_code.strip('\x1b[').strip('m')
    parts = color_code.split(';')

    # Extract foreground color information
    foreground = int(parts[-1])

    # Check if background color is provided
    if len(parts) > 1:
        background = int(parts[-2])
        return curses.color_pair(foreground + background * 8)
    
    return curses.color_pair(foreground)

def main(stdscr, regex_input, file_path):
    if type(file_path) is list:
        for f in file_path:
            handleFile(stdscr, regex_input, f)
    else:
        handleFile(stdscr, regex_input, file_path)

def handleFile(stdscr, regex_input, file_path):
    # Initialize color support for curses
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    # Clear the screen and initialize variables
    stdscr.clear()
    stdscr.refresh()

    # Read file and find matches
    with open(file_path, 'r') as f:
        content = f.readlines()

    pattern = re.compile(regex_input)
    new_content = []

    inside_comment = False
    i = 0
    lns = []
    match_count = 0
    for line in content:
        if "*/" in line.strip():
            inside_comment = False
        elif line.strip().startswith("/*"):
            inside_comment = True
        if inside_comment:
            i += 1
            new_content.append(line)
            continue
        match = pattern.search(line)
        if match:
            match_count += 1
    cur_match = 0

    while i < len(content):
        line = content[i]
        if "*/" in line.strip():
            inside_comment = False
        elif "/*" in line.strip():
            inside_comment = True
        if inside_comment:
            i += 1
            new_content.append(line)
            continue
        match = pattern.search(line)
        lns.append(i)

        if match:
            stdscr.clear()  # Clear previous output
            cur_match += 1
            print_with_color(stdscr, f"{Fore.RED}File: {Fore.WHITE}{file_path}{Fore.RED}. \nLine: {Fore.WHITE} {i} / {len(content)}\nMatch: {cur_match} / {match_count}\n\n", None, False)

            print_with_color(stdscr, f"{Fore.WHITE}Match found:\n", None, False)
            print_with_color(stdscr, line, regex_input, False)
            stdscr.addstr("\n")

            closing_bracket = find_closing_bracket(content, i)
            opening_bracket = find_symbol(content, i, '{')
            closing_semicolon = find_symbol(content, i)

            if opening_bracket <= closing_semicolon:
                method_lines = content[i:closing_bracket+1]
                i = closing_bracket + 1
            else:
                method_lines = content[i:closing_semicolon+1]
                i = closing_semicolon + 1

            # highlighted_code = highlight(''.join(method_lines), get_lexer_by_name('cpp'), Terminal256Formatter(style='native'))
            # lines = highlighted_code.splitlines()

            for code_line in method_lines:
                print_with_color(stdscr, code_line, regex_input)
                stdscr.addstr("\n")

            stdscr.refresh()
            prompt_line = f"\n{Fore.WHITE}Comment out this block? (y/n):"
            print_with_color(stdscr, prompt_line, None, False)

            # stdscr.addstr(len(lines)+1, 0, "Comment out this method/declaration? (y/n):")
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

        else:
            new_content.append(line)
            i += 1

    # Write modified content back to the file
    with open(file_path, 'w') as f:
        f.writelines(new_content)

    print_with_color(stdscr, f"\n{Fore.MAGENTA}File {file_path} updated! Press any key to continue", None, False)
    # print(lns)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python comment_out_cpp.py <regex_pattern> <file_path>...")
        sys.exit(1)

    regex_input = sys.argv[1]
    file_path = sys.argv[2: len(sys.argv)]
    curses.wrapper(main, regex_input, file_path)
