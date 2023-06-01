import json
import argparse
import re

def callgrind_to_json(callgrind_content):
    result = {}
    lines = callgrind_content.split('\n')
    for line in lines:
        if line.startswith("fn="):
            function_name = line.split('=')[1].strip()
            result[function_name] = {}
        elif line.startswith("cfn="):
            called_function_name = line.split('=')[1].strip()
            if 'calls' not in result[function_name]:
                result[function_name]['calls'] = []
            result[function_name]['calls'].append(called_function_name)
        elif line.startswith("calls="):
            call_count = line.split('=')[1].strip()
            result[function_name]['call_count'] = call_count
    return result

def callgrind_from_file(file):
    with open(file, 'r') as f:
        return callgrind_to_json(f.read())

def check_unique_identifiers_and_map(json_data):
    identifier_pattern = r'\((\d+)\)'
    identifier_to_fn_map = {}
    identifiers = set()

    for fn in json_data.keys():
        match = re.search(identifier_pattern, fn)
        if match:
            identifier = match.group(1)

            # Check for uniqueness
            if identifier in identifiers:
                raise ValueError(f'Duplicate identifier found: {identifier} in function {fn}')

            identifiers.add(identifier)

            # Map the identifier to the function name
            identifier_to_fn_map[identifier] = fn
    
    return identifier_to_fn_map

def main():
    parser = argparse.ArgumentParser(description='Transform callgrind format to json.')
    parser.add_argument('callgrind_file', help='The callgrind input file to be converted.')
    args = parser.parse_args()

    data = callgrind_from_file(args.callgrind_file)
    json_data = json.dumps(data, indent=2)

    print(check_unique_identifiers_and_map(data))

    with open('output.json', 'w') as json_file:
        json_file.write(json_data)

if __name__ == "__main__":
    main()