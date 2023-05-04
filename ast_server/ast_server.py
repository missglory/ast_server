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

def get_ast(node):
    # ast = {
    #     "kind": str(node.kind),
    #     "spelling": node.spelling,
    #     "children": [],
    #     ""
    # }
    location = node.location
    ast = {
        "kind": str(node.kind),
        "spelling": node.spelling,
        "location": {
            "line": location.line,
            "column": location.column,
            "offset": location.offset,
            "endLine": node.extent.end.line,
            "endColumn": node.extent.end.column
        },
        "children": []
    }

    for child in node.get_children():
        ast["children"].append(get_ast(child))

    print(ast)
    return ast


@app.route("/code_from_ast", methods=["POST"])
def code_from_ast():
    ast = request.get_json()
    if "ast" in ast:
        ast = ast["ast"]
    code = ast_parser.ast_to_code(ast, "")
    return code


@app.route("/ast", methods=["POST"])
def ast():
    code = request.data.decode("utf-8")

    index = clang.cindex.Index.create()
    translation_unit = index.parse(
        path="sample.cpp", unsaved_files=[("sample.cpp", code)], args=["-std=c++17", "-x", "c++"]
    )

    root = translation_unit.cursor
    ast = get_ast(root)

    return jsonify(ast)


@app.route("/ast_from_file", methods=["POST"])
def ast_from_file():
    path = request.data.decode("utf-8")
    path = utils.find_files_with_name("/home/mg/chromium/src/third_party/blink", path)

    if len(path) > 1:
        return jsonify(path)
    
    path = path[0]

    index = clang.cindex.Index.create()
    translation_unit = index.parse(
        path=path, args=["-std=c++17", "-x", "c++"]
    )

    root = translation_unit.cursor
    ast = get_ast(root)

    return jsonify(ast)


@app.route("/src", methods=["POST"])
@cross_origin()
def src():
    path = request.data.decode("utf-8")
    path = utils.find_files_with_name("/home/mg/chromium/src/third_party/blink", path)

    if len(path) > 1 or len(path) == 0:
        return jsonify(path)
    
    path = path[0]
    with open(path, 'r') as file:
        return jsonify({'contents': file.read()})


if __name__ == "__main__":
    app.run(debug = True, port = 5000, host='0.0.0.0')
