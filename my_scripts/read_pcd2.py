import open3d as o3d

# 读取PCD文件
pcd = o3d.io.read_point_cloud("semantic_lidar_data_000069.pcd")

# 可以使用以下代码查看点云数据的一些基本信息
print(pcd)
print(f"Number of points: {len(pcd.points)}")
print(f"Point cloud type: {pcd.points[0].dtype}")

# 可以将点云数据可视化
o3d.visualization.draw_geometries([pcd])




import open3d as o3d
import numpy as np

# 定义类别到颜色的映射字典
classes = {
    0: [0, 0, 0],  # None
    1: [70, 70, 70],  # Buildings
    2: [190, 153, 153],  # Fences
    3: [72, 0, 90],  # Other
    4: [220, 20, 60],  # Pedestrians
    5: [153, 153, 153],  # Poles
    6: [157, 234, 50],  # RoadLines
    7: [128, 64, 128],  # Roads
    8: [244, 35, 232],  # Sidewalks
    9: [107, 142, 35],  # Vegetation
    10: [0, 0, 255],  # Vehicles
    11: [102, 102, 156],  # Walls
    12: [220, 220, 0],  # TrafficSigns
    13: [70, 130, 180],  # Sky
    14: [81, 0, 81],  # Ground
    15: [150, 100, 100],  # Bridge
    16: [230, 150, 140],  # RailTrack
    17: [180, 165, 180],  # All types of guard rails/crash barriers.
    18: [250, 170, 30],  # Traffic Light
    19: [110, 190, 160],  # Static
    20: [170, 120, 50],  # Dynamic
    21: [45, 60, 150],  # Water
    22: [145, 170, 100]  # Terrain
}

# def read_pcd(file_path):
# 	pcd = o3d.io.read_point_cloud(file_path)
# 	print(np.asarray(pcd.points))
# 	colors = np.asarray(pcd.colors) * 255
# 	points = np.asarray(pcd.points)
# 	print(points.shape, colors.shape)
# 	return np.concatenate([points, colors], axis=-1)
#
#
# # 调用函数读取PCD文件
# file_path = "semantic_lidar_data_000069.pcd"  # 替换为你的PCD文件路径
# # pcd = read_class_pcd(file_path)
# pcd = read_pcd(file_path)
#
#
# # 获取点云数据、分类标签信息
# points = pcd[:, :3]
# class_labels = pcd[:, 3]
#
# # 根据类别为每个点赋予颜色
# point_colors = np.zeros((len(class_labels), 3), dtype=np.uint8)
# for class_label in np.unique(class_labels):
#     mask = class_labels == class_label
#     color = classes.get(class_label, [255, 255, 255])  # 默认为白色
#     point_colors[mask] = color
#
# # 创建点云对象并设置颜色
# pcd.points = o3d.utility.Vector3dVector(points)
# pcd.colors = o3d.utility.Vector3dVector(point_colors)
#
# # 可视化点云数据
# o3d.visualization.draw_geometries([pcd])
