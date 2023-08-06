import requests
import json
import random
import string
import hashlib

requests.packages.urllib3.disable_warnings()  # 忽视本地SSL


class HiApi:
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/54.0.2840.99 Safari/537.36"}
    prefix = "https://bbs.f021.top/api/"
    appcode = ""
    appkey = ""
    url = ""
    out = []
    result = None

    def __init__(self, appcode="", appkey=""):
        self.appcode = appcode
        self.appkey = appkey

    def api_get(self, name: str, params={}):
        # 从a-zA-Z0-9生成指定数量的随机字符：
        r = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        md5 = name + self.appcode + self.appkey + str(r)
        md5 = hashlib.md5(md5.encode("utf-8")).hexdigest()
        params["r"] = str(r)
        params["code"] = self.appcode
        params["sign"] = md5
        url = self.prefix + name + "/"
        res = requests.get(url, params=params, headers=self.header, verify=False)  # 调用接口
        try:
            self.out.append(json.loads(res.content))  # 将json数据转换为字典
            self.result = self.out[-1]["data"]
            self.url = res.url
            return self.out[-1]
        except json.decoder.JSONDecodeError:
            self.result = res.text.encode("utf-8")
            self.url = res.url


