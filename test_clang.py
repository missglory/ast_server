import clang.cindex as clang

def parse_cpp_code(code):
    index = clang.Index.create()
    tu = index.parse('file.cpp', args=['-x', 'c++', '-std=c++17'], unsaved_files=[('file.cpp', code)])

    classes = {}
    namespaces = {}

    def visit_namespace(node, namespace_name):
        namespaces[namespace_name] = []
        for child in node.get_children():
            if child.kind == clang.CursorKind.NAMESPACE:
                visit_namespace(child, namespace_name + '::' + child.spelling)
            elif child.kind == clang.CursorKind.CLASS_DECL:
                visit_class(child, namespace_name)

    def visit_class(node, namespace_name):
        class_name = node.spelling
        classes[class_name] = {'namespace': namespace_name, 'functions': [], 'fields': []}
        for child in node.get_children():
            if child.kind == clang.CursorKind.CXX_METHOD:
                visit_function(child, class_name, namespace_name)
            elif child.kind == clang.CursorKind.FIELD_DECL:
                visit_field(child, class_name)

    def visit_function(node, class_name, namespace_name):
        function_name = node.spelling
        function_args = []
        for arg in node.get_children():
            if arg.kind == clang.CursorKind.PARM_DECL:
                arg_name = arg.spelling
                arg_type = arg.type.spelling
                function_args.append({'name': arg_name, 'type': arg_type})
        classes[class_name]['functions'].append({'name': function_name, 'args': function_args})

    def visit_field(node, class_name):
        field_name = node.spelling
        field_type = node.type.spelling
        field_offset = node.location.offset
        field_end_offset = field_offset + node.extent.end.offset - node.extent.start.offset
        classes[class_name]['fields'].append({'name': field_name, 'type': field_type, 'offset': field_offset, 'end_offset': field_end_offset})

    for node in tu.cursor.get_children():
        if node.kind == clang.CursorKind.NAMESPACE:
            visit_namespace(node, node.spelling)
        elif node.kind == clang.CursorKind.CLASS_DECL:
            visit_class(node, '')

    return classes, namespaces

parse