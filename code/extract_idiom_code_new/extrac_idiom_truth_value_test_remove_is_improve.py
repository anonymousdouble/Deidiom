import sys,ast,os

sys.path.append("../..")
sys.path.append("../../../")
import util,traceback
from extract_simp_cmpl_data import ast_util
import complicated_code_util

from pathos.multiprocessing import ProcessingPool as newPool


def is_simple_object(e):

    if isinstance(e, (ast.Compare,ast.BoolOp, ast.Call,ast.Constant)):# 这里的constant是 true false 如 while true
        return False
    elif isinstance(e, ast.UnaryOp):
        if isinstance(e.op, ast.Not):
            operand=e.operand
            if isinstance(operand, (ast.Compare, ast.BoolOp, ast.Call,ast.Constant)):
                return False
            else:
                return True

    return True

def find_not_op_contains_idiom(node):
    operand=node.operand
    if isinstance(operand,(ast.Call,ast.Compare,ast.BoolOp, ast.Not)):
            return False
    return True
def get_idiom_truth_value_test_improve_add_parent_node(tree):

    code_info=dict()
    for node in ast.walk(tree):
        if isinstance(node, (ast.stmt)):
            for child_node in ast.walk(node):
                # stmt node
                if hasattr(child_node, "test"):
                    # print("come here")
                    v = child_node.test
                    if is_simple_object(v):
                        if v in code_info:
                            code_info[v][0]=node
                        else:
                            code_info[v]=[node,None]


                for child in ast.iter_child_nodes(child_node):
                    if hasattr(child, "test"):
                        v = child.test
                        if is_simple_object(v):
                            if v in code_info:
                                code_info[v][1] = child
                            else:
                                code_info[v] = [None, child]

    if code_info:
        print("code_info: ",code_info)
    return code_info
def get_idiom_truth_value_test_improve(tree):
    code_list = []
    for node in ast.walk(tree):
        if hasattr(node,"test"):
            # print("come here")
            v=node.test
            if is_simple_object(v):
                # code_list.append([ast.unparse(v), [v.lineno, v.end_lineno, v.col_offset, v.end_col_offset]])
                code_list.append([v])

    return code_list
def get_idiom_truth_value_test(tree):
    code_list = []
    for node in ast.walk(tree):
        if hasattr(node,"test"):
            # print("come here")
            v=node.test
            if is_simple_object(v):
                code_list.append([ast.unparse(v), [v.lineno, v.end_lineno, v.col_offset, v.end_col_offset]])


    return code_list

def get_idiom_truth_value_test_add_node(tree):
    code_list = []
    for node in ast.walk(tree):
        if hasattr(node,"test"):
            # print("come here")
            v=node.test
            if is_simple_object(v):
                code_list.append([ast.unparse(v), ast.unparse(node), [v.lineno, v.end_lineno, v.col_offset, v.end_col_offset]])


    return code_list

def save_repo_for_else_complicated(repo_name):
    count_complicated_code=0
    #print("come the repo: ", repo_name)
    one_repo_for_else_code_list = []
    dict_file = dict()

    for file_info in dict_repo_file_python[repo_name]:

        file_path = file_info["file_path"]
        # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     continue
        file_html = file_info["file_html"]
        #print("come this file: ", file_path)
        try:
            content = util.load_file_path(file_path)
        except:
            print(f"{file_path} is not existed!")
            continue
        #print("content: ",content)
        try:
            file_tree = ast.parse(content)
            ana_py = ast_util.Fun_Analyzer()
            ana_py.visit(file_tree)

            dict_class = dict()
            for tree, class_name in ana_py.func_def_list:
                code_list = get_idiom_truth_value_test(tree)
                if code_list:
                    ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)
            if dict_class:
                dict_file[file_html] = dict_class

        except SyntaxError:

            print("the file has syntax error")

            continue

        except ValueError:

            traceback.print_exc()

            print("the file has value error: ", file_html)

            continue
        #break
    if 1:#one_repo_for_else_code_list:
        # count_complicated_code=count_complicated_code+len(one_repo_for_else_code_list)
        # print("it exists for else complicated code1: ", len(one_repo_for_else_code_list))
        util.save_pkl(save_complicated_code_dir_pkl, repo_name, dict_file)

        # util.save_json(save_complicated_code_dir, repo_name, one_repo_for_else_code_list)
        #print("save successfully! ", save_complicated_code_dir + repo_name)

    # return count_complicated_code

if __name__ == '__main__':
    require_nodes = ['Assign', 'For', 'While', 'With','Compare']
    code ='''
func(a, b=c, *d, **e)
c,b,(w,e),*a=p
# for i,(e,w) in enumerate(range(10)):
#     print(i,e)
# else:
#     print("yes")
while 2>a>1:
    a.append(e)
else:
    ...
    print("Yes")
with open("f.txt",'r') as f:
    f.read()
    
while a:
    pass
if not a:
    pass
    
'''
    print(get_idiom_truth_value_test(ast.parse(code)))
    dict_repo_file_python= util.load_json(util.data_root, "python3_1000repos_files_info")
    save_complicated_code_dir= util.data_root + "idiom_code_dir_star_1000/truth_value_test_idiom_code/"
    save_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl/truth_value_test_idiom_code/"
    save_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl/truth_value_test_idiom_code_improve/"

    repo_list = []
    for ind, repo_name in enumerate(dict_repo_file_python):
        #print("repo infor: ",dict_repo_file_python[repo_name])
        if os.path.exists(save_complicated_code_dir_pkl+repo_name+".pkl"):
            continue
        repo_list.append(repo_name)
    print("count: ",len(repo_list))

    '''
    pool = newPool(nodes=30)
    pool.map(save_repo_for_else_complicated, repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    print("run complete")
    '''

    files_num_list = []
    star_num_list = []
    contributor_num_list = []
    count_repo, file_count, me_count, code_count = 0, 0, 0, 0
    file_list = set([])
    repo_code_num = dict()
    result_compli_for_else_list = []
    all_count_repo, all_file_count, all_me_count = 0, 0, 0
    for file_name in os.listdir(save_complicated_code_dir_pkl):
        all_count_repo += 1
        repo_name = file_name[:-4]
        # files_num_list.append(repo_files_info[repo_name])
        # star_num_list.append(repo_star_info[repo_name])
        # contributor_num_list.append(repo_contributor_info[repo_name])

        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)

        repo_file_count, repo_me_count, repo_code_count, repo_all_file_count, repo_all_me_count = complicated_code_util.get_code_count(
            complicate_code)
        # for code_list, file_path, file_html in complicate_code:
        code_count += repo_code_count
        file_count += repo_file_count
        me_count += repo_me_count
        all_file_count += repo_all_file_count
        all_me_count += repo_all_me_count
        repo_exist = 0
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        repo_exist = 1
                        for code in complicate_code[file_html][cl][me]:
                            # print("html: ",file_html,cl,me,ast.unparse(code1[0]))
                            #                code_index_start_end_list.append([node,assign_stmt,node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str])
                            # ass_str = []
                            # for ass in code1[0]:
                            #     ass_str.append(ast.unparse(ass))

                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, code[0]])

            # print(f"{file_html} of {repo_name} has  {len(code_list)} code1 fragments")
        count_repo += repo_exist

    # a=dict(sorted(repo_code_num.items(), key=lambda item: item[1], reverse=True))
    # print(a)
    # print(np.median(list(a.values())), np.max(list(a.values())), np.min(list(a.values())))
    # print(np.median(files_num_list), np.max(files_num_list), np.min(files_num_list))
    # print(np.median(star_num_list), np.max(star_num_list), np.min(star_num_list))
    # print(np.median(contributor_num_list), np.max(contributor_num_list), np.min(contributor_num_list))
    print("count: ", count_repo, code_count, file_count, me_count, all_count_repo, all_file_count, all_me_count)

    #'''
    # count=0
    # result_compli_for_else_list=[]
    # for file_name in os.listdir(save_complicated_code_dir):
    #     complicate_code=util.load_json(save_complicated_code_dir,file_name[:-5])
    #     for each_file in complicate_code:
    #
    #         # for code_list, file_path,file_html in each_file:
    #         #
    #         #     print("count: ",code_list)
    #             code_list=each_file[0]
    #             file_path=each_file[1]
    #             file_html=each_file[2]
    #             count += len(code_list)
    #             # print("count: ", count)
    #             for code1 in code_list:
    #                 repo_name=file_html.split("/")[4]
    #                 result_compli_for_else_list.append([repo_name,code1[0],code1[1],file_html,file_path])
    #                 #print("one code1: ",repo_name,code1,file_html,file_path)
    #     #             break
    #     #         break
    #     # # print("file: ",file_name)
    #     # break
    # print("count: ",count,len(os.listdir(save_complicated_code_dir)))
    # util.save_csv(util.data_root+"idiom_code_dir_star_1000/truth_value_test_idiom_code.csv",result_compli_for_else_list,["repo_name","code1","line_no","file_html","file_path"])


