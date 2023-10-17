
import os
import re
import time

import json

start_time = time.time()
print(f"脚本开始运行时间: {time.ctime(start_time)}")

# 定义主文件夹路径
main_folder_path  = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_23_20_47_11"



# 使用正则表达式匹配文件名
pattern = r"semantic_lidar_data_(\d+)_semantic_lidar(frontlast|backfirst|left|right)_point\.pcd"



# 定义递归函数来搜索文件夹中的PCD文件
def search_pcd_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # 使用正则表达式匹配文件名
            match = re.match(pattern, filename)
            if match:
                file_number = match.group(1)
                front_or_back = match.group(2)
                front_back_pair = os.path.join(root, filename)
                yield file_number, front_or_back, front_back_pair

# 遍历主文件夹中的每个子文件夹
for subfolder in os.listdir(main_folder_path):
    subfolder_path = os.path.join(main_folder_path, subfolder)
    if os.path.isdir(subfolder_path):
        # 创建一个字典，用于存储匹配的文件对
        file_dict = {}
        # 调用递归函数来搜索子文件夹中的PCD文件
        for file_number, front_or_back, front_back_pair in search_pcd_files(subfolder_path):
            if file_number not in file_dict:
                file_dict[file_number] = {}
            file_dict[file_number][front_or_back] = front_back_pair



        # 遍历字典，执行合并操作
        for file_number, file_pair in file_dict.items():


            # 检查是否有匹配的front和back文件
            if 'frontlast' in file_pair and 'backfirst' in file_pair and 'left' in file_pair and 'right' in file_pair:
                front_pcd = file_pair['frontlast']
                back_pcd = file_pair['backfirst']
                left_pcd = file_pair['left']
                right_pcd = file_pair['right']
                # 在这里执行合并操作
                # 你可以使用前面的代码示例来合并front和back文件
                # 打印一些信息以供参考

                # front_pcd = subfolder_path + "/" + file_pair['front']
                # back_pcd = subfolder_path + "/" + file_pair['back']

                # 在这里执行合并操作
                # 你可以使用前面的代码示例来合并front和back文件
                # 打印一些信息以供参考
                # combine2pcl(front_filename, back_filename)

                merged_pcd = subfolder_path + "/"  + file_number+ "_semantic.pcd"
                # 读取第一个PCD文件
                with open(front_pcd, "r") as file1:
                    lines1 = file1.readlines()

                # 读取第二个PCD文件，从第12行开始
                with open(back_pcd, "r") as file2:
                    lines2 = file2.readlines()

                # 读取第一个PCD文件
                with open(left_pcd, "r") as file3:
                    lines3 = file3.readlines()

                # 读取第二个PCD文件，从第12行开始
                with open(right_pcd, "r") as file4:
                    lines4 = file4.readlines()

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

                points3 = 0
                for line in lines3:
                    if line.startswith("POINTS"):
                        points3 = int(line.split()[1])
                        break

                # 提取第二个文件的POINTS字段值
                points4 = 0
                for line in lines4:
                    if line.startswith("POINTS"):
                        points4 = int(line.split()[1])
                        break

                # 计算总点数
                total_points = points1 + points2 + points3 + points4

                # 更新新的文件中的POINTS字段的值
                with open(merged_pcd, "w") as merged_file:
                    # 写入pcd文件头部
                    merged_file.write("# .PCD v0.7 - Point Cloud Data file format\n")
                    merged_file.write("VERSION 0.7\n")
                    merged_file.write("FIELDS x y z rgb\n")
                    merged_file.write("SIZE 4 4 4 4\n")
                    merged_file.write("TYPE F F F I\n")
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

                    for line in lines3[11:]:
                        merged_file.write(line)
                    for line in lines4[11:]:
                        merged_file.write(line)

#                print(f"In {subfolder}, merging {front_filename} and {back_filename}...")



end_time = time.time()
print(f"脚本结束运行时间: {time.ctime(end_time)}")
print(f"脚本运行总时间: {end_time - start_time} 秒")