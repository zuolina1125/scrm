import os
import random

import yaml


class Randoms:
    # 获得随机数
    def get_random_number(self, min, max):
        rm = random.randint(int(min), int(max))
        return rm

    # 读取config yaml的值
    def read_config(self, one_node, two_node):
        with open(os.getcwd() + "/config/config.yaml", encoding='utf-8')as f:
            value = yaml.load(f, Loader=yaml.FullLoader)
            return value[one_node][two_node]

            # 读取extract yaml中的值
    def read_extract_data(self, key):
        with open(os.getcwd() + '/config/extract.yaml', encoding='utf-8') as f:
            value = yaml.load(f, Loader=yaml.FullLoader)
            return value[key]

