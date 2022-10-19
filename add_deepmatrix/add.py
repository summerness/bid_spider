import json

import requests
from diskcache import Cache


class DataInfo():
    def __init__(self, corpid, secret):
        self.corpid = corpid
        self.secret = secret
        self.API = "https://api.deepmatrix.cn"
        self.access_token = None
        self.getToken()

    def getToken(self):
        tokenUrl = "{}/information/createaccesstoken".format(self.API)
        tokenKey = "TOKENKEY"
        cache = Cache("./access_token")
        self.access_token = cache.get(tokenKey)
        if self.access_token is not None:
            return
        rep = requests.post(tokenUrl, json={
            "corpid": self.corpid,
            "secret": self.secret
        })
        reqDic = json.loads(rep.content)
        if reqDic["code"] == 0:
            self.access_token = reqDic["data"]["access_token"]
            cache.set(tokenKey, self.access_token, expire=60 * 60)

    def getAllDataList(self, pageCode):
        dataUrl = "{}/page/alldatalist".format(self.API)
        rep = requests.post(dataUrl, json={
            "page_size": 100,
            "page_index": 1,
            "page_code": pageCode
        }, params={
            "access_token": self.access_token
        })
        reqDic = json.loads(rep.content)
        if reqDic["code"] == 0:
            return reqDic["data"]["info"]

    def addOneData(self, pageCode, appCode, pageType, dataList):
        dataUrl = "{}/page/insertonedata".format(self.API)
        rep = requests.post(dataUrl, json={
            "page_code": pageCode,
            "app_code": appCode,
            "page_type": pageType,
            "field_data_list": dataList,
        }, params={
            "access_token": self.access_token
        })
        print(rep.content)


if __name__ == '__main__':
    d = DataInfo("b5c9a0b0-d7be-4e4b-b057-c94b1de3c77d", "ea106dc2fe4a3cc47d57e8688c9c4c2607aad5e8")
    print(d.getAllDataList("f976fb11-7e3e-489d-b84e-bbf209182a5b"))
