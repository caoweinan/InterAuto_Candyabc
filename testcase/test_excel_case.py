from config.Conf import ConfigYaml
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
from common import Base
from utils.AssertUtil import AssertUtil
from config import Conf
from common.Base import init_db
import os
import json
import pytest
import allure
import re


# 测试用例文件
case_file = os.path.join(Conf.get_data_path(), ConfigYaml().get_excel_file())
# 测试用例中sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 获取可运行的测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()
# 日志
log = my_log()
# 初始化dataconfig
data_key = ExcelConfig.DataConfig


# 测试用例方法
class TestExcel:

    def run_api(self, url, method, params=None, header=None, cookie=None):
        """
        发送请求api
        :return:
        """
        request = Request()
        # 验证params
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        if str(method).lower() == "get":
            res = request.get(url, json=params, headers=header, cookies=cookie)
        elif str(method).lower() == "post":
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method：%s" % method)
        return res

    def run_pre(self, pre_case):
        # pass
        url = ConfigYaml().get_config_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]

        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)

        res = self.run_api(url, method, params, header, cookie)
        print("前置用例执行：%s" % res)
        return res

    # 初始化信息
    @pytest.mark.parametrize("case", run_list)
    def test_run(self, case):

        url = ConfigYaml().get_config_url() + case[data_key.url]
        print(url)
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_verify = case[data_key.db_verify]

        # 验证前置条件
        if pre_exec:
            # pass
            pre_case = data_init.get_case_pre(pre_exec)
            print("前置条件信息为：%s" % pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies = self.get_correlation(headers, cookies, pre_res)

        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        res = self.run_api(url, method, params, header, cookie)
        print("测试用例执行：%s" % res)

        # allure
        allure.dynamic.feature(sheet_name)
        allure.dynamic.story(case_model)
        allure.dynamic.title(case_id + case_name)
        desc = "<font color='red'>请求URL：</font>{}<Br/>" \
               "<font color='red'>请求类型：</font>{}<Br/>" \
               "<font color='red'>期望结果：</font>{}<Br/>" \
               "<font color='red'>实际结果：</font>{}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)

        # 状态码
        assert_util = AssertUtil()
        assert_util.assert_code(int(res["code"]), int(code))

        # 返回结果内容
        assert_util.assert_in_body(str(res["body"]), str(expect_result))

        # 数据库相关结果验证
        Base.assert_db("db_1", res["body"]["data"], db_verify)

    def get_correlation(self, headers, cookies, pre_res):
        """
        关联
        :param headers:
        :param cookies:
        :param pre_res:
        :return:
        """
        # 验证是否有关联
        headers_para, cookies_para = Base.params_find(headers, cookies)
        if len(headers_para):
            headers_data = pre_res["body"]["data"][headers_para[0]]
            headers = Base.res_sub(headers, headers_data)

        if len(cookies_para):
            cookies_data = pre_res["body"][cookies_para[0]]

            cookies = Base.res_sub(cookies, cookies_data)
        return headers, cookies


if __name__ == '__main__':
    report_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    pytest.main(["-s", "test_excel_case.py", "--alluredir", report_path])
    Base.allure_report(report_path, report_html_path)
    # Base.send_mail(title="接口测试报告结果", content=report_html_path)
