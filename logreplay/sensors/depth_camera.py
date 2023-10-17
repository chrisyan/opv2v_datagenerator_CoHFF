# -*- coding: utf-8 -*-
"""
CARLA Semantic Camera Sensor
"""
# Author: Runsheng Xu <rxx3386@ucla.edu>
# License: TDG-Attribution-NonCommercial-NoDistrib
import os.path
import weakref

import carla
import cv2
import numpy as np

from opencood.hypes_yaml.yaml_utils import save_yaml_wo_overwriting
from logreplay.sensors.utils import get_camera_intrinsic
from logreplay.sensors.base_sensor import BaseSensor


class DepthCamera(BaseSensor):
    """
    Depth camera.

    Parameters
    ----------
    vehicle : carla.Vehicle
        The carla.Vehicle, this is for cav.

    world : carla.World
        The carla world object, this is for rsu.

    config : dict
        depth camera configuration.

    global_position : list
        Global position of the infrastructure, [x, y, z]

    Attributes
    ----------
    image : np.ndarray
        Current received rgb image.
    sensor : carla.sensor
        The carla sensor that mounts at the vehicle.

    """

    def __init__(self, agent_id, vehicle, world, config, global_position):
        super().__init__(agent_id, vehicle, world, config, global_position)
        if vehicle is not None:
            world = vehicle.get_world()

        self.agent_id = agent_id
        self.name = 'depth_camera'

        blueprint = world.get_blueprint_library(). \
            find('sensor.camera.depth')
        blueprint.set_attribute('fov', str(config['fov']))
        blueprint.set_attribute('image_size_x', str(config['image_size_x']))
        blueprint.set_attribute('image_size_y', str(config['image_size_y']))
        self.height = config['height']
#        self.visualize = config['visualize']

        spawn_point = self.spawn_point_estimation(global_position)

        if vehicle is not None:
            self.sensor = world.spawn_actor(
                blueprint, spawn_point, attach_to=vehicle)
        else:
            self.sensor = world.spawn_actor(blueprint, spawn_point)

        self.image = None
        self.depth_image = None # initialize a depth_image

        self.timstamp = None
        self.frame = 0
        weak_self = weakref.ref(self)

        self.sensor.listen(
            lambda event: DepthCamera._on_rgb_image_event(
                weak_self, event))

        # self.sensor.listen(
        #     lambda image: image.save_to_disk('tutorial/new_depth_output/%.6d.jpg' % image.frame,carla.ColorConverter.LogarithmicDepth))

        # camera attributes
        self.image_width = int(self.sensor.attributes['image_size_x'])
        self.image_height = int(self.sensor.attributes['image_size_y'])

    def spawn_point_estimation(self, global_position):

        pitch = 0
        carla_location = carla.Location(x=3, y=0, z=self.height)

        if global_position is not None:
            carla_location = carla.Location(
                x=global_position[0],
                y=global_position[1],
                z=self.height)

        carla_rotation = carla.Rotation(roll=0, yaw=0, pitch=pitch)
        spawn_point = carla.Transform(carla_location, carla_rotation)

        return spawn_point


    def decode_depth_image(self, bgr_image):
        """
        将深度数据解码为以米为单位的深度图像

        Parameters
        ----------
        bgr_image : np.ndarray
            BGR image
        """
        # 解码深度值
        r_channel = bgr_image[:, :, 0]
        g_channel = bgr_image[:, :, 1]
        b_channel = bgr_image[:, :, 2]
        depth_image = (r_channel + g_channel * 256 + b_channel * 256 * 256) / (256 * 256 * 256 - 1)
        depth_image = 1000 * depth_image  # 转换为以米为单位的深度值

        return depth_image


    # def decode_depth_image(self, depth_image):
    #
    #     # 将深度值从以米为单位转换为可视化图像
    #     normalized = depth_image / 1000  # 以米为单位的深度
    #     depth_image_vis = (normalized * 256 * 256 * 256 - 1).astype(np.uint32)
    #     r_channel = (depth_image_vis % 256).astype(np.uint8)
    #     g_channel = ((depth_image_vis // 256) % 256).astype(np.uint8)
    #     b_channel = ((depth_image_vis // (256 * 256)) % 256).astype(np.uint8)
    #
    #     depth_image_vis = cv2.merge([b_channel, g_channel, r_channel])
    #
    #     return depth_image_vis
    array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))

    # image is rgba format

    array = np.reshape(array, (sensor_data.height, sensor_data.width, 4))

    array = array[:, :, :3]

    self.sensor_queue_dict[sensor_name].put((sensor_data.frame, array))


def add_default_sensor(self, world):
    self.add_sensor('seg_cam', 'sensor.camera.semantic_segmentation', world)

    self.add_sensor('dep_cam', 'sensor.camera.depth', world)


def listen(self):
    self.sensor_dict['seg_cam'].listen(lambda image: self.sensor_callback(image, 'seg_cam'))

    self.sensor_dict['dep_cam'].listen(lambda image: self.sensor_callback(image, 'dep_cam'))


def sensor_callback(self, sensor_data, sensor_name):
    if sensor_name == 'seg_cam':
        sensor_data.convert(carla.ColorConverter.CityScapesPalette)

    # sensor_data.convert(carla.ColorConverter.LogarithmicDepth)

    array = np.frombuffer(sensor_data.raw_data, dtype=np.dtype("uint8"))

    # image is rgba format

    array = np.reshape(array, (sensor_data.height, sensor_data.width, 4))

    array = array[:, :, :3]

    self.sensor_queue_dict[sensor_name].put((sensor_data.frame, array))


    @staticmethod
    def _on_rgb_image_event(weak_self, event):
        """CAMERA  method"""
        self = weak_self()
        if not self:
            return
        #image = np.array(event.raw_data)
        image = event.raw_data
        print("self.image", self.image)


        image = carla.Image(image)

        image.save_to_disk('testtutorial/new_depth_output/%.6d.jpg' % image.frame,
                                         carla.ColorConverter.LogarithmicDepth)


        #image = image.reshape((self.image_height, self.image_width, 4))
        # we need to remove the alpha channel
        #image = image[:, :, :3]

        # self.image is the dumped data
        #self.image = np.array(self.labels_to_array(image), dtype=np.int)
        # self.vis_image = \
        #     cv2.cvtColor(self.labels_to_cityscapes_palette(self.image),
        #                  cv2.COLOR_BGR2RGB)

       # self.depth_image = self.decode_depth_image(image)
        # print("image: ", self.depth_image)

        self.frame = event.frame
        self.timestamp = event.timestamp

    # def visualize_data(self):
    #     if self.visualize:
    #         while not hasattr(self, 'vis_image') or self.vis_image is None:
    #             continue
    #         cv2.imshow('bev seg camera agent %s' % self.agent_id,
    #                    self.vis_image)
    #         cv2.waitKey(1)

    def data_dump_depth_head(self, output_root, cur_timestamp, sensor_name):
        print("!!!!!!!!!")
        # while not hasattr(self, 'vis_image') or self.vis_image is None:
        #     continue
        # # dump visualization
        # output_vis_name = os.path.join(output_root,
        #                                cur_timestamp + '_bev_sem_vis.png')
        # cv2.imwrite(output_vis_name, self.vis_image)
        #
        # # dump the label
        # output_label_name = os.path.join(output_root,
        #                                  cur_timestamp + '_bev_sem_label.png')
        # cv2.imwrite(output_label_name, self.image)

        # dump depth image
        output_depth_name = os.path.join(output_root,
                                         cur_timestamp + '_depth_image.png')

        # print("self.depth_image", self.depth_image)
        # print("depth_image shape before ", self.depth_image.shape)

        #depth_image = self.decode_depth_image(self.image)  # 解码深度图像
        #print("depth_image", depth_image)
        # print("depth_image shape after", self.depth_image.shape)

        # if self.depth_image is not None:
        #     cv2.imwrite(output_depth_name, self.depth_image)
        # else:
        #     print("Depth image is empty or None")

       # self.image.save_to_disk(output_depth_name, carla.Depth)




        # dump the yaml
        # save_yaml_name = os.path.join(output_root,
        #                               cur_timestamp +
        #                               '_additional.yaml')
        # # intrinsic
        # camera_intrinsic = get_camera_intrinsic(self.sensor)
        # # pose under world coordinate system
        # camera_transformation = self.sensor.get_transform()
        # cords = [camera_transformation.location.x,
        #          camera_transformation.location.y,
        #          camera_transformation.location.z,
        #          camera_transformation.rotation.roll,
        #          camera_transformation.rotation.yaw,
        #          camera_transformation.rotation.pitch]
        #
        # bev_sem_cam_info = {'bev_sem_cam':
        #                         {'intrinsic': camera_intrinsic,
        #                          'cords': cords
        #                          }}
        # save_yaml_wo_overwriting(bev_sem_cam_info,
        #                          save_yaml_name)
