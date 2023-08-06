from ..hiapi import HiApi
import math
import random


class Address(HiApi):
    long = 103
    lat = 30

    def __init__(self, phone, appcode="", appkey=""):
        super().__init__(appcode, appkey)
        self.phone = phone

    def generate_random_gps(self, radius=500000):
        radius_in_degrees = radius / 111300
        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))
        w = radius_in_degrees * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)
        longitude = y + self.long
        latitude = x + self.lat
        # 这里是想保留6位小数点
        self.long = '%.6f' % longitude
        self.lat = '%.6f' % latitude

    def get_phone_place(self):
        self.api_get("phonePlace", {"phone": self.phone})

        if self.out[-1]["stu"] == 1:
            self.long = self.result["data"]["longitude"]
            self.lat = self.result["data"]["latitude"]

            self.api_get("addr", {"latitude": self.lat, "longitude": self.long})

            self.result = self.out[-2]["data"]
            del self.result["province"], self.result["city"]
            self.result["address"] = self.out[-1]["data"]

        else:
            self.result = self.out[-1]
