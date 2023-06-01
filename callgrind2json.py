import json
import argparse
import re
from collections import defaultdict

def callgrind_to_json(callgrind_content, postprocess = True):
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
    if postprocess:
        identifier_to_fn_map, identifiers_count = check_unique_identifiers_and_map(result)
        result = post_process_callgrind_json(result, identifier_to_fn_map=identifier_to_fn_map)
    return result


def callgrind_from_file(file):
    with open(file, 'r') as f:
        return callgrind_to_json(f.read())

def check_unique_identifiers_and_map(json_data):
    identifier_pattern = r'\((\d+)\)'
    identifier_to_fn_map = defaultdict(list)
    identifiers_count = defaultdict(int)

    for fn in json_data.keys():
        match = re.search(identifier_pattern, fn)
        if match:
            identifier = match.group(1)

            # Count the occurrence of identifiers
            identifiers_count[identifier] += 1

            # Map the identifier to the function name
            identifier_to_fn_map[identifier].append(fn)
    
    return identifier_to_fn_map, identifiers_count

def post_process_callgrind_json(data, identifier_to_fn_map):
    for function_name in list(data.keys()):
        identifier = re.search(r'\((\d+)\)', function_name).group(1)
        # If the function name is empty, replace it with the one from the map
        if function_name == f'({identifier})':
            new_function_name = max(identifier_to_fn_map.get(identifier, function_name), key=len)
            target = data.pop(function_name)
            data[new_function_name] = target
        else:
            new_function_name = function_name
        # Check the called function names
        data[new_function_name]["label"] = new_function_name
        if 'calls' in data[new_function_name]:
            for i, called_function_name in enumerate(data[new_function_name]['calls']):
                identifier = re.search(r'\((\d+)\)', called_function_name).group(1)
                if called_function_name == f'({identifier})':
                    new_called_function_name = identifier_to_fn_map.get(identifier, called_function_name)
                    data[new_function_name]['calls'][i] = new_called_function_name
    return data


def main():
    parser = argparse.ArgumentParser(description='Transform callgrind format to json.')
    parser.add_argument('callgrind_file', help='The callgrind input file to be converted.')
    args = parser.parse_args()

    data = callgrind_from_file(args.callgrind_file)
    # json_data = json.dumps(data, indent=2)

    # identifier_to_fn_map, identifiers_count = check_unique_identifiers_and_map(data)
    # for identifier, count in identifiers_count.items():
    #     if count > 1:
    #         print(f'Identifier: {identifier}, Count: {count}, Functions: {identifier_to_fn_map[identifier]}')

    # json_data = post_process_callgrind_json(data, identifier_to_fn_map)
    json_data = json.dumps(json_data, indent=2)

    with open('output.json', 'w') as json_file:
        json_file.write(json_data)

if __name__ == "__main__":
    main()