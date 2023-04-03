import json
import os

# 数据驱动，读取测试用例的yaml文件
import traceback

import yaml

from common.yaml_util import read_data_yaml


def read_testcase_yaml(yaml_path):
    try:
        with open(os.getcwd() + yaml_path, encoding='utf-8') as f:
            caseinfo = yaml.load(f, Loader=yaml.FullLoader)
            if len(caseinfo) >= 2:
                return caseinfo
            else:
                if 'parameterize' in dict(*caseinfo).keys():
                    new_caseinfo = ddt(*caseinfo)
                    return new_caseinfo
                else:
                    return caseinfo

    except Exception as e:
        print("读取测试用例read_testcase_yaml方法异常：%s" % str(traceback.format_exc()))


def ddt(caseinfo):
    try:
        if 'parameterize' in caseinfo.keys():
            caseinfo_str = json.dumps(caseinfo)
            for param_key, param_value in caseinfo['parameterize'].items():
                key_list = param_key.split("-")
                # 规范yaml数据写法
                length_flag = True
                data_list = read_data_yaml(param_value)
                for data in data_list:
                    if len(data) != len(key_list):
                        length_flag = False
                        break
                # 替换值
                new_caseinfo = []
                if length_flag:
                    for x in range(1, len(data_list)):
                        temp_caseinfo = caseinfo_str
                        for y in range(0, len(data_list[x])):
                            if data_list[0][y] in key_list:
                                if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                                    temp_caseinfo = temp_caseinfo.replace('"$ddt{' + data_list[0][y] + '}"',
                                                                          str(data_list[x][y]))
                                else:
                                    temp_caseinfo = temp_caseinfo.replace("$ddt{" + data_list[0][y] + "}",
                                                                          str(data_list[x][y]))

                        new_caseinfo.append(json.loads(temp_caseinfo))
                return new_caseinfo

        else:
            return caseinfo
    except Exception as e:
        print("数据驱动ddt方法异常：%s" % str(traceback.format_exc()))



