from flask import Flask, request, jsonify
import clang.cindex
import os
import ast_parser
import utils
from flask_cors import CORS, cross_origin

# Set the path to the libclang library file
clang.cindex.Config.set_library_file("/home/mg/gh/llvm-project/build/lib/libclang.so")

app = Flask(__name__)
CORS(app)

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
    ast = ast_parser.get_ast(root)

    return jsonify(ast)


include_dirs = [
    "/home/mg/chromium/src",
    # "/path/to/your/second/include",
]

# Convert the include directories into Clang-compatible arguments
include_args = [f"-I{include_dir}" for include_dir in include_dirs]


@app.route("/ast_from_file", methods=["POST"])
@cross_origin()
def ast_from_file():
    path = request.data.decode("utf-8")
    translation_unit = ast_parser.get_translation_unit(path)
    try:
        root = translation_unit.cursor
        ast = ast_parser.get_ast(root)
        return jsonify({'contents': ast})
    except:
        return translation_unit


@app.route('/tokenize', methods=['POST'])
def tokenize():
    path = request.data.decode("utf-8")
    tu = ast_parser.get_translation_unit(path)
    try:
        tokens = []
        for token in tu.get_tokens(extent=tu.cursor.extent):
            tokens.append({'spelling': token.spelling, 'kind': str(token.kind)})
    except:
        return tu
    
    return jsonify(tokens)

@app.route("/src", methods=["POST"])
@cross_origin()
def src():
    path = request.data.decode("utf-8")
    path = utils.find_files_with_name("/home/mg/chromium/src/third_party/blink", path)

    if not len(path) == 1:
        return jsonify(path)
    
    path = path[0]
    with open(path, 'r') as file:
        return jsonify({'contents': file.read()})


if __name__ == "__main__":
    app.run(debug = True, port = 5000, host='0.0.0.0')
