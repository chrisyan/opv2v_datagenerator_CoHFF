"""
This is mainly used to filter out objects that is not in the sight
of cameras.
"""
import weakref

import carla
import cv2
import numpy as np
from logreplay.sensors.base_sensor import BaseSensor

import os
import pickle
import open3d as o3d

import json

class SemanticLidar(BaseSensor):
    def __init__(self, agent_id, vehicle, world, config, global_position):
        super().__init__(agent_id, vehicle, world, config, global_position)

        if vehicle is not None:
            world = vehicle.get_world()

        self.agent_id = agent_id

        blueprint = world.get_blueprint_library(). \
            find('sensor.lidar.ray_cast_semantic')
        # set attribute based on the configuration
        blueprint.set_attribute('upper_fov', str(config['upper_fov']))
        blueprint.set_attribute('lower_fov', str(config['lower_fov']))
        blueprint.set_attribute('channels', str(config['channels']))
        blueprint.set_attribute('range', str(config['range']))
        blueprint.set_attribute(
            'points_per_second', str(
                config['points_per_second']))
        blueprint.set_attribute(
            'rotation_frequency', str(
                config['rotation_frequency']))


        relative_position = config['relative_pose']
        spawn_point = self.spawn_point_estimation(relative_position,
                                                  global_position)
        self.name = 'semantic_lidar' + str(relative_position)
        print(self.name)
        self.thresh = config['thresh']

        if vehicle is not None:
            self.sensor = world.spawn_actor(
                blueprint, spawn_point, attach_to=vehicle)
        else:
            self.sensor = world.spawn_actor(blueprint, spawn_point)

        # lidar data
        self.points = None
        self.obj_idx = None
        self.obj_tag = None

        self.timestamp = None
        self.frame = 0

        weak_self = weakref.ref(self)
        self.sensor.listen(
            lambda event: SemanticLidar._on_data_event(
                weak_self, event))

    @staticmethod
    def _on_data_event(weak_self, event):
        """Semantic Lidar  method"""
        self = weak_self()
        if not self:
            return

        # shape:(n, 6)
        data = np.frombuffer(event.raw_data, dtype=np.dtype([
            ('x', np.float32), ('y', np.float32), ('z', np.float32),
            ('CosAngle', np.float32), ('ObjIdx', np.uint32),
            ('ObjTag', np.uint32)]))

        # (x, y, z, intensity)
        self.points = np.array([data['x'], data['y'], data['z']]).T
        self.obj_tag = np.array(data['ObjTag'])
        self.obj_idx = np.array(data['ObjIdx'])

        self.data = data
        self.frame = event.frame
        self.timestamp = event.timestamp

    @staticmethod
    def spawn_point_estimation(relative_position, global_position):

        pitch = 0
        carla_location = carla.Location(x=0, y=0, z=0)

        if global_position is not None:
            carla_location = carla.Location(
                x=global_position[0],
                y=global_position[1],
                z=global_position[2])
            pitch = -35

        if relative_position == 'left': #2

            carla_location = carla.Location(x=carla_location.x + 0.0,
                                            y=carla_location.y + 6.3,
                                            z=carla_location.z + 1.8)
            yaw = 100

        elif relative_position == 'backfirst': #1
            carla_location = carla.Location(x=carla_location.x + 8.5, #11.0 8.5
                                            y=carla_location.y,
                                            z=carla_location.z + 1.0)
            yaw = 180

        elif relative_position == 'frontlast': #4
            carla_location = carla.Location(x=carla_location.x - 8.5, #-9.5
                                            y=carla_location.y,
                                            z=carla_location.z + 1.5)
            yaw = 0



        elif relative_position == 'right':  # 1
            carla_location = carla.Location(x=carla_location.x +0.0,
                                            y=carla_location.y- 6.3,
                                            z=carla_location.z + 1.8)
            yaw = -100



        carla_rotation = carla.Rotation(roll=0, yaw=yaw, pitch=pitch)
        spawn_point = carla.Transform(carla_location, carla_rotation)

        return spawn_point

    def tick(self):
        while self.obj_idx is None or self.obj_tag is None or \
                self.obj_idx.shape[0] != self.obj_tag.shape[0]:
            continue

        # label 10 is the vehicle
        vehicle_idx = self.obj_idx[self.obj_tag == 10]
        # each individual instance id
        vehicle_unique_id = list(np.unique(vehicle_idx))
        vehicle_id_filter = []

        for veh_id in vehicle_unique_id:
            if vehicle_idx[vehicle_idx == veh_id].shape[0] > self.thresh:
                vehicle_id_filter.append(veh_id)

        # these are the ids that are visible
        return vehicle_id_filter



    def data_extend(self, points, obj_tag):
        self.points.extend(points)
        self.obj_tag.extend(obj_tag)


# 第四个字母 U 表示第四个属性的数据类型为无符号整数（Unsigned Integer）。这是点云的第四个属性的数据类型，通常用于表示颜色信息，例如RGB颜色值。
    def data_dump_back_first(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:  # self.points is not None:
            # 创建保存数据的目录（如果不存在）
            os.makedirs(output_root, exist_ok=True)
            # 构造保存文件的路径
            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_point.pcd')
            # if sensor_name =="lidarfront":
            # 写入点云数据
            # 将点云数据保存为pcd文件
            save_label_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_label.json')
            curr_label_dict = {'labels': []}
            with open(save_path, 'w') as file:
                # 写入pcd文件头部
                file.write("# .PCD v0.7 - Point Cloud Data file format\n")
                file.write("VERSION 0.7\n")
                file.write("FIELDS x y z rgb\n")
                file.write("SIZE 4 4 4 4\n")
                file.write("TYPE F F F I\n")
                file.write("COUNT 1 1 1 1\n")
                file.write("WIDTH {}\n".format(len(self.points)))
                file.write("HEIGHT 1\n")
                file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
                file.write("POINTS {}\n".format(len(self.points)))
                file.write("DATA ascii\n")
                for point, tag in zip(self.points, self.obj_tag):
                    x, y, z = point
                    # 将点坐标和tag写入文件
                    curr_label_dict['labels'].append(int(tag))
                    file.write("{} {} {} {}\n".format(-x+9.0, -y, z-0.89, tag)) # -x+11.5 9.0
            with open(save_label_path, 'w') as json_file:
                json.dump(curr_label_dict, json_file)
            print(f'Saved Semantic Lidar data to {save_path}')

    def data_dump_left(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:#self.points is not None:
            # 创建保存数据的目录（如果不存在）
            os.makedirs(output_root, exist_ok=True)
            # 构造保存文件的路径
            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_point.pcd')
            # if sensor_name =="lidarfront":
            # 写入点云数据
    # 将点云数据保存为pcd文件
            save_label_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_label.json')
            curr_label_dict = {'labels': []}
            with open(save_path, 'w') as file:
                # 写入pcd文件头部
                file.write("# .PCD v0.7 - Point Cloud Data file format\n")
                file.write("VERSION 0.7\n")
                file.write("FIELDS x y z rgb\n")
                file.write("SIZE 4 4 4 4\n")
                file.write("TYPE F F F I\n")
                file.write("COUNT 1 1 1 1\n")
                file.write("WIDTH {}\n".format(len(self.points)))
                file.write("HEIGHT 1\n")
                file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
                file.write("POINTS {}\n".format(len(self.points)))
                file.write("DATA ascii\n")
            #     for point, tag in zip(self.points, self.obj_tag):
            #         x, y, z = point
            #         # 将点坐标和tag写入文件
            #         file.write("{} {} {} {}\n".format(x+3.0, y, z-0.89, tag))
            #
            # print(f'Saved Semantic Lidar data to {save_path}')

                # 定义旋转角度（100度）
                angle = np.radians(100)

                # 定义旋转矩阵
                rotation_matrix = np.array([
                    [np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1]
                ])

                # 执行点云旋转
                rotated_point_cloud = np.dot(self.points, rotation_matrix.T)

                for point, tag in zip(rotated_point_cloud, self.obj_tag):
                    x, y, z = point
                    # 将点坐标和tag写入文件
                    curr_label_dict['labels'].append(int(tag))
                    file.write("{} {} {} {}\n".format(x + 0.49, y+6.3, z - 0.099, tag))
                    # 0.49 = 50.034358978271484 - 49.54359817504883
                    # 0.315 = 139.88629150390625-  139.5711669921875
                    # -0.099 = 1.8329250812530518 - 1.9321409463882446
            with open(save_label_path, 'w') as json_file:
                json.dump(curr_label_dict, json_file)
            print(f'Saved Semantic Lidar data to {save_path}')

    def data_dump_right(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:  # self.points is not None:
            # 创建保存数据的目录（如果不存在）
            os.makedirs(output_root, exist_ok=True)
            # 构造保存文件的路径
            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_point.pcd')
            # if sensor_name =="lidarfront":
            # 写入点云数据
            # 将点云数据保存为pcd文件
            save_label_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_label.json')
            curr_label_dict = {'labels': []}
            with open(save_path, 'w') as file:
                # 写入pcd文件头部
                file.write("# .PCD v0.7 - Point Cloud Data file format\n")
                file.write("VERSION 0.7\n")
                file.write("FIELDS x y z rgb\n")
                file.write("SIZE 4 4 4 4\n")
                file.write("TYPE F F F I\n")
                file.write("COUNT 1 1 1 1\n")
                file.write("WIDTH {}\n".format(len(self.points)))
                file.write("HEIGHT 1\n")
                file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
                file.write("POINTS {}\n".format(len(self.points)))
                file.write("DATA ascii\n")
                #     for point, tag in zip(self.points, self.obj_tag):
                #         x, y, z = point
                #         # 将点坐标和tag写入文件
                #         file.write("{} {} {} {}\n".format(x+3.0, y, z-0.89, tag))
                #
                # print(f'Saved Semantic Lidar data to {save_path}')

                # 定义旋转角度（100度）
                angle = np.radians(-100)

                # 定义旋转矩阵
                rotation_matrix = np.array([
                    [np.cos(angle), -np.sin(angle), 0],
                    [np.sin(angle), np.cos(angle), 0],
                    [0, 0, 1]
                ])

                # 执行点云旋转
                rotated_point_cloud = np.dot(self.points, rotation_matrix.T)

                for point, tag in zip(rotated_point_cloud, self.obj_tag):
                    x, y, z = point
                    # 将点坐标和tag写入文件
                    curr_label_dict['labels'].append(int(tag))
                    file.write("{} {} {} {}\n".format(x + 0.49, y - 6.3, z - 0.099, tag))
                    # 0.49 = 50.034358978271484 - 49.54359817504883
                    # 0.315 = 139.88629150390625-  139.5711669921875
                    # -0.099 = 1.8329250812530518 - 1.9321409463882446
            with open(save_label_path, 'w') as json_file:
                json.dump(curr_label_dict, json_file)
            print(f'Saved Semantic Lidar data to {save_path}')

    def data_dump_front_last(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:  # self.points is not None:
            # 创建保存数据的目录（如果不存在）
            os.makedirs(output_root, exist_ok=True)
            # 构造保存文件的路径
            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_point.pcd')
            # if sensor_name =="lidarfront":
            # 写入点云数据
            # 将点云数据保存为pcd文件
            save_label_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}_label.json')
            curr_label_dict = {'labels': []}
            with open(save_path, 'w') as file:
                # 写入pcd文件头部
                file.write("# .PCD v0.7 - Point Cloud Data file format\n")
                file.write("VERSION 0.7\n")
                file.write("FIELDS x y z rgb\n")
                file.write("SIZE 4 4 4 4\n")
                file.write("TYPE F F F I\n")
                file.write("COUNT 1 1 1 1\n")
                file.write("WIDTH {}\n".format(len(self.points)))
                file.write("HEIGHT 1\n")
                file.write("VIEWPOINT 0 0 0 1 0 0 0\n")
                file.write("POINTS {}\n".format(len(self.points)))
                file.write("DATA ascii\n")
                for point, tag in zip(self.points, self.obj_tag):
                    x, y, z = point
                    # 将点坐标和tag写入文件
                    curr_label_dict['labels'].append(int(tag))
                    file.write("{} {} {} {}\n".format(x -8.0, y, z - 0.4, tag)) # -9.0
            with open(save_label_path, 'w') as json_file:
                json.dump(curr_label_dict, json_file)

            print(f'Saved Semantic Lidar data to {save_path}')
        else:
            print('No Semantic Lidar data to save.')
