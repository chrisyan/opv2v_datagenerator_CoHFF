
front_pcd = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_21_22_21_37/2987/semantic_lidar_data_000073_semantic_lidarfront.pcd"
back_pcd = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_21_22_21_37/2987/semantic_lidar_data_000073_semantic_lidarback.pcd"

def combine2pcl(front_pcd, back_pcd):
    #merged_pcd = front_pcd+ "_merged.pcd"
    merged_pcd = "/home/gaiax/cooperative/OpenCOOD_root/OpenCOOD/my_scripts/"+ "_merged2.pcd"
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



combine2pcl(front_pcd, back_pcd)