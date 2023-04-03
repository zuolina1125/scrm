import pytest

from common.parameterize_util import read_testcase_yaml
from common.request_util import RequestsUtil

from hotloads.randoms import Randoms


class TestScrm:

    @pytest.mark.parametrize('caseinfo', read_testcase_yaml('/testcase/test_scrm1_1/test_login.yaml'))
    def test_login(self, caseinfo):
        res = RequestsUtil(Randoms()).standard_yaml(caseinfo)
