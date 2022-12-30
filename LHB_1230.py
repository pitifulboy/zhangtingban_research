import numpy as np
from my_time_func import get_my_start_end_date_list, datelist_add_days
from df_manage_func import add_share_msg_to_df
from select_shares import select_days_longhubang, select_one_share_by_startdate, select_data_by_shareslist_startdate, \
    select_data_by_shareslist_datelist
import pandas as pd


# 匹配交易数据，分析龙虎榜日榜次日表现。
def xiwei_ana(my_datelist, this_exalter):
    # 获取该席位龙虎榜买入记录
    my_longhubang_datelist = select_days_longhubang(my_datelist)

    #  datalist_add 在原日期list基础上增加天数。由于是分析涨停后1日内涨幅，因此需要在指定龙虎榜日期基础上增加1个交易日。
    # 为节约工作量，默认增加3天（只考虑周末的影响），其他情况手动增加天数。

    my_tradedate_datelist = datelist_add_days(my_longhubang_datelist, 3)

    print(my_tradedate_datelist)
    lhb_sharelist = ['688787.SH', '000821.SZ']
    # 获取目标交易日期的目标个股的交易数据
    trade_data_datelist = select_data_by_shareslist_datelist(my_tradedate_datelist, lhb_sharelist)
    print(trade_data_datelist)
















# 龙虎榜数据透视，【上榜次数，交易金额，平均交易金额】

def lhb_fenxi(data_df):
    # 选定买入的数据部分,去重多个原因上榜。
    my_lhb_side0 = data_df.loc[data_df['side'] == '0'].loc[:,
                   ['trade_date', 'ts_code', 'exalter', 'buy']]

    # 由于多个原因重复上榜，需要去重
    my_lhb_side0_unique = my_lhb_side0.drop_duplicates(keep='first')

    print(my_lhb_side0)

    path = r'D:\00 量化交易\\' + '当前周期龙虎榜汇总' + '.xlsx'
    my_lhb_side0_unique.to_excel(path, sheet_name='龙虎榜打板情况统计', engine='openpyxl')

    # 透视,统计上榜次数和金额
    lhb_df_povit = pd.pivot_table(my_lhb_side0_unique, index='exalter', values='buy',
                                  aggfunc={'exalter': np.count_nonzero, 'buy': np.sum})

    '''
    设置dataframe格式，涨跌幅小数点后2位，交易额以万为单位
    '''

    # 排序,按照买入交易额降序
    lhb_df_sorted = lhb_df_povit.fillna(0).sort_values(by='buy', ascending=False)

    print(lhb_df_sorted)
    '''
       设置dataframe格式，涨跌幅小数点后2位，交易额以万为单位
    '''

    path2 = r'D:\00 量化交易\\' + '当前周期龙虎榜透视表' + '.xlsx'
    lhb_df_sorted.to_excel(path2, sheet_name='打板数据透视', engine='openpyxl')

    return lhb_df_sorted


def lhb_analysis(my_datelist):
    # 获取指定周期内，龙虎榜数据
    lhb_data = select_days_longhubang(my_datelist)
    print(lhb_data)
    # 透视上榜次数，金额，平均金额
    toushi_df = lhb_fenxi(lhb_data)
    # 按照席位出现次数筛选，减小计算量
    top_exalter_povittable = toushi_df.loc[
        (toushi_df.exalter.astype('int') < 35) & (toushi_df.exalter.astype('int') > 10)]

    dfs = []

    # 遍历筛选过后的席位
    for i in range(0, len(top_exalter_povittable)):
        print('还剩席位数：')
        print(len(top_exalter_povittable) - i)
        # 单个席位查询计算
        exalter_name = top_exalter_povittable.index[i]
        print('计算中的席位：')
        print(df_exalter_name)
        # 执行查询计算
        df_exalter_name = xiwei_ana(my_datelist, exalter_name)

        # 结果汇总
        dfs.append(df_exalter_name)

    alldata = pd.concat(dfs)
    print(alldata)

    # 导出结果
    path = r'D:\00 量化交易\\汇总.xlsx'
    alldata.to_excel(path, sheet_name='1', engine='openpyxl')

    alldata_as_type = alldata.astype({'买入额': 'float'})

    # 透视,统计上榜次数和金额
    lhb_df_povit = pd.pivot_table(alldata_as_type, index='席位',
                                  values=['买入额', '当日收盘涨幅', '次日开盘涨幅', '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅'],
                                  aggfunc={'席位': np.count_nonzero, '买入额': np.sum, '当日收盘涨幅': np.average,
                                           '次日开盘涨幅': np.average, '次日最大涨幅': np.average, '次日最小涨幅': np.average,
                                           '次日收盘涨幅': np.average})

    lhb_df_sorted = lhb_df_povit.sort_values(by='买入额', ascending=False)

    # 导出结果
    path2 = r'D:\00 量化交易\\汇总透视.xlsx'
    lhb_df_sorted.to_excel(path2, sheet_name='1', engine='openpyxl')


my_datelist = get_my_start_end_date_list('20221201', '20221229', 'tushare')
lhb_analysis(my_datelist)
