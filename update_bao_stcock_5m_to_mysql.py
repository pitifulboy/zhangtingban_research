import baostock as bs
import pandas as pd
from select_shares import select_chuban
from tushare_to_baostock import baostock_date_to_tuhshare, tuhshare_to_baostock_sharecode
from sqlalchemy import create_engine
from my_time_func import date_list_gen


def baostock_data_signalday_signalshare(trade_date, share_code):
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(share_code,
                                      "date,time,code,open,high,low,close,volume,amount,adjustflag",
                                      start_date=trade_date, end_date=trade_date,
                                      frequency="5", adjustflag="3")
    # print('query_history_k_data_plus respond error_code:' + rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    return result


def baostock_to_mysql_5m(trade_date, share_code_list):
    # 选定日期
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    # print('login respond error_code:' + lg.error_code)
    # print('login respond  error_msg:' + lg.error_msg)

    # 建立mysql数据库的连接
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')

    for i in range(0, len(share_code_list)):
        print(share_code_list[i])
        share_code = tuhshare_to_baostock_sharecode(share_code_list[i])
        data = baostock_data_signalday_signalshare(trade_date, share_code)
        print(data)
        data.to_sql('chuban_5_minute_data', con=conn, if_exists='append', index=False)

    #### 登出系统 ####
    bs.logout()


if __name__ == '__main__':

    start_date = '2022-04-22'
    end_date = '2022-04-22'

    date_list = date_list_gen(start_date, end_date)

    for i in range(len(date_list)):
        trade_date = date_list[i]

        # 将bao_stock时间格式转换为tushare格式
        trade_date_tushare = baostock_date_to_tuhshare(trade_date)
        print(trade_date_tushare)
        # 获取tushare触板股票代码
        share_code_list = select_chuban(trade_date_tushare)
        print(share_code_list)

        baostock_to_mysql_5m(trade_date, share_code_list)
