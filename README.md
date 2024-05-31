This is the extended data generator based on OpenCOOD (https://github.com/DerrickXuNu/OpenCOOD)

Data generator for Collaborative Semantic Occupancy Prediction with Hybrid Feature Fusion in Connected Automated Vehicles (https://rruisong.github.io/publications/CoHFF/)

Step 1: download OpenCOOD base
$ git clone https://github.com/DerrickXuNu/OpenCOOD

Step 2: download this data generator
$ git clone https://github.com/chrisyan/opv2v_datagenerator_CoHFF.git

Step 3: If you collect data with 4 semantic lidars, please copy and paste /opv2v_datagenerator_CoHFF/logreplay/hypes_yaml/replay_4.yaml to /OpenCOOD/logreplay/hypes_yaml, copy and paste /opv2v_datagenerator_CoHFF/logreplay/sensors/semantic_4/semantic_lidar.py and /opv2v_datagenerator_CoHFF/logreplay/sensors/semantic_4/sensor_manager.py to /OpenCOOD/logreplay/sensors,

Then change line 73 from scene_params = load_yaml('../hypes_yaml/replay.yaml') to scene_params = load_yaml('../hypes_yaml/replay_4.yaml') in /OpenCOOD/logreplay/scenario/scenarios_manager.py


or Step 4: if you collect data with 18 semantic lidars, please copy and paste /opv2v_datagenerator_CoHFF/logreplay/hypes_yaml/replay_18.yaml to /OpenCOOD/logreplay/hypes_yaml, copy and paste /opv2v_datagenerator_CoHFF/logreplay/sensors/semantic_18/semantic_lidar.py and /opv2v_datagenerator_CoHFF/logreplay/sensors/semantic_18/sensor_manager.py to /OpenCOOD/logreplay/sensors,

Then change line 73 from scene_params = load_yaml('../hypes_yaml/replay.yaml') to scene_params = load_yaml('../hypes_yaml/replay_18.yaml') in /OpenCOOD/logreplay/scenario/scenarios_manager.py


Step 5: collect data by using $ python3 scenarios_manager.py in /OpenCOOD/logreplay/scenario



