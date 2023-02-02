import os,sys
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
import util
dict_list_compre={'Call': 51528, 'Name': 22070, 'Subscript': 16067, 'BinOp': 8465, 'Compare': 1190, 'Attribute': 10982, 'Tuple': 6609, 'ListComp': 1385, 'IfExp': 2848, 'JoinedStr': 1174, 'Constant': 1224, 'List': 1718, 'BoolOp': 277, 'UnaryOp': 204, 'Dict': 2536, 'Lambda': 11, 'SetComp': 7, 'DictComp': 127, 'Set': 15, 'Await': 1, 'Yield': 1, 'GeneratorExp': 2}
dict_set_compre={'Attribute': 860, 'Subscript': 704, 'Call': 897, 'BoolOp': 6, 'Name': 958, 'Tuple': 311, 'IfExp': 35, 'BinOp': 94, 'JoinedStr': 24, 'UnaryOp': 1}
dict_dict_compre_key={'Subscript': 1328, 'Name': 11016, 'BinOp': 292, 'Call': 1524, 'Attribute': 1471, 'JoinedStr': 194, 'BoolOp': 5, 'Tuple': 133, 'IfExp': 34, 'Constant': 2, 'UnaryOp': 3}
dict_dict_compre_value={'Subscript': 1909, 'Name': 5895, 'Attribute': 721, 'List': 318, 'Call': 4508, 'Dict': 244, 'IfExp': 697, 'Constant': 584, 'Tuple': 210, 'Set': 10, 'BoolOp': 22, 'ListComp': 159, 'DictComp': 83, 'BinOp': 527, 'SetComp': 25, 'UnaryOp': 25, 'JoinedStr': 21, 'Compare': 41, 'Lambda': 3}

dict_chain_compare={'Attribute': 1822, 'Call': 2364, 'Name': 5657, 'Subscript': 1308, 'BinOp': 534, 'BoolOp': 4, 'Constant': 149, 'Yield': 1, 'Tuple': 24, 'ListComp': 4, 'UnaryOp': 15, 'Compare': 6, 'List': 3, 'Set': 3}
dict_truth_test={'Name': 188893, 'Attribute': 108557, 'UnaryOp': 103459, 'GeneratorExp': 11, 'BinOp': 3060, 'Subscript': 13898, 'ListComp': 110, 'NamedExpr': 550, 'Yield': 34, 'Tuple': 22, 'Await': 27, 'IfExp': 127, 'List': 6, 'YieldFrom': 1, 'Dict': 1}
dict_star={'Subscript': 2420, 'Constant': 92, 'Attribute': 4069, 'ListComp': 2075, 'Name': 52151, 'Call': 4718, 'GeneratorExp': 635, 'Tuple': 106, 'BinOp': 788, 'BoolOp': 74, 'List': 272, 'IfExp': 57, 'SetComp': 2, 'YieldFrom': 1}
dict_loop_else={'Attribute': 423, 'List': 42, 'Name': 761, 'Call': 1212, 'Subscript': 116, 'BoolOp': 22, 'UnaryOp': 13, 'BinOp': 14, 'Compare': 122, 'Tuple': 71, 'IfExp': 1, 'ListComp': 5, 'GeneratorExp': 4, 'Constant': 4}
dict_ass_multi_tar_value={'Attribute': 12237, 'BinOp': 3678, 'Call': 150167, 'Subscript': 14695, 'Constant': 11127, 'Name': 22949, 'UnaryOp': 497, 'Dict': 734, 'ListComp': 1088, 'BoolOp': 205, 'Lambda': 33, 'IfExp': 497, 'Yield': 396, 'GeneratorExp': 314, 'Await': 22, 'JoinedStr': 31, 'Compare': 37, 'YieldFrom': 100, 'Starred': 50, 'DictComp': 12, 'SetComp': 2}
dict_for_multi_tar={'Call': 75448, 'Name': 11170, 'Attribute': 2454, 'BoolOp': 34, 'Subscript': 620, 'GeneratorExp': 59, 'Tuple': 897, 'List': 1047, 'IfExp': 16, 'BinOp': 56, 'ListComp': 62, 'Set': 2, 'SetComp': 1}

save_complicated_code_feature_dir_pkl = util.data_root + "usage_context/"
dict_list_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "list_compre")
dict_set_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "set_compre")
dict_dict_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "dict_compre")
dict_chain_compare=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare")
dict_truth_test=util.load_pkl(save_complicated_code_feature_dir_pkl, "truth_value_test")
dict_star=util.load_pkl(save_complicated_code_feature_dir_pkl, "starred")
# util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_targets_object", dict_tar_type)
#     util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object", dict_value_type)

# dict_ass_multi_tar_value=util.load_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object")
# dict_for_multi_tar=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_multi_tar_object")


all_keys=set(dict_list_compre.keys())|set(dict_set_compre.keys())|set(dict_dict_compre.keys())|\
         set(dict_chain_compare.keys())|set(dict_truth_test.keys())|set(dict_star.keys())
print("dict_list_compre: ",dict_list_compre.keys())
print("dict_set_compre: ",dict_set_compre.keys())
print("dict_dict_compre: ",dict_dict_compre.keys())
print("dict_chain_compare: ",dict_chain_compare.keys())
print("dict_truth_test: ",dict_truth_test.keys())
print("dict_star: ",dict_star.keys())
print("all_keys: ",all_keys)
result=[dict_list_compre,dict_set_compre,dict_dict_compre,dict_chain_compare,
        dict_truth_test,dict_star]
# ,dict_loop_else,dict_ass_multi_tar_value,
#         dict_for_multi_tar

colum=["node","list_compre","set_compre","dict_compre","chain_compare",
        "truth_test","starred"]
# ,"loop_else","ass_multi_tar",
#         "for_multi_tar"
result_csv=[]
for key in all_keys:
    row_data=[key]
    for dict_idiom in result:
        total=sum(dict_idiom.values())
        if key in dict_idiom:
            row_data.append(dict_idiom[key]/total)
        else:
            row_data.append(0)
    result_csv.append(row_data)


util.save_csv(util.data_root + "rq_1/all_idioms_usage_context.csv",
                  result_csv,
                  colum)






