from datetime import datetime, timedelta
import pandas as pd


def date_list_gen(startdate, enddate):
    start_time = datetime.strptime(startdate, "%Y-%m-%d")
    end_time = datetime.strptime(enddate, "%Y-%m-%d")

    t = (end_time - start_time).days + 1

    datelist = []

    for i in range(t):
        i_date = start_time + timedelta(days=i)
        i_date_str = i_date.strftime("%Y-%m-%d")
        datelist.append(i_date_str)

    return datelist


def date_list_gen_tushare(startdate, enddate):
    start_time = datetime.strptime(startdate, "%Y%m%d")
    end_time = datetime.strptime(enddate, "%Y%m%d")
    t = (end_time - start_time).days + 1
    datelist = []

    for i in range(t):
        i_date = start_time + timedelta(days=i)
        i_date_str = i_date.strftime("%Y%m%d")
        datelist.append(i_date_str)

    return datelist


def date_list_gen_tushare_n(n, enddate):
    end_time = datetime.strptime(enddate, "%Y%m%d")
    start_time = end_time - timedelta(days=n)

    datelist = []

    for i in range(0, n + 1):
        i_date = start_time + timedelta(days=i)
        i_date_str = i_date.strftime("%Y%m%d")
        datelist.append(i_date_str)

    return datelist


# new
# 使用period_range函数
def get_today_date(type_str):
    # 今天
    today_1 = pd.Timestamp.now()

    today_tushare_format = today_1.strftime('%Y%m%d')
    today_tushare_baostock = today_1.strftime('%Y-%m-%d')

    if type_str == 'tushare':
        date_str = today_tushare_format
    elif type_str == 'baostock':
        date_str = today_tushare_baostock

    return date_str


def get_my_startdate_list(startdate, num, type_str):
    t = pd.period_range(start=startdate, periods=num)

    new_list = []

    for i in range(0, num):

        if type_str == 'baostock':
            new_list.append(t[i].strftime('%Y-%m-%d'))
        elif type_str == 'tushare':
            new_list.append(t[i].strftime('%Y%m%d'))

    return new_list


def get_my_enddate_list(enddate, num, type_str):
    t = pd.period_range(end=enddate, periods=num)

    new_list = []

    for i in range(0, num):

        if type_str == 'baostock':
            new_list.append(t[i].strftime('%Y-%m-%d'))
        elif type_str == 'tushare':
            new_list.append(t[i].strftime('%Y%m%d'))

    return new_list


def get_my_start_end_date_list(startdate, enddate, type_str):
    t = pd.period_range(start=startdate, end=enddate)

    new_list = []

    for i in range(0, len(t)):

        if type_str == 'baostock':
            new_list.append(t[i].strftime('%Y-%m-%d'))
        elif type_str == 'tushare':
            new_list.append(t[i].strftime('%Y%m%d'))

    return new_list


# 获取前一天
def get_days_before_tushare(datestr, n):
    date_datetime = pd.to_datetime(datestr, format='%Y%m%d')

    date_daybefore = date_datetime - timedelta(n)

    date_daybefore = date_daybefore.strftime('%Y%m%d')

    return date_daybefore
