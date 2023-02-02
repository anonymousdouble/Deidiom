import ast,copy
def get_op_str(node):
    if isinstance(node, (ast.Eq)):
        return "=="
        # dict_feature["num_Eq"] += 1
    elif isinstance(node, (ast.NotEq)):
        return "!="
    elif isinstance(node, (ast.Lt)):
        return "<"
    elif isinstance(node, (ast.LtE)):
        return "<="
    elif isinstance(node, (ast.Gt)):
        return ">"
    elif isinstance(node, (ast.GtE)):
        return ">="
    elif isinstance(node, (ast.Is)):
        return "is"
    elif isinstance(node, (ast.IsNot)):
        return "is not"
    elif isinstance(node, (ast.In)):
        return "in"
    elif isinstance(node, (ast.NotIn)):
        return "not in"
def transform_idiom_chain_compare(node):

    # ast.unparse(node)
    print("old str: ",ast.unparse(node))

    new_node_str_list=[f"{ast.unparse(node.left)}"]
    for ind,e in enumerate(node.comparators[:-1]):
        op=node.ops[ind]
        op_str=get_op_str(op)
        new_node_str_list.append(op_str)
        new_node_str_list.append(ast.unparse(e))
        new_node_str_list.append("and")
        new_node_str_list.append(ast.unparse(e))
    new_node_str_list.append(get_op_str(node.ops[-1]))
    new_node_str_list.append(ast.unparse(node.comparators[-1]))
    new_node_str="("+" ".join(new_node_str_list)+")"
    print("new str: ",new_node_str)
    return [node, [new_node_str, "", ""]]
    # for new_node in ast.walk(ast.parse(new_node_str)):
    #         if isinstance(new_node,ast.Expr):
    #             # print('new str: ',ast.unparse(new_node))
    #             # return [node, new_node]
    #             return [node, [ast.unparse(new_node),"",""]]

