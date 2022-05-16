import numpy as np

from A_longhubang_history import xiwei_ana
from classify_shares_market import get_zhangdie_limit
from my_time_func import get_my_start_end_date_list
from select_shares import select_days_longhubang, select_data_by_shareslist_startdate
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


# 指定日期区间，龙虎榜席位列表

def get_lhb_xiwei_list(my_datelist):
    # 获取指定时间段的全部龙虎榜数据

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

    lhb_df_xiwei_list = lhb_df_sorted.index.tolist()

    return lhb_df_xiwei_list


# 席位买入榜top100 涨停数和涨停率


# 选定席位,判断是否涨停
def caculate_lhb_xiwei_daban(my_datelist, this_exalter):
    # 获取指定时间段的全部龙虎榜数据
    my_longhubang_datelist = select_days_longhubang(my_datelist)

    # 修正龙虎榜时间
    # my_longhubang_datelist['trade_date'] = my_longhubang_datelist.apply(lambda x: get_days_before_tushare(x.trade_date, 1), axis=1)

    # 获取该席位龙虎榜买入记录
    lhb_this_exalter = my_longhubang_datelist.loc[
        (my_longhubang_datelist['exalter'] == this_exalter) & (my_longhubang_datelist['side'] == '0')]

    # 选定买入的数据部分,去重多个原因上榜。
    lhb_this_exalter_drop_reason = lhb_this_exalter.loc[my_longhubang_datelist['side'] == '0'].loc[:,
                                   ['trade_date', 'ts_code', 'exalter', 'buy']]

    # 由于多个原因重复上榜，需要去重
    lhb_this_exalter_unique = lhb_this_exalter_drop_reason.drop_duplicates(keep='first')

    # 获取龙虎榜最早日期，以此日期开始一次性读取所有个股交易数据。
    start_date = lhb_this_exalter_unique.trade_date.min()
    #  获取个股list，并去重
    lhb_sharelist = lhb_this_exalter_unique.ts_code.tolist()
    lhb_sharelist_unique = list(set(lhb_sharelist))

    # 查询上榜个股交易数据
    df_lhb_one_exalter = select_data_by_shareslist_startdate(lhb_sharelist_unique, start_date)

    # merge 龙虎榜和当日交易数据
    df_lhb_and_dailytrade = pd.merge(left=lhb_this_exalter_unique, right=df_lhb_one_exalter,
                                     on=['trade_date', 'ts_code'])
    # 添加判断是否涨停
    df_lhb_and_dailytrade['if_zhangting'] = 'status'

    # 分析每次上榜，涨停数据
    fina_data_list = []
    for i in range(0, len(lhb_this_exalter_unique)):
        # 上榜日
        trade_date = lhb_this_exalter_unique.iloc[i, 0]
        # 上榜个股
        ts_code = lhb_this_exalter_unique.iloc[i, 1]
        # 上榜后表现数据

        share_after_lhb = df_lhb_one_exalter.loc[(df_lhb_one_exalter['ts_code'] == ts_code) & (
                df_lhb_one_exalter['trade_date'].astype('int') >= int(trade_date))]

        # 判断上榜日是否涨停
        limit = get_zhangdie_limit(ts_code)
        close = '%.2f' % share_after_lhb.iloc[0].close
        pre_close = share_after_lhb.iloc[0].pre_close

        # 涨停价
        up_limit = '%.2f' % (pre_close * (1 + limit))

        if close == up_limit:
            fina_data_list.append(i)
            # 标记是否涨停
            df_lhb_and_dailytrade.iloc[i, 13] = 'yes'
        else:
            # 标记是否涨停
            df_lhb_and_dailytrade.iloc[i, 13] = 'no'

    return df_lhb_and_dailytrade.loc[:, ['trade_date', 'ts_code', 'exalter', 'buy', 'pct_chg', 'if_zhangting']]


# 选定多个龙虎榜交易记录,判断是否涨停
def caculate_lhb_xiwei_lotsof_daban(my_datelist):
    # 获取指定时间段的全部龙虎榜数据
    my_longhubang_datelist = select_days_longhubang(my_datelist)

    # 修正龙虎榜时间
    # my_longhubang_datelist['trade_date'] = my_longhubang_datelist.apply(lambda x: get_days_before_tushare(x.trade_date, 1), axis=1)

    # 获取龙虎榜最早日期，以此日期开始一次性读取所有个股交易数据。
    start_date = my_longhubang_datelist.trade_date.min()
    #  获取个股list，并去重
    lhb_sharelist = my_longhubang_datelist.ts_code.tolist()
    lhb_sharelist_unique = list(set(lhb_sharelist))

    # 查询上榜个股交易数据
    df_lhb_sharelists_dailytrade = select_data_by_shareslist_startdate(lhb_sharelist_unique, start_date)

    # merge 龙虎榜和当日交易数据
    df_lhb_and_dailytrade = pd.merge(left=my_longhubang_datelist, right=df_lhb_sharelists_dailytrade,
                                     on=['trade_date', 'ts_code'])
    # 添加判断是否涨停
    df_lhb_and_dailytrade['if_zhangting'] = 'status'

    # 分析每次上榜，涨停数据
    fina_data_list = []
    for i in range(0, len(df_lhb_and_dailytrade)):
        # 上榜个股
        ts_code = df_lhb_and_dailytrade.iloc[i, 1]
        # 上榜后表现数据

        # 判断上榜日是否涨停
        limit = get_zhangdie_limit(ts_code)
        close = '%.2f' % df_lhb_and_dailytrade.iloc[i].close
        pre_close = df_lhb_and_dailytrade.iloc[i].pre_close

        # 涨停价
        up_limit = '%.2f' % (pre_close * (1 + limit))

        if close == up_limit:
            fina_data_list.append(i)
            # 标记是否涨停
            df_lhb_and_dailytrade.iloc[i, 19] = 'yes'
        else:
            # 标记是否涨停
            df_lhb_and_dailytrade.iloc[i, 19] = 'no'

    return df_lhb_and_dailytrade.loc[:, ['trade_date', 'ts_code', 'exalter', 'buy', 'side', 'pct_chg', 'if_zhangting']]


# 龙虎榜席位分析

def lhb_daban_fenxi(data_df):
    # 获取指定时间段的全部龙虎榜数据

    my_longhubang_datelist = data_df

    # 选定买入的数据部分,去重多个原因上榜。
    my_lhb_side0 = my_longhubang_datelist.loc[my_longhubang_datelist['side'] == '0'].loc[:,
                   ['trade_date', 'ts_code', 'exalter', 'buy', 'pct_chg', 'if_zhangting']]

    # 由于多个原因重复上榜，需要去重
    my_lhb_side0_unique = my_lhb_side0.drop_duplicates(keep='first')

    print(my_lhb_side0)

    path = r'D:\00 量化交易\\' + '4月龙虎榜打板情况统计' + '.xlsx'
    my_lhb_side0_unique.to_excel(path, sheet_name='4月龙虎榜打板情况统计', engine='openpyxl')

    # 透视,统计上榜次数和金额
    lhb_df_povit = pd.pivot_table(my_lhb_side0_unique, index='exalter', values='ts_code', columns='if_zhangting',
                                  aggfunc={'ts_code': np.count_nonzero})

    # 排序,按照买入交易额降序
    lhb_df_sorted = lhb_df_povit.fillna(0).sort_values(by='yes', ascending=False)

    print(lhb_df_sorted)
    path2 = r'D:\00 量化交易\\' + '4月打板数据透视' + '.xlsx'
    lhb_df_sorted.to_excel(path2, sheet_name='4月打板数据透视', engine='openpyxl')

    return lhb_df_sorted


# 选定分析周期
my_datelist = get_my_start_end_date_list('20220401', '20220429', 'tushare')
# 获取龙虎榜数据
lhb_data = caculate_lhb_xiwei_lotsof_daban(my_datelist)

toushi_df = lhb_daban_fenxi(lhb_data)
# 筛选部分席位，减小计算量
top_exalter_povittable = toushi_df.loc[(toushi_df.yes.astype('int') > 5) & (toushi_df.no.astype('int') < 40)]

# 4月上榜次数超过9次的


for i in range(0, len(top_exalter_povittable)):
    exalter_name = top_exalter_povittable.index[i]
    print(exalter_name)
    xiwei_ana(my_datelist, exalter_name)
