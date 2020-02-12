import xlrd
import os


class SheetTypeError:
    pass


class ExcelReader:

    def __init__(self, excel_file, sheet_by):
        # 验证文件是否存在
        if os.path.exists(excel_file):
            self.excel_file = excel_file
            self.sheet_by = sheet_by
            self._data = list()
        else:
            raise FileNotFoundError("excel文件不存在，请确认！")

    # 读取sheet的方式：名称、索引
    def data(self):
        if not self._data:
            workbook = xlrd.open_workbook(self.excel_file)
            if type(self.sheet_by) not in [str, int]:
                raise SheetTypeError("请输入int或者str类型")
            elif type(self.sheet_by) == int:
                sheet = workbook.sheet_by_index(self.sheet_by)
            elif type(self.sheet_by) == str:
                sheet = workbook.sheet_by_name(self.sheet_by)

            # 读取sheet内容
            # 获取首行信息
            title = sheet.row_values(0)
            for col in range(1, sheet.nrows):
                col_value = sheet.row_values(col)
                # 每一行分别与首行进行拼接
                self._data.append(dict(zip(title, col_value)))

        return self._data


if __name__ == '__main__':
    reader = ExcelReader("../data/testdata.xlsx", "Candyabc接口测试")
    print(reader.data())

