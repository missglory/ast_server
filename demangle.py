import sys
import subprocess
import json
import concurrent.futures
import cxxfilt

def get_demangled_symbols(obj_path):
    try:
        # Run the `objdump -t` command to extract symbol names from the object file
        objdump_output = subprocess.check_output(['objdump', '-t', obj_path])
    except subprocess.CalledProcessError:
        return []

    # Decode the output and split it into lines
    objdump_lines = objdump_output.decode().splitlines()

    # Extract the symbol names and demangle them using the C++ ABI library
    symbols = []
    for line in objdump_lines:
        parts = line.split()
        if len(parts) >= 7 and parts[1] in ['F', 'f', 'O', 'o', 'G', 'g', 'C', 'c']:
            symbol_name = parts[-1]
            try:
                demangled_name = cxxfilt.demangle(symbol_name)
                symbols.append(demangled_name)
            except cxxfilt.InvalidName:
                symbols.append(symbol_name)

    return symbols

def get_all_symbols(obj_paths):
    all_symbols = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(get_demangled_symbols, obj_path) for obj_path in obj_paths]
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            symbols = future.result()
            all_symbols[obj_paths[i]] = {'deps': symbols}

    return all_symbols

def store_symbols_to_json(obj_paths, json_path):
    symbols = get_all_symbols(obj_paths)
    with open(json_path, 'w') as f:
        # Write the symbols to a JSON file
        json.dump(symbols, f, indent=4)

# Example usage
if __name__ == '__main__':
    obj_paths = [line.strip() for line in sys.stdin]
    json_path = 'output.json'
    store_symbols_to_json(obj_paths, json_path)
