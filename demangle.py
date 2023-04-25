import sys
import subprocess
import json
import concurrent.futures
import cxxfilt
import threading
import multiprocessing

def get_demangled_symbols(obj_path):
    # Run the objdump command to extract the symbol names from the object file
    objdump_output = subprocess.check_output(['objdump', '-t', obj_path])

    # Parse the objdump output and extract the symbol names
    symbols = []
    for line in objdump_output.decode().splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[1] in ['F', 'f', 'O', 'o', 'G', 'g', 'C', 'c', 'T', 't', '.text']:
            symbol_name = parts[-1]
            try:
                demangled_name = cxxfilt.demangle(symbol_name)
                symbols.append(demangled_name)
            except cxxfilt.InvalidName:
                symbols.append(symbol_name)

    return obj_path, symbols

def get_all_symbols(obj_paths):
    # Use a ThreadPoolExecutor to run the `get_demangled_symbols` function concurrently
    all_symbols = {}
    # with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        # futures = [executor.submit(get_demangled_symbols, obj_path) for obj_path in obj_paths]
        # concurrent.futures.wait(futures)
        # for i, future in enumerate(concurrent.futures.as_completed(futures)):
            # obj_path = obj_paths[i]
            # symbols = future.result()
            # all_symbols[obj_path] = {'deps': symbols}
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for res in pool.map(get_demangled_symbols, obj_paths):
            if len(res[1]):
                all_symbols[res[0]] = {'deps': res[1]}
    return all_symbols

def store_symbols_to_json(obj_paths, json_path):
    symbols = get_all_symbols(obj_paths)
    with open(json_path, 'w') as f:
        # Write the symbols to a JSON file
        for k in symbols.keys():
            if 'longhands' in k:
                print(len(symbols[k]["deps"]))
        json.dump(symbols, f, indent=4)

# Example usage
if __name__ == '__main__':
    obj_paths = [line.strip() for line in sys.stdin]
    json_path = 'output.json'
    store_symbols_to_json(obj_paths, json_path)