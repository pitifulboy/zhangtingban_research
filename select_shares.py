# 建立mysql数据库的连接
from sqlalchemy import create_engine
import pandas as pd


# 涨停股票dataframe

def select_zhangtingban_df(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)

    # 涨停个股角标数字
    share_list_num = []
    for i in range(len(df1)):
        close = '%.2f' % (df1["close"][i])

        pre_close = df1["pre_close"][i]
        # 涨停价
        up_limit = '%.2f' % (pre_close * 1.1)

        if close == up_limit:
            share_list_num.append(i)

    return df1.iloc[share_list_num]


# 选出炸板股票dataframe
def select_zhaban_df(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)
    share_list_num = []

    for i in range(len(df1)):
        high = '%.2f' % (df1["high"][i])
        close = '%.2f' % (df1["close"][i])
        pre_close = df1["pre_close"][i]
        # 涨停价
        up_limit = '%.2f' % (pre_close * 1.1)

        # 炸板股票
        if high == up_limit and close < up_limit:
            share_list_num.append(i)

    return df1.iloc[share_list_num]


# 跌停股票dataframe

def select_dietingban_df(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)

    share_list_num = []

    for i in range(len(df1)):
        close = '%.2f' % (df1["close"][i])
        pre_close = df1["pre_close"][i]
        # 跌停价
        down_limit = '%.2f' % (pre_close * 0.9)

        if close == down_limit:
            share_list_num.append(i)

    return df1.iloc[share_list_num]


# 选择一只股票所有交易数据
def select_one_share(sharecode):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE ts_code = '" + sharecode + "' ORDER BY trade_date ASC"
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选择所有股票某一段时间内的所有数据
def select_shares_period(datelist):
    str = ",".join(datelist)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date IN (" + str + ") "
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选择一组股票交易数据
def select_data_by_shareslist(share_list):
    str = "','".join(share_list)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE ts_code IN ('" + str + "') ORDER BY trade_date ASC"
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选择一组股票交易数据
def select_data_by_shareslist_lastdate(share_list, lastdate):
    str = "','".join(share_list)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE ts_code IN ('" + str + "') AND trade_date <= " + lastdate + " ORDER BY trade_date ASC"
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选出一天的所有交易数据
def select_share_by_date(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)

    return df1


'''
# 选出某一天所有股票代码

def select_sharecode_by_date(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM dailytrade WHERE trade_date = '" + tradedate + "' "
    df1 = pd.read_sql(mysql_1, conn)
    df_sharecode = df1.ts_code

    return df_sharecode
'''


# 获取股票中文名称

# 选择一只股票信息
def select_one_share_msg(sharecode):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM share_list WHERE ts_code = '" + sharecode + "' "
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选择一组股票信息
def select_msg_by_shareslist(share_list):
    str = "','".join(share_list)

    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM share_list WHERE ts_code IN ('" + str + "') "
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 5分钟数据查询
# 5分钟数据查询
# 5分钟数据查询

def select_5m_data(tradedate, share_code):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql = "SELECT  * FROM chuban_5_minute_data WHERE date = '" + tradedate + "' AND code = '" + share_code + "'"
    df = pd.read_sql(mysql, conn)
    return df


def select_5m_data_bydate(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql = "SELECT  * FROM chuban_5_minute_data WHERE date = '" + tradedate + "'"
    df = pd.read_sql(mysql, conn)
    return df


# 选择单个席位的龙虎榜数据
def select_one_share_by_longhubang_xiwei(xiwei):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql_1 = "SELECT  * FROM longhubang WHERE exalter = '" + xiwei + "' ORDER BY trade_date ASC"
    df1 = pd.read_sql(mysql_1, conn)

    return df1


# 选择单日的龙虎榜
def select_one_day_longhubang(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql = "SELECT  * FROM longhubang WHERE trade_date = '" + tradedate + "'"
    df = pd.read_sql(mysql, conn)
    return df

# 选择全部龙虎榜
def get_longhubang():
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql = "SELECT  * FROM longhubang "
    df = pd.read_sql(mysql, conn)
    return df