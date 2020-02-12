from utils.ExcelUtil import ExcelReader
from common.ExcelConfig import DataConfig


class Data:

    def __init__(self, testcase_file, sheet_name):
        self.reader = ExcelReader(testcase_file, sheet_name)
        # print(reader.data())

    def get_run_data(self):
        """
        根据列 是否运行 == y ，获取可执行的测试用例
        :return:
        """
        run_list = list()
        for line in self.reader.data():
            if str(line[DataConfig().is_run]).lower() == "y":
                # print(line)
                run_list.append(line)
        print(run_list)
        return run_list

    def get_case_list(self):
        """
        获取全部的测试用例   list
        :return:
        """
        run_list = [line for line in self.reader.data()]
        return run_list

    def get_case_pre(self, pre):
        """
        根据 前置条件：从全部测试用例中取到对应的测试用例
        :param pre:
        :return:
        """
        run_list = self.get_case_list()
        for line in run_list:
            if pre in dict(line).values():
                return line
        return None
