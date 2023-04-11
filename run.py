import os
import time

import pytest

from common.parameterize_util import read_testcase_yaml

if __name__ == '__main__':
    pytest.main()
    time.sleep(4)
    # os.system('allure generate ./temps -o ./reports --clean')
    # print(read_testcase_yaml('/testcase/test_scrm1_1/test_login.yaml'))



