import baostock as bs
import pandas as pd

from select_shares import select_share_by_date
from tushare_to_baostock import baostock_date_to_tuhshare, tuhshare_to_baostock_sharecode, tuhshare_date_to_baostock
from sqlalchemy import create_engine
from my_time_func import get_my_start_end_date_list


# 指定日期，单个个股的5分钟数据
def baostock_data_signalday_signalshare(trade_date, share_code):
    rs = bs.query_history_k_data_plus(share_code,
                                      "date,time,code,open,high,low,close,volume,amount,adjustflag",
                                      start_date=trade_date, end_date=trade_date,
                                      frequency="5", adjustflag="3")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    return result


# 指定日期，指定个股list的5分钟数据
def baostock_to_mysql_5m(trade_date, share_code_list):
    #### 登陆系统 ####
    lg = bs.login()

    # 建立mysql数据库的连接
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')

    data_list = []

    for i in range(0, len(share_code_list)):
        print("剩余数量：")
        print(len(share_code_list)-i)
        share_code = tuhshare_to_baostock_sharecode(share_code_list[i])
        data = baostock_data_signalday_signalshare(trade_date, share_code)
        print(data.head())
        data_list.append(data)

    df_datalist = pd.concat(data_list)
    print("当日数据汇总")
    print(df_datalist)
    df_datalist.to_sql('5_minutes_data', con=conn, if_exists='append', index=False)

    #### 登出系统 ####
    bs.logout()


if __name__ == '__main__':

    # 已经存入数据日期 2022年6月20日-2022年6月24日
    start_date = '20220625'
    end_date = '20220625'

    # 生成日期list
    date_list = get_my_start_end_date_list(start_date, end_date, 'tushare')
    # 按日期循环
    for i in range(0, len(date_list)):
        trade_date = date_list[i]
        print("数据日期")
        print(trade_date)
        # 获取tushare当日交易股票代码
        share_code_list = select_share_by_date(trade_date).ts_code.tolist()
        # 只遍历交易日数据
        if len(share_code_list) > 0:
            # 日期转换
            trade_date_baostock = tuhshare_date_to_baostock(trade_date)
            # 对当前日期的list执行操作
            baostock_to_mysql_5m(trade_date_baostock, share_code_list)
