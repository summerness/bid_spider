import datetime
import time
import requests
import re
import json
from lxpy import DateGo
from lxml import etree

import spider


class China(object):
    '''中国采购网'''

    def __init__(self):
        self.url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1'
        self.headers = {
            'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
            'Host': 'search.ccgp.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36',
            'keep-alive': 'False'
        }
        self.start_time = ''
        self.end_time = ':'.join(DateGo.now_ymd())

    def get_count(self, kw):
        self.params = {
            'searchtype': '1',
            'page_index': '1',
            'bidSort': '0',
            'pinMu': '0',
            'bidType': 0,
            'displayZone': '',
            'zoneId': '',
            'kw': kw,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'timeType': '3'
        }
        try:
            html = requests.get(url=self.url, params=self.params, headers=self.headers).text
        except:
            return 1
        count_list = re.findall('<span style="color:#c00000">(\d+)</span>', html)  # 根据总条数计算页数
        if len(count_list) == 0:
            return 1
        count = count_list[0]
        if int(count) % 20 == 0:
            return int(int(count) / 20)
        else:
            return int(int(count) // 20) + 1

    def get_page(self, page_index, kw):
        self.params = {
            'searchtype': '1',
            'page_index': '1',
            'bidSort': '0',
            'pinMu': '0',
            'bidType': 0,
            'displayZone': '',
            'zoneId': '',
            'kw': kw,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'timeType': '3'
        }

        try:
            self.params['page_index'] = page_index
            response = requests.get(url=self.url, headers=self.headers, params=self.params)
            if response.status_code == 200:
                html = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
                return html
            else:
                print(response.status_code)
        except:
            return None

    def get_all_url(self, html):
        pattern1 = '<.*?(href=".*?htm").*?'
        href_url = re.findall(pattern1, html, re.I)
        url_list = []
        for url in href_url:
            url1 = url.replace('href=', '').replace('"', '')
            url_list.append(url1)
        return url_list

    def get_detail_page(self, url):
        try:
            response = requests.get(url=url, timeout=15)
            if response.status_code == 200:
                html = response.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
                return html
        except requests.ConnectionError:
            return None

    def parse_detail_page(self, html, url, kw):
        table_list = html.xpath('//div[@class="table"]//tr')
        info = spider.Info()
        info.source_name = "中国采购网"
        info.keyword = kw
        info.url = url

        list = html.xpath('//a[@class="CurrChnlCls"]/text()')
        if len(list) > 0:
            info.project_status = list[-1]
        try:
            for table in table_list:
                if len(table.xpath('td[@class="title"]/text()')) > 0:
                    title = ''.join(table.xpath('td[@class="title"]/text()'))
                    value = ''.join(table.xpath('td[@colspan="3"]/text()'))
                    if title == "采购项目名称":
                        info.procurement_project_name = value
                    if title.find('附件') == 0:
                        value = 'http://www.ccgp.gov.cn/oss/download?uuid=' + ''.join(
                            table.xpath('td[@colspan="3"]/a/@id'))
                        info.appendix = value
                    if '公告时间' in title:
                        value = table.xpath('td[@width="168"]/text()')[1]
                        area = (table.xpath('td[@width="168"]/text()'))[0]
                        info.area = area
                        comment_time = time.strptime(value, "%Y年%m月%d日  %H:%M")
                        info.comment_time = int(round(time.mktime(comment_time) * 1000))
                    if '首次公告日期' in title:
                        first_comment_time = table.xpath('td[@width="168"]/text()')[0]
                        info.first_comment_time = first_comment_time
                        corrections_time = table.xpath('td[@width="168"]/text()')[1]
                        info.corrections_time = corrections_time
                    if '本项目招标公告日期中标日期' in title:
                        bid_comment_time = table.xpath('td[@width="168"]/text()')[0]
                        bid_comment_time = time.strptime(bid_comment_time, "%Y年%m月%d日  %H:%M")
                        info.bid_comment_time = int(round(time.mktime(bid_comment_time) * 1000))
                        bid_winner_time = table.xpath('td[@width="168"]/text()')[1]
                        info.bid_winner_time = bid_winner_time

                    if '本项目招标公告日期成交日期' in title:
                        bid_winner_success_time = table.xpath('td[@width="168"]/text()')[0]
                        info.bid_winner_success_time = bid_winner_success_time
                    if '成交金额' in title:
                        info.bid_winner_price = value
                    if '项目联系人' in title:
                        info.project_contact_name = value
                    if '项目联系电话' in title:
                        info.project_contact_phone = value
                    if '采购单位' in title:
                        info.procurement_corp_name = value
                    if '采购单位地址' in title:
                        info.procurement_corp_address = value
                    if '采购单位联系方式' in title:
                        info.procurement_corp_contact_phone = value
                    if '代理机构名称' in title:
                        info.agency_name = value
                    if '代理机构地址' in title:
                        info.agency_address = value
                    if '代理机构联系方式' in title:
                        info.agency_contact_phone = value
                    if '品目' in title:
                        info.items = value
                    if '中标金额' in title:
                        info.bid_winner_price = value
                    if '招标文件售价' in title:
                        info.bid_document_price = value
        except:
            return None
        return info

    def start_get_info(self, url, kw):
        html = self.get_detail_page(url)
        html = etree.HTML(html)
        info = self.parse_detail_page(html, url, kw)
        return info

    def main(self, keyword_list):
        data = []
        for kw in keyword_list:
            count_page = self.get_count(kw=kw)
            for i in range(1, count_page + 1):
                html = self.get_page(page_index=i, kw=kw)
                try:
                    url_list = self.get_all_url(html)
                    for url in url_list:
                        all_info = self.start_get_info(url, kw)
                        data.append(all_info)
                except:
                    continue

        return data


if __name__ == '__main__':
    c = China()
    data = c.main(
        ['招投标系统', '毕业论文', '研究生管理', '工作量', '表单', '科研管理', '应用大厅', '元数据', '信息服务', '应用搭建', '低代码', '零代码', '一张表', '一表通',
         '数据服务'])

    for each in data:
        print(vars(each))
