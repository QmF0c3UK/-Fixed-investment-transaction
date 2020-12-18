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
# -*- coding:utf-8 -*-


import requests
import json
import time
import datetime

session = requests.Session()
id = '002190' #基金ID
moneny = 2000 #月投资金额：
usemoney = 0 #以投资金额
paramsGet = {"fundCode": id,
             "pageIndex": "1",
             "endDate": "",
             "pageSize": "1000",
             "startDate": "2019.12.10",
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
        print(">>>报错了兄弟:1<<<")

def eomonth(date_object):  ##计算当月天数##
    if date_object.month == 12:
        next_month_first_date = datetime.date(date_object.year + 1, 1, 1)
    else:
        next_month_first_date = datetime.date(date_object.year, date_object.month + 1, 1)
    return next_month_first_date - datetime.timedelta(1)

def GetData(): ##获取所有数据##
    try:
        response = session.get("http://api.fund.eastmoney.com/f10/lsjz", params=paramsGet, headers=headers)
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
    # UnusedMoneny = moneny - usemoney #计算使用额度，每月重置
    # NumDays = eomonth(datetime.datetime.strptime(week_data[7]['日期'], '%Y-%m-%d')).day #最后一天的月份天数
    # Remainingday = 0 #已投资天数
    if week_data[7]['累计净值为'] < avg:
        DayTR = moneny/eomonth(datetime.datetime.strptime(week_data[7]['日期'], '%Y-%m-%d')).day * (1+(100*(avg - week_data[7]['累计净值为'])))
        SumTR = OutData['总投入'] + DayTR
        SumFE = OutData['总份额'] + DayTR/week_data[7]['累计净值为']
        SumJZ = SumFE * week_data[7]['累计净值为'] #总价值
        SumSY = '{:.2%}'.format((SumJZ-SumTR)/SumTR)
        OutData.update({'该日净值': week_data[7]['累计净值为'],
                        '下次定投日': week_data[7]['日期'],
                        '日投入': DayTR,
                        '总投入': SumTR,
                        '总份额': SumFE,
                        '总价值': SumJZ,
                        '总收益率': SumSY})
        # print('%s-%s累计净值(%s)小于前七天平均净值(%s)，建议买入' % (week_data[0]['日期'], week_data[6]['日期'], week_data[7]['累计净值为'], avg))
        print("下次定投日：%s    该日净值为：%s    该日投入：%s     总收益率：%s    总投入：%s    总价值：%s    总份额：%s"  % (week_data[7]['日期'], week_data[7]['累计净值为'], DayTR, SumSY, SumTR, SumJZ, SumFE))
    # elif week_data[7]['累计净值为'] == avg:
    #     print('%s-%s累计净值(%s)和前七天平均净值(%s)相等，建议观望' % (week_data[0]['日期'], week_data[6]['日期'], week_data[7]['累计净值为'], avg))
    #     # print('差额为：%s' % (avg - week_data[7]['累计净值为']))
    elif week_data[7]['累计净值为'] >= avg:
        # # print(week_data)
        # SumJZ = week_data[7]['累计净值为'] *OutData['总份额']
        # SumTR = OutData['总投入']
        # # print(OutData['下次定投日'],SumTR,SumJZ)
        # OutData.update({'总价值': SumJZ,
                        # '总收益率': SumSY})
        print("下次定投日：%s    该日净值为：%s    该日投入：%s     总收益率：%s    总投入：%s    总价值：%s    总份额：%s" % (
        week_data[7]['日期'], week_data[7]['累计净值为'], OutData['日投入'], OutData['总收益率'], OutData['总投入'], OutData['总价值'], OutData['总份额']))
    else:
        print(">>>报错了兄弟:4<<<")
        return
        # print(">>>报错了兄弟:4<<<")


def average(week_data):    ##计算过去7天净值平均值##
    try:
        sum = 0
        for j in range(0, 7):
            sum = sum + week_data[j]['累计净值为']
        # print('从%s到%s的平均净值为：%s' % (week_data[0]['日期'], week_data[6]['日期'], sum / 7))
        return sum/7
    except:
        print(">>>报错了兄弟:2<<<")

def main():
    print("[+] ========= %s %s " % (id, GetName()))
    Data=GetData()
    print('首次投资日：%s' % Data[0]['日期'])
    for i in range(0, len(Data) - 7):
        try:
                week_data = Data[i:i + 8]
                Calculation(week_data, average(week_data))
        except:
            print(">>>报错了兄弟:3<<<")
    print('最后投资%s' % Data[-1]['日期'])
    #平均值

if __name__ == '__main__':
    main()
    # GetData()


