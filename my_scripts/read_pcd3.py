import open3d as o3d
import numpy as np

from label import trainId2label

# 定义类别到颜色的映射字典
classes = {
    0: [0, 0, 0],  # None
    1: [70, 70, 70],  # Buildings
    2: [190, 153, 153],  # Fences
    3: [72, 0, 90],  # Other
    4: [220, 20, 60],  # Pedestrians
    5: [153, 153, 153],  # Poles
    6: [157, 234, 50],  # RoadLines
    7: [160,32,240],  # Roads
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

def read_pcd(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    print(np.asarray(pcd.points))
    colors = np.asarray(pcd.colors) * 255
    points = np.asarray(pcd.points)
    print(points.shape, colors.shape)
    return pcd, np.concatenate([points, colors], axis=-1)

# 调用函数读取PCD文件
file_path = "semantic_lidar_data_000069.pcd"
pcd = read_pcd(file_path)[0]



###########
# 打开PCD文件
file_path = "semantic_lidar_data_000069.pcd"
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

################
class_labels = np.asarray(class_labels)


# 获取点云数据、分类标签信息
points = np.asarray(pcd.points)

#class_labels = np.asarray(pcd.colors).astype(int)

def semantics_to_colors(semantics):
    # default color is black to hide outscreen points
    colors = np.zeros((semantics.shape[0], 3))

    for id in trainId2label:
        label = trainId2label[id]
        if id == 255 or id == -1:
            continue

        color = label.color
        indices = semantics == id
        colors[indices] = (color[0] / 255, color[1] / 255, color[2] / 255)

    return colors

colors = semantics_to_colors(class_labels)


# 根据类别为每个点赋予颜色
point_colors = np.zeros((len(class_labels), 3), dtype=np.uint8)
for class_label in np.unique(class_labels):
    mask = class_labels == class_label
    color = classes.get(class_label, [255, 255, 255])  # 默认为白色
    point_colors[mask] = color

# 创建点云对象并设置颜色
pcd.points = o3d.utility.Vector3dVector(points)
pcd.colors = o3d.utility.Vector3dVector(colors)

# 可视化点云数据
o3d.visualization.draw_geometries([pcd])




