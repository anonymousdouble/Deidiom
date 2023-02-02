
import sys, ast, os, copy
import tokenize
import sys,shutil
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"test_case/")
sys.path.append("..")
sys.path.append("../../")
import time
import util, github_util,get_test_case_acc_util,configure_pro_envir_util,file_replace
def get_test_acc(save_test_acc_dir_list):
    repo_list=set([])
    me_count = 0
    file_count = 0
    repo_count = 0
    complic_code_count = 0
    total_count = 0
    total_acc_count = 0
    total_tcs = []
    for save_test_acc_dir in save_test_acc_dir_list:
        for file in os.listdir(save_test_acc_dir):
            repo_name = file[:-4]
            complicate_code = util.load_pkl(save_test_acc_dir, repo_name)
            repo_list.add(repo_name)
            total_count+=complicate_code['total_count']
            total_acc_count+=complicate_code['total_acc_count']
            repo_count+=complicate_code['repo_count']
            file_count+=complicate_code['file_count']
            res = complicate_code['record_res']
            for each_res in res:
                total_tcs.extend(["".join(list(e)) for e in each_res[-1]])

            me_count+=complicate_code['me_count']
            complic_code_count+=complicate_code['complic_code_count']
    print("repo_count,file_count,me_count,complic_code_count,total_tcs:",repo_count,file_count,me_count,complic_code_count,len(total_tcs),len(set(total_tcs)))
    print("acc: ",total_acc_count,total_count,total_acc_count/total_count)
    print("repo_list: ",len(repo_list))
save_test_acc_dir_list = util.data_root + "idiom_test_case_benchmark_dir_new/for_compre_list_acc_dir/"
save_test_acc_dir_set = util.data_root + "idiom_test_case_benchmark_dir_new/for_compre_set_acc_dir/"
save_test_acc_dir_dict = util.data_root + "idiom_test_case_benchmark_dir_new/for_compre_dict_acc_dir/"
save_test_acc_dir_chain = util.data_root + "idiom_test_case_benchmark_dir/chained_comparison/"
save_test_acc_dir_loop_else = util.data_root + "idiom_test_case_benchmark_dir_new/for_else/"
save_acc_res_csv_dir_for_multi = util.data_root + "idiom_test_case_benchmark_dir/for_multi_tar/"
save_test_acc_dir_ass = util.data_root + "idiom_test_case_benchmark_dir/multi_assign_tmp_chain_ass_var_depend_new/"
save_test_acc_dir_truth = util.data_root + "idiom_test_case_benchmark_dir/truth_value_test_new_create_func/"
save_test_acc_dir_star = util.data_root + "idiom_test_case_benchmark_dir/call_star/"
save_test_acc_dir_list=[save_test_acc_dir_list,save_test_acc_dir_set,save_test_acc_dir_dict
                        ,save_test_acc_dir_chain,save_test_acc_dir_loop_else,save_acc_res_csv_dir_for_multi,
                        save_test_acc_dir_ass,save_test_acc_dir_truth,save_test_acc_dir_star ]

get_test_acc(save_test_acc_dir_list)