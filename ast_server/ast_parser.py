import clang
from flask import jsonify
import utils

def get_ast(node):
    location = node.location
    ast = {
        "kind": str(node.kind),
        "spelling": node.spelling,
        "location": {
            "line": location.line,
            "column": location.column,
            "offset": location.offset,
            "endLine": node.extent.end.line,
            "endColumn": node.extent.end.column,
            "endOffset": node.extent.end.offset
        },
        "children": []
    }

    for child in node.get_children():
        ast["children"].append(get_ast(child))

    return ast


def ast_to_code(node, code):
    # print(node)

    if node["kind"] == "CursorKind.NAMESPACE":
        code += f"namespace {node['spelling']} \n"
    elif node["kind"] == "CursorKind.TYPEDEF_DECL":
        code += f"typedef {node['spelling']};\n"
    elif node["kind"] == "CursorKind.CLASS_DECL":
        code += f"class {node['spelling']} \n"
    elif node["kind"] == "CursorKind.CXX_ACCESS_SPEC_DECL":
        code += f"{node['spelling']}:\n"
    elif node["kind"] == "CursorKind.FIELD_DECL":
        code += f"{node['spelling']};\n"
    elif node["kind"] == "CursorKind.FUNCTION_DECL":
        code += f"{node['spelling']}() {{\n"
    elif node["kind"] == "CursorKind.CXX_METHOD":
        code += f"{node['spelling']}() {{\n"
    elif node["kind"] == "CursorKind.RETURN_STMT":
        code += "return "
    elif node["kind"] == "CursorKind.INTEGER_LITERAL":
        code += f"{node['spelling']}"

    for child in node["children"]:
        code = ast_to_code(child, code)

    if node["kind"] in ["CursorKind.NAMESPACE", "CursorKind.CLASS_DECL", "CursorKind.CXX_METHOD", "CursorKind.FUNCTION_DECL"]:
        code += "}\n"

    return code


def get_translation_unit(path: str):
    path = utils.find_files_with_name("/home/mg/chromium/src/third_party/blink", path)
    if not len(path) == 1:
        return jsonify(path)
    path = path[0]

    index = clang.cindex.Index.create()
    translation_unit = index.parse(
        path=path, args=["-std=c++17", "-x"]
    )

    return translation_unit