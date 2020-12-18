# -*- coding:utf-8 -*-
banner = """
        888888ba             dP                     
        88    `8b            88                     
       a88aaaa8P' .d8888b. d8888P .d8888b. dP    dP 
        88   `8b. 88'  `88   88   Y8ooooo. 88    88 
        88    .88 88.  .88   88         88 88.  .88 
        88888888P `88888P8   dP   `88888P' `88888P' 
   ooooooooooooooooooooooooooooooooooooooooooooooooooooo 
                @time:2020/12/18 WeekAutoinvest.py
                        C0de by  @batsu                  
 """
print(banner)
import requests
import json
import time
import datetime

session = requests.Session()

id = '002191' #基金ID
startDate = "2019-10-31"
endDate = datetime.date.today()
moneny = 2000 #月投资金额：
usemoney = 0 #以投资金额
proxies={'http': '127.0.0.1:8080'}
Numlen = 1

paramsGet = {"fundCode": id,
             "pageIndex": "1",
             "endDate": endDate,
             "pageSize": Numlen,
             "startDate": startDate,
             "_": int(time.time())}
headers = {"Accept": "*/*",
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
           "Referer": "http://fundf10.eastmoney.com/",
           "Connection": "close",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9"}
NewData = []
OutData = {'下次定投日': '',
           '该日净值': 0,
           '日投入': 0,
           '总投入': 0,
           '总收益率': '',
           '总价值': 0,
           '总份额': 0
           }

def GetName():  ##获取基金名称##
    try:
        response = session.get("http://api.fund.eastmoney.com/fund/fundgz", params=paramsGet, headers=headers)
        return json.loads(response.text)['Data'][0]['name']
    except:
        print(">>>报错了兄弟:2<<<")

def GetData(): ##获取所有数据##
    try:
        response = session.get("http://api.fund.eastmoney.com/f10/lsjz", params=paramsGet, headers=headers,
                               proxies=proxies)
        # print(response.url) #获取url
        for i in json.loads(response.text)['Data']['LSJZList']:
            # print("时间：%s " % i['FSRQ'], "单位净值为：%s" % i['DWJZ'], "累计净值为：%s" % i['LJJZ'], "日增长率为：%s" % i['JZZZL'])
            data = {
                '日期': i['FSRQ'],
                '单位净值为': float(i['DWJZ']),
                '累计净值为': float(i['LJJZ']),
                '日增长率为': i['JZZZL']
            }
            NewData.append(data)
        return NewData[::-1]
        # return NewData
    except:
        print(">>>报错了兄弟:1<<<")
def Calculation(week_data,avg):
    if len(week_data) >= 7:
        print(7)
        print(week_data, avg)
    elif len(week_data) > 0:
        print('大于0')
        print(week_data, avg)
    else:
        print(">>>报错了兄弟:4<<<")


def average(week_data):    ##计算过去7天净值平均值##
    try:
        sum = 0
        # print(len(week_data))
        for j in range(-1, len(week_data)-1):
            sum = sum + week_data[j]['累计净值为']
        # print('从%s到%s的平均净值为：%s' % (week_data[0]['日期'], week_data[6]['日期'], sum / 7))
        return sum/len(week_data)
    except:
        print(">>>报错了兄弟:2<<<")

def main():
    print("[+] ========= %s %s " % (id, GetName()))
    Numlen = json.loads(session.get("http://api.fund.eastmoney.com/f10/lsjz", params=paramsGet, headers=headers,
                               proxies=proxies).text)['TotalCount']
    paramsGet.update({"pageSize":Numlen})
    Data = GetData()
    first =len(Data) -1
    print('首次投资日：%s' % Data[first]['日期'])
    for i in range(0, len(Data)):
        try:
            week_data = Data[i:i + 7]
            # print(week_data)
            Calculation(week_data, average(week_data))
        except:
            print(">>>报错了兄弟:3<<<")
    print('最后投资%s' % Data[-1]['日期'])

if __name__ == '__main__':
    main()
