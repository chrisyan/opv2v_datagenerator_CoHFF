import os
import re
from combine2pcls import combine2pcl

# 定义文件夹路径
folder_path = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_16_22_26_54/641"

# 使用正则表达式匹配文件名
pattern = r"semantic_lidar_data_(\d+)_semantic_lidar(front|back)\.pcd"

# 创建一个字典，用于存储匹配的文件对
file_dict = {}

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 使用正则表达式匹配文件名
    match = re.match(pattern, filename)
    if match:
        file_number = match.group(1)
        front_or_back = match.group(2)
        if file_number not in file_dict:
            file_dict[file_number] = {}
        file_dict[file_number][front_or_back] = filename

# 遍历字典，执行合并操作
for file_number, file_pair in file_dict.items():
    # 检查是否有匹配的front和back文件
    if 'front' in file_pair and 'back' in file_pair:
        front_filename = file_pair['front']
        back_filename = file_pair['back']


        front_pcd = folder_path + "/" + file_pair['front']
        back_pcd = folder_path + "/" + file_pair['back']

        # 在这里执行合并操作
        # 你可以使用前面的代码示例来合并front和back文件
        # 打印一些信息以供参考
        #combine2pcl(front_filename, back_filename)

        merged_pcd = "/home/gaiax/cooperative/OpenCOOD_root/OpenCOOD/my_scripts/641/" + front_filename[:26] + "_merged.pcd"
        # 读取第一个PCD文件
        with open(front_pcd, "r") as file1:
            lines1 = file1.readlines()

        # 读取第二个PCD文件，从第12行开始
        with open(back_pcd, "r") as file2:
            lines2 = file2.readlines()

        # 提取第一个文件的POINTS字段值
        points1 = 0
        for line in lines1:
            if line.startswith("POINTS"):
                points1 = int(line.split()[1])
                break

        # 提取第二个文件的POINTS字段值
        points2 = 0
        for line in lines2:
            if line.startswith("POINTS"):
                points2 = int(line.split()[1])
                break

        # 计算总点数
        total_points = points1 + points2

        # 更新新的文件中的POINTS字段的值
        with open(merged_pcd, "w") as merged_file:
            # 写入pcd文件头部
            merged_file.write("# .PCD v0.7 - Point Cloud Data file format\n")
            merged_file.write("VERSION 0.7\n")
            merged_file.write("FIELDS x y z rgb\n")
            merged_file.write("SIZE 4 4 4 4\n")
            merged_file.write("TYPE F F F F\n")
            merged_file.write("COUNT 1 1 1 1\n")
            merged_file.write("WIDTH {}\n".format(total_points))
            merged_file.write("HEIGHT 1\n")
            merged_file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
            merged_file.write("POINTS {}\n".format(total_points))
            merged_file.write("DATA ascii\n")
            for line in lines1[11:]:
                merged_file.write(line)
            for line in lines2[11:]:
                merged_file.write(line)
        print(f"Merging {front_filename} and {back_filename}...")