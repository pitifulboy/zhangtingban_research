# 建立mysql数据库的连接
import itertools
from select_shares import select_msg_by_shareslist, select_zhangtingban_df
from tushare_to_baostock import tuhshare_to_baostock_sharecode, tuhshare_date_to_baostock
from select_shares import select_5m_data_bydate
import pandas as pd
from datetime import datetime, timedelta


def get_share_5m_status_list(df):
    list = []

    for j in range(len(df)):
        open_5m = df.iloc[j].open
        high_5m = df.iloc[j].high
        low_5m = df.iloc[j].low
        close_5m = df.iloc[j].close

        # 5分钟内未开板
        if open_5m == high_5m == low_5m == close_5m == df.high.max():
            list.append(2)
        # 五分钟之内，触板
        elif high_5m == df.high.max():
            list.append(1)
        # 五分钟之内，未触板
        else:
            list.append(0)

    return list


# 判断涨停板类型
def judge_share_zhangting_type(df):
    list_status = get_share_5m_status_list(df)
    # 删除重复状态0，1，2
    new_list1 = [k for k, g in itertools.groupby(list_status)]

    # 判断触板  print("触板")
    if new_list1[-1] == 0:
        share_type = '炸板'
    # 涨停中的一字板   print(baostock_code + '一字板')
    elif new_list1 == [2]:
        share_type = '一字板'
    # 判断非一字板种类
    elif new_list1 == [1, 2] or new_list1 == [0, 1, 2]:
        share_type = '秒板'
    # print("开板" + str(n) + "次")
    else:
        n = new_list1.count(2) - 1
        share_type = '回封板'

    return share_type


def judge_share_type(df):
    list_status = get_share_5m_status_list(df)
    # 删除重复状态0，1，2
    new_list1 = [k for k, g in itertools.groupby(list_status)]

    # 判断触板  print("触板")
    if new_list1[-1] == 0:
        share_type = 'touch'
    # 涨停中的一字板   print(baostock_code + '一字板')
    elif new_list1 == [2]:
        share_type = 'one'
    # 判断非一字板种类
    # print("开板" + str(n) + "次")
    else:
        n = new_list1.count(2) - 1
        share_type = 'open_' + str(n)

    return share_type

'''# 获取某日回封板股票list
def select_shares_zhangting_type(tradedate_tushare):
    # 获取触板股票列表
    list = select_zhangtingban_df(tradedate_tushare)
    # 获取股票中文名称
    df_msg = select_msg_by_shareslist(list)

    # 将日期格式转换为bao_stock需要的格式 '2022-03-28'
    tradedate_baostock = tuhshare_date_to_baostock(tradedate_tushare)
    # 一次读取指定日期所有股票的5分钟数据。节约读取时间
    df = select_5m_data_bydate(tradedate_baostock)

    result_list = []

    for j in range(0, len(list)):
        baostock_code = tuhshare_to_baostock_sharecode(list[j])
        df1 = df[df.code == baostock_code]

        this_share_name = df_msg.loc[df_msg.ts_code == list[j]].iloc[0, 2]

        result_list.append([tradedate_tushare, list[j][3:], this_share_name[0:2], judge_share_zhangting_type(df1)])

    dfs = pd.DataFrame(result_list, columns=['交易日', '代码', '名称', '类型'])

    return dfs


'''