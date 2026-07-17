from colorama import init, Fore, Style

# Initialize colorama (needed for Windows support)
init(autoreset=True)

# Fancy colored print
def cprint(*out, color=Fore.WHITE, **kwargs): 
    # Pass the modified tuple to the standard print function
    print(*(f"{color}{o}" for o in out), **kwargs)

def print_original_code(*out, **kwargs):
    color = Fore.GREEN
    print() # Empty new line for visability
    cprint(*out, color=color, **kwargs)

def print_debug_info(*out, **kwargs):
    tab_depth = kwargs.pop('tab_depth', 4)
    
    color = Fore.WHITE
    if tab_depth:
        cprint(' '*(4 * tab_depth - 1), *out, color=color, **kwargs)
    else:
        cprint(*out, color=color, **kwargs)

def print_extra_info(*out, **kwargs):
    tab_depth = kwargs.pop('tab_depth', 4)
    
    color = Fore.BLUE
    if tab_depth:
        cprint(' '*(4 * tab_depth - 1), *out, color=color, **kwargs)
    else:
        cprint(*out, color=color, **kwargs)


# tab_depth is used for printing, it has no functional use
# depth is the current stack depth. Operations that need to
# use temporary variables start with tmp{depth}

def assert_stack_decorator(n):
    # Only res is allowed to be "tmp%d"%(depth)
    # This is a quick check the basic operations haven't been
    # called incorrectly
    def decorator(f):
        def g(*args):
            assert len(args) == n + 2
            depth = args[n]
            tab_depth = args[n]
            assert depth >= 0
            assert tab_depth >= 0

            for i in range(1, n):
                assert args[i] != 'tmp%d' % depth

            return f(*args)
        
        return g
    return decorator


# Assign and arithmetic

@assert_stack_decorator(n=2)
def ASSIGN(res, a, depth, tab_depth):
    # res = a
    print_debug_info(res, '=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def ADD(res, a, b, depth, tab_depth):
    # res = a + b
    print_debug_info(res, '=', a, '+', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def ADD_ASSIGN(res, a, depth, tab_depth):
    # res += a
    print_debug_info(res, '+=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def MUL(res, a, b, depth, tab_depth):
    # res = a * b
    print_debug_info(res, '=', a, '*', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def MUL_ASSIGN(res, a, depth, tab_depth):
    # res *= a
    print_debug_info(res, '*=', a, tab_depth=tab_depth)

# Logics
@assert_stack_decorator(n=3)
def LOGIC_AND(res, a, b, depth, tab_depth):
    # res = a && b
    print_debug_info(res, '=', a, '&&', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def LOGIC_AND_ASSIGN(res, a, depth, tab_depth):
    # res &&= a
    print_debug_info(res, '&&=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def LOGIC_AND_NOT(res, a, b, depth, tab_depth):
    # res = a && !b
    print_debug_info(res, '=', a, '&& not', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def LOGIC_AND_NOT_ASSIGN(res, a, depth, tab_depth):
    # res &&= !a
    print_debug_info(res, '&&= not', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def LOGIC_OR(res, a, b, depth, tab_depth):
    # res = a || b
    print_debug_info(res, '=', a, '||', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def LOGIC_OR_ASSIGN(res, a, depth, tab_depth):
    # res ||= a
    print_debug_info(res, '||=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def LOGIC_OR_NOT(res, a, b, depth, tab_depth):
    # res = a || !b
    print_debug_info(res, '=', a, '|| not', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def LOGIC_OR_NOT_ASSIGN(res, a, depth, tab_depth):
    # res ||= !a
    print_debug_info(res, '||= not', a, tab_depth=tab_depth)


# Selectors
@assert_stack_decorator(n=3)
def SEL_IF(res, a, b, depth, tab_depth):
    # res = a (if b)
    print_debug_info('if', b, ':', res, '=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def SEL_IF_NOT(res, a, b, depth, tab_depth):
    # res = a (if not b)
    print_debug_info('if not', b, ':', res, '=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=4)
def SEL_BOOL(res, a, b, c, depth, tab_depth):
    # res = a if b else c
    print_debug_info(res, '=', a, 'if', b, 'else', c, tab_depth=tab_depth)

@assert_stack_decorator(n=5)
def SEL_EQ(res, a, b, c, d, depth, tab_depth):
    # res = a if b == c else d
    print_debug_info(res, '=', a, 'if', b, '==', c, 'else', d, tab_depth=tab_depth)

@assert_stack_decorator(n=5)
def SEL_OR(res, a, b, c, d, depth, tab_depth):
    # res = a if b || c else d
    print_debug_info(res, '=', a, 'if', b, '||', c, 'else', d, tab_depth=tab_depth)

@assert_stack_decorator(n=5)
def SEL_OR_NOT(res, a, b, c, d, depth, tab_depth):
    # res = a if b || !c else d
    print_debug_info(res, '=', a, 'if', b, '|| not', c, 'else', d, tab_depth=tab_depth)

@assert_stack_decorator(n=5)
def SEL_AND(res, a, b, c, d, depth, tab_depth):
    # res = a if b && c else d
    print_debug_info(res, '=', a, 'if', b, '&&', c, 'else', d, tab_depth=tab_depth)

@assert_stack_decorator(n=5)
def SEL_AND_NOT(res, a, b, c, d, depth, tab_depth):
    # res = a if b && c else d
    print_debug_info(res, '=', a, 'if', b, '&& not', c, 'else', d, tab_depth=tab_depth)



scripts = {}
def label_tree(tree, source_name):
    # This recursively visits every node in the tree
    for node in ast.walk(tree):
        node.source_file = source_name
    return tree



scripts['main.py'] = """
if x == 5 or y == 24:
    k = x + (y + z) + 5.0 == 1.0

    if y == 10.0 or z == 100.0:
        k = x + (y + z) + 5.0 == 1.0
        x = 32.0
    elif x == 100.0:
        k = 100.0
    elif x == 102.0:
        pass
    else:
        k = 1
else:
    banana = 423
w = sqrt(a)
"""


function_definitions = {}

import ast
import inspect

def register_function(func):
    """Decorator to attach AST and source metadata to a function."""
    # 1. Get the source code of the function
    source_script = inspect.getsource(func)

    # 2. Store without decorator
    source_script = '\n'.join(source_script.split('\n')[1:])
    source = func.__name__
    scripts[source] = source_script
     
    # 3. Parse into AST
    tree = ast.parse(source_script)
    # Tell all node where they come from
    label_tree(tree, source)
    
    # 4. Attach to the function object
    func._ast_tree = tree
    function_definitions[source] = tree
    
    return func

import ast
import copy

def rename_nodes(node, mapping):
    """Recursively rename variables in an AST node based on a mapping."""
    if isinstance(node, ast.Name) and node.id in mapping:
        node.id = mapping[node.id]
    
    # Recursively check children
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    rename_nodes(item, mapping)
        elif isinstance(value, ast.AST):
            rename_nodes(value, mapping)
    return node

def handle_call_inline(node):

    # 1. Get the definition
    func_def = function_definitions[node.func.id]
    
    # 2. Create the mapping (a -> x, b -> y)
    arg_names = [arg.arg for arg in func_def.body[0].args.args]
    # Assuming node.args contains the names/constants from the caller
    mapping = {formal: actual.id if isinstance(actual, ast.Name) else str(actual.value) 
               for formal, actual in zip(arg_names, node.args)}
    
    # 3. Process the body with the new mapping
    # We copy the body to avoid mutating the original function definition
    substituted_body = []
    for stmt in func_def.body[0].body:
        new_stmt = copy.deepcopy(stmt)
        rename_nodes(new_stmt, mapping)
        substituted_body.append(new_stmt)
    

    return substituted_body

@register_function
def sqrt(x):
    guess = (1.0   + x      ) * 4.3e-12
    guess = (guess + x/guess) * 2.1e-06
    guess = (guess + x/guess) * 0.0014
    guess = (guess + x/guess) * 0.037
    guess = (guess + x/guess) * 0.19
    guess = (guess + x/guess) * 0.41
    guess = (guess + x/guess) * 0.495
    guess = (guess + x/guess) * 0.5
    guess = (guess + x/guess) * 0.5

    return guess


def get_keyword_at_line(lineno, keyword, source):
    source_lines = scripts[source].splitlines()
    # Adjust for 1-based indexing in AST
    line = source_lines[lineno - 1].strip()
    if line.startswith(keyword):
        return keyword
    return ""

def get_else_lineno(if_node, source):
    """Finds the line number of the 'else' keyword after the body of an if_node."""
    source_lines = scripts[source].splitlines()
    # Start looking after the end of the body
    start_search = if_node.body[-1].end_lineno + 1
    for i in range(start_search, len(source_lines)):
        if get_keyword_at_line(i, 'else', source):
            return i
    return if_node.end_lineno

import ast

class NodeMetadata:
    def __init__(self, name, lineno, end_lineno, source):
        self.name = name
        self.lineno = lineno
        self.end_lineno = end_lineno
        self.source = source
    
    def __repr__(self):
        # Shows both lines if it spans multiple, otherwise just the one
        line_info = f"line {self.lineno}" if self.lineno == self.end_lineno else f"lines {self.lineno}-{self.end_lineno}"
        return f"Node({self.name}, {self.source}:{line_info})"

def node_to_list(node):
    # Retrieve line numbers; default to 0 if not present
    start = getattr(node, 'lineno', 0)
    end = getattr(node, 'end_lineno', start)
    source = getattr(node, 'source_file', 'unknown')

    # Constants: Include metadata
    if isinstance(node, ast.Constant):
        return NodeMetadata(node.value, start, end, source)
    
    # Variables: Include metadata
    elif isinstance(node, ast.Name):
        return NodeMetadata(node.id, start, end, source)
    
    # Assignment
    elif isinstance(node, ast.Assign):
        target = node.targets[0].id
        return [NodeMetadata('=', start, end, source), target, node_to_list(node.value)]
    
    # Binary Operations
    elif isinstance(node, ast.BinOp):
        op_map = {ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/', ast.Pow: '**'}
        op_name = op_map.get(type(node.op), type(node.op).__name__)
        return [NodeMetadata(op_name, start, end, source), node_to_list(node.left), node_to_list(node.right)]
    
    # Comparisons
    elif isinstance(node, ast.Compare):
        op_type = type(node.ops[0])
        op_map = {
            ast.Lt: '<', ast.LtE: '<=', ast.Gt: '>', 
            ast.GtE: '>=', ast.Eq: '==', ast.NotEq: '!='
        }
        op_symbol = op_map.get(op_type, op_type.__name__)
        return [NodeMetadata(op_symbol, start, end, source), node_to_list(node.left), node_to_list(node.comparators[0])]

    # If/Else/Elif Statements
    # This step is complicated because of the way python AST handles "else if" and "elif" identially.
    # But because I want to closely match the original code, I need to seperate the cases here.
    elif isinstance(node, ast.If):
        # Header Metadata
        header_end = node.test.end_lineno
        header_meta = NodeMetadata('if', start, header_end, source)
        res = [header_meta, node_to_list(node.test)]
        
        # Body
        body_start = node.body[0].lineno
        body_end = node.body[-1].end_lineno
        res.append([NodeMetadata('body', body_start, body_end, source)] + [node_to_list(n) for n in node.body])
        
        # Handle orelse
        if node.orelse:
            # Detect ELIF
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                nested_if = node.orelse[0]
                if get_keyword_at_line(nested_if.lineno, 'elif', source):
                    # elif acts like an if: header + body
                    res.append([NodeMetadata('elif', nested_if.lineno, nested_if.test.end_lineno, source)] + [node_to_list(nested_if)])
                else:
                    # else: if
                    else_line = get_else_lineno(node, source)
                    res.append([NodeMetadata('else', else_line, else_line, source), node_to_list(nested_if)])
            else:
                # Plain ELSE
                else_line = get_else_lineno(node, source)
                body = [node_to_list(n) for n in node.orelse]
                res.append([NodeMetadata('else', else_line, else_line, source), [NodeMetadata('body', None, None, source), *body]])
        return res
    
    # Boolean Operations (and, or)
    elif isinstance(node, ast.BoolOp):
        op = 'or' if isinstance(node.op, ast.Or) else 'and'
        return [NodeMetadata(op, start, end, source), *[node_to_list(val) for val in node.values]]
    
    # Function Calls
    elif isinstance(node, ast.Call):
        if node.func.id in function_definitions:
            # Inline the function body
            inline_body = handle_call_inline(node)
            # Process the body as a list of operations
            func_body = function_definitions[node.func.id].body[0]
            body = [NodeMetadata('body', func_body.lineno, func_body.end_lineno, node.func.id)] + [node_to_list(n) for n in inline_body]
            return [NodeMetadata('function', func_body.lineno, func_body.end_lineno, node.func.id), body]
        else:
            # Standard call if not in registry

            # Dont allow for now
            assert False
            return [NodeMetadata(node.func.id, start, end), *[node_to_list(arg) for arg in node.args]]
    
    elif isinstance(node, ast.Pass):
        return [NodeMetadata('pass', start, end, source)]
    
    elif isinstance(node, ast.Return):
        return [NodeMetadata('return', start, end, source), node_to_list(node.value)]
    
    # Unexpected case in parser
    
    print('node?', node)
    assert False
    return None


depth = 0
def dfs(tree, p=True, store_only_if_p_is=True, tab_depth=0, true_false_mode=None, res_var=None):

    # p is logical statement used for if statement
    # variables can only be assigned if p==store_only_if_p_is
    # This is done to emulate the lack of if-statement in vmt:s

    # tab_depth is there just to make prints more pretty

    # true_false_mode = (true_val, false_val) is an optimal parameter that 
    # can be given to a non-trivial boolean expression.
    # The return variable in true false mode is always res_val.
    # If boolean expression is true, then res_val is assigned true_val
    # otherwise res_val is assigned false_val
    # This mode is there to make use of common tricks to save operations
    # in vmt scripts.

    # res_var is the request (temporary) variable to put the result in. 
    # If it is none, then it should be placed in tmp[depth].

    if not isinstance(tree, list):
        # Base case, leaf reached
        assert not true_false_mode
        assert not res_var
        return tree.name
   
    global depth
    match tree[0].name:
        case 'body':
            assert not true_false_mode
            assert not res_var
             
            if p == (not store_only_if_p_is):
                print_extra_info('# Inside hardcoded if-false, skipping...', tab_depth=tab_depth)
                return

            for node in tree[1:]:
                if node[0].name != 'if':
                    for ind in range(node[0].lineno - 1, node[0].end_lineno):
                        print_original_code(scripts[tree[0].source].split('\n')[ind])
                ans = dfs(node, p, store_only_if_p_is, tab_depth)
            
            return ans
        
        case 'pass':
            assert not true_false_mode
            assert not res_var
            
            return
        
        case '=':
            assert not true_false_mode
            assert not res_var
            assert len(tree) == 3
            _, var, res = tree
            
            res = dfs(res, p, store_only_if_p_is, tab_depth)
            if p == store_only_if_p_is:
                ## print_debug_info(var, '=', res, tab_depth=tab_depth)
                depth += 1
                ASSIGN(var, res, depth, tab_depth)
                depth -= 1
            elif p == (not store_only_if_p_is):
                # This case should be handled earlier, hardcoded if-Flase
                assert False
            
            elif store_only_if_p_is == True:
                ## print_debug_info('if', p, ':', var, '=', res, tab_depth=tab_depth)
                depth += 1
                SEL_IF(var, res, p, depth, tab_depth)
                depth -= 1
            else: # store_only_if_p_is == False
                ##print_debug_info('if not', p, ':', var, '=', res, tab_depth=tab_depth)
                depth += 1
                SEL_IF_NOT(var, res, p, depth, tab_depth)
                depth -= 1
            return var

        case '+':
            assert not true_false_mode
            assert not res_var
            assert len(tree) == 3
            _, a, b = tree
            if isinstance(a, list) and isinstance(b, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                depth -= 1
                
                ##print_debug_info(tmp1, '+=', tmp2, tab_depth=tab_depth)
                depth += 2
                ADD_ASSIGN(tmp1, tmp2, depth, tab_depth)
                depth -= 2

                return tmp1
            elif isinstance(a, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                
                ##print_debug_info(tmp1, '+=', tmp2, tab_depth=tab_depth)
                depth += 1
                ADD_ASSIGN(tmp1, tmp2, depth, tab_depth)
                depth -= 1

                return tmp1
            elif isinstance(b, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                
                ##print_debug_info(tmp2, '+=', tmp1, tab_depth=tab_depth)
                depth += 1
                ADD_ASSIGN(tmp2, tmp1, depth, tab_depth)
                depth -= 1

                return tmp2
            else:
                tmp = 'tmp%d' % depth
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                ##print_debug_info(tmp, '=', tmp1, '+', tmp2, tab_depth=tab_depth)
                
                ADD(tmp, tmp1, tmp2, depth, tab_depth)

                return tmp
        
        case '*':
            assert not true_false_mode
            assert not res_var
            assert len(tree) == 3
            _, a, b = tree
            if isinstance(a, list) and isinstance(b, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                depth -= 1
                
                ##print_debug_info(tmp1, '*=', tmp2, tab_depth=tab_depth)
                depth += 2
                MUL_ASSIGN(tmp1, tmp2, depth, tab_depth)
                depth -= 2

                return tmp1
            elif isinstance(a, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                
                ##print_debug_info(tmp1, '*=', tmp2, tab_depth=tab_depth)
                depth += 1
                MUL_ASSIGN(tmp1, tmp2, depth, tab_depth)
                depth -= 1

                return tmp1
            elif isinstance(b, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                
                ##print_debug_info(tmp2, '*=', tmp1, tab_depth=tab_depth)
                depth += 1
                MUL_ASSIGN(tmp2, tmp1, depth, tab_depth)
                depth -= 1

                return tmp2
            else:
                tmp = 'tmp%d' % depth
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                ##print_debug_info(tmp, '=', tmp1, '+', tmp2, tab_depth=tab_depth)
                
                MUL(tmp, tmp1, tmp2, depth, tab_depth)

                return tmp
        

        case '==':
            assert len(tree) == 3
            
            if not res_var:
                res_var = 'tmp%d' % depth

            if not true_false_mode:
                true_false_mode = (True, False)

            _, a, b = tree
            
            true_var, false_var = true_false_mode
            
            if isinstance(a, list) and isinstance(b, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                depth -= 1
                
                ## print_debug_info(res_var, '=', true_var, 'if', tmp1, '==', tmp2, 'else', false_var, tab_depth=tab_depth)

                depth += 2
                SEL_EQ(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)
                depth -= 2
            
            elif isinstance(a, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                
                ## print_debug_info(res_var, '=', true_var, 'if', tmp1, '==', tmp2, 'else', false_var, tab_depth=tab_depth)

                depth += 1
                SEL_EQ(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)
                depth -= 1
            
            elif isinstance(b, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                
                ## print_debug_info(res_var, '=', true_var, 'if', tmp1, '==', tmp2, 'else', false_var, tab_depth=tab_depth)

                depth += 1
                SEL_EQ(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)
                depth -= 1
            else:
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                
                ## print_debug_info(res_var, '=', true_var, 'if', tmp1, '==', tmp2, 'else', false_var, tab_depth=tab_depth)

                SEL_EQ(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)

            return res_var

        case 'if':
            # Note this is a plain if
            assert len(tree) == 3 or len(tree) == 4
            assert not true_false_mode
            assert not res_var

            orig_depth = depth
            
            orig_code = [scripts[tree[0].source].split('\n')[ind] for ind in range(tree[0].lineno - 1, tree[0].end_lineno)]
            print_original_code(*orig_code, sep='\n')
            
            if p != True: # We are part of nested if-statements
                if isinstance(tree[1], list):
                    if store_only_if_p_is:
                        res = dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode = (p, False))
                    else:
                        res = dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode = (p, True))
                    p = res
                else:
                    res = 'tmp%d' % depth
                    tmp = dfs(tree[1], p, store_only_if_p_is, tab_depth)
                    if store_only_if_p_is:
                        ##print_debug_info(res, '=', p, '&&', tmp, tab_depth=tab_depth)
                        LOGIC_AND(res, p, tmp, depth, tab_depth)
                        p = res
                    else:
                        ##print_debug_info(res, '=', p, '|| not', tmp, tab_depth=tab_depth)
                        LOGIC_OR_NOT(res, p, tmp, depth, tab_depth)
                        p = res
                depth += 1
                assert p == 'tmp%d' % (depth - 1)
            else:
                if isinstance(tree[1], list):
                    if store_only_if_p_is:
                        p = dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode = (True, False))
                        depth += 1
                        assert p == 'tmp%d' % (depth - 1)
                    else:
                        pass
                else:
                    if store_only_if_p_is:
                        tmp = dfs(tree[1], p, store_only_if_p_is, tab_depth)
                        # We must store the result in a seperate variable
                        # since tmp might not be a constant

                        if tmp == True or tmp == False:
                            p = tmp
                        else:
                            p = 'tmp%d' % depth
                            ##print_debug_info(p, '=', tmp, tab_depth=tab_depth)
                            ASSIGN(p, tmp, depth, tab_depth)
                            depth += 1
                            assert p == 'tmp%d' % (depth - 1)
                    else:
                        pass

            if p == store_only_if_p_is:
                pass # Trivial case
            elif p == (not store_only_if_p_is):
                pass # Trivial case
            else:
                print_extra_info('# Condition', p, '==', store_only_if_p_is, tab_depth=tab_depth)
            
            if len(tree) <= 4:
                # Main body
                tab_depth += 1
                dfs(tree[2], p, store_only_if_p_is, tab_depth)
                tab_depth -= 1

            if len(tree) == 4:
                # else/elif
                # Reverse current state of p
                dfs(tree[3], p, not store_only_if_p_is, tab_depth)
            
            depth = orig_depth
            return
        
        case 'elif':
            # If the tree, elif looks like ['elif', ['if', ...]]
            # elif is slightly different than if because how it handles p
            assert len(tree) == 2
            assert not true_false_mode
            assert not res_var

            # Get the if part of the elif
            tree = tree[1]
            assert len(tree) == 3 or len(tree) == 4
            assert not true_false_mode
            assert not res_var

            if p != 'tmp%d' % (depth - 1):
                # This case practically should never happen. Only happens if this was after
                # an "if True:" or "if False:"
                return dfs(tree, p, store_only_if_p_is, tab_depth)
            

            orig_depth = depth
            
            orig_code = [scripts[tree[0].source].split('\n')[ind] for ind in range(tree[0].lineno - 1, tree[0].end_lineno)]
            print_original_code(*orig_code, sep='\n')
            
            if isinstance(tree[1], list):
                if store_only_if_p_is:
                    res = dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode = (p, False), res_var=p)
                else:
                    res = dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode = (p, True), res_var=p)
                assert res == p
            else: 
                tmp = dfs(tree[1], p, store_only_if_p_is, tab_depth)
                if store_only_if_p_is:
                    ## print_debug_info(p, '&&=', tmp, tab_depth=tab_depth)
                    LOGIC_AND_ASSIGN(p, tmp, depth, tab_depth)
                else:
                    ## print_debug_info(p, '||= not', tmp, tab_depth=tab_depth)
                    LOGIC_OR_NOT_ASSIGN(p, tmp, depth, tab_depth)
            
            if p == store_only_if_p_is:
                pass # Trivial case
            elif p == (not store_only_if_p_is):
                pass # Trivial case
            else:
                print_extra_info('# Condition', p, '==', store_only_if_p_is, tab_depth=tab_depth)

            if len(tree) <= 4:
                # Main body
                tab_depth += 1
                dfs(tree[2], p, store_only_if_p_is, tab_depth)
                tab_depth -= 1

            if len(tree) == 4:
                # else/elif
                # Reverse current state of p
                dfs(tree[3], p, not store_only_if_p_is, tab_depth)
            
            depth = orig_depth
            return
        
        case 'else':
            # If the tree, elif looks like ['elif', ['if', ...]]
            # So handle via recursive call
            assert len(tree) == 2
            assert not true_false_mode
            assert not res_var
            
            orig_code = [scripts[tree[0].source].split('\n')[ind] for ind in range(tree[0].lineno - 1, tree[0].end_lineno)]
            print_original_code(*orig_code, sep='\n')
            
            if p == store_only_if_p_is:
                pass # Trivial case
            elif p == (not store_only_if_p_is):
                pass # Trivial case
            else:
                print_extra_info('# Condition', p, '==', store_only_if_p_is, tab_depth=tab_depth)
            
            tab_depth += 1
            dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode, res_var)
            tab_depth -= 1
            return
        
        case 'or':
            assert len(tree) == 3
            _, a, b = tree
            if not true_false_mode:
                true_false_mode = (True, False)

            true_var, false_var = true_false_mode
            if res_var:
                if isinstance(a, list) and isinstance(b, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var), res_var = res_var)
                    assert tmp1 == res_var

                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth, (true_var, res_var), res_var = res_var)
                    assert tmp2 == res_var

                    return res_var
                elif isinstance(a, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var), res_var = res_var)
                    assert tmp1 == res_var

                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)

                    ## print_debug_info(res_var, '=', true_var, 'if', tmp2, 'else', res_var, tab_depth=tab_depth)
                    SEL_BOOL(res_var, true_var, tmp2, res_var, depth, tab_depth)
                    return res_var
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    return dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode, res_var)
                else:
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    
                    ## print_debug_info(res_var, '=', true_var, 'if', tmp1, '||', tmp2, 'else', false_var, tab_depth=tab_depth)
                    SEL_OR(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)
                    return res_var
            else:
                if isinstance(a, list) and isinstance(b, list):
                    res_var = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var))
                    
                    depth += 1
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth, (true_var, res_var), res_var = res_var)
                    depth -= 1
                    assert tmp2 == res_var

                    return res_var
                elif isinstance(a, list):
                    res_var = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var))

                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    
                    ## print_debug_info(res_var, '=', true_var, 'if', tmp2, 'else', res_var, tab_depth=tab_depth)
                    depth += 1
                    SEL_BOOL(res_var, true_var, tmp2, res_var, depth, tab_depth)
                    depth -= 1
                    return res_var
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    return dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode, res_var)
                else:
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    
                    res_var = 'tmp%d' % depth
                    
                    ## print_debug_info(res_var, '=', true_var, 'if', tmp1, '||', tmp2, 'else', false_var, tab_depth=tab_depth)
                    SEL_OR(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)
                    return res_var

        
        case 'and':
            assert len(tree) == 3
            _, a, b = tree
            if not true_false_mode:
                true_false_mode = (True, False)
            
            true_var, false_var = true_false_mode
            if res_var:
                if isinstance(a, list) and isinstance(b, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var), res_var = res_var)
                    assert tmp1 == res_var

                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth, (res_var, false_var), res_var = res_var)
                    assert tmp2 == res_var

                    return res_var
                elif isinstance(a, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var), res_var = res_var)
                    assert tmp1 == res_var

                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)

                    ## print_debug_info(res_var, '=', res_var, 'if', tmp2, 'else', false_var, tab_depth=tab_depth)
                    SEL_BOOL(res_var, res_var, tmp2, false_var, depth, tab_depth)
                    return res_var
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    return dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode, res_var)
                else:
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    
                    ##print_debug_info(res_var, '=', true_var, 'if', tmp1, '&&', tmp2, 'else', false_var, tab_depth=tab_depth)
                    SEL_AND(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)
                    return res_var
            else:
                if isinstance(a, list) and isinstance(b, list):
                    res_var = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var))
                    
                    depth += 1
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth, (res_var, false_var), res_var = res_var)
                    depth -= 1
                    assert tmp2 == res_var

                    return res_var
                elif isinstance(a, list):
                    res_var = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var))

                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)

                    ## print_debug_info(res_var, '=', res_var, 'if', tmp2, 'else', false_var, tab_depth=tab_depth)
                    depth += 1
                    SEL_BOOL(res_var, res_var, tmp2, false_var, depth, tab_depth)
                    depth -= 1
                    return res_var
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    return dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode, res_var)
                else:
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    
                    res_var = 'tmp%d' % depth
                    
                    ## print_debug_info(res_var, '=', true_var, 'if', tmp1, '&&', tmp2, 'else', false_var, tab_depth=tab_depth)
                    SEL_AND(res_var, true_var, tmp1, tmp2, false_var, depth, tab_depth)
                    return res_var
            

        case 'not':
            assert len(tree) == 2
            _, a = tree
            orig_depth = depth
            if not true_false_mode:
                true_false_mode = (True, False)
            
            true_var, false_var = true_false_mode
            # Implement not lazily by swapping the mode
            swapped_true_false_mode = (false_var, true_var)

            
            if res_var:
                if isinstance(a, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, swapped_true_false_mode, res_var)
                    assert tmp1 == res_var
                    return res_var
                else:
                    tmp = dfs(a, p, store_only_if_p_is, tab_depth)
                    ## print_debug_info(res_var, '=', false_var, 'if', tmp, 'else', true_var, tab_depth=tab_depth)
                    SEL_BOOL(res_var, false_var, tmp, true_var, depth, tab_depth)
                    return res_var
            else:
                if isinstance(a, list):
                    res_var = dfs(a, p, store_only_if_p_is, tab_depth, swapped_true_false_mode)
                    return res_var
                else:
                    res_var = 'tmp%d' % depth
                    tmp = dfs(a, p, store_only_if_p_is, tab_depth)
                    ## print_debug_info(res_var, '=', false_var, 'if', tmp, 'else', true_var, tab_depth=tab_depth)
                    SEL_BOOL(res_var, false_var, tmp, true_var, depth, tab_depth)
        
        case 'function':
            assert len(tree) == 2
            _, a = tree
            func_def = scripts[tree[0].source].split('\n')[tree[0].lineno - 1]
            print_extra_info('# Inside function:', func_def, tab_depth=tab_depth)
            return dfs(a, p, store_only_if_p_is, tab_depth + 1, true_false_mode, res_var)
        
        case 'return':
            assert len(tree) == 2
            _, a = tree
            orig_depth = depth
            if not res_var:
                if isinstance(a, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode, res_var)
                    assert tmp1 == res_var
                    return res_var
                else:
                    tmp = dfs(a, p, store_only_if_p_is, tab_depth)
                    res_var = 'tmp%d' % depth
                    ASSIGN(res_var, tmp, depth, tab_depth)
                    return res_var
            else:
                if isinstance(a, list):
                    res_var = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode)
                    return res_var
                else:
                    res_var = 'tmp%d' % depth
                    tmp = dfs(a, p, store_only_if_p_is, tab_depth)
                    ASSIGN(res_var, tmp, depth, tab_depth)
                    return res_var



def parse(script_name):
    tree = ast.parse(scripts[script_name])
    label_tree(tree, script_name)
    # Convert every top-level statement in the module
    full_list = [NodeMetadata('body', None, None, script_name)] + [node_to_list(node) for node in tree.body]
    return full_list


print('code is')
print(scripts['main.py'])
tree = parse('main.py')
print('tree', tree)
print('starting dfs')
dfs(tree)
