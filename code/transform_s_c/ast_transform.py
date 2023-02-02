import ast
import copy


class Rewrite_compre(ast.NodeTransformer):
    def __init__(self,node=None,replace_node=None):
        self.lineno =node.lineno
        self.colset=node.col_offset
        self.replace_node=replace_node
        pass
        # self.ass =ass_node
        # self.new_node =new_node
        # self.remove_ass_flag =remove_ass_flag
    def visit_ListComp(self, node):
        # return ast.Name("a")
        if node.lineno==self.lineno and node.col_offset==self.colset:
            return self.replace_node
        else:
            return node
    def visit_DictComp(self, node):
        # return ast.Name("a")
        if node.lineno==self.lineno and node.col_offset==self.colset:
            return self.replace_node
        else:
            return node
    def visit_SetComp(self, node):
        # return ast.Name("a")
        if node.lineno==self.lineno and node.col_offset==self.colset:
            return self.replace_node
        else:
            return node
    # def generic_visit(self, node):
    #     if isinstance(node,ast.ListComp) :
    #         return ast.Name("a")
    #     return node
    #     if hasattr(node, "body"):
    #         # print("node: ",ast.unparse(node))
    #         ass_re=None
    #         for ind,child in enumerate(node.body):
    #             old_len = len(node.body)
    #             if 1:
    #             # for ind, child in enumerate(node.body):
    #                 # print("child: ",ast.unparse(child),child.lineno)
    #                 if ast.unparse(child) == ast.unparse(self.ass) and self.ass.lineno == child.lineno:
    #                     # print(">>>>come here: ", ast.unparse(child))
    #                     # node.body.remove(child)
    #                     ass_re=child
    #                     continue
    #                 if child.lineno == self.old_node.lineno and isinstance(child, ast.For) and ast.unparse(
    #                         child) == ast.unparse(self.old_node):
    #                     # print(">>>>come for node here: ", ast.unparse(child))
    #                     node.body.remove(child)
    #
    #                     node.body.insert(ind, self.new_node)
    #                     # instru_ment = f'print("I come here")'
    #                     # for node_instru in ast.walk(ast.parse(instru_ment)):
    #                     #     if isinstance(node_instru, ast.stmt):
    #                     #         node.body.insert(ind+1, self.new_node)
    #                     # return node
    #                     break
    #                 bia = old_len - len(node.body)
    #                 # print("bias: ", bia)
    #                 node.body[ind - bia] = self.generic_visit(node.body[ind - bia])
    #         if ass_re and self.remove_ass_flag:
    #             node.body.remove(ass_re)
    #             # print("child: ",ast.unparse(child),child.lineno)
    #             # if child.lineno == self.call_node.lineno:
    #             #     print("come the lineo: ", ast.unparse(child))
    #             #     # if isinstance(child,ast.Expr) and isinstance(child.value,ast.Call):
    #             #     #     node.body[ind].value = self.visit_Call(node.body[ind].value)
    #             #
    #             #     re=Rewrite_call(self.old_node,self.new_node,self.call_node)
    #             #     node.body[ind]=re.visit(node.body[ind])
    #             # re = Rewrite_ass(self.old_node, self.ass_node, self.new_node)
    #             # node.body[ind] = re.visit(node.body[ind])
    #             # node.body[ind] = self.generic_visit(node.body[ind])
    #     if hasattr(node,"orelse"):
    #         # print("come here")
    #         for ind,child in enumerate(node.orelse):
    #             node.orelse[ind]=self.generic_visit(child)
    #     return node
if __name__ == '__main__':
    code='''f.write('\tINVERSION = AUTO\\n')
f.write('\tMODULATION = QPSK\\n')
b=[str(x) for x in defs.pids]
pids = "+".join([str(x) for x in defs.pids])   
with open(chan_file, 'w') as f:
    pids = "+".join([str(x) for x in defs.pids])  
def f():
    pids = "+".join([[str(x) for x in defs.pids] for i in a])  
'''
    code_node=ast.parse(code)
    new_tree=Rewrite_compre().visit(copy.deepcopy(code_node))
    print("new_tree: ",ast.unparse(new_tree))
    print("code_node: ", ast.unparse(code_node))
    pass