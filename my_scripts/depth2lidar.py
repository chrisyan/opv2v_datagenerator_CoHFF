import cv2
import numpy as np
import matplotlib.pyplot as plt


def sensor2world(sensor_x, sensor_y, sensor_yaw, x, y):
    rotation_matrix = np.array([[np.cos(sensor_yaw), -np.sin(sensor_yaw)],
                                [np.sin(sensor_yaw), np.cos(sensor_yaw)]])

    pXY = np.dot(rotation_matrix, np.array([x, y])) + np.array([sensor_x, sensor_y])

    return pXY[0], pXY[1]



def pixel2sensor(u, v, depth, dx=800, dy=600, fov_deg=90):
    Cu = dx / 2
    Cv = dy / 2

    fx = dx / (2 * np.tan(fov_deg * np.pi / 360))
    fy = dy / (2 * np.tan(fov_deg * np.pi / 360))

    K = np.array([[fx, 0, Cu],
                  [0, fy, Cv],
                  [0, 0, 1]])

    p_img = np.array([u, v, 1])
    # point in sensor coordinate-system
    p_sensor = np.dot(np.linalg.inv(K), p_img) * depth

    return p_sensor[0], p_sensor[1]


depth_image = cv2.imread("/home/gaiax/cooperative/OpenCOOD_root/OpenCOOD/logreplay/scenario/tutorial/new_depth_output/000008.jpg", cv2.IMREAD_UNCHANGED)


print(depth_image.shape)
def show():
    px_list = []
    py_list = []

    pX_list = []
    pY_list = []
    for v in range(600):
        for u in range(800):
            x, y = pixel2sensor(u, v, depth_image[v, u])
            pX, pY = sensor2world(sensor_x=3, sensor_y=0, sensor_yaw=0, x=x, y=y)
            # px_list.append(x)
            # py_list.append(y)

            pX_list.append(pX)
            pY_list.append(pY)

    print("pX_list", pX_list)
    print("pY_list", pY_list)
    plt.plot(pX_list,pY_list,'o')
    plt.show()


import numpy as np



fx = 800
fy = 600
Cu = depth_image.shape[1] / 2
Cv = depth_image.shape[0] / 2

#create a empty list
point_cloud = []
pX_list = []
pY_list = []

# 遍历深度图像中的每个像素
for u in range(depth_image.shape[1]):
    for v in range(depth_image.shape[0]):
        # 获取深度值（以米为单位）
        depth = depth_image[v, u]

        # 计算点在相机坐标系中的坐标
        x = (u - Cu) * depth / fx
        y = (v - Cv) * depth / fy

        # 将点添加到点云中
        point_cloud.append([x, y, depth])

        pX, pY = sensor2world(sensor_x=3, sensor_y=0, sensor_yaw=0, x=x, y=y)
        # px_list.append(x)
        # py_list.append(y)

        pX_list.append(pX)
        pY_list.append(pY)

# 将点云转换为NumPy数组
point_cloud = np.array(point_cloud)


# 创建 .pcd 文件的头部信息
pcd_header = """# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH {width}
HEIGHT 1
VIEWPOINT 0 0 0 1 0 0 0
POINTS {num_points}
DATA ascii
"""

# 保存点云为 .pcd 文件
file_path = 'point_cloud.pcd'
with open(file_path, 'w') as f:
    # 写入 .pcd 头部信息
    pcd_header = pcd_header.format(width=3, num_points=len(point_cloud))
    f.write(pcd_header)

    # 写入点云数据
    for point in point_cloud:
        x, y, z = point
        f.write(f"{x} {y} {z}\n")

print(f"Point cloud saved to {file_path} in .pcd format")

plt.plot(pX_list, pY_list, 'o')
plt.show()