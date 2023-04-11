import json
import re
import traceback

import jsonpath
import requests

from common.logging_util import logs, error_log
from common.yaml_util import write_extract_yaml


class RequestsUtil:
    session = requests.session()

    # 1.处理基础路径
    def __init__(self, obj):
        self.obj = obj

    # 2.替换值
    def replace_value(self, data):
        if data:
            data_type = type(data)
            # 判断数据类型，转换为string
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.dumps(data)
            else:
                str_data = str(data)
            # 替换
            for cs in range(1, str_data.count('${') + 1):
                start_index = str_data.index('${')
                end_index = str_data.index('}', start_index)
                old_value = str_data[start_index:end_index + 1]
                # 提取方法名
                func_name = old_value[2:old_value.index('(')]
                # 提取参数
                args_value1 = old_value[old_value.index('(') + 1:old_value.index(')')]
                if args_value1 != "":
                    # 分割
                    args_value2 = args_value1.split(',')
                    # 通过反射取新的值
                    new_value = getattr(self.obj, func_name)(*args_value2)
                else:
                    new_value = getattr(self.obj, func_name)()
                if isinstance(new_value, int) or isinstance(new_value, float):
                    str_data = str_data.replace(old_value, str(new_value))
                else:
                    str_data = str_data.replace(old_value, str(new_value))
                    # 还原数据类型
            if isinstance(data, dict) or isinstance(data, list):
                data = json.loads(str_data)
            else:
                data = data_type(str_data)
        return data

    # 规范yaml的测试用例
    def standard_yaml(self, cassinfo):
        try:
            logs("----------------接口测试开始--------------------")
            cassinfo_keys = cassinfo.keys()
            if 'base_url' in cassinfo_keys and 'name' in cassinfo_keys and 'request' in cassinfo_keys and 'validate' in cassinfo_keys:
                request_keys = cassinfo['request'].keys()
                if 'method' in request_keys and 'url' in request_keys:
                    # 发送请求
                    name = cassinfo['name']
                    base_url = cassinfo.pop('base_url')
                    method = cassinfo['request'].pop('method')
                    url = cassinfo['request'].pop('url')
                    logs("接口名称:%s" % name)
                    res = self.send_request(method, base_url + url, **cassinfo['request'])
                    # 接口关联
                    return_text = res.text
                    return_code = res.status_code
                    return_json = ''
                    request_json = cassinfo["request"]["json"]
                    try:
                        return_json = res.json()
                    except Exception as e:
                        logs("返回结果不是json格式，不能使用jsonpath")
                    if 'extract' in cassinfo_keys:
                        for key, value in cassinfo['extract'].items():
                            if '(.*?)' in value or '(.+?)' in value:
                                zz_value = re.search(value, return_text)
                                if zz_value:
                                    extract_value = {key: zz_value.group(1)}
                                    write_extract_yaml(extract_value)
                            else:
                                js_value1 = jsonpath.jsonpath(return_json, value)
                                js_value2 = jsonpath.jsonpath(request_json, value)
                                if js_value1:
                                    extract_value = {key: js_value1[0]}
                                    write_extract_yaml(extract_value)
                                elif js_value2:
                                    extract_value = {key: js_value2[0]}
                                    extract_value2 = self.replace_value(extract_value)
                                    write_extract_yaml(extract_value2)
                    # 断言
                    yq_result = cassinfo['validate']
                    sj_result = return_json
                    self.assert_result(yq_result, sj_result, return_code)
                    return res
                else:
                    error_log('判断request下的二级关键字：method、url')
            else:
                error_log('判断一级关键字是否有base_url、name、request、validate')
        except Exception as e:
            error_log('规范yaml的standard_yaml方法异常')

    # 断言判断
    def assert_result(self, yq_result, sj_result, return_code):
        try:
            all_flag = 0
            for yq in yq_result:
                for key, value in yq.items():
                    if key == 'equals':
                        flag = self.equals_assert(value, sj_result, return_code)
                        all_flag = all_flag + flag
                    elif key == 'contains':
                        flag = self.contains_assert(value, sj_result)
                        all_flag = all_flag + flag
                    else:
                        logs("暂时不支持此断言")
            logs("预期结果:%s" % yq_result)
            logs("实际结果:%s" % json.loads(json.dumps(sj_result).replace(r'\\', '\\')))
            logs("接口测试成功")
            logs("----------------接口测试结束--------------------\n")
            assert all_flag == 0
        except Exception as e:
            logs("接口测试失败！！！")
            logs("----------------接口测试结束--------------------\n")
            error_log("断言判断的assert_result方法异常：%s" % str(traceback.format_exc()))

    # 相等断言
    def equals_assert(self, value, sj_result, return_code):
        flag = 0
        for assert_key, assert_value in value.items():
            if assert_key == 'status_code':
                if assert_value != return_code:
                    flag += 1
                    error_log("断言失败：Status Codee为：%s" % assert_value)
            else:
                lists = jsonpath.jsonpath(sj_result, '$..%s' % assert_key)
                if lists:
                    if assert_value not in lists:
                        flag = flag + 1
                        error_log('断言失败' + assert_key + '不等于' + str(assert_value))
                else:
                    flag = flag + 1
                    error_log('断言失败：返回的结果中不存在：' + assert_key)

        return flag

    # 包含断言
    def contains_assert(self, value, sj_result):
        flag = 0
        if str(value) not in str(sj_result):
            flag = flag + 1
            error_log('断言失败，返回的结果中不包含' + str(value))

        return flag

    # 统一请求封装
    def send_request(self, method, url, **kwargs):
        try:
            method = str(method).lower()
            url = self.replace_value(url)
            for key, value in kwargs.items():
                if key in ['params', 'data', 'json', 'headers']:
                    kwargs[key] = self.replace_value(value)
                elif key == 'files':
                    for file_key, file_path in value.items():
                        value[file_key] = open(file_path, 'rb')
            logs("请求方式:%s" % method)
            logs("请求路径:%s" % url)
            if "params" in kwargs.keys():
                logs("请求params参数:%s" % kwargs["params"])
            elif "data" in kwargs.keys():
                logs("请求data参数:%s" % kwargs["data"])
            elif "json" in kwargs.keys():
                logs("请求json参数:%s" % kwargs["json"])

            elif "files" in kwargs.keys():
                logs("files文件上传:%s" % kwargs['files'])

            if 'headers' in kwargs.keys():
                logs("请求头:%s" % kwargs['headers'])
            # 处理请求方法
            res = RequestsUtil.session.request(method, url, **kwargs)
            return res
        except Exception as e:
            error_log("统一请求封装的send_request方法异常：%s" % str(traceback.format_exc()))
