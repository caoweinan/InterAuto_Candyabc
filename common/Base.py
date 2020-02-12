from config.Conf import ConfigYaml
from utils.MysqlUtil import Mysql
from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
from utils.EmailUtil import SendEmail
import subprocess
import json
import re


p_data = '\${(.*)}\$'
log = my_log()


def init_db(db_alias):

    # 初始化数据库信息
    db_info = ConfigYaml().get_db_config_info(db_alias)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])

    # 初始化mysql对象
    conn = Mysql(host, user, password, name, charset, port)
    # print(conn)
    return conn


def assert_db(db_name, result, db_verify):
    assert_util = AssertUtil()

    # 数据库相关结果验证
    sql = init_db(db_name)
    # 查询sql
    db_res = sql.fetchone(db_verify)
    log.debug("数据库查询结果：{}".format(str(db_res)))
    # 结果验证
    verify_list = list(dict(db_res).keys())
    for line in verify_list:
        res_line = result[line]
        res_db_line = dict(db_res)[line]
        assert_util.assert_in_body(str(res_line), str(res_db_line))


def json_parse(data):
    """
    格式化字符，转换json
    :param data:
    :return:
    """
    return json.loads(data) if data else data


def res_find(data, pattern_data=p_data):
    """
    查询
    :param data:
    :param pattern_data:
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    return re_res


def res_sub(data, replace, pattern_data=p_data):
    """
    替换
    :param data:
    :param replace:
    :param pattern_data:
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        return re.sub(pattern_data, replace, data)
    return re_res


def params_find(headers, cookies):
    """
    验证请求中是否有${}$
    :param headers:
    :param cookies:
    :return:
    """
    if "${" in headers:
        headers = res_find(headers)
    if "${" in cookies:
        cookies = res_find(cookies)
    return headers, cookies


def allure_report(report_path, report_html):
    """
    生成allure报告
    :param report_path:
    :param report_html:
    :return:
    """
    allure_cmd = "allure generate %s -o %s --clean" % (report_path, report_html)
    log.info("报告地址")
    try:
        subprocess.call(allure_cmd, shell=True)
    except:
        log.debug("执行用例失败，请检查测试环境相关配置")
        raise


def send_mail(report_html_path="", content="", title="测试"):
    """
    发送邮件
    :param report_html_path:
    :param content:
    :param title:
    :return:
    """
    email_info = ConfigYaml().get_email_info()
    smtpserver = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    rece = email_info["receiver"]
    email = SendEmail(
        smtpserver=smtpserver,
        username=username,
        password=password,
        rece=rece,
        title=title,
        content=content,
        file=report_html_path)
    email.send_mail()


if __name__ == '__main__':
    init_db("db_1")
    print(res_find('{"Authorization": "basic ${base64Token}$"}'))
    # print(res_sub('{"Authorization": "basic ${base64Token}$"}', "123"))



