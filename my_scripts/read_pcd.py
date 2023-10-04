import open3d as o3d

# # 读取PCD文件
# pcd = o3d.io.read_point_cloud("000085.pcd")
#
# # 可以使用以下代码查看点云数据的一些基本信息
# print(pcd)
# print(f"Number of points: {len(pcd.points)}")
# print(f"Point cloud type: {pcd.points[0].dtype}")
#
# # 可以将点云数据可视化
# o3d.visualization.draw_geometries([pcd])

file_path = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional/2021_08_21_22_21_37/2987/semantic_lidar_data_000075_semantic_lidarbackfirst.pcd"


import open3d as o3d
import numpy as np

# 读取点云数据文件
point_cloud = o3d.io.read_point_cloud(file_path)
print(np.asarray(point_cloud.colors))

###### save on disk


# 创建一个示例的NumPy数组
my_array = np.array(point_cloud.colors)

# 指定要保存的文件路径
file_path = "my_array.txt"

# 使用numpy.savetxt将数组保存到文本文件
np.savetxt(file_path, my_array, fmt='%d', delimiter=', ')

# 提示用户已保存
print(f"已将NumPy数组保存到 {file_path}")


# 可以对点云进行各种操作和可视化
#o3d.visualization.draw_geometries([point_cloud])


