import requests
from utils.LogUtil import my_log


class Request:

    def __init__(self):
        self.log = my_log("Requests")

    # 公共方法
    def request_api(self, url, data=None, json=None, headers=None, cookies=None, method="get"):

        if method == "get":
            # get请求
            self.log.debug("发送get请求")
            r = requests.get(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "post":
            # post请求
            self.log.debug("发送post请求")
            r = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)

        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text

        res = dict()
        res["code"] = code
        res["body"] = body

        return res

    # get
    def get(self, url, **kwargs):
        return self.request_api(url, method="get", **kwargs)

    # post
    def post(self, url, **kwargs):
        return self.request_api(url, method="post", **kwargs)
