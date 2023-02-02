import ast,copy,os,sys
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "transform_c_s/")
# from transform_var_unpack_for_target_compli_to_simple_new import RewriteName
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
def get_for_str(tmp_var,node,space = ""):
    code_str=""
    generators = node.generators
    elt=node.elt
    for gen in generators:
        tar = gen.target
        iter = gen.iter
        ifs = gen.ifs
        for_str_list = [space, "for ", ast.unparse(tar), " in ", ast.unparse(iter), ":\n"]
        code_str+="".join(for_str_list)
        for ind_if, if_node in enumerate(ifs):
            space += "    "
            if_str_list = [space, "if ", ast.unparse(if_node), ":\n"]
            code_str += "".join(if_str_list)
        space += "    "
    code_str+=trans_elt(tmp_var, elt, space)
    return code_str
def trans_elt(tmp_var,node,space):
    if not isinstance(node,ast.ListComp):
        if isinstance(node,ast.IfExp):
            return "".join([space,"if ",ast.unparse(node.test),":\n", space+"    "+tmp_var,".add(",ast.unparse(node.body),")","\n",space+"else:\n"])+ \
                   trans_elt(tmp_var, node.orelse, space+"    ")
        else:
            return "".join([space,tmp_var,".add(",ast.unparse(node),")","\n"])
    else:
        new_tmp_var=tmp_var[:-1]+str(int(tmp_var[-1])+1) if tmp_var[-1].isdigit() else tmp_var+"1"
        return "".join([space,new_tmp_var,"= set([])\n"])+get_for_str(new_tmp_var,node, space)+"".join([space,tmp_var,".add(",new_tmp_var,")","\n"])
def get_Subscript_node(code_str):
    for node in ast.walk(ast.parse(code_str)):
        if isinstance(node,ast.Subscript):
            return node


def trasnform_target(elts,Map_var, pre_str):
    #
    # if isinstance(target,(ast.List,ast.Tuple)):
    #     elts=target.elts
        count_sub=0
        # bias=1
        for ind,e_elt in enumerate(elts):
            if isinstance(e_elt, (ast.Starred)):
                if ind==len(elts)-1:
                    Map_var[ast.unparse(e_elt.value)] = get_Subscript_node(f"{pre_str}[{count_sub}:]")
                else:
                    Map_var[ast.unparse(e_elt.value)] = get_Subscript_node(f"{pre_str}[{count_sub}:{ind-len(elts)+1}]")
                bias=-1
                count_sub=ind-len(elts)
            elif isinstance(e_elt,(ast.List,ast.Tuple)):
                trasnform_target(e_elt.elts, Map_var,  f"{pre_str}[{(count_sub)}]")
            else:
                Map_var[ast.unparse(e_elt)] = get_Subscript_node(f"{pre_str}[{count_sub}]")
            count_sub+=1
    #         trasnform_target(e_elt,Map_var,count_sub,f"{pre_str}[{count}]")
    #         count_sub+=1
    # elif isinstance(target,(ast.Starred)):
    #     Map_var[target] = f"{pre_str}[{count}:]"
    #     pass
    # else:
    #     Map_var[target]=f"{pre_str}[{count}]"
class RewriteName(ast.NodeTransformer):
    def __init__(self, Map_var):
        self.Map_var = Map_var

    # def visit_Subscript(self, node):
    #     # print("visit_Subscript node: ", ast.unparse(node))
    #     if ast.unparse(node) in self.Map_var:
    #         # print("yes: ",ast.unparse(node))
    #         return self.Map_var[ast.unparse(node)]
    #     else:
    #         # node=RewriteName().visit(node)
    #         if isinstance(node.value,ast.Subscript):
    #             node.value=self.visit_Subscript(node.value)
    #         if isinstance(node.slice,ast.Subscript):
    #             node.slice = self.visit_Subscript(node.slice)
    #         return node
    def generic_visit(self, node):

        if ast.unparse(node) in self.Map_var:
            # print("yes it need to replce:",node,ast.unparse(node))
            if isinstance(node, ast.Expr):
                return ast.Expr(self.Map_var[ast.unparse(node)])
            else:
                return self.Map_var[ast.unparse(node)]
            # return ast.Expr(self.Map_var[ast.unparse(node)])
        #
        for ind_field, k in enumerate(node._fields):
            # print("transfrom: ", k)
            try:
                # if 1:
                v = getattr(node, k)
                # print("here: ", k,v )
                if isinstance(v, ast.AST):
                    if v._fields:
                        setattr(node, k, self.generic_visit(v))
                    # node._fields[k] = self.generic_visit(v)
                    pass
                elif isinstance(v, list):
                    # print(">>>>come list old: ", v)
                    for ind, e in enumerate(v):
                        if hasattr(e, '_fields'):
                            # print(">>>>come list e: ", v,e)
                            v[ind] = self.generic_visit(e)
                    # print("come list: ",v)
                    setattr(node, k, v)
                    # node._fields[k][ind]=self.generic_visit(e)
                    # pass
            except:
                continue
            #     print("error: ", ast.unparse(v))
            #     if ast.unparse(v) in self.Map_var:
            #         setattr(node, k, self.Map_var[ast.unparse(v)])
            # #         # node._fields[k]= self.Map_var[ast.unparse(v)]
            #     continue
        #
        #
        return node
class For_Else_C_S():
    def __init__(self):
        self.code_node_change="flag_else=0"
        code_node_change="flag_else=0"
        for if_node in ast.walk(ast.parse(code_node_change)):
            if isinstance(if_node,ast.Assign):
                self.flag_node_change=if_node
                break
        self.has_break=0
    def iter_ele(self,body):
        index_list=[]
        copy_body=copy.deepcopy(body)
        bias=0
        for ind, child in enumerate(copy_body):
            if isinstance(child, (ast.For, ast.While)):
                if child.orelse:
                    self.traverse_cur_layer_no_body(body[ind+bias])
                # self.traverse_cur_layer(body[ind + bias])
                # if hasattr(child, "orelse") and child.orelse:
                #     for ind_orelse,e_orelse in enumerate(body[ind+bias].orelse):
                #         self.traverse_cur_layer(body[ind+bias].orelse[ind_orelse])
                continue
            if isinstance(child, ast.Break):
                # index=body.index(child)
                # index_list.append(ind)
                self.has_break+=1
                body.insert(ind+bias, self.flag_node_change)
                bias+=1

                pass
            else:
                self.traverse_cur_layer(body[ind+bias])
        # for ind_break,index in enumerate(index_list):
        #     body.insert(index+ind_break, self.flag_node_change)
    def traverse_cur_layer_no_body(self,tree):
        if hasattr(tree, "orelse"):
            self.iter_ele(tree.orelse)
        if hasattr(tree, "handlers"):
            for handle in tree.handlers:
                self.iter_ele(handle.body)
        if hasattr(tree, "finalbody"):
            self.iter_ele(tree.finalbody)
    def traverse_cur_layer(self,tree):
        if hasattr(tree, "body"):

            self.iter_ele(tree.body)
            # for ind, child in enumerate(tree.body):
            #     if isinstance(child,(ast.For,ast.While)):
            #         continue
            #     if isinstance(child,ast.Break):
            #         pass
            #     else:
            #         traverse_cur_layer(child)
        if hasattr(tree, "orelse"):
            self.iter_ele(tree.orelse)
        if hasattr(tree, "handlers"):
            for handle in tree.handlers:
                self.iter_ele(handle.body)
        if hasattr(tree, "finalbody"):
            self.iter_ele(tree.finalbody)




def transform_idiom_for_else(node):
    print("old_str: ",ast.unparse(node))

    new_node=copy.deepcopy(node)
    new_node.orelse=[]
    code_init="flag_else=1"
    for_else=For_Else_C_S()
    for_else.traverse_cur_layer(new_node)
    has_break=for_else.has_break
    for if_node in ast.walk(ast.parse(code_init)):
        if isinstance(if_node,ast.Assign):
            node_init=if_node
            break
    if_code='''
if flag_else:
    pass
    '''
    for if_node in ast.walk(ast.parse(if_code)):
        if isinstance(if_node,ast.If):
            if_node.body=copy.deepcopy(node.orelse)
            break
    # print(">>>>>new_code:\n",ast.unparse(node_init))
    # print(ast.unparse(new_node))
    # print(ast.unparse(if_node))

    if has_break:
        complte_code="\n".join([ast.unparse(node_init),"",ast.unparse(new_node)+"\n"+ast.unparse(if_node)])
        print("complete_code: ", complte_code)
        return [node,[ast.unparse(node_init),"",ast.unparse(new_node)+"\n"+ast.unparse(if_node)],node,complte_code,has_break]
    else:
        complte_code="\n".join([ast.unparse(new_node),"","".join([ast.unparse(e)+"\n" for e in node.orelse])])
        print("complete_code: ",complte_code)
        # return [node,[ast.unparse(new_node),"","".join([ast.unparse(e)+"\n" for e in node.orelse])],node,complte_code,has_break]
        return [node,["","","".join([ast.unparse(new_node)+"\n"]+[ast.unparse(e)+"\n" for e in node.orelse])],node,complte_code,has_break]

    '''
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
    new_node_str=" ".join(new_node_str_list)
    print("new str: ",new_node_str)
    for new_node in ast.walk(ast.parse(new_node_str)):
            if isinstance(new_node,ast.Expr):
                print('new str: ',ast.unparse(new_node))
                return [node, new_node]
    '''
