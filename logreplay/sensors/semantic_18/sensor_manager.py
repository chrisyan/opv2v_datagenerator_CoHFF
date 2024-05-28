# -*- coding: utf-8 -*-
"""
Sensor Manager for each cav
"""
# Author: Runsheng Xu <rxx3386@ucla.edu>
# License: TDG-Attribution-NonCommercial-NoDistrib
import importlib
import os
from collections import OrderedDict


class SensorManager:
    """
    The manager controls all sensor data streaming and dumping for each cav.
    todo: rsu not considered yet.
    Parameters
    ----------
    agent_id : str
        The cav's original id.

    vehicle_content : dict
        The content of the cav.

    world : carla.World
        Carla simulation server object.

    config_yaml : dict
        Configurations for the sensor manager.

    output_root : str
        Output directory for data dumping.

    Attributes
    ----------
    sensor_list : list
        A list of sensors to dump/visualize data.
    """
    def __init__(self, agent_id,
                 vehicle_content,
                 world, config_yaml, output_root):

        self.agent_id = agent_id
        self.output_root = output_root
        self.vehicle = vehicle_content['actor']
        self.world = world
        self.sensor_list = []
        # this is used to gather the meta information return from sensors
        self.sensor_meta = OrderedDict()
        print(config_yaml)

        for sensor_content in config_yaml['sensor_list']:
            sensor = None
            sensor_name = sensor_content['name']

            # find the relative path
            sensor_filename = "logreplay.sensors." + sensor_name
            sensor_lib = importlib.import_module(sensor_filename)
            target_sensor_name = sensor_name.replace('_', '')

            # the sensor corresponding class has to have the same
            # name pattern as the file
            for name, cls in sensor_lib.__dict__.items():
                if name.lower() == target_sensor_name.lower():
                    sensor = cls

            assert sensor is not None, 'The sensor class name has to be the' \
                                       'same as the file name. e.g. ' \
                                       'bev_semantic_camera -> ' \
                                       'BevSemanticCamera'
            # todo: rsu is not considered yet
            sensor_instance = sensor(self.agent_id,
                                     self.vehicle,
                                     self.world,
                                     sensor_content['args'],
                                     None)
            self.sensor_list.append(sensor_instance)

    def run_step(self, cur_timestamp):
        for sensor_instance in self.sensor_list:
            sensor_name = sensor_instance.name
            sensor_instance.visualize_data()

            meta_info = sensor_instance.tick()
            self.sensor_meta.update({sensor_name: meta_info})

            # for data dumping
            output_folder = os.path.join(self.output_root,
                                         self.agent_id)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)



            if sensor_name == "semantic_lidarhead":
                sensor_instance.data_dump_head(output_folder,
                                  cur_timestamp, sensor_name)

            elif sensor_name == "semantic_lidarfront1a":
                sensor_instance.data_dump_front1a(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarfront2a":
                sensor_instance.data_dump_front2a(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarfront3a":
                sensor_instance.data_dump_front3a(output_folder,
                                  cur_timestamp, sensor_name)

            elif sensor_name == "semantic_lidarfront1b":
                sensor_instance.data_dump_front1b(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarfront2b":
                sensor_instance.data_dump_front2b(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarfront3b":
                sensor_instance.data_dump_front3b(output_folder,
                                  cur_timestamp, sensor_name)

            elif sensor_name == "semantic_lidarleft1a":
                sensor_instance.data_dump_left1a(output_folder,
                                                cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarleft2a":
                sensor_instance.data_dump_left2a(output_folder,
                                                cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarrighta":
                sensor_instance.data_dump_righta(output_folder,
                                      cur_timestamp, sensor_name)

            elif sensor_name == "semantic_lidarleft1b":
                sensor_instance.data_dump_left1b(output_folder,
                                                cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarleft2b":
                sensor_instance.data_dump_left2b(output_folder,
                                                cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarrightb":
                sensor_instance.data_dump_rightb(output_folder,
                                      cur_timestamp, sensor_name)

            elif sensor_name == "semantic_lidarback1a":
                sensor_instance.data_dump_back1a(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarback2a":
                sensor_instance.data_dump_back2a(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarback3a":
                sensor_instance.data_dump_back3a(output_folder,
                                  cur_timestamp, sensor_name)

            elif sensor_name == "semantic_lidarback1b":
                sensor_instance.data_dump_back1b(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarback2b":
                sensor_instance.data_dump_back2b(output_folder,
                                  cur_timestamp, sensor_name)
            elif sensor_name == "semantic_lidarback3b":
                sensor_instance.data_dump_back3b(output_folder,
                                  cur_timestamp, sensor_name)

            else:
                print("Error!")

    def destroy(self):
        for sensor_instance in self.sensor_list:
            sensor_instance.destroy()

