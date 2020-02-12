import pytest
import os
from config import Conf
from common import Base

if __name__ == '__main__':

    report_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    pytest.main(["-s", "--alluredir", report_path])
    Base.allure_report(report_path, report_html_path)
    # Base.send_mail(title="接口测试报告结果", content=report_html_path)
