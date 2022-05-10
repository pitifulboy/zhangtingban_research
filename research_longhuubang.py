import numpy as np

from classify_shares_market import get_zhangdie_limit
from df_manage_func import add_share_msg_to_df
from my_time_func import get_my_start_end_date_list, get_days_before_tushare
from select_shares import get_longhubang, select_days_longhubang, select_one_share_by_startdate, \
    select_data_by_shareslist_startdate
import pandas as pd


# 龙虎榜席位分析

def xiwei_ana_longhubang():
    # 获取指定时间段的全部龙虎榜数据
    my_datelist = get_my_start_end_date_list('20220401', '20220429', 'tushare')
    my_longhubang_datelist = select_days_longhubang(my_datelist)

    # 选定买入的数据部分,去重多个原因上榜。
    my_lhb_side0 = my_longhubang_datelist.loc[my_longhubang_datelist['side'] == '0'].loc[:,
                   ['trade_date', 'ts_code', 'exalter', 'buy']]

    # 由于多个原因重复上榜，需要去重
    my_lhb_side0_unique = my_lhb_side0.drop_duplicates(keep='first')

    print(my_lhb_side0)

    path = r'D:\00 量化交易\\' + '4月龙虎榜2' + '.xlsx'
    my_lhb_side0_unique.to_excel(path, sheet_name='4月龙虎榜', engine='openpyxl')

    # 透视,统计上榜次数和金额
    lhb_df_povit = pd.pivot_table(my_lhb_side0_unique, index='exalter', values='buy',
                                  aggfunc={'exalter': np.count_nonzero, 'buy': np.sum})

    # 排序,按照买入交易额降序
    lhb_df_sorted = lhb_df_povit.sort_values(by='buy', ascending=False)

    print(lhb_df_povit)
    path2 = r'D:\00 量化交易\\' + '4月龙虎榜透视' + '.xlsx'
    lhb_df_sorted.to_excel(path2, sheet_name='4月龙虎榜透视', engine='openpyxl')


# 龙虎榜交易额top100

def get_lhb_top_100_amount():
    # 获取指定时间段的全部龙虎榜数据
    my_datelist = get_my_start_end_date_list('20220401', '20220429', 'tushare')
    my_longhubang_datelist = select_days_longhubang(my_datelist)

    # 选定买入的数据部分,去重多个原因上榜。
    my_lhb_side0 = my_longhubang_datelist.loc[my_longhubang_datelist['side'] == '0'].loc[:,
                   ['trade_date', 'ts_code', 'exalter', 'buy']]

    # 由于多个原因重复上榜，需要去重
    my_lhb_side0_unique = my_lhb_side0.drop_duplicates(keep='first')

    # 透视,统计上榜次数和金额
    lhb_df_povit = pd.pivot_table(my_lhb_side0_unique, index='exalter', values='buy',
                                  aggfunc={'exalter': np.count_nonzero, 'buy': np.sum})

    # 排序,按照买入交易额降序
    lhb_df_sorted = lhb_df_povit.sort_values(by='buy', ascending=False)

    lhb_df_sorted_top100_list = lhb_df_sorted.head(100).index.tolist()

    return lhb_df_sorted_top100_list


# 席位买入榜top100 涨停数和涨停率


# 获取指定时间段的全部龙虎榜数据
my_datelist = get_my_start_end_date_list('20220401', '20220429', 'tushare')
my_longhubang_datelist = select_days_longhubang(my_datelist)

# 修正龙虎榜时间
#my_longhubang_datelist['trade_date'] = my_longhubang_datelist.apply(lambda x: get_days_before_tushare(x.trade_date, 1), axis=1)

# 选定席位

this_exalter = '华鑫证券有限责任公司宁波分公司'

# 获取该席位龙虎榜买入记录
lhb_this_exalter = my_longhubang_datelist.loc[
    (my_longhubang_datelist['exalter'] == this_exalter) & (my_longhubang_datelist['side'] == '0')]

# 获取龙虎榜最早日期，以此日期开始一次性读取所有个股交易数据。
start_date = lhb_this_exalter.trade_date.min()
#  获取个股list，并去重
lhb_sharelist = lhb_this_exalter.ts_code.tolist()
lhb_sharelist_unique = list(set(lhb_sharelist))

# 查询上榜个股交易数据
df_lhb_one_exalter = select_data_by_shareslist_startdate(lhb_sharelist_unique, start_date)


# 分析每次上榜，是否涨停
fina_data_list = []
for i in range(0, len(lhb_this_exalter)):
    # 上榜日
    trade_date = lhb_this_exalter.iloc[i, 0]
    # 上榜个股
    ts_code = lhb_this_exalter.iloc[i, 1]
    # 上榜后表现数据

    share_after_lhb = df_lhb_one_exalter.loc[(df_lhb_one_exalter['ts_code'] == ts_code) & (df_lhb_one_exalter['trade_date'].astype('int')>= int(trade_date))]
    print(share_after_lhb)

    #当日是否涨停
    limit =get_zhangdie_limit(ts_code)

