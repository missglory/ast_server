lexer = CppLexer()

# Tokenize the code using the lexer
tokens = lexer.get_tokens(code)

# Initialize variables to store classes, namespaces, and functions
classes = {}
namespaces = {}
functions = {}

# Initialize variables to store the current namespace and class
current_namespace = ''
current_class = ''

# Loop over the tokens and extract classes, namespaces, and functions
for token_type, token_value in tokens:
		if token_type is Name.Namespace:
				current_namespace = token_value
				namespaces[current_namespace] = []
				current_class = ''
		elif token_type is Keyword and token_value == 'class':
				current_class = next(tokens)[1]
				classes[current_class] = {
						'namespace': current_namespace, 'functions': []}
		elif token_type is Name.Function:
				function_name = token_value
				function_args = []

				# Loop over the tokens until we find the end of the function definition
				for sub_token_type, sub_token_value in tokens:
						if sub_token_type is Punctuation and sub_token_value == '(':
								# We've found the start of the argument list
								break
				else:
						# We didn't find the start of the argument list, so skip this token
						continue

				# Loop over the tokens in the argument list
				for sub_token_type, sub_token_value in tokens:
						if sub_token_type is Punctuation and sub_token_value == ')':
								# We've found the end of the argument list
								break
						elif sub_token_type is Name:
								# We've found an argument name
								function_args.append(sub_token_value)

				# Store the function information in the current class or namespace
				if current_class:
						classes[current_class]['functions'].append(
								{'name': function_name, 'args': function_args})
				else:
						namespaces[current_namespace].append(
								{'name': function_name, 'args': function_args})