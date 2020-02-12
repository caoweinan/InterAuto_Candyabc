import os
import yaml


class YamlReader:

    # 验证文件是否存在
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("文件不存在，请确认！")
        self._data = None
        self._data_all = None

    # yaml单个文档读取
    def data(self):
        if not self._data:  # self._data不存在则读取
            with open(self.yamlf, "rb") as f:
                self._data = yaml.safe_load(f)
        return self._data

    # yaml多个文档读取
    def data_all(self):
        if not self._data_all:  # self._data不存在则读取
            with open(self.yamlf, "rb") as f:
                self._data_all = list(yaml.safe_load_all(f))
        return self._data_all
