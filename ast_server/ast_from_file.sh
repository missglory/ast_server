#!sh
server_url="http://192.168.0.155:5000"

# Read the C++ code from a file (e.g., sample.cpp)
input_file="min_sample.cpp"
cpp_code="computed_style_utils.cc"

# Send the C++ code to the /ast endpoint and store the result in a variable
ast_result=$(curl -s -X POST -H "Content-Type: text/plain" --data "$cpp_code" $server_url/ast_from_file)

echo "$ast_result"
