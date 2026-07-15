import ast

def node_to_list(node):
    # Handle Constants (numbers, strings)
    if isinstance(node, ast.Constant):
        return node.value
    # Handle Variables
    elif isinstance(node, ast.Name):
        return node.id
    # Handle Assignments (x = 5)
    elif isinstance(node, ast.Assign):
        target = node.targets[0].id
        return ['=', target, node_to_list(node.value)]
    # Handle Binary Operations (x + y)
    elif isinstance(node, ast.BinOp):
        op_map = {ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/', ast.Pow: '**'}
        return [op_map.get(type(node.op), '?'), node_to_list(node.left), node_to_list(node.right)]
    # Handle Comparisons (<=, >=)
    elif isinstance(node, ast.Compare):
        # Note: Simplified for single comparison
        op = type(node.ops[0]).__name__
        op_map = { 'LtE': '<=', 'GtE': '>=', 'Eq': '==', 'NotEq': '!=' }
        op_symbol = op_map.get(op, op)
        return [op_symbol, node_to_list(node.left), node_to_list(node.comparators[0])]
    # Handle If/Else blocks
    elif isinstance(node, ast.If):
        res = ['if', node_to_list(node.test)]
        res.append(['root'] + [node_to_list(n) for n in node.body])
        if node.orelse:
            res.append(['root'] + [node_to_list(n) for n in node.orelse])
        return res
    # Handle function calls (abs, etc.)
    elif isinstance(node, ast.Call):
        return [node.func.id, *[node_to_list(arg) for arg in node.args]]
    # Handle boolean logic (OR)
    elif isinstance(node, ast.BoolOp):
        op = 'or' if isinstance(node.op, ast.Or) else 'and'
        return [op, *[node_to_list(val) for val in node.values]]
    # Handle Unary Operators (not x, -x)
    elif isinstance(node, ast.UnaryOp):
        op_map = {ast.Not: 'not', ast.USub: '-'}
        op_symbol = op_map.get(type(node.op), type(node.op).__name__)
        return [op_symbol, node_to_list(node.operand)]
    return None




depth = 0
def dfs(tree, p=True, store_only_if_p_is=True, tab_depth=0, true_false_mode=None):

    # p is logical statement used for if statement
    # variables can only be assigned if p==store_only_if_p_is
    # This is done to emulate the lack of if-statement in vmt:s

    # tab_depth is there just to make prints more pretty

    # true_false_mode = (true_val, false_val, res_val) is an optimal parameter that 
    # can be given to a non-trivial boolean expression.
    # The return variable in true false mode is always res_val.
    # If boolean expression is true, then res_val is assigned true_val
    # otherwise res_val is assigned false_val
    # This mode is there to make use of common tricks to save operations
    # in vmt scripts.


    if not isinstance(tree, list):
        # Base case, leaf reached
        assert not true_false_mode
        return tree
    
    def my_print(*out, **kwargs):
        if tab_depth:
            print(' '*(4 * tab_depth), *out, **kwargs)
        else:
            print(*out, **kwargs)


    global depth
    match tree[0]:
        case 'root':
            for node in tree[1:]:
                dfs(node, p, store_only_if_p_is, tab_depth)
        
        case '=':
            assert len(tree) == 3
            _, var, res = tree
            res = dfs(res, p, store_only_if_p_is, tab_depth)
            if store_only_if_p_is == True:
                if p == True:
                    my_print(var, '=', res)
                else:
                    my_print('if', p, ':', var, '=', res)
            else:

                if p == True:
                    pass
                else:
                    my_print('if not', p, ':', var, '=', res)
            
        case '+':
            assert len(tree) == 3
            _, a, b = tree
            if isinstance(a, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                depth -= 1
                my_print(tmp1, '+=', tmp2)
                return tmp1
            elif isinstance(b, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                my_print(tmp2, '+=', tmp1)
                return tmp2
            else:
                tmp = 'tmp%d' % depth
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                my_print(tmp, '=', tmp1, '+', tmp2)
                return tmp
        

        case '==':
            assert len(tree) == 3
            _, a, b = tree
            if true_false_mode:
                true_var, false_var, res_var = true_false_mode
                
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                depth += 1
                tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                depth -= 1
                my_print(res_var, '=', true_var, 'if', tmp1, '==', tmp2, 'else', false_var)
                return res_var

            else:
                if isinstance(a, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    depth += 1
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    depth -= 1
                    my_print(tmp1, '=', tmp1, '==', tmp2)
                    return tmp1
                elif isinstance(b, list):
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    my_print(tmp2, '=', tmp1, '==', tmp2)
                    return tmp2
                else:
                    tmp = 'tmp%d' % depth
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)
                    my_print(tmp, '=', tmp1, '==', tmp2)
                    return tmp


        case 'if':
            assert len(tree) == 3 or len(tree) == 4

            orig_depth = depth

            if p != True: # We are part of nested if-statements
                if isinstance(tree[1], list):
                    tmp = 'tmp%d' % depth
                    depth += 1
                    if store_only_if_p_is:
                        res = dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode = (p, False, tmp))
                    else:
                        res = dfs(tree[1], p, store_only_if_p_is, tab_depth, true_false_mode = (p, True, tmp))
                    assert res == tmp
                    p = tmp
                else:
                    tmp = 'tmp%d' % depth
                    tmp2 = dfs(tree[1], p, store_only_if_p_is, tab_depth)
                    depth += 1
                    if store_only_if_p_is:
                        my_print(tmp, '=', p, '&&', tmp2)
                        p = tmp
                    else:
                        my_print(tmp, '=', p, '|| not', tmp2)
                        p = tmp
            else:
                if store_only_if_p_is:
                    p = dfs(tree[1], p, store_only_if_p_is, tab_depth)
                    depth += 1
                else:
                    return

                
            if len(tree) <= 4:
                # Main body
                my_print('# if:', p)
                tab_depth += 1
                dfs(tree[2], p, store_only_if_p_is, tab_depth)
                tab_depth -= 1

            if len(tree) == 4:
                # else body
                my_print('# else:')
                tab_depth += 1
                dfs(tree[3], p, not store_only_if_p_is, tab_depth)
                tab_depth -= 1
                # Has an else statement
            
            depth = orig_depth
            return
        
        case 'or':
            assert len(tree) == 3
            _, a, b = tree
            if true_false_mode:
                true_var, false_var, res_var = true_false_mode
                if isinstance(a, list):
                    if isinstance(b, list):
                
                        tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var, res_var))
                        assert tmp1 == res_var

                        tmp2 = dfs(b, p, store_only_if_p_is, tab_depth, (true_var, res_var, res_var))
                        assert tmp2 == res_var

                        return res_var
                    else:
                        tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var, res_var))
                        assert tmp1 == res_var

                        tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)

                        my_print(res_var, '||=', tmp2)
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode)
                else:
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    
                    print(res_var, '=', true_var, 'if', tmp1, '||', tmp2, 'else', false_var)
                    return res_var

            else:
                if isinstance(a, list):
                    if isinstance(b, list):
                        tmp1 = dfs(b, p, store_only_if_p_is, tab_depth)
                        depth += 1
                        res = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode = (True, tmp1, tmp1))
                        assert res == tmp1
                        depth -= 1
                        return tmp1
                    else:
                        tmp = 'tmp%d' % depth
                        
                        tmp1 = dfs(b, p, store_only_if_p_is, tab_depth)
                        depth += 1
                        res = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode = (True, tmp1, tmp))
                        assert res == tmp
                        depth -= 1
                        return tmp
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    return dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode)
                else:
                    tmp = 'tmp%d' % depth
                    
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    print(tmp, '=', tmp1, '||', tmp2)
                    return tmp
        
        case 'and':
            assert len(tree) == 3
            _, a, b = tree
            if true_false_mode:
                true_var, false_var, res_var = true_false_mode
                if isinstance(a, list):
                    if isinstance(b, list):
                
                        tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var, res_var))
                        assert tmp1 == res_var

                        tmp2 = dfs(b, p, store_only_if_p_is, tab_depth, (res_var, false_var, res_var))
                        assert tmp2 == res_var

                        return res_var
                    else:
                        tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (true_var, false_var, res_var))
                        assert tmp1 == res_var

                        tmp2 = dfs(b, p, store_only_if_p_is, tab_depth)

                        my_print(res_var, '&&=', tmp2)
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode)
                else:
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    print(res_var, '=', true_var, 'if', tmp1, '&&', tmp2, 'else', false_var)

            else:
                if isinstance(a, list):
                    if isinstance(b, list):
                        tmp1 = dfs(b, p, store_only_if_p_is, tab_depth)
                        depth += 1
                        res = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode = (tmp1, False, tmp1))
                        assert res == tmp1
                        depth -= 1
                        return tmp1
                    else:
                        tmp = 'tmp%d' % depth
                        
                        tmp1 = dfs(b, p, store_only_if_p_is, tab_depth)
                        depth += 1
                        res = dfs(a, p, store_only_if_p_is, tab_depth, true_false_mode = (tmp1, False, tmp))
                        assert res == tmp
                        depth -= 1
                        return tmp
                elif isinstance(b, list):
                    # Call with reversed order of a and b
                    return dfs([_, b, a], p, store_only_if_p_is, tab_depth, true_false_mode)
                else:
                    tmp = 'tmp%d' % depth
                    
                    tmp1 = dfs(a, p, store_only_if_p_is, tab_depth)
                    tmp2 = dfs(a, p, store_only_if_p_is, tab_depth)
                    print(tmp, '=', tmp1, '&&', tmp2)
        case 'not':
            assert len(tree) == 2
            _, a = tree
            orig_depth = depth
            if true_false_mode:
                true_var, false_var, res_var = true_false_mode
            else:
                res_var = 'tmp%d' % depth
                depth += 1
                true_var, false_var, res_var = False, True, res_var
            
            if isinstance(a, list):
                tmp1 = dfs(a, p, store_only_if_p_is, tab_depth, (false_var, true_var, res_var))
                assert tmp1 == res_var
                depth = orig_depth
                return tmp1
            else:
                tmp = dfs(a, p, store_only_if_p_is, tab_depth)
                print(res_var, '=', false_var, 'if', tmp, 'else', true_var)
                depth = orig_depth
                return res_var
            

def parse(code):
    tree = ast.parse(code)
    # Convert every top-level statement in the module
    full_list = ['root'] + [node_to_list(node) for node in tree.body]
    return full_list

#code = """
#x = 5
#y = 3 * 4
#if (x - y <= 3 or y >= 5):
#    z = abs(x - y*z)**0.5
#else:
#    z = 5
#"""
#print(parse(code))

code = """
if x == 5 or y == 24:
    k = x + (y + z) + 5.0 == 1.0
    if y == 10.0 or z == 100.0:
        k = x + (y + z) + 5.0 == 1.0
    else:
        k = 100.0

"""
print('code is')
print(code)
tree = parse(code)
print('tree', tree)
print('starting dfs')
dfs(tree)
