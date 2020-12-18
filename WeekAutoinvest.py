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

id = '002190'  # 基金ID
startDate = "2019-10-31"
endDate = datetime.date.today()
moneny = 2000  # 月投资金额：

proxies = {'http': '127.0.0.1:8080'}
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
OutData = {'该日净值': 0,
           '日投入': 0,
           '总投入': 0,
           '总收益率': '',
           '总价值': 0,
           '总份额': 0,
           '上次投资日期': startDate
           }


def GetName():  ##获取基金名称##
    try:
        response = session.get("http://api.fund.eastmoney.com/fund/fundgz", params=paramsGet, headers=headers)
        return json.loads(response.text)['Data'][0]['name']
    except:
        print(">>>报错了兄弟:2<<<")


def eomonth(date_object):  ##计算当月天数##
    if date_object.month == 12:
        next_month_first_date = datetime.date(date_object.year + 1, 1, 1)
    else:
        next_month_first_date = datetime.date(date_object.year, date_object.month + 1, 1)
    return next_month_first_date - datetime.timedelta(1)


def DifferencdDays(StartDay, EndDay):  # 计算两个日期差值
    d1 = datetime.datetime.strptime(StartDay, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(EndDay, '%Y-%m-%d')
    interval = d1 - d2
    return interval.days


def GetData():  ##获取所有数据##
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


def Calculation(week_data, avg):
    if week_data[len(week_data) - 1]['累计净值为'] < avg:
        XCTS = DifferencdDays(week_data[len(week_data) - 1]['日期'], OutData['上次投资日期'])  # 距离上次投资的相差天数
        # TZCE = avg-week_data[len(week_data)-1]['累计净值为'] #投资差额
        BYTS = eomonth(datetime.datetime.strptime(week_data[len(week_data) - 1]['日期'], '%Y-%m-%d')).day  # 本月天数
        DayTR = round(moneny / BYTS) * XCTS
        SumTR = OutData['总投入'] + DayTR
        SumFE = OutData['总份额'] + DayTR / week_data[len(week_data) - 1]['累计净值为']
        SumJZ = SumFE * week_data[len(week_data) - 1]['累计净值为']  # 最新总价值
        SumSY = '{:.2%}'.format((SumJZ - SumTR) / SumTR)  # 最新总收益
        OutData.update({'该日净值': week_data[len(week_data) - 1]['累计净值为'],
                        '日投入': DayTR,
                        '总投入': SumTR,
                        '总份额': SumFE,
                        '总价值': SumJZ,
                        '总收益率': SumSY,
                        '上次投资日期': week_data[len(week_data) - 1]['日期']})
        print("下次定投日：%s    该日净值为：%s    该日投入：%s     总收益率：%s    总投入：%s    总价值：%s    总份额：%s" % (
            week_data[0]['日期'], week_data[len(week_data) - 1]['累计净值为'], DayTR, SumSY, SumTR, SumJZ,
            SumFE))
        # print("七日平均值为:%.4f.最后一日平均值为:%s.净值差额为:%s." % (avg, week_data[len(week_data)-1]['累计净值为'],TZCE))
    else:
        SumJZ = OutData['总份额'] * week_data[len(week_data) - 1]['累计净值为']
        SumSY = '{:.2%}'.format((SumJZ - OutData['总投入']) / OutData['总投入'])
        OutData.update({'总价值': SumJZ,
                        '总收益率': SumSY})
        print("下次定投日：%s    该日净值为：%s    该日投入：%s     总收益率：%s    总投入：%s    总价值：%s    总份额：%s" % (
            week_data[0]['日期'], week_data[len(week_data) - 1]['累计净值为'], OutData['日投入'], SumSY,
            OutData['总投入'], SumJZ, OutData['总份额']))


def average(week_data):  ##计算过去7天净值平均值##
    try:
        sum = 0
        for j in range(-1, len(week_data) - 1):
            sum = sum + week_data[j]['累计净值为']
        # print('从%s到%s的平均净值为：%s' % (week_data[0]['日期'], week_data[6]['日期'], sum / 7))
        return sum / len(week_data)
    except:
        print(">>>报错了兄弟:2<<<")


def main():
    print("[+] ========= %s %s " % (id, GetName()))
    Numlen = json.loads(session.get("http://api.fund.eastmoney.com/f10/lsjz", params=paramsGet, headers=headers,
                                    proxies=proxies).text)['TotalCount']
    paramsGet.update({"pageSize": Numlen})
    Data = GetData()
    first = len(Data) - 1
    print('首次投资日：%s' % Data[0]['日期'])
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
