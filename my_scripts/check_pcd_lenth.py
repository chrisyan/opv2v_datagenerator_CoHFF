with open('/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_23_20_47_11/109/000086_semantic.pcd','r') as file:
    li = file.readlines()
    total_line = len(li)

print(f"Number of lines in the notepad file: {total_line}")
print(f"Number of lines in the notepad file: {total_line-11}")
