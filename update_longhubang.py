from sqlalchemy import create_engine
import tushare as ts

from my_time_func import get_my_start_end_date_list
from my_token import get_tushare_token


def update_longhubang(querydate):
    # 建立mysql数据库的连接
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')

    mytoken = get_tushare_token()

    # 初始化pro接口
    pro = ts.pro_api(mytoken)

    # 拉取数据
    df = pro.top_inst(**{
        "trade_date": querydate,
        "ts_code": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "trade_date",
        "ts_code",
        "exalter",
        "buy",
        "buy_rate",
        "sell",
        "sell_rate",
        "net_buy",
        "side",
        "reason"
    ])
    print(df)

    new_df = df.fillna(value=0)
    new_df.to_sql('longhubang', con=conn, if_exists='append', index=False)


# querydate = '20220425'
#  update_longhubang(querydate)

# 20211201 - 5月6日
date_list = get_my_start_end_date_list('20220518', '20220523', 'tushare')

for i in range(0, len(date_list)):
    update_longhubang(date_list[i])
