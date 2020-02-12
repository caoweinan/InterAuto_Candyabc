from utils.LogUtil import my_log
import json


class AssertUtil:

    def __init__(self):
        self.log = my_log("AssertUtil")

    def assert_code(self, code, expected_code):
        """
        验证返回状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            self.log.error("code error, code is %s, expected_code is %s" % (code, expected_code))
            raise

    def assert_body(self, body, expected_body):
        """
        验证返回结果内容相等
        :param body:
        :param expected_body:
        :return:
        """
        try:
            assert body == expected_body
            return True
        except:
            self.log.error("body error, body is %s, expected_body is %s" % (body, expected_body))
            raise

    def assert_in_body(self, body, expected_body):
        """
        验证返回结果，是否包含期望结果
        :param body:
        :param expected_body:
        :return:
        """
        try:
            body = json.dumps(body)
            assert expected_body in body
            return True
        except:
            self.log.error("expected_body not in body or body error, body is %s, expected_body is %s" % (body, expected_body))
            raise

