from collections import Counter
import re
import subprocess
from flask import Flask, request, jsonify
import clang.cindex
import os
import ast_parser
import utils
from flask_cors import CORS, cross_origin
import shlex
# from sh import git

# Set the path to the libclang library file
clang.cindex.Config.set_library_file("/home/mg/clang-llvm/rel-build/lib/libclang.so")

app = Flask(__name__)
CORS(app)

def get_ast(node, file, pass_flag=False):
    # ast = {
    #     "kind": str(node.kind),
    #     "spelling": node.spelling,
    #     "children": [],
    #     ""
    # }
    try:
        # location = node.location
        location = node.extent.start
        # print(location.file)
        if not (location.file is None or location.file.name == file):
        # if not (location.file.name == file or pass_flag):
            return None
        ast = {
            "kind": str(node.kind),
            "spelling": node.spelling,
            "nodeType": node.type.spelling,
            "location": {
                "line": location.line,
                "column": location.column,
                "offset": location.offset,
                "endLine": node.extent.end.line,
                "endColumn": node.extent.end.column,
                "endOffset": node.extent.end.offset
            },
            "offset": location.offset,
            "children": []
        }

        for child in node.get_children():
            ch = get_ast(child, file)
            if not ch is None: ast["children"].append(ch)

        return ast
    except Exception as e:
        return None


@app.route("/code_from_ast", methods=["POST"])
@cross_origin()
def code_from_ast():
    ast = request.get_json()
    if "ast" in ast:
        ast = ast["ast"]
    code = ast_parser.ast_to_code(ast, "")
    return code


@app.route("/ast", methods=["POST"])
@cross_origin()
def ast():
    code = request.data.decode("utf-8")

    index = clang.cindex.Index.create()
    translation_unit = index.parse(
        path="sample.cpp", unsaved_files=[("sample.cpp", code)], args=["-std=c++17", "-x", "c++"]
    )

    root = translation_unit.cursor
    ast = get_ast(root)

    return jsonify(ast)


include_dirs = [
    "/home/mg/chromium/src",
    # "/path/to/your/second/include",
]

# Convert the include directories into Clang-compatible arguments
include_args = [f"-I{include_dir}" for include_dir in include_dirs]

@app.route("/ast_from_file", methods=["GET"])
@cross_origin()
def ast_from_file():
    path = request.args.get('file')
    commit = request.args.get('commit', 'HEAD')
    repo_path = "/home/mg/chromium/src/third_party/blink"

    path = utils.find_files_with_name(repo_path, path)
    if len(path) > 1 or len(path) == 0:
        return jsonify(path)

    abs_path = path[0]
    path = "./" + os.path.relpath(path[0], repo_path)
    latest_commit = subprocess.check_output(
        f"cd {repo_path} && git log -n 1 --pretty=format:%H {path}", shell=True
    ).decode().strip()
    try:
        # subprocess.run(
        #     f"cd {repo_path} && git show {commit}:{path} > {path} && cd -", shell=True, check=True
        # )
        # except:
            # pass
        command = f"cd {repo_path} && git show {commit}:{path} && cd -"
        file_contents = subprocess.check_output(command, shell=True).decode('utf-8')

        index = clang.cindex.Index.create()
        args=["-std=c++17", "-x", "c++", "-I/home/mg/chromium/src/"]
        # args = include_args
        # args=[]
        translation_unit = index.parse(
            path=abs_path, args=args
            , unsaved_files=[(abs_path, file_contents)]
        )
        root = translation_unit.cursor
        ast = get_ast(root, abs_path, True)
        # try:
        # subprocess.run(
        #     f"cd {repo_path} && git show {latest_commit}:{path} > {path} && cd -", shell=True, check=True
        # )
        # except:
        #     pass
        return jsonify({'contents': ast})
    except:
        return jsonify({'contents': subprocess.getoutput()})


@app.route("/src", methods=["GET"])
@cross_origin()
def src():
    path = request.args.get('file')
    commit = request.args.get('commit', 'HEAD')
    repo_path = "/home/mg/chromium/src/third_party/blink"
    path = utils.find_files_with_name(repo_path, path)

    if len(path) > 1 or len(path) == 0:
        return jsonify(path)
    
    path = "./" + os.path.relpath(path[0], repo_path)
    command = f"cd {repo_path} && git show {commit}:{path} && cd -"
    file_contents = subprocess.check_output(command, shell=True).decode('utf-8')
    # with open(path, 'r') as file:
    return jsonify({'contents': file_contents})

@app.route('/git', methods=['GET'])
@cross_origin()
def git_rev_parse():
    rev_arg = request.args.get('rev')
    rev_arg = shlex.quote(rev_arg)
    repo_dir = "/home/mg/chromium/src/third_party/blink"
    cmd = f"git -C {repo_dir} rev-parse {rev_arg}"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return jsonify({'success': True, 'message': stdout.decode().strip()})
    else:
        return jsonify({'success': False, 'message': stderr.decode().strip()}), 400

@app.route('/histogram', methods=['GET'])
@cross_origin()
def histogram():
    path = request.args.get('text')
    path = utils.find_files_with_name("/home/mg/chromium/src/third_party/blink", path)

    if len(path) > 1 or len(path) == 0:
        return jsonify(path)
    
    path = path[0]
    regex = request.args.get('regex', "[A-Za-z_][A-Za-z_0-9]*")
    with open(path, 'r') as f:
        text = f.read()
    
    if not text or not regex:
        return jsonify(error='Please provide both text and regex parameters')
    
    matches = re.findall(regex, text)
    counts = Counter(matches)
    
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    return jsonify(sorted_counts)


@app.route('/tokenize', methods=['POST'])
@cross_origin()
def tokenize():
    path = request.data.decode("utf-8")
    path = utils.find_files_with_name("/home/mg/chromium/src/third_party/blink", path)
    if len(path) > 1 or len(path) == 0:
        return jsonify(path)
    path = path[0]
    index = clang.cindex.Index.create()
    args=["-std=c++17", "-x", "c++"]
    # args = include_args
    # args=[]
    tu = index.parse(
        path=path, args=args
    )
    try:
        tokens = []
        for token in tu.get_tokens(extent=tu.cursor.extent):
            tokens.append({'spelling': token.spelling, 'kind': str(token.kind)})
    except:
        return tu
    
    return jsonify(tokens)


if __name__ == "__main__":
    app.run(debug = True, port = 5000, host='0.0.0.0')
