import json
import argparse

def callgrind_to_json(callgrind_file):
    result = {}
    with open(callgrind_file, 'r') as f:
        for line in f:
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

def main():
    parser = argparse.ArgumentParser(description='Transform callgrind format to json.')
    parser.add_argument('callgrind_file', help='The callgrind input file to be converted.')
    args = parser.parse_args()

    data = callgrind_to_json(args.callgrind_file)
    json_data = json.dumps(data, indent=2)

    with open('output.json', 'w') as json_file:
        json_file.write(json_data)

if __name__ == "__main__":
    main()

