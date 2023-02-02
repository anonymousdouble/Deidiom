import ast,copy,sympy,math
import traceback

'''
lower-upper 相减为常量 and step为常量
否则 不能重构
'''
class Rewrite_star(ast.NodeTransformer):
    def __init__(self,node=None,replace_node=None):
        self.lineno =node.lineno
        self.colset=node.col_offset
        self.replace_node=replace_node
        pass
        # self.ass =ass_node
        # self.new_node =new_node
        # self.remove_ass_flag =remove_ass_flag
    def visit_Starred(self, node):
        # return ast.Name("a")
        if node.lineno==self.lineno and node.col_offset==self.colset:
            return self.replace_node
        else:
            return node
def determine_refactor(star_node):
    additional_ass=[]
    value = star_node.value

    if isinstance(value,(ast.List,ast.Tuple,ast.Set)):
        e_list=[ast.unparse(e) for e in value.elts]
        return 1,", ".join(e_list),additional_ass
    elif isinstance(value,(ast.Constant)):
        try:
            print("value: ",value)
            e_list=[e for e in value.value]
            return 1,", ".join(e_list),additional_ass
        except:
            return 0, "Cannot explain",additional_ass
            print("Please check the code!!!")
            traceback.print_exc()
    else:
        number_ele = None
        if isinstance(value, ast.Subscript) and isinstance(value.slice, ast.Slice):
            slice = value.slice
            star_var = value.value
            step = '1' if not slice.step else ast.unparse(slice.step)
            try:
                step_int=int(step)
            except:
                step_int=None
                pass

            if step_int:
                if step_int>0:
                    upper= f"len({ast.unparse(star_var)})" if not slice.upper else ast.unparse(slice.upper)
                    try:
                        upper_int=int(upper)
                    except:
                        upper_int=None
                    lower = '0' if not slice.lower else ast.unparse(slice.lower)
                    try:
                        lower_int=int(lower)
                    except:
                        lower_int=None
                    #当是同号的时候才可以确切知道元素的个数
                    if lower_int is not None and upper_int is not None and ((lower_int>=0 and upper_int>=0) or (lower_int<=0 and upper_int<=0)):
                        if upper_int-lower_int<=0:
                            number_ele=0
                        else:
                            number_ele=math.ceil((upper_int-lower_int)/step_int)
                    elif lower_int is None or upper_int is None:
                        try:
                            number_ele = math.ceil(int(sympy.sympify(upper + "-(" + lower + ")"))/abs(step_int))
                        except:
                            number_ele =None

                else:
                    upper = None if not slice.upper else ast.unparse(slice.upper)
                    try:
                        upper_int = int(upper)
                    except:
                        upper_int = None
                    lower = None if not slice.lower else ast.unparse(slice.lower)
                    try:
                        lower_int = int(lower)
                    except:
                        lower_int = None
                    if lower_int is not None and upper_int is not None and ((lower_int>=0 and upper_int>=0) or (lower_int<=0 and upper_int<=0)):
                        if lower_int-upper_int<=0:
                            number_ele=0
                        else:
                            number_ele = math.ceil((lower_int - upper_int) / abs(step_int))
                    elif upper is None and lower_int is not None and lower_int>=0:
                        number_ele = math.ceil((lower_int+1) / abs(step_int))
                    elif lower is None and upper_int is not None and upper_int<0:
                        number_ele = math.ceil((-upper_int -1) / abs(step_int))
                    elif lower_int is None or upper_int is None:
                        try:
                            number_ele = math.ceil(int(sympy.sympify(lower + "-(" + upper + ")")) / abs(step_int))
                        except:
                            number_ele = None
                    if not slice.lower:
                        lower='-1'



            # print(">>>>>number_ele: ",upper_int,lower_int,number_ele)
        star_var_str = f"tmp_arg={ast.unparse(value)}"
        additional_ass.append(star_var_str)
        star_var_str = "tmp_arg"
        # star_var_str=ast.unparse(value)
        if number_ele and number_ele>0:
                print("********",ast.unparse(star_node),star_var,type(lower), type(step_int),type(number_ele),lower,step_int,number_ele)
                try:
                    return 1, ", ".join([f"{ast.unparse(star_var)}[{str(int(lower) + step_int * i)}]" for i in
                                         range(number_ele)]), []
                except:
                    return 1, ", ".join([f"{ast.unparse(star_var)}[{lower + str(step_int * i)}]" for i in
                                         range(number_ele)]), []

                # print("********",ast.unparse(star_node),star_var,type(lower), type(step_int),type(number_ele),lower,step_int,number_ele)
            # if lower.isdigit():
            #     # print("********",[f"{ast.unparse(star_var)}[{str(int(lower)+step_int*i)}]" for i in range(number_ele)])
            #     return 1, ", ".join([f"{ast.unparse(star_var)}[{str(int(lower) + step_int * i)}]" for i in
            #                          range(number_ele)]), additional_ass
            #
            # else:
            #     return 1, ", ".join([f"{ast.unparse(star_var)}[{lower + str(step_int * i)}]" for i in
            #                          range(number_ele)]), additional_ass
            # return 1, ", ".join([f"{ast.unparse(star_var)}[{str(lower+step_int*i)}]" for i in range(number_ele)]),additional_ass

            # return 1, ", ".join([f"{star_var_str}[{i}]" for i in range(number_ele)]),additional_ass

        else:
            return 0, f"{star_var_str}[0], {star_var_str}[1], ..., {star_var_str}[len({star_var_str}) - 1]",additional_ass

def transform_idiom_call_star(parent_call, star_node,stmt_node):
    '''
    note_str="EMPTY_VALUE belongs to [None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]"
    new_code_list=[]
    if isinstance(node,ast.UnaryOp):
        value=node.operand
        new_code_list=[ast.unparse(value)," in ","[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]"]
        # pass
    else:
        new_code_list=[ast.unparse(node), " not in ", "[None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)]"]
        # pass
    # ast.unparse(node)
    new_code="".join(new_code_list)
    for e in ast.walk(ast.parse(new_code)):
        if isinstance(e,ast.Compare):
            return [node, [e]]
    # print("old str: ",ast.unparse(node))
    '''
    print("old str: ", ast.unparse(parent_call),ast.unparse(star_node))
    note_str = "Cannot be refactored "
    # ast_transform.Rewrite_compre(node, name).visit(copy.deepcopy(parent_node))
    # Rewrite_star(star_node,).visit(parent_call)

    flag, new_code,additional_ass = determine_refactor(star_node)
    print(">>>>>>>>>>>>>>>new_code: ", ast.unparse(star_node), additional_ass, new_code, flag)

    # [line_head, "from decimal import Decimal\nfrom fractions import Fraction\n"]
    compltet_code = new_code
    if additional_ass:

        return [star_node, [new_code, "", "", [stmt_node.lineno, additional_ass[0]]], compltet_code,
                ast.unparse(parent_call), flag]
    else:

        return [star_node, [new_code, "", ""], compltet_code, ast.unparse(parent_call), flag]
    # if flag:
    #
    #     if additional_ass:
    #
    #         return [star_node, [new_code, "", "",[stmt_node.lineno,additional_ass[0]]], compltet_code,ast.unparse(parent_call),flag]
    #     else:
    #
    #         return [star_node, [new_code, "", ""], compltet_code,ast.unparse(parent_call),flag]
    # return [star_node, [new_code, "", ""], compltet_code,ast.unparse(parent_call),flag]
    #
    # if flag:
    #     return [star_node, [new_code,"",""],flag]
    # else:
    #     return []#[star_node, [new_code, "", ""], flag]
    # return [star_node, [new_code,"",""],flag]
