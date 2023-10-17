import open3d as o3d
import numpy as np

from label import trainId2label
import matplotlib as plt

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
    22: [145, 170, 100],  # Terrain
    23: [255, 255, 0], # 'ReflectorPost'
    24: [255, 51, 51], # 'Barrier'
    25: [0, 255, 0] #  'TrafficCone'
}

    # 'ReflectorPost','Barrier', 'TrafficCone'
# [255,255,0],[139,0,0],[255,0,255]

def read_pcd(file_path):
    pcd = o3d.io.read_point_cloud(file_path)
    return pcd

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
    #print("RGB Values:", class_labels)
    unique_values = np.unique(class_labels)

    print("unique_values: ", unique_values)
    class_labels = np.asarray(class_labels)
    return class_labels

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



if __name__ == "__main__":
    lidar = "raw_lidar"
    #lidar = "semantic_lidar"
    #lidar = "both"
    #frame_number = "000077"

    if lidar == "raw_lidar":
        import open3d as o3d
        # 读取PCD文件
        #pcd2 = o3d.io.read_point_cloud("{}.pcd".format(frame_number))

        pcd2 = o3d.io.read_point_cloud("/home/gaiax/cooperative/OpenCOOD_root/OpenCOOD/my_scripts/point_cloud.pcd")
       # pcd2 = o3d.io.read_point_cloud("/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/2021_08_23_20_47_11/109/000078.pcd")

        # 可以使用以下代码查看点云数据的一些基本信息
        print(pcd2)
        print(f"Number of points: {len(pcd2.points)}")
        print(f"Point cloud type: {pcd2.points[0].dtype}")

        # 可视化点云数据
        o3d.visualization.draw_geometries([pcd2])

    if lidar == "semantic_lidar":
        # 调用函数读取PCD文件
        #file_path = "semantic_lidar_data_{}.pcd".format(frame_number)
        file_path = "000077_merged.pcd"

        pcd = read_pcd(file_path)
        class_labels = get_class_channel(file_path)

        # 获取点云数据
        points = np.asarray(pcd.points)
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
        o3d.visualization.draw_geometries([pcd])

    if lidar == "both":
        # 调用函数读取PCD文件 merged ### semantic lidar ###
        #file_path = "semantic_lidar_data_{}.pcd".format(frame_number)
        frame_number = "000078"

        #file_path = "/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/additional_final/2021_08_23_20_47_11/109/{}_semantic.pcd".format(frame_number)
        #semantic_lidar_data_000070_semantic_lidarfront.pcd
        # 000070_semantic

        file_path = "/home/gaiax/cooperative/OpenCOOD_root/OpenCOOD/my_scripts/test.pcd"


        pcd = read_pcd(file_path)
        class_labels = get_class_channel(file_path)
        #print("class_labels: ",class_labels)
        unique_values_class_labels = np.unique(class_labels)
        print("unique_values_class_labels:", unique_values_class_labels)

        # count number of one class
        value_to_count = 30
        count = np.count_nonzero(class_labels == value_to_count)
        print(f"before值 {value_to_count} 的数量是 {count}")

        # 获取点云数据
        points = np.asarray(pcd.points)
        colors_o3d = np.asarray(pcd.colors)
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
        o3d.visualization.draw_geometries([pcd])
        import open3d as o3d

        # 读取PCD文件 ### raw lidar ###
        #pcd2 = o3d.io.read_point_cloud("{}.pcd".format(frame_number))
        pcd2 = o3d.io.read_point_cloud("/home/gaiax/cooperative/OpenCOOD_root/opv2v_data_dumping/train/2021_08_23_20_47_11/109/{}.pcd".format(frame_number))

        # 可以使用以下代码查看点云数据的一些基本信息
        print(pcd2)
        print(f"Number of points: {len(pcd2.points)}")
        print(f"Point cloud type: {pcd2.points[0].dtype}")

        # 可视化点云数据
        o3d.visualization.draw_geometries([pcd, pcd2])
        #plt.save(pcd)







