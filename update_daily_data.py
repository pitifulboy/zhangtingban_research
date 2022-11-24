from sqlalchemy import create_engine
import tushare as ts

from my_time_func import get_my_start_end_date_list
from my_token import get_tushare_token


# 更新单日交易数据
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


# 更新多日交易数据
def update_tradedata_from_toshare_by_datelist(datelist):
    for i in range(0, len(datelist)):
        update_tradedata_from_toshare(datelist[i])




'''# 获取mysql中存储的最新日期
    maxdate = get_dailytrade_maxdate()
    # 起始日期是mysql日期的后一天
    update_start = get_days_after_tushare(maxdate, 1)

    # 判断mysql中是否已经更新最新数据，如果不是最新数据
    if maxdate != today_date:
        # 生成需要更新的datelist
        date_list = get_my_start_end_date_list(update_start, today_date, 'tushare')
        # 更新日常交易数据
        update_tradedata_from_toshare_by_datelist(date_list)'''
