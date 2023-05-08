#!sh
# server_url="http://192.168.0.155:5000"
server_url="http://localhost:5000"
data="${2:-computed_style_utils.cc}"
endpoint="${1:-ast_from_file}"
ast_result=$(curl -s -X POST -H "Content-Type: text/plain" --data "$data" "$server_url"/"$endpoint")
echo "$ast_result"
