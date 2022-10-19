from add_deepmatrix.add import DataInfo
from concurrent.futures import ThreadPoolExecutor
from spider import china, liaoning
from datetime import datetime
import time
# 以下信息自行配置
Corpid = ''
Secret = ''
keywordPageCode = 'f976fb11-7e3e-489d-b84e-bbf209182a5b'
keywordFieldKey = 'bfb6dcea-5453-4d4b-ac74-338c94ee50a7'
bidInfoPageCode = '0610a8f1-8ee6-4c38-893c-196fd4a3e6ea'
appCode = '466369c3-0530-4c67-afdf-64aae91a872f'

# FIELD_KEY#
ProjectName = 'fe53e82c-4d61-4778-b5f3-e4ab1c493d17'
URL = 'f39c2c25-9e86-4dc6-b3e0-b581cc5d97c5'
projectStatus = '353fbeb8-893a-4ea1-beff-a5a9db17dfd7'
procurementCorpName = '78d1b86e-f105-4009-a53e-a03648f11a46'
commentTime = 'd7fae4b6-f4b6-447a-af33-dc3d2d707681'
area = '9bb7a414-f659-4d51-82a1-77657c05edac'
projectContact = '860dcd28-d895-49f8-ad20-148b12c610dd'
projectContactPhone = 'c0e673f7-74f7-4f44-8f83-efb4b2344c95'
procurementCorpAddress = 'fe9bb93d-7a59-4d66-a175-d2fb84a4cec7'
procurementCorpContactPhone = 'e16cb133-cc13-499c-b9e0-b647bc087f7e'
bidWinnerName = '3798a5f5-d047-401c-bb0c-1a8395d229f7'
bidWinnerPrice = '843f2166-a5c9-464b-b4e3-c65954db67ea'
budget = 'a3c3b0a4-2d02-41f7-8c73-408ebc35e7d7'
sourceName = '49a669c4-dd61-41a7-b803-222fe419999a'
keyword = '2b20804f-8a88-4dcf-9f94-233df57ebfc0'
agencyName = 'af05fa33-1d34-4a98-b197-1f9f5b579c87'
agencyAddress = '0e9dea18-c914-411f-aee8-1c4986a470d3'
agencyContactPhone = 'f2898723-f47d-4de0-8f4d-09a303782f98'

maxWorkThread = 5


def to_spider(keyword_list, object_list):
    pool = ThreadPoolExecutor(max_workers=int(maxWorkThread))
    data = []
    for fn in object_list:
        try:
            s = pool.submit(fn.main, keyword_list).result()
            data.extend(s)
        except KeyError:
            continue
    pool.shutdown(wait=True)
    return data


def get_keyword_list(d, page_code, keyword_field_key):
    data = d.getAllDataList(page_code)
    keywords = []
    for each in data:
        keywords.append(each[keyword_field_key])
    return keywords


def main():
    d = DataInfo(Corpid, Secret)
    keywords = get_keyword_list(d, keywordPageCode, keywordFieldKey)
    c = china.China()
    ln = liaoning.Liaoning()
    object_list = [c, ln]
    data = to_spider(keywords, object_list)
    for each in data:
        if each is None:
            continue
        ntime = datetime.now()
        datime = time.localtime(each.comment_time/1000)
        if datime.tm_year == ntime.year and datime.tm_mon == ntime.month and datime.tm_mday == ntime.day:
            d.addOneData(
                bidInfoPageCode,
                appCode,
                0,
                [
                    {
                        "field_key": ProjectName,
                        "field_data": each.procurement_project_name if each.procurement_project_name else ""
                    },
                    {
                        "field_key": URL,
                        "field_data": each.url if each.url else ""
                    },
                    {
                        "field_key": projectStatus,
                        "field_data": each.project_status if each.project_status else ""
                    },
                    {
                        "field_key": procurementCorpName,
                        "field_data": each.procurement_project_name if each.procurement_project_name else ""
                    },
                    {
                        "field_key": commentTime,
                        "field_data": str(each.comment_time) if each.comment_time else ""
                    },
                    {
                        "field_key": area,
                        "field_data": each.area if each.area else ""
                    },
                    {
                        "field_key": projectContact,
                        "field_data": each.project_contact_name if each.project_contact_name else ""
                    },
                    {
                        "field_key": projectContactPhone,
                        "field_data": each.project_contact_phone if each.project_contact_phone else ""
                    },
                    {
                        "field_key": procurementCorpAddress,
                        "field_data": each.procurement_corp_address if each.procurement_corp_address else ""
                    },
                    {
                        "field_key": procurementCorpContactPhone,
                        "field_data": each.procurement_corp_contact_phone if each.procurement_corp_contact_phone else ""
                    },
                    {
                        "field_key": bidWinnerName,
                        "field_data": each.bid_winner_name if each.bid_winner_name else ""
                    },
                    {
                        "field_key": bidWinnerPrice,
                        "field_data": each.bid_winner_price if each.bid_winner_price else ""
                    },
                    {
                        "field_key": budget,
                        "field_data": each.budget if each.budget else ""
                    },
                    {
                        "field_key": sourceName,
                        "field_data": each.source_name if each.source_name else ""
                    },
                    {
                        "field_key": keyword,
                        "field_data": each.keyword if each.keyword else ""
                    },
                    {
                        "field_key": agencyName,
                        "field_data": each.agency_name if each.agency_name else ""
                    },
                    {
                        "field_key": agencyAddress,
                        "field_data": each.agency_address if each.agency_address else ""
                    },
                    {
                        "field_key": agencyContactPhone,
                        "field_data": each.agency_contact_phone if each.agency_contact_phone else ""
                    },
                ]
            )




if __name__ == '__main__':
    main()
