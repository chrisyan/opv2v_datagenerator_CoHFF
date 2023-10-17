from combine4pcls_folder_1scenaio_baoli import *
from move_old_semantic import *
from generate_json import *

if __name__ == "__main__":
    # specify a scenario path
    main_folder_path  = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/2021_08_23_20_47_11"
    combine_4lidar_1scenario(main_folder_path)

    # create a new folder to save original 4 semantic lidars
    folder_name = os.path.basename(main_folder_path)
    print(folder_name)
    new_parent_folder_name = "new_"+folder_name
    move_4lidars2new(main_folder_path, new_parent_folder_name)

    # generate json for each pcd
    process_folder(main_folder_path)
    print("处理完成，每个子文件夹中的JSON文件存储在相应的文件夹中。")
