import logging
import datetime
import os
from config import Conf
from config.Conf import ConfigYaml


# 定义日志级别映射
log_l = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}


# 封装log工具类
class Logger:

    # 日志文件名称，Loggername，日志级别
    def __init__(self, log_file, log_name, log_level):
        self.log_file = log_file    # 扩展名
        self.log_name = log_name    # 参数
        self.log_level = log_level  # 配置文件
        # 设置logger名称
        self.logger = logging.getLogger(self.log_name)
        # 设置logger级别
        self.logger.setLevel(log_l[self.log_level])

        # 判断handler是否存在
        if not self.logger.handlers:

            # 创建handler（控制台）
            fh_stream = logging.StreamHandler()
            # 设置日志级别（控制台）
            fh_stream.setLevel(log_l[self.log_level])
            # 定义输出格式（控制台）
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
            fh_stream.setFormatter(formatter)

            # 创建handler（写入文件）
            fh_file = logging.FileHandler(self.log_file)
            # 设置日志级别（写入文件）
            fh_file.setLevel(log_l[self.log_level])
            # 定义输出格式（写入文件）
            fh_file.setFormatter(formatter)

            # 3.6 添加handler（控制台）
            self.logger.addHandler(fh_stream)
            # 3.6 添加handler（写入文件）
            self.logger.addHandler(fh_file)

# log目录
log_path = Conf.get_logs_path()
# 当前时间
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
# 扩展名
log_extension = ConfigYaml().get_config_log_extension()
# 日志文件名称
log_file = os.path.join(log_path, current_time + log_extension)
# print(log_file)

# 日志文件级别
loglevel = ConfigYaml().get_config_log_level()
# print(loglevel)


def my_log(log_name=__file__):

    return Logger(log_file=log_file, log_name=log_name, log_level=loglevel).logger


if __name__ == '__main__':
    my_log().debug("this is a debug")


