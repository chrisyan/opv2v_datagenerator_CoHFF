import os
from collections import OrderedDict

from opencood.hypes_yaml.yaml_utils import load_yaml
from logreplay.scenario.scene_manager import SceneManager


class ScenariosManager:
    """
    Format all scenes in a structured way.

    Parameters
    ----------
    scenario_params: dict
        Overall parameters for the replayed scenes.

    Attributes
    ----------

    """

    def __init__(self, scenario_params):
        # this defines carla world sync mode, weather, town name, and seed.
        self.scene_params = scenario_params

        # e.g. /opv2v/data/train
        root_dir = self.scene_params['root_dir']

        # first load all paths of different scenarios
        scenario_folders = sorted([os.path.join(root_dir, x)
                                   for x in os.listdir(root_dir) if
                                   os.path.isdir(os.path.join(root_dir, x))])
        self.scenario_database = OrderedDict()

        # loop over all scenarios
        for (i, scenario_folder) in enumerate(scenario_folders):
            scene_name = os.path.split(scenario_folder)[-1]
            self.scenario_database.update({scene_name: OrderedDict()})

            # load the collection yaml file
            protocol_yml = [x for x in os.listdir(scenario_folder)
                            if x.endswith('.yaml')]
            collection_params = load_yaml(os.path.join(scenario_folder,
                                                       protocol_yml[0]))

            # create the corresponding scene manager
            cur_sg = SceneManager(scenario_folder,
                                  scene_name,
                                  collection_params,
                                  scenario_params)
            self.scenario_database[scene_name].update({'scene_manager':
                                                       cur_sg})

    def tick(self):
        """
        Tick for every scene manager to do the log replay.
        """
        for scene_name, scene_content in self.scenario_database.items():
            print('log replay %s' % scene_name)
            scene_manager = scene_content['scene_manager']
            run_flag = True

            scene_manager.start_simulator()

            while run_flag:
                run_flag = scene_manager.tick()

            scene_manager.close()


if __name__ == '__main__':
    import time

    start_time = time.time()
    script_start_time = time.ctime(start_time)

    from opencood.hypes_yaml.yaml_utils import load_yaml
    #scene_params = load_yaml('./hypes_yaml/replay.yaml')
    scene_params = load_yaml('./replay.yaml')
    scenarion_manager = ScenariosManager(scenario_params=scene_params)
    scenarion_manager.tick()
    print('test passed')

    end_time = time.time()
    script_end_time = time.ctime(end_time)
    script_run_time = (end_time - start_time)//60

    # 将时间信息保存到以脚本开始时间命名的文本文件
    file_name = f"开始时间_{start_time}.txt"
    with open(file_name, "w") as file:
        file.write(f"脚本开始运行时间: {script_start_time}\n")
        file.write(f"脚本结束运行时间: {script_end_time}\n")
        file.write(f"脚本运行总时间: {script_run_time} min\n")

    print(f"时间信息已保存到文件: {file_name}")

