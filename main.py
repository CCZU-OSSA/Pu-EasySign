from config import PU_USERNAME,PU_PASSWORD,SID
import requests

import base64
import json
import os
import time
import secrets
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from time import sleep


class PuSpider:
    def __init__(self):
        self.username = PU_USERNAME
        self.password = PU_PASSWORD
        self.authorization = None
        self.tribe_id=None
        self.activities={}
        self.session = requests.Session()

    # def get_school(self):
    #     get_school_url="https://pocketuni.net/index.php?app=api&mod=Sitelist&act=getSchools"
    #     get_school_headers={
    #         "host": "pocketuni.net",
    #         "sec-ch-ua-platform": "Linux",
    #         "user-agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36',
    #         "accept": "application/json, text/plain, */*",
    #         "sec-ch-ua": '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    #         "sec-ch-ua-mobile": "?0",
    #         "origin": "https://pc.pocketuni.net",
    #         "sec-fetch-site": "same-site",
    #         "sec-fetch-mode": "cors",
    #         "sec-fetch-dest": "empty",
    #         "referer": "https://pc.pocketuni.net/",
    #         "accept-encoding": "gzip, br",
    #         "accept-language": "zh-CN,zh;q=0.9",
    #         "priority": "u=1, i"
    #     }
    #     resp = self.session.get(get_school_url, headers=get_school_headers)
    #     print(resp.status_code)
    #     print(resp.json())
    #     # print(self.session.cookies.get_dict())
    #     # {'name': '常州大学', 'email': '@jpu.com', 'school': '626', 'display_order': 'CZDX', 'cas_url': '', 'is_go': '1', 'go_id': '222766320254976'}

    def login(self):
        login_url = "https://apis.pocketuni.net/uc/user/login"
        payload = {
            "userName": self.username,
            "password": self.password,
            "sid": SID,
            "device": "pc"
        }
        login_headers = {
            "host": "apis.pocketuni.net",
            "sec-ch-ua-platform": '"Linux"',
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "sec-ch-ua": '"Google Chrome";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
            "content-type": "application/json",
            "sec-ch-ua-mobile": "?0",
            "origin": "https://class.pocketuni.net",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://class.pocketuni.net/",
            "accept-encoding": "gzip, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "priority": "u=1, i",
        }
        resp = self.session.post(login_url, json=payload, headers=login_headers).json()
        token=resp['data']['token']
        sid=resp['data']['sid']
        self.authorization=f"Bearer {token}:{sid}"
        userinfo = resp["data"]['baseUserInfo']
        realname = userinfo["realname"]
        collegename = userinfo["collegeName"]
        classname = userinfo["className"]
        politicalname = userinfo["politicalName"]
        print(f"姓名:{realname} \n学院:{collegename} \n班级:{classname} \n政治面貌:{politicalname} \n")

    def tribe(self):
        tribe_url="https://apis.pocketuni.net/apis/tribe/myList"
        tribe_headers = {
              "host": "apis.pocketuni.net",
              "content-length": "29",
              "sec-ch-ua-platform": "\"Linux\"",
              "authorization": self.authorization,
              "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
              "accept": "application/json, text/plain, */*",
              "sec-ch-ua": "\"Google Chrome\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
              "content-type": "application/json",
              "sec-ch-ua-mobile": "?0",
              "origin": "https://class.pocketuni.net",
              "sec-fetch-site": "same-site",
              "sec-fetch-mode": "cors",
              "sec-fetch-dest": "empty",
              "referer": "https://class.pocketuni.net/",
              "accept-encoding": "gzip, br, zstd",
              "accept-language": "zh-CN,zh;q=0.9",
              "priority": "u=1, i"
        }
        tribe_json={"page":1,"limit":2,"type":2}
        tribe_resp=self.session.post(tribe_url, json=tribe_json, headers=tribe_headers).json()
        self.tribe_id=tribe_resp['data']['list'][0]['id']


    """
        Bearer-token:("token":"7e2bffd9b81111f19b2300163e44521e")+("sid": 222766320254976)
        "tribeID":316255524225074
    """
    def activity(self):
        activity_url = "https://apis.pocketuni.net/apis/tribe/eventList"
        activity_headers = {
              "host": "apis.pocketuni.net",
              "content-length": "46",
              "sec-ch-ua-platform": "\"Linux\"",
              "authorization": self.authorization,
              "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
              "accept": "application/json, text/plain, */*",
              "sec-ch-ua": "\"Google Chrome\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
              "content-type": "application/json",
              "sec-ch-ua-mobile": "?0",
              "origin": "https://class.pocketuni.net",
              "sec-fetch-site": "same-site",
              "sec-fetch-mode": "cors",
              "sec-fetch-dest": "empty",
              "referer": "https://class.pocketuni.net/",
              "accept-encoding": "gzip, br, zstd",
              "accept-language": "zh-CN,zh;q=0.9",
              "priority": "u=1, i"
        }
        activity_json={
            "page": 1,
            "limit": 5,
            "tribeID":self.tribe_id
        }
        activity_resp=self.session.post(activity_url, json=activity_json, headers=activity_headers).json()
        activity_list=activity_resp['data']['list']
        for index,activity in enumerate(activity_list):
            name = activity['name']
            activity_id = activity['id']
            self.activities[activity_id] = name
            print(f"第{index+1}个活动：")
            print(f"活动名称：{name} \n")
            print(f"活动状态：{activity['statusName']} \n")
            print(f"开始时间：{activity['startTime']} \n")
            print(f"结束时间：{activity['endTime']} \n")

    def x_sign(self):
        key = bytes([121, 121, 0, 19, 5, 49, 2, 43, 13, 17, 11, 9, 4, 29, 60, 11])
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits

        payload = {
            "echo": "".join(secrets.choice(chars) for _ in range(16)),
            "timestamp": str(int(time.time())),
            "client": "web",
        }
        plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        return base64.b64encode(iv + ciphertext).decode()


    def sign(self):
        sign_url="https://apis.pocketuni.net/apis/activity/join"
        sign=" "
        sign_headers = {
                  "host": "apis.pocketuni.net",
                  "content-length": "30",
                  "sec-ch-ua-platform": "\"Linux\"",
                  "authorization": self.authorization,
                  "sec-ch-ua": "\"Google Chrome\";v=\"153\", \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"153\"",
                  "sec-ch-ua-mobile": "?0",
                  "x-sign": sign,
                  "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
                  "accept": "application/json, text/plain, */*",
                  "content-type": "application/json",
                  "origin": "https://class.pocketuni.net",
                  "sec-fetch-site": "same-site",
                  "sec-fetch-mode": "cors",
                  "sec-fetch-dest": "empty",
                  "referer": "https://class.pocketuni.net/",
                  "accept-encoding": "gzip, br, zstd",
                  "accept-language": "zh-CN,zh;q=0.9",
                  "priority": "u=1, i"
        }
        for activity_id, name in self.activities.items():
            sign_headers["x-sign"] = self.x_sign()  # 每次请求重新签名
            sign_json = {"activityId": activity_id}
            sign_resp = self.session.post(sign_url, json=sign_json, headers=sign_headers).json()
            sleep(3)
            sign_status = sign_resp.get('message', '')
            if sign_status in ("您已报名，请勿重复操作", "成功"):
                print(f"活动 {name} 签到成功")
            else:
                print(f"活动 {name} 签到失败: {sign_resp}")



if __name__ == '__main__':
    spider = PuSpider()
    # spider.get_school()
    spider.login()
    spider.tribe()
    spider.activity()
    spider.sign()

