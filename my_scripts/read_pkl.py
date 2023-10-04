import pickle

# 打开.pkl文件，以二进制读取模式打开
with open('semantic_lidar_data_000663.pkl', 'rb') as file:
    loaded_data = pickle.load(file)

# 现在，loaded_data变量包含了从.pkl文件中读取的数据
# 你可以使用loaded_data进行后续处理
print(loaded_data)