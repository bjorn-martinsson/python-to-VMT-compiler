from colorama import init, Fore, Style

# Initialize colorama (needed for Windows support)
init(autoreset=True)

# Fancy colored print
def cprint(*out, color=Fore.WHITE, **kwargs): 
    # Pass the modified tuple to the standard print function
    print(*(f"{color}{o}" for o in out), **kwargs)

def print_original_code(*out, **kwargs):
    tab_depth = kwargs.pop('tab_depth', 0)
    sep = kwargs.pop('sep', '\n')
    
    color = Fore.GREEN

    first = True
    out_with_sep = []
    for x in out:
        if not first:
            out_with_sep.append(sep)
        out_with_sep.append(str(x))

    print() # Empty new line for visability
    
    for line in ''.join(out_with_sep).split('\n'):
        if tab_depth:
            cprint(' '*(4 * tab_depth - 1), line.lstrip(), color=color, **kwargs)
        else:
            cprint(line.lstrip(), color=color, **kwargs)

def print_debug_info(*out, **kwargs):
    tab_depth = kwargs.pop('tab_depth', 0)
    
    color = Fore.WHITE
    if tab_depth:
        cprint(' '*(4 * tab_depth - 1), *out, color=color, **kwargs)
    else:
        cprint(*out, color=color, **kwargs)

def print_extra_info(*out, **kwargs):
    tab_depth = kwargs.pop('tab_depth', 0)
    
    color = Fore.BLUE
    if tab_depth:
        cprint(' '*(4 * tab_depth - 1), *out, color=color, **kwargs)
    else:
        cprint(*out, color=color, **kwargs)


# tab_depth is used for printing, it has no functional use
# depth is the current stack depth. Operations that need to
# use temporary variables start with tmp{depth}

LOW_LEVEL_FUNCTIONS = set()

def assert_stack_decorator(n):
    # Only res is allowed to be "tmp%d"%(depth)
    # This is a quick check the basic operations haven't been
    # called incorrectly
    def decorator(f):
        LOW_LEVEL_FUNCTIONS.add(f.__name__)

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
def SUB(res, a, b, depth, tab_depth):
    # res = a - b
    print_debug_info(res, '=', a, '-', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def SUB_ASSIGN(res, a, depth, tab_depth):
    # res -= a
    print_debug_info(res, '-=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def MUL(res, a, b, depth, tab_depth):
    # res = a * b
    print_debug_info(res, '=', a, '*', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def MUL_ASSIGN(res, a, depth, tab_depth):
    # res *= a
    print_debug_info(res, '*=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=3)
def DIV(res, a, b, depth, tab_depth):
    # res = a / b
    print_debug_info(res, '=', a, '/', b, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def DIV_ASSIGN(res, a, depth, tab_depth):
    # res /= a
    print_debug_info(res, '/=', a, tab_depth=tab_depth)

@assert_stack_decorator(n=2)
def RDIV_ASSIGN(res, a, depth, tab_depth):
    # res \= a
    # This means res = a/res
    print_debug_info(res, '\\=', a, tab_depth=tab_depth)

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

@assert_stack_decorator(n=5)
def SEL_LEQ(res, a, b, c, d, depth, tab_depth):
    # res = a if b <= c else d
    print_debug_info(res, '=', a, 'if', b, '<=', c, 'else', d, tab_depth=tab_depth)


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
w = sqrt(a + b)

if x == 52:
    y = sqrt(sqrt(y))
c = a * b
c = a + b
c = a / b

if x == 52:
    y = sqrt(z) + 42
"""


function_definitions = {}
safe_functions = set() # Functions where return value is not an in parameter
hidden_functions = set() # Functions that are not printed

import ast
import inspect

def register_function(safe=True, hidden=False):
    def decorator(func):
        """Decorator to attach AST and source metadata to a function."""
        # 1. Get the source code of the function
        source_script = inspect.getsource(func)
        
        # 1.5 Remove any extra indentation
        line0 = source_script.split('\n')[0]
        to_be_removed = len(line0) - len(line0.lstrip())
        source_script = '\n'.join(line[to_be_removed:] for line in source_script.split('\n'))

        # 2. Store without decorator
        source_script = '\n'.join(source_script.split('\n')[1:])
        source = func.__name__
        scripts[source] = source_script
        if safe: safe_functions.add(source)
        if hidden: hidden_functions.add(source)
         
        # 3. Parse into AST
        tree = ast.parse(source_script)

        # Tell all node where they come from
        label_tree(tree, source)
        
        # 4. Attach to the function object
        func._ast_tree = tree
        function_definitions[source] = tree
        return func
    return decorator
register_safe_function = register_function(safe=True)
register_unsafe_function = register_function(safe=False, hidden=True)


import ast
import copy

def get_return_name(func_def):
    """Finds the variable name being returned."""
    for node in reversed(func_def.body):
        if isinstance(node, ast.Return):
            if isinstance(node.value, ast.Name):
                return node.value.id
    return None

def get_all_locals(func_def, protected_names):
    """Finds all unique variables that are actually stored/used as data."""
    locals_found = set()
    
    # We walk the tree and look at parents to filter out function names
    for node in ast.walk(func_def):
        if isinstance(node, ast.Name):
            # 1. Skip if it's an argument (protected)
            if node.id in protected_names:
                continue
            
            # 2. Check the context to ensure it's not a function call
            # If it's a function call, the Name node will be the 'func' attribute of an ast.Call
            # We can detect this by checking the parent, but a simpler way is checking 
            # if the name is ever used in a 'Store' context.
            if isinstance(node.ctx, (ast.Store, ast.Load)):
                locals_found.add(node.id)
                
    # To truly filter out function calls, we exclude any names that only ever appear 
    # as the 'func' attribute of an ast.Call
    func_names = set()
    for node in ast.walk(func_def):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            func_names.add(node.func.id)
            
    return locals_found - func_names


def handle_call_inline(node, call_args, res_var, depth, hidden=False):
    func_def = function_definitions[node.source]
     
    # 1. Setup metadata
    formal_args = [arg.arg for arg in func_def.body[0].args.args]
    arg_map = dict(zip(formal_args, call_args))
    return_var = get_return_name(func_def.body[0])

    assert return_var != None
 
    # 2. Identify locals and build the renaming map
    # We define what shouldn't be renamed to 'tmp'
    protected = set(arg_map.keys())
    local_vars = get_all_locals(func_def, protected)
    
    # Build mapping: return_var gets mapped to res_var, others to tmpX
    rename_map = {return_var: res_var}
    current_depth = depth
    for var in local_vars:
        if var != return_var:
            rename_map[var] = f"tmp{current_depth}"
            current_depth += 1
            
    # 3. Apply transformation
    class InlineTransformer(ast.NodeTransformer):
        def visit_Name(self, node):
            # If it's an argument, map to the call_args
            if node.id in arg_map:
                node.id = arg_map[node.id]
            # If it's a local/return, map to the generated name
            elif node.id in rename_map:
                node.id = rename_map[node.id]
            return node

    new_body = copy.deepcopy(func_def)

    transformer = InlineTransformer()
    inline_body = [transformer.visit(stmt) for stmt in new_body.body[0].body]

    # Apply node_to_list
    func_body = function_definitions[node.source].body[0]
    if hidden:
        ret = [NodeMetadata('hidden_body', func_body.lineno, func_body.end_lineno, node.source)] + [node_to_list(n) for n in inline_body]
    else:
        ret = [NodeMetadata('body', func_body.lineno, func_body.end_lineno, node.source)] + [node_to_list(n) for n in inline_body]
    
    return ret, len(rename_map) - 1


@register_safe_function
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
    
    guess = sel_ge(guess, guess, 0.0, 0.0)

    return guess

def internal_stuff(): 

    @register_unsafe_function
    def sel_leq(a,b,c,d):
        # return a if b <= c else d
        out = SEL_LEQ(a,b,c,d)
        return out

    @register_unsafe_function
    def sel_ge(a,b,c,d):
        # return a if b > c else d
        out = SEL_LEQ(a,b,c,d)
        return out
    
    @register_unsafe_function
    def min(a,b):
        # return a if a <= b else b
        out = SEL_LEQ(a,a,b,b)
        return out
    
    @register_unsafe_function
    def max(a,b):
        # return a if a <= b else b
        out = SEL_LEQ(b,a,b,a)
        return out
    
    @register_unsafe_function
    def __add__(a,b):
        # return a + b
        out = ADD(a,b)
        return out
    
    @register_unsafe_function
    def __sub__(a,b):
        # return a - b
        out = SUB(a,b)
        return out
    
    @register_unsafe_function
    def __mul__(a,b):
        # return a * b
        out = MUL(a,b)
        return out
    
    @register_unsafe_function
    def __div__(a,b):
        # return a / b
        out = DIV(a,b)
        return out

internal_stuff()


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
            func_body = function_definitions[node.func.id].body[0]
#            print([node_to_list(val) for val in node.args], 'node?')
            return [NodeMetadata('function', func_body.lineno, func_body.end_lineno, node.func.id), [node_to_list(val) for val in node.args]]
#            # Inline the function body
#            inline_body = handle_call_inline(node)
#            # Process the body as a list of operations
#            func_body = function_definitions[node.func.id].body[0]
#            body = [NodeMetadata('body', func_body.lineno, func_body.end_lineno, node.func.id)] + [node_to_list(n) for n in inline_body]
#            return [NodeMetadata('function', func_body.lineno, func_body.end_lineno, node.func.id), body]
        elif node.func.id in LOW_LEVEL_FUNCTIONS:
            return [NodeMetadata('internal_function', None, None, node.func.id), [node_to_list(val) for val in node.args]]
        else:
            # Standard call if not in registry

            # Dont allow for now
            print('Called unknown function:', node.func.id)
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
                        print_original_code(scripts[tree[0].source].split('\n')[ind], tab_depth=tab_depth)
                ans = dfs(node, p, store_only_if_p_is, tab_depth)
            
            return ans
        
        case 'hidden_body':
            # Same as body, except dont print anything
            assert not true_false_mode
            assert not res_var
             
            if p == (not store_only_if_p_is):
                return

            for node in tree[1:]:
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
            
            if p == store_only_if_p_is:
                ## print_debug_info(var, '=', res, tab_depth=tab_depth)
                if isinstance(res, list):
                    res = dfs(res, p, store_only_if_p_is, tab_depth, res_var=var)
                    assert res == var
                else:
                    res = dfs(res, p, store_only_if_p_is, tab_depth)
                    depth += 1
                    ASSIGN(var, res, depth, tab_depth)
                    depth -= 1
            elif p == (not store_only_if_p_is):
                # This case should be handled earlier, hardcoded if-Flase
                assert False
            
            elif store_only_if_p_is == True:
                res = dfs(res, p, store_only_if_p_is, tab_depth)
                ## print_debug_info('if', p, ':', var, '=', res, tab_depth=tab_depth)
                depth += 1
                SEL_IF(var, res, p, depth, tab_depth)
                depth -= 1
            else: # store_only_if_p_is == False
                res = dfs(res, p, store_only_if_p_is, tab_depth)
                ##print_debug_info('if not', p, ':', var, '=', res, tab_depth=tab_depth)
                depth += 1
                SEL_IF_NOT(var, res, p, depth, tab_depth)
                depth -= 1
            return var

        case '+':
            assert not true_false_mode
#            assert not res_var
            assert len(tree) == 3
            _, a, b = tree
            if not res_var:
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
            else:
                orig_depth = depth

                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                if isinstance(a, list):
                    depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                if isinstance(b, list):
                    depth += 1
                
                ADD(res_var, tmp1, tmp2, depth, tab_depth)
                depth = orig_depth
                return res_var
        
        case '*':
            assert not true_false_mode
#            assert not res_var
            assert len(tree) == 3
            _, a, b = tree

            if not res_var:
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
            else: # res_var given
                orig_depth = depth

                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                if isinstance(a, list):
                    depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                if isinstance(b, list):
                    depth += 1
                
                MUL(res_var, tmp1, tmp2, depth, tab_depth)
                depth = orig_depth
                return res_var
        
        case '/':
            assert not true_false_mode
#            assert not res_var
            assert len(tree) == 3
            _, a, b = tree
            if not res_var:
                if isinstance(a, list) and isinstance(b, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    depth += 1
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    depth -= 1
                    
                    ##print_debug_info(tmp1, '/=', tmp2, tab_depth=tab_depth)
                    depth += 2
                    DIV_ASSIGN(tmp1, tmp2, depth, tab_depth)
                    depth -= 2

                    return tmp1
                elif isinstance(a, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    
                    ##print_debug_info(tmp1, '/=', tmp2, tab_depth=tab_depth)
                    depth += 1
                    DIV_ASSIGN(tmp1, tmp2, depth, tab_depth)
                    depth -= 1

                    return tmp1
                elif isinstance(b, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    
                    ##print_debug_info(tmp2, '\\=', tmp1, tab_depth=tab_depth)
                    depth += 1
                    RDIV_ASSIGN(tmp2, tmp1, depth, tab_depth)
                    depth -= 1

                    return tmp2
                else:
                    tmp = 'tmp%d' % depth
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    ##print_debug_info(tmp, '=', tmp1, '/', tmp2, tab_depth=tab_depth)
                    
                    DIV(tmp, tmp1, tmp2, depth, tab_depth)

                    return tmp
            else: # res_var given
                orig_depth = depth

                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                if isinstance(a, list):
                    depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                if isinstance(b, list):
                    depth += 1
                
                DIV(res_var, tmp1, tmp2, depth, tab_depth)
                depth = orig_depth
                return res_var

        

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
            print_original_code(*orig_code, sep='\n', tab_depth=tab_depth)
            
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
            print_original_code(*orig_code, sep='\n', tab_depth=tab_depth)
            
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
            print_original_code(*orig_code, sep='\n', tab_depth=tab_depth)
            
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
            node, *args = tree
            func_def = scripts[node.source].split('\n')[node.lineno - 1]

            orig_depth = depth

            if node.source in safe_functions:
                my_res = 'tmp%d' % depth
                depth += 1

                call_args = []
                for arg in args[0]:
                    if isinstance(arg, list):
                        tmp = dfs(arg, p, store_only_if_p_is, tab_depth)
                        call_args.append(tmp)
                        depth += 1
                    else:
                        tmp = dfs(arg, p, store_only_if_p_is, tab_depth)
                        call_args.append(tmp)

                
                print_extra_info(tab_depth=tab_depth) # newline
                print_extra_info('# Inlining function call', my_res,'=', func_def[4:].split('(')[0], '(', *call_args, ')', tab_depth=tab_depth)
                
                inline_tree, number_of_extra_variables = handle_call_inline(node, call_args, my_res, depth)
                depth += number_of_extra_variables

                ret = dfs(inline_tree, True, True, tab_depth + 1)
                assert ret == my_res
                
                if res_var:
                    ASSIGN(res_var, my_res, depth, tab_depth) 
                    print_extra_info('# end of inlined function call.', tab_depth=tab_depth)
                    depth = orig_depth
                    return res_var
                else:
                    print_extra_info('# end of inlined function call.', tab_depth=tab_depth)
                    depth = orig_depth
                    return my_res
            else:
                hidden = node.source in hidden_functions#
                if not hidden: 
                    print_extra_info('# reached unsafe function', func_def, tab_depth=tab_depth)
                else:
                    tab_depth -= 1

                if not res_var:
                    res_var = 'tmp%d' % depth

                call_args = []
                for arg in args[0]:
                    if isinstance(arg, list):
                        tmp = dfs(arg, p, store_only_if_p_is, tab_depth)
                        call_args.append(tmp)
                        depth += 1
                    else:
                        tmp = dfs(arg, p, store_only_if_p_is, tab_depth)
                        call_args.append(tmp)
                
                if not hidden:
                    print_extra_info(tab_depth=tab_depth) # newline
                    print_extra_info('# Inlining unsafe function call', res_var,'=', func_def[4:].split('(')[0], '(', *call_args, ')', tab_depth=tab_depth)
                
                    inline_tree, number_of_extra_variables = handle_call_inline(node, call_args, res_var, depth, hidden=False)
                else:
                    inline_tree, number_of_extra_variables = handle_call_inline(node, call_args, res_var, depth, hidden=True)
                
                depth += number_of_extra_variables

                ret = dfs(inline_tree, True, True, tab_depth + 1)
                assert ret == res_var
                
                if not hidden:
                    print_extra_info('# end of inlined unsafe function call.', tab_depth=tab_depth)
                depth = orig_depth
                return res_var
        
        case 'internal_function':
            assert res_var
            node, *args = tree
            
            orig_depth = depth

            call_args = []
            for arg in args[0]:
                if isinstance(arg, list):
                    tmp = dfs(arg, p, store_only_if_p_is, tab_depth)
                    call_args.append(tmp)
                    depth += 1
                else:
                    tmp = dfs(arg, p, store_only_if_p_is, tab_depth)
                    call_args.append(tmp)

            globals()[node.source](res_var, *call_args, depth, tab_depth)

            orig_depth = depth
            return res_var

        case 'return':
            assert len(tree) == 2
            _, a = tree
            orig_depth = depth
            if res_var:
                if isinstance(a, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode, res_var)
                    assert tmp1 == res_var
                    return res_var
                else:
                    tmp = dfs(a, p, store_only_if_p_is, tab_depth)
                    ASSIGN(res_var, tmp, depth, tab_depth)
                    return res_var
            else:
                if isinstance(a, list):
                    res_var = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode)
                    return res_var
                else:
                    tmp = dfs(a, p, store_only_if_p_is, tab_depth)
                    return tmp



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
