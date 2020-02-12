import os
from utils.YamlUtil import YamlReader


# 获取当前文件的绝对路径
current = os.path.abspath(__file__)
# print(current)
d = os.path.dirname(current)
# print(d)
BASE_DIR = os.path.dirname(os.path.dirname(current))
# print(BASE_DIR)

# 定义config目录的路径
_config_path = BASE_DIR + os.sep + "config"
# print(_config_path)

# 定义data目录的路径
_data_path = BASE_DIR + os.sep + "data"
# print(_data_path)

# 定义conf.yml文件路径
_config_file = _config_path + os.sep + "conf.yml"
# print(_config_file)

# 定义logs目录路径
_log_path = BASE_DIR + os.sep + "logs"

# 定义db_conf.yml文件路径
_db_config_file = _config_path + os.sep + "db_conf.yml"

# 定义report目录的路径
_report_path = BASE_DIR + os.sep + "report"
# print(_report_path)


def get_report_path():
    """
    获取report绝对路径
    :return:
    """

    return _report_path


def get_config_path():

    return _config_path


def get_config_file():

    return _config_file


def get_data_path():

    return _data_path


def get_logs_path():

    return _log_path


def get_db_config_file():

    return _db_config_file


# 读取配置文件
class ConfigYaml:

    # yaml读取配置文件
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()

    def get_config_url(self):
        return self.config["BASE"]["test"]["url"]

    def get_excel_file(self):
        """
        获取Excel测试用例 文件名称
        :return:
        """
        return self.config["BASE"]["test"]["case_file"]

    def get_excel_sheet(self):
        """
        获取Excel测试用例 sheet名称
        :return:
        """
        return self.config["BASE"]["test"]["case_sheet"]

    def get_config_log_level(self):
        """
        获取日志级别
        :return:
        """
        return self.config["BASE"]["log_level"]

    def get_config_log_extension(self):
        """
        获取文件拓展名
        :return:
        """
        return self.config["BASE"]["log_extension"]

    def get_db_config_info(self, db_alias):
        """
        根据db_alias获取该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.db_config[db_alias]

    def get_email_info(self):
        """
        获取邮件配置相关信息
        :return:
        """
        return self.config["email"]


if __name__ == '__main__':
    conf_read = ConfigYaml()
    # print(conf_read.get_config_url())
    # print(conf_read.get_config_log_level())
    # print(conf_read.get_config_log_extension())
    # print(conf_read.get_db_config_info("db_1"))
    # print(conf_read.get_db_config_info("db_2"))
    # print(conf_read.get_db_config_info("db_3"))
    # print(conf_read.get_excel_file())
    # print(conf_read.get_excel_sheet())
    print(conf_read.get_email_info())
