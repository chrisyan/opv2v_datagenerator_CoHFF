import os
import json
import numpy as np

def get_class_channel(file_path):
    '''open pcd file, and get class channel'''
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 提取RGB值
    class_labels = []
    for line in lines[11:]:  # 从第12行开始是点云数据
        line = line.strip('\n')
        xyzrgb = line.split(' ')
        rgb = int(xyzrgb[-1])  # 提取最后一个字段作为RGB值
        class_labels.append(rgb)

    # 打印提取的RGB值
    print("RGB Values:", class_labels)
    unique_values = np.unique(class_labels)

    print("unique_values: ", unique_values)
    class_labels = np.asarray(class_labels)
    return class_labels

def process_folder(folder_path):
    # 循环处理文件夹中的每个PCD文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith(".pcd"):
            class_labels = get_class_channel(file_path)

            # 构建输出JSON文件的路径
            json_file_path = os.path.join(folder_path, f'{os.path.splitext(filename)[0]}_label.json')

            # 存入JSON文件
            data = {"labels": class_labels.tolist()}  # 将NumPy数组转换为Python列表
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file)
        elif os.path.isdir(file_path):
            # 如果是子文件夹，则递归处理
            process_folder(file_path)
    print("****************************** STEP 3 DONE!!! *************************************")



if __name__ == "__main__":
    # 指定包含PCD文件的主文件夹路径
    main_folder_path = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_23_20_47_11"
    # 处理主文件夹中的子文件夹
    process_folder(main_folder_path)
    print("处理完成，每个子文件夹中的JSON文件存储在相应的文件夹中。")
