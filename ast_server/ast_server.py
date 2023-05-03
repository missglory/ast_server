from flask import Flask, request, jsonify
import clang.cindex
import os
import ast_parser

# Set the path to the libclang library file
clang.cindex.Config.set_library_file("/home/mg/gh/llvm-project/build/lib/libclang.so")

app = Flask(__name__)

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
            "column": location.column
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

if __name__ == "__main__":
    app.run()