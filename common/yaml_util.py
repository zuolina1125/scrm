# 读取测试用例的yaml 文件
import os

import yaml


# 读取测试用例的yaml 文件
# def read_testcase_yaml(yaml_path):
#     with open(os.getcwd() + yaml_path, encoding="utf-8") as f:
#         caseinfo = yaml.load(f, Loader=yaml.FullLoader)
#         print(caseinfo)
#         return caseinfo


# 写入extract yaml文件
def write_extract_yaml(data):
    with open(os.getcwd() + "/config/extract.yaml", encoding="utf-8", mode="a+") as f:
        yaml.dump(data=data, stream=f, allow_unicode=True)


# 读取extract yaml文件
def read_extract_yaml(key):
    with open(os.getcwd() + "/config/extract.yaml", encoding="utf-8") as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value[key]


# 清空extract yaml文件
def clean_extract_yaml():
    with open(os.getcwd() + "/config/extract.yaml", encoding="utf-8", mode='w') as f:
        f.truncate()


# 读取config yaml文件
def read_config_yaml(one_node, two_node):
    with open(os.getcwd() + '/config/config.yaml', encoding='utf-8') as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value[one_node][two_node]


# 读取ddt yaml数据
def read_data_yaml(yaml_path):
    with open(os.getcwd() + yaml_path, encoding='utf-8') as f:
        value = yaml.load(f, Loader=yaml.FullLoader)
        return value


