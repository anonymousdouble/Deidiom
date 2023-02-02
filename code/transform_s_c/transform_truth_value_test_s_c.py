import ast,copy

def transform_idiom_truth_value_test(node,tree):
    note_str="EMPTY_VALUE belongs to [None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]"
    new_code_list=[]
    line_head=1
    try:

        body=tree.body
        for e in body:
            if isinstance(e, (ast.Import, ast.ImportFrom,ast.Expr)):
                line_head=e.end_lineno+1
            else:
                break
    except:
        line_head=1

    a = "def own_func_truth_test(var):\n\
    if var in [None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]:\n\
        return False \n\
    elif hasattr(var,'__bool__'):\n\
        return bool(var)\n\
    elif hasattr(var, '__len__'):\n\
        return len(var)!=0\n\
    else:\n\
        return True"
    if isinstance(node,ast.UnaryOp):
        value=node.operand
        new_code_list=[f"(not bool({ast.unparse(value)}))"]
        new_code_list=["(",f"(hasattr({ast.unparse(value)},'__bool__') and bool({ast.unparse(value)})==False))"]
        new_code_list=["(",f"(hasattr({ast.unparse(value)},'__len__') and len({ast.unparse(value)})==0))"]
        new_code_list=[f"(hasattr({ast.unparse(value)},'__bool__') )"]
        new_code_list=[f"(hasattr({ast.unparse(value)},'__len__') )"]
        # new_code_list=[f"(not bool({ast.unparse(value)}) if hasattr({ast.unparse(value)}, '__bool__') else ",ast.unparse(value), " in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]

        # new_code_list=[ast.unparse(value)," in ","[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]"]
        # new_code_list=[f"(not bool({ast.unparse(value)}) if hasattr({ast.unparse(value)}, '__bool__') else len({ast.unparse(value)})==0 if hasattr({ast.unparse(value)}, '__len__') else ",ast.unparse(value), " in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]
        # new_code_list=[f"(len({ast.unparse(value)})==0 if hasattr({ast.unparse(value)}, '__len__') else ",ast.unparse(value), " in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]

        # new_code_list=["(",ast.unparse(value), " in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]", f" or not bool({ast.unparse(value)}) if hasattr({ast.unparse(value)}, '__bool__') else hasattr({ast.unparse(value)}, '__len__') and len({ast.unparse(value)})==0)",]
        # new_code_list=["(",ast.unparse(value), " in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]
        # new_code_list=["(",ast.unparse(value), " in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)] or ",f"(bool({ast.unparse(value)})==False if hasattr({ast.unparse(value)},'__bool__') else (hasattr({ast.unparse(value)},'__len__') and len({ast.unparse(value)})==0)))"]
        # new_code_list=["(",ast.unparse(value), " in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]", f" if isinstance({ast.unparse(value)},(bool,int,float,str,list,dict,set,Decimal,Fraction,tuple,range,frozenset,complex,type(None))) else ",f"(bool({ast.unparse(value)})==False if hasattr({ast.unparse(value)},'__bool__') else (hasattr({ast.unparse(value)},'__len__') and len({ast.unparse(value)})==0)))"]
        new_code_list=[f"own_func_truth_test({ast.unparse(value)})==False"]

    # pass
    else:
        new_code_list=[f"(bool({ast.unparse(node)})) "]
        new_code_list=["(",f"(hasattr({ast.unparse(node)},'__bool__') and bool({ast.unparse(node)})==True))"]
        new_code_list=["(",f"(hasattr({ast.unparse(node)},'__len__') and len({ast.unparse(node)})!=0))"]
        new_code_list=[f"(hasattr({ast.unparse(node)},'__bool__') )"]
        new_code_list=[f"(hasattr({ast.unparse(node)},'__len__') )"]

        # new_code_list=[f"(bool({ast.unparse(node)}) if hasattr({ast.unparse(node)}, '__bool__') else ",ast.unparse(node), " not in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]

        # new_code_list=[f"(bool({ast.unparse(node)}) if hasattr({ast.unparse(node)}, '__bool__') else len({ast.unparse(node)})!=0 if hasattr({ast.unparse(node)}, '__len__') else ",ast.unparse(node), " not in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]
        # new_code_list=[f"(len({ast.unparse(node)})!=0 if hasattr({ast.unparse(node)}, '__len__') else ",ast.unparse(node), " not in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]

        # new_code_list=["(",ast.unparse(node), " not in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]", f" or bool({ast.unparse(node)}) if hasattr({ast.unparse(node)}, '__bool__') else hasattr({ast.unparse(node)}, '__len__') and len({ast.unparse(node)})!=0)",]
        # new_code_list=["(",ast.unparse(node), " not in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])"]
        # new_node 第一个是替换的内容,第二个是加在前面的stmt, 第三个是加在后面的stmt

        # new_code_list=["(",ast.unparse(node), " not in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]", f" if isinstance({ast.unparse(node)},(bool,int,float,str,list,dict,set,Decimal,Fraction,tuple,range,frozenset,complex,type(None))) else ",f"(bool({ast.unparse(node)})==True if hasattr({ast.unparse(node)},'__bool__') else  (hasattr({ast.unparse(node)},'__len__') and len({ast.unparse(node)})!=0)))"]
        new_code_list = [f"own_func_truth_test({ast.unparse(node)})==True"]

        # pass
    # ast.unparse(node)
    return [node, ["".join(new_code_list),"","",[line_head,"from decimal import Decimal\nfrom fractions import Fraction\n"+a]]]

    # return [node, ["".join(new_code_list),"","",[line_head,"from decimal import Decimal\nfrom fractions import Fraction\n"]]]
    # return [node, ["n != 0","","",[line_head,"from decimal import Decimal\nfrom fractions import Fraction\n"]]]

    # new_code="".join(new_code_list)
    # for e in ast.walk(ast.parse(new_code)):
    #     if isinstance(e,ast.Compare):
    #         return [node, [e]]
    # print("old str: ",ast.unparse(node))
    # new_node=node
    # return [node, [new_node]]
