import os
import shutil

def move_4lidars2new(parent_folder_path, new_parent_folder_name):
    # 指定新的父文件夹的路径
    new_parent_folder_path = os.path.join(os.path.dirname(parent_folder_path), new_parent_folder_name)

    # 创建新的父文件夹
    os.makedirs(new_parent_folder_path)

    # 遍历父文件夹下的所有文件和子文件夹
    for root, _, files in os.walk(parent_folder_path):
        for file in files:
            if file.startswith("semantic_lidar_data_"):
                # 构建源文件的路径
                source_file_path = os.path.join(root, file)

                # 构建目标文件的路径
                relative_path = os.path.relpath(source_file_path, parent_folder_path)
                destination_file_path = os.path.join(new_parent_folder_path, relative_path)

                # 确保目标文件的目录已经存在，如果不存在则创建
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

                # 使用shutil.move()来执行移动操作
                shutil.move(source_file_path, destination_file_path)

    print("文件移动完成，并且创建了新的父文件夹", new_parent_folder_name)
    print("****************************** STEP 2 DONE!!! *************************************")

if __name__ == "__main__":
    parent_folder_path = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_23_20_47_11"
    # 指定父文件夹的路径
    folder_name = os.path.basename(parent_folder_path)
    print(folder_name)
    new_parent_folder_name = "new_"+folder_name
    # 指定新的父文件夹的名称
    new_parent_folder_name = "new_"+folder_name
    move_4lidars2new(parent_folder_path, new_parent_folder_name)
