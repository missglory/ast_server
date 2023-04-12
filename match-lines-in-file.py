import sys
from colorama import Fore

# Check that the user provided a filename as the first argument
if len(sys.argv) < 2:
    print("Usage: python script.py filename")
    sys.exit(1)

filename = sys.argv[1]

# Open the file and read its contents into a set
try:
    with open(filename, "r") as f:
        lines = set(f.read().splitlines())
except FileNotFoundError:
    print(f"Error: File '{filename}' not found")
    sys.exit(1)

# Read lines from stdin, and for each one, check if it's in the set of lines from the file
for i, line in enumerate(sys.stdin):
    line = line.strip().replace("./", "")
    for ii, lf in enumerate(lines):
        if line in lf:
            print(Fore.GREEN + f"{line} > {filename}:{ii+1}")
            break
    sys.stderr.write(Fore.RED + f"{line} > {filename}:{-1}\n")

