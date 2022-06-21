from sqlalchemy import create_engine
import baostock as bs
import pandas as pd
from tushare_to_baostock import baostock_to_tuhshare_sharecode


def update_A50_HS300_ZZ500():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')

    # 登陆系统
    lg = bs.login()

    # 获取上证50成分股
    rs = bs.query_sz50_stocks()

    # 打印结果集
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        sz50_stocks.append(rs.get_row_data())
    a50 = pd.DataFrame(sz50_stocks, columns=rs.fields)
    # 将baostock格式转为tushare格式
    a50.code = a50.code.apply(baostock_to_tuhshare_sharecode)

    # 获取沪深300成分股
    rs = bs.query_hs300_stocks()

    # 打印结果集
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs.get_row_data())
    hs300 = pd.DataFrame(hs300_stocks, columns=rs.fields)
    hs300.code = hs300.code.apply(baostock_to_tuhshare_sharecode)

    # 获取中证500成分股
    rs = bs.query_zz500_stocks()

    # 打印结果集
    zz500_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs.get_row_data())
    zz500 = pd.DataFrame(zz500_stocks, columns=rs.fields)
    zz500.code = zz500.code.apply(baostock_to_tuhshare_sharecode)

    # 登出系统
    bs.logout()

    a50.to_sql('a50', con=conn, if_exists='replace', index=False)
    print(a50)

    hs300.to_sql('hs300', con=conn, if_exists='replace', index=False)
    print(hs300)

    zz500.to_sql('zz500', con=conn, if_exists='replace', index=False)
    print(zz500)


update_A50_HS300_ZZ500()
