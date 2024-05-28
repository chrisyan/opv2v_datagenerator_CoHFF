This is the extended data generator based on OpenCOOD (https://github.com/DerrickXuNu/OpenCOOD)

Data generator for Collaborative Semantic Occupancy Prediction with Hybrid Feature Fusion in Connected Automated Vehicles (https://rruisong.github.io/publications/CoHFF/)


By default, data generation with 18 semantic lidars. 
$ python3 scenarios_manager.py

If you collect data with 4 semantic lidars, you need to copy and paste two files from /opv2v_datagenerator_CoHFF/logreplay/sensors/semantic_4/semantic_lidar.py and /opv2v_datagenerator_CoHFF/logreplay/sensors/semantic_4/sensor_manager.py to /opv2v_datagenerator_CoHFF/logreplay/sensors
Then change line 79 from scene_params = load_yaml('./replay_18.yaml') to scene_params = load_yaml('./replay_4.yaml')

