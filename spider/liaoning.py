import requests
import spider
import time
import json


class Liaoning(object):
    def __init__(self):
        self.url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do'
        self.header = {
            'Connection': 'keep-alive',
            'Content-Length': '93',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=B4289084560FE973FB884FED46741FD2; sto-id-20480=HMKMMFDLCJCD',
            'Host': 'www.ccgp-liaoning.gov.cn',
            'Origin': 'http://www.ccgp-liaoning.gov.cn',
            'Referer': 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=goZNSS&znss=%E9%9B%B7%E8%BE%BE',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        }

    def get_html(self, page_index=0, kw=""):
        params = {
            'method': 'getPubInfoList',
            't_k': 'null',
        }
        data = {
            'current': page_index,
            'rowCount': 10,
            'infoTypeCode': 'null',
            'title': kw,
            'queryType': 'znss',
        }
        jsonData = requests.post(url=self.url, params=params, data=data, headers=self.header).json()
        data = []
        for item in jsonData['rows']:
            editor = item['editor']
            url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpen&infoId=' + item['id']
            title = item.get('title')
            releaseDate = item.get('releaseDate')
            comment_time = time.strptime(releaseDate, "%Y-%m-%d")
            info_type_name = item.get("infoTypeName")
            district_name = item.get("districtName")
            info = spider.Info()
            info.source_name = "辽宁政府采购"
            info.keyword = kw
            info.url = url
            info.procurement_project_name = title
            info.comment_time = int(round(time.mktime(comment_time) * 1000))
            info.project_status = info_type_name
            info.agency_name = editor
            info.area = district_name
            data.append(info)
        return data

    def main(self, keyword_list):
        data = []
        for kw in keyword_list:
            page_index = 0
            while True:
                page_index += 1
                info_list = self.get_html(page_index, kw)
                if len(info_list) == 0:
                    break
                data.extend(info_list)

        return data


if __name__ == '__main__':
    l = Liaoning()
    print(l.main(["AA"]))
