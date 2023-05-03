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
