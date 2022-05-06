import numpy as np

from df_manage_func import add_share_msg_to_df
from select_shares import get_longhubang
import pandas as pd


def get_top_exalter(n):
    # 获取全部龙虎榜数据
    lhb_df = get_longhubang().fillna(value='0')
    # 透视
    lhb_df_povit = pd.pivot_table(lhb_df, values='buy', index='exalter', columns='side', aggfunc=np.sum, fill_value=0)
    # 排序,按照买入交易额降序
    lhb_df_sorted = lhb_df_povit.sort_values(by='0', ascending=False).head(n)
    top_list = lhb_df_sorted.index.tolist()
    return top_list


# 根据席位查询历史龙虎榜
def query_longhubang_by_exalter(exalter):
    # 获取全部龙虎榜数据
    lhb_df = get_longhubang().fillna(value='0')
    # 根据席位 查询买入上榜记录
    df_i = lhb_df.loc[(lhb_df['exalter'] == exalter) & (lhb_df['side'] == '0')]
    # 按照日期倒序排列
    df_i_sorted = df_i.sort_values(by='trade_date', ascending=False, ignore_index=True)

    # 添加个股信息
    share_df_full = add_share_msg_to_df(df_i_sorted)
    share_df_full_partvalues = share_df_full.loc[:, ['trade_date', 'ts_code', 'name', 'buy', 'exalter']]

    print(share_df_full_partvalues.head())
    return share_df_full_partvalues


mylist = get_top_exalter(200)
l = len(mylist)
for i in range(0, l):
    print(mylist[i])
