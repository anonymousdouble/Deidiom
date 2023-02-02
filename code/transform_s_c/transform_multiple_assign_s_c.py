import ast,copy
import traceback




def whether_repeat_var(target_list,value_list):
    tmp_ass_list=[]
    new_value_list=value_list

    count = 0

    for ind_tar, tar in enumerate(target_list[:-1]):
        for ind,value in enumerate(value_list[ind_tar+1:]):


            for node in ast.walk(ast.parse(value)):
                if ast.unparse(node) == tar:
                    tmp_str = f"tmp{count}"
                    tmp_ass_list.append("".join([tmp_str," = ",value]))
                    new_value_list[ind+ind_tar+1]=tmp_str
                    count += 1
                    break
            else:
                for node in ast.walk(ast.parse(tar)):
                    if ast.unparse(node) == value:
                        tmp_str = f"tmp{count}"
                        tmp_ass_list.append("".join([tmp_str, " = ", value]))
                        new_value_list[ind+ind_tar+1] = tmp_str
                        count += 1
                        break
                else:
                    continue
                break
            break
        # else:
        #     continue
        # break
    return tmp_ass_list,new_value_list,count


# count represent the number of temporary values
def whether_add_tmp_var(target_list,value_list):
    tmp_ass_list, new_value_list,count = whether_repeat_var(target_list, value_list)
    new_ass_list = []
    new_ass_list.extend(tmp_ass_list)
    for ind, tar in enumerate(target_list):
        new_ass_list.append("".join([target_list[ind], " = ", new_value_list[ind]]))
    return "\n".join(new_ass_list),count
'''
def whether_add_tmp_var(target_list,value_list):


    count=0
    tmp_str=f"tmp{count}"

    new_ass_list=[]
    for ind,tar in enumerate(target_list):
        if ind+1<len(value_list) and tar in value_list[ind+1:]:
            index=value_list.index(tar)
            value_list[index]=tmp_str
            new_ass_list.append("".join([tmp_str," = ",tar]))
            new_ass_list.append("".join([target_list[ind]," = ",value_list[ind]]))
            count+=1
            tmp_str = f"tmp{count}"

        else:
            new_ass_list.append("".join([target_list[ind], " = ", value_list[ind]]))



    return "\n".join(new_ass_list)
'''
def whether_unpack_value_is_valid(e,value_elts):
    count = 0
    flag_star = 0
    for ind, cur in enumerate(e.elts):
        if isinstance(cur, ast.Starred):
            flag_star = 1
            continue
        count += 1

    if (flag_star and len(value_elts) < count) or (not flag_star and len(value_elts) != count):
        return 1
    return 0
def get_basic_object_value_star(e,tar,var_list=[],value_list=[]):
    if isinstance(e, (ast.Tuple,ast.List)):
        # count += len(e.elts)
        try:
            # if hasattr(value,"elts"):

                tar_elts=tar.elts
                bias=0
                for ind, cur in enumerate(e.elts):
                    if isinstance(cur, ast.Starred):
                        #
                        # var_list.append(ast.unparse(tar))
                        # value_list.append(ast.unparse(e))
                        star_len=len(tar_elts)-len(e.elts)
                        new_tar_list=[i for i in tar_elts[ind:ind+star_len+1]]
                        bias+=star_len
                        get_basic_object_value_star(cur, new_tar_list, var_list,value_list)
                    else:
                        get_basic_object_value_star(cur, tar_elts[ind+bias], var_list,value_list)

        except:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>SYNTAXERROR>>>>>>>>>>>>>>>>>>")
            var_list.append("SYNTAXERROR")
            value_list.append("SYNTAXERROR")
    elif isinstance(e,ast.Starred):
        # var_list.append(e.value)
        value=ast.unparse(e.value)
        value_list.extend([value+f"[{i}]" for i,v in enumerate(tar)])
        var_list.extend([ast.unparse(v) for i,v in enumerate(tar)])
    else:
        var_list.append(ast.unparse(tar))
        value_list.append(ast.unparse(e))
def get_basic_object(e,value,var_list=[],value_list=[],tmp_ass_list=[]):
    if isinstance(e, (ast.Tuple,ast.List)):
        # count += len(e.elts)
        try:
            if hasattr(value,"elts"):

                    value_elts=value.elts
                    bias=0

                    for ind, cur in enumerate(e.elts):
                        if isinstance(cur, ast.Starred):
                            # var_list.append(ast.unparse(e))
                            # value_list.append(ast.unparse(value))
                            star_len=len(value_elts)-len(e.elts)
                            new_value_list=[i for i in value_elts[ind:ind+star_len+1]]
                            bias+=star_len
                            get_basic_object(cur, new_value_list, var_list,value_list,tmp_ass_list)
                        else:
                            get_basic_object(cur, value_elts[ind+bias], var_list,value_list,tmp_ass_list)
            else:
                value_str_e = ast.unparse(value)
                for e_val in ast.walk(value):
                    if isinstance(e_val,ast.Call):
                        # var_list.append("tmp_fun")
                        # value_list.append(value_str_e)
                        value_str_e="tmp_fun_"+str(len(tmp_ass_list))
                        tmp_ass_list.append("".join([value_str_e, " = ",ast.unparse(value),"\n"]))

                        break



                for ind, cur in enumerate(e.elts):
                    if isinstance(cur, ast.Starred):
                        star_len = len(e.elts) - ind
                        if star_len==1:
                            value_str = value_str_e + f"[{ind}:]"
                        else:
                            value_str = value_str_e + f"[{ind}:-{star_len-1}]"
                    else:
                        value_str=value_str_e+f"[{ind}]"
                    for w in ast.walk(ast.parse(value_str)):
                        if isinstance(w,ast.Subscript):
                            get_basic_object(cur, w, var_list, value_list,tmp_ass_list)
                            break
        except:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>SYNTAXERROR>>>>>>>>>>>>>>>>>>")
            var_list.append("SYNTAXERROR")
            value_list.append("SYNTAXERROR")

    elif isinstance(e,ast.Starred):
        # var_list.append(e.value)
        var_list.append(ast.unparse(e.value))
        if isinstance(value,list):
            a=f"[{','.join([ast.unparse(v) for v in value])}]"
        else:
            a=ast.unparse(value)
        value_list.append(a)
    else:
        var_list.append(ast.unparse(e))
        value_list.append(ast.unparse(value))
        # print(e.__dict__, " are not been parsed")
def get_tmp_object(e,value,var_list=[],value_list=[],index_list=[],tmp_var=""):
    if isinstance(e, (ast.Tuple,ast.List)):
        # print(">>>get_tmp_object,e: ",ast.unparse(e),ast.unparse(value))
        # count += len(e.elts)
        try:
                # print(">>>value_elts: ", value.elts, ast.unparse(value))
            # if hasattr(value,"elts"):
                value_elts=value.elts
                bias=0

                for ind, cur in enumerate(e.elts):
                    if isinstance(cur, ast.Starred):
                        star_len=len(value_elts)-len(e.elts)
                        new_value_list=[i for i in value_elts[ind:ind+star_len+1]]
                        bias+=star_len
                        copy_index_list=copy.deepcopy(index_list)
                        copy_index_list.append([ind, ind + star_len + 1])
                        get_tmp_object(cur, new_value_list, var_list,value_list,copy_index_list,tmp_var)
                    else:
                        copy_index_list = copy.deepcopy(index_list)
                        copy_index_list.append([ind + bias])
                        get_tmp_object(cur, value_elts[ind+bias], var_list,value_list,copy_index_list,tmp_var)

        except:
            traceback.print_exc()
            var_list.append("SYNTAXERROR")
            value_list.append("SYNTAXERROR")

    else:
        var_list.append(ast.unparse(e))
        tmp_tmp_list=[tmp_var]
        for ind in index_list:
            if len(ind)>1:
                tmp_tmp_list.append(f"[{ind[0]}:{ind[1]}]")
            else:
                tmp_tmp_list.append(f"[{ind[0]}]")
        value_list.append("".join(tmp_tmp_list))

def transform_idiom_multi_ass(node_1):

    # ast.unparse(node)
    print("old_ass_str: ",ast.unparse(node_1))
    count_tmp_func=0
    count_tmp=0
    count_targets=0
    count_star_total=0
    new_ass_str=""
    new_ass_str_list=[]
    ass_trans_list = []
    if len(node_1.targets)>1:
        tmp_ass_list = []
        tmp_value = "tmp_value"
        new_ass_str_list = [f"{tmp_value} = {ast.unparse(node_1.value)}\n"]
        # tmp_ass_list = [f"{tmp_value} = {ast.unparse(node.value)}"]
        count_targets=len(node_1.targets)
        for tar in  node_1.targets:
            ass_node_str="".join([ast.unparse(tar)," = ",tmp_value])
            for e in ast.walk(ast.parse(ass_node_str)):
                if isinstance(e,ast.Assign):
                    ass_trans_list.append(e)
                    break
    else:
        ass_trans_list.append(node_1)
        # new_ass_str_list.append(node)
    for node in ass_trans_list:
        for tar in node.targets:
            tmp_ass_list=[]
            var_list = []
            value_list = []
            count_star_tar=0
            for e in ast.walk(tar):
                if isinstance(e,ast.Starred):
                    count_star_tar+=1
            count_star_total+=count_star_tar
            # if count_star_tar>1:
            #     return []
            count_star_val = 0
            for e in ast.walk(node.value):
                if isinstance(e, ast.Starred):
                    count_star_val += 1
            count_star_total += count_star_val
            if count_star_val > 1 or count_star_tar>1:
                return [[],"None","None","None",count_targets,count_star_total,"Do not compute"]
            if count_star_val>=1 and count_star_tar>=1:
                # return []# cannot explain
                return [[], "None", "None","None",count_targets, count_star_total,"Do not compute"]

            if count_star_val:
                get_basic_object_value_star(copy.deepcopy(node.value), tar, var_list, value_list)
            else:
                # if count_star_tar:
                    get_basic_object(tar, copy.deepcopy(node.value), var_list, value_list,tmp_ass_list)
            if "SYNTAXERROR" in var_list:
                return [[],"SYNTAXERROR","None","None",count_targets, count_star_total,"Do not compute"]
            # print("var_list,value_list: ", var_list,value_list)
            # new_ass_str+=whether_add_tmp_var(var_list, value_list)+"\n"
            new_str,count_tmp_each=whether_add_tmp_var(var_list, value_list)
            new_str="".join(tmp_ass_list)+new_str
            new_ass_str_list.extend(new_str+ "\n")
            count_tmp+=count_tmp_each
            count_tmp_func+=len(tmp_ass_list)

    compli_ass_stmt="".join(new_ass_str_list)
    compli_ass_stmt_list=compli_ass_stmt.split("\n")
    # print("new_ass_str: ", compli_ass_stmt)
    return [node_1, [compli_ass_stmt_list[0],"","\n".join(compli_ass_stmt_list[1:])],compli_ass_stmt,count_tmp,count_targets,count_star_total,count_tmp_func]


