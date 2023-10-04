import json


file = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional_copy/2021_08_23_20_47_11/109/000076_semantic_label.json"

with open(file, 'r') as f:
    curr_labels = json.load(f)
    curr_l = curr_labels["labels"]

print(len(curr_l))