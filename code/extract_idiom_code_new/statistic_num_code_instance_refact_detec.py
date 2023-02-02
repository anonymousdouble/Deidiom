import os,sys
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
import util
save_complicated_code_feature_dir_pkl=util.data_root +"idiom_code_dir_star_1000_csv/"
dict_list_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "list_comprehension_idiom_code_shuffle")
dict_set_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "set_comprehension_idiom_code_shuffle")
dict_dict_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "dict_comprehension_idiom_code_shuffle")
dict_chain_compare=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_idiom_code_shuffle")
dict_truth_test=util.load_pkl(save_complicated_code_feature_dir_pkl, "truth_value_test_idiom_code")
dict_star=util.load_pkl(save_complicated_code_feature_dir_pkl, "star_call_idiom_code_many_circumstances_cannot_explain")
dict_loop_else=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_else_idiom_code_shuffle")
# util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_targets_object", dict_tar_type)
#     util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object", dict_value_type)

dict_ass_multi_tar_value=util.load_pkl(save_complicated_code_feature_dir_pkl, "multi_assign_idiom_code_shuffle")
dict_for_multi_tar=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_multi_tar_idiom_code_shuffle")

total_num=len(dict_list_compre)+len(dict_set_compre)+len(dict_dict_compre)+len(dict_chain_compare)+\
    len(dict_truth_test)+len(dict_star)+len(dict_loop_else)+len(dict_ass_multi_tar_value)+\
    len(dict_loop_else)+len(dict_for_multi_tar)

print("number of refactorings: ",total_num)
