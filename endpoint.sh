#!sh
# server_url="http://192.168.0.155:5000"
set -e
server_url="http://localhost:5000"
endpoint="${1:-ast_from_file}"
data="${2:-computed_style_utils.cc}"
method="${3:-GET}"
ast_result=$(curl -s -X $method -H "Content-Type: text/plain" "$server_url"/"$endpoint"?$data)
echo "$ast_result"
