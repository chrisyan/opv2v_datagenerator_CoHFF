import os

#semantic_merged_

# semantic_lidar_data_

folder_path = "/media/gaiax/ruiii/cooocc_additional/validate"

# 使用os.walk遍历文件夹及其子文件夹
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.startswith("semantic_lidar_data_") and file.endswith(".pcd"):
            file_path = os.path.join(root, file)
            os.remove(file_path)

# 如果您想删除空的子文件夹，可以使用以下代码
for root, dirs, files in os.walk(folder_path, topdown=False):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):  # 检查子文件夹是否为空
            os.rmdir(dir_path)

