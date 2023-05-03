#!/bin/bash

# Set the server URL
server_url="http://127.0.0.1:5000"

# Read the C++ code from a file (e.g., sample.cpp)
input_file="min_sample.cpp"
cpp_code=$(cat $input_file)

# Send the C++ code to the /ast endpoint and store the result in a variable
ast_result=$(curl -s -X POST -H "Content-Type: text/plain" --data "$cpp_code" $server_url/ast)

# echo "$ast_result"

# Send the AST result to the /code_from_ast endpoint and store the result in a variable
code_from_ast=$(curl -s -X POST -H "Content-Type: application/json" --data "$ast_result" $server_url/code_from_ast)

# Print the generated code
echo "$code_from_ast"
