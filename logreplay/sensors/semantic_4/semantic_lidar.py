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

        if relative_position == 'head':
            carla_location = carla.Location(x=carla_location.x +2.5, #2.5
                                            y=carla_location.y,
                                            z=carla_location.z + 1.0)
            yaw = 0 # 0

        elif relative_position == 'front':
            carla_location = carla.Location(x=carla_location.x + 2.5, #2.5
                                            y=carla_location.y,
                                            z=carla_location.z + 1.0)
            yaw = 0 # 0

        elif relative_position == 'right':
            carla_location = carla.Location(x=carla_location.x + 0.0,
                                            y=carla_location.y + 0.3,
                                            z=carla_location.z + 1.8)
            yaw = 0

        elif relative_position == 'left':
            carla_location = carla.Location(x=carla_location.x + 0.0,
                                            y=carla_location.y - 0.3, # -0.3
                                            z=carla_location.z + 1.8)
            yaw = 0


        else:
            carla_location = carla.Location(x=carla_location.x - 2.0,
                                            y=carla_location.y,
                                            z=carla_location.z + 1.5)
            yaw = 0



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

    def data_dump_head(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:#self.points is not None:

            os.makedirs(output_root, exist_ok=True)

            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}.pcd')
            # if sensor_name =="lidarfront":

            with open(save_path, 'w') as file:
   
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

                    file.write("{} {} {} {}\n".format(x + 3.0 +3.5, y, z - 0.89, tag))

            print(f'Saved Semantic Lidar data to {save_path}')

    def data_dump_front(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:#self.points is not None:

            os.makedirs(output_root, exist_ok=True)
 
            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}.pcd')
            # if sensor_name =="lidarfront":

            with open(save_path, 'w') as file:
 
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
  
                    file.write("{} {} {} {}\n".format(x + 3.0, y, z - 0.89, tag))

            print(f'Saved Semantic Lidar data to {save_path}')

    def data_dump_back(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:  # self.points is not None:

            os.makedirs(output_root, exist_ok=True)

            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}.pcd')
            # if sensor_name =="lidarfront":
  
            with open(save_path, 'w') as file:
    
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
           
                    file.write("{} {} {} {}\n".format(x-1.5, y, z-0.4, tag))
            print(f'Saved Semantic Lidar data to {save_path}')

    def data_dump_right(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:  # self.points is not None:

            os.makedirs(output_root, exist_ok=True)

            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}.pcd')
            # if sensor_name =="lidarfront":

            with open(save_path, 'w') as file:
     
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
        
                    file.write("{} {} {} {}\n".format(x + 0.49, y+0.315, z - 0.099, tag))
       
            print(f'Saved Semantic Lidar data to {save_path}')

    def data_dump_left(self, output_root, cur_timestamp, sensor_name):
        '''save semantic lidar as .pcd'''
        if True:  # self.points is not None:

            os.makedirs(output_root, exist_ok=True)

            save_path = os.path.join(output_root, f'semantic_lidar_data_{cur_timestamp}_{sensor_name}.pcd')
            # if sensor_name =="lidarfront":

            with open(save_path, 'w') as file:
 
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
            
                    file.write("{} {} {} {}\n".format(x + 0.51, y - 0.2845, z - 0.099, tag))

 


            print(f'Saved Semantic Lidar data to {save_path}')

