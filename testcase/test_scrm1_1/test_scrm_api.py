import allure
import pytest
from common.parameterize_util import read_testcase_yaml
from common.request_util import RequestsUtil

from hotloads.randoms import Randoms


@allure.epic("接口自动化平台")
@allure.feature("V1.0")
class TestScrm:

    @allure.story("登录模块")
    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_login.yaml'))
    def test_login(self, caseinfo):
        res = RequestsUtil(Randoms()).standard_yaml(caseinfo)

    @allure.story("创建任务模块")
    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_task_create.yaml'))
    def test_task_create(self, caseinfo):
        RequestsUtil(Randoms()).standard_yaml(caseinfo)

    @allure.story("根据任务名称查询任务，获取任务id")
    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_select_tasklist.yaml'))
    def test_select_tasklist(self, caseinfo):
        RequestsUtil(Randoms()).standard_yaml(caseinfo)

    @allure.story("暂停任务")
    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_task_stop.yaml'))
    def test_task_stop(self, caseinfo):
        RequestsUtil(Randoms()).standard_yaml(caseinfo)

    @allure.story("开启任务")
    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_task_start.yaml'))
    def test_task_start(self, caseinfo):
        RequestsUtil(Randoms()).standard_yaml(caseinfo)

    @allure.story("终止任务")
    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_task_zhongzhi.yaml'))
    def test_task_zhongzhi(self, caseinfo):
        RequestsUtil(Randoms()).standard_yaml(caseinfo)

    @allure.story("删除任务")
    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_task_delete.yaml'))
    def test_task_delete(self, caseinfo):
        RequestsUtil(Randoms()).standard_yaml(caseinfo)


