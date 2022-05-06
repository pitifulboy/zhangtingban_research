from sqlalchemy import create_engine
import tushare as ts
from my_time_func import date_list_gen
from my_token import get_tushare_token
from tushare_to_baostock import baostock_date_to_tuhshare


def update_tradedata_from_toshare(trade_date):
    # 建立mysql数据库的连接
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')

    mytoken = get_tushare_token()

    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    df = pro.daily(**{
        "ts_code": "",
        "trade_date": trade_date,
        "start_date": "",
        "end_date": "",
        "offset": "",
        "limit": ""
    }, fields=[
        "ts_code",
        "trade_date",
        "open",
        "high",
        "low",
        "close",
        "pre_close",
        "change",
        "pct_chg",
        "vol",
        "amount"
    ])
    # 写入mysql数据库
    print(df)
    df.to_sql('dailytrade', con=conn, if_exists='append', index=False)


def update_tradedata_from_toshare_by_datelist(start, end):
    datelist = date_list_gen(start, end)
    update_tradedata_from_toshare_by_datelist(datelist)

    for i in range(0, len(datelist)):
        trade_date = baostock_date_to_tuhshare(datelist[i])
        update_tradedata_from_toshare(trade_date)


update_tradedata_from_toshare('20220506')

'''# 更新一段时间

start = '2022-04-22'
end = '2022-04-22'
update_tradedata_from_toshare_by_datelist(start,end)

# 获取单独一天，所有股票当天的开盘价，收盘价，交易额等行情数据
'''