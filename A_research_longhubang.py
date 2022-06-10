import numpy as np
from my_time_func import get_my_start_end_date_list
from df_manage_func import add_share_msg_to_df
from select_shares import select_days_longhubang, select_one_share_by_startdate, select_one_day_longhubang
import pandas as pd


# 根据席位查询历史龙虎榜
def query_longhubang_by_exalter(exalter):
    my_datelist = get_my_start_end_date_list('20220401', '20220429', 'tushare')
    # 获取全部龙虎榜数据
    lhb_df = select_days_longhubang(my_datelist).fillna(value='0')
    # 根据席位 查询买入上榜记录
    df_i = lhb_df.loc[(lhb_df['exalter'] == exalter) & (lhb_df['side'] == '0')]
    # 按照日期倒序排列
    df_i_sorted = df_i.sort_values(by='trade_date', ascending=False, ignore_index=True)

    # 添加个股信息
    share_df_full = add_share_msg_to_df(df_i_sorted)
    share_df_full_partvalues = share_df_full.loc[:, ['trade_date', 'ts_code', 'name', 'buy', 'exalter']]

    return share_df_full_partvalues


# 匹配交易数据，分析龙虎榜日榜次日表现。
def xiwei_ana(my_datelist, this_exalter):
    # 获取该席位龙虎榜买入记录
    my_longhubang_datelist = select_days_longhubang(my_datelist)

    lhb_this_exalter = my_longhubang_datelist.loc[
        (my_longhubang_datelist['exalter'] == this_exalter) & (my_longhubang_datelist['side'] == '0')]

    fina_data_list = []

    for i in range(0, len(lhb_this_exalter)):

        # 上榜后表现数据
        share_after_lhb = select_one_share_by_startdate(lhb_this_exalter.iloc[i, 1], lhb_this_exalter.iloc[i, 0])

        # 分析上榜后n日数据
        num_day = 2
        #  添加股票信息,保留3个交易日数据
        share_after_lhb_ful_msg = add_share_msg_to_df(share_after_lhb).head(num_day)

        # 保留待分析信息
        share_after_lhb_part = share_after_lhb_ful_msg.loc[:,
                               ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'name']]
        anay_list = []
        # 计算上榜后1日，开盘涨幅，最大涨幅，最大跌幅，收盘涨幅，

        # print(share_after_lhb_part)

        if len(share_after_lhb_part) < 2:
            pass
        else:
            for j in range(0, num_day):
                open_this = float(share_after_lhb_part.loc[j, 'open'])
                high_this = float(share_after_lhb_part.loc[j, 'high'])
                low_this = float(share_after_lhb_part.loc[j, 'low'])
                close_this = float(share_after_lhb_part.loc[j, 'close'])
                pre_close_this = float(share_after_lhb_part.loc[j, 'pre_close'])

                # print(open_this, high_this, low_this, close_this, pre_close_this)
                # 开盘涨幅
                kp_zf = float('%.2f' % (open_this / pre_close_this * 100 - 100))
                # 最大涨幅
                zd_zf = float('%.2f' % (high_this / pre_close_this * 100 - 100))
                # 最小涨幅
                zx_zf = float('%.2f' % (low_this / pre_close_this * 100 - 100))
                # 收盘涨幅
                sp_zf = float('%.2f' % (close_this / pre_close_this * 100 - 100))

                anay_list.append([kp_zf, zd_zf, zx_zf, sp_zf])

            # 将信息和数据汇总
            ts_code = share_after_lhb_part.iloc[0, 0]
            # 龙虎榜日期
            trade_date = share_after_lhb_part.iloc[0, 1]

            name = share_after_lhb_part.iloc[0, 7]

            # 上榜买入金额
            amount = '%.0f' % float(lhb_this_exalter.iloc[i, 3])

            msg_df = [[this_exalter, trade_date, ts_code, name, amount]]
            # 拼接个股信息和数据
            ful_df = msg_df + anay_list
            print(ful_df)
            fina_data_list.append([x for list_elements in ful_df for x in list_elements])

    # 将数据转换为df格式
    data_df = pd.DataFrame(fina_data_list,
                           columns=['席位', '上榜日', '代码', '名称', '买入额', '当日开盘涨幅', '当日最大涨幅', '当日最小涨幅', '当日收盘涨幅', '次日开盘涨幅',
                                    '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅'])

    # data_df['代码名称'] = data_df['代码'] + data_df['名称']
    # data_df['代码名称'] = data_df['代码名称'].str[3:11]
    # df_anay = data_df.loc[:, ['席位', '上榜日', '代码名称', '买入额', '当日收盘涨幅', '次日开盘涨幅', '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅']]

    # 由于多个原因重复上榜，需要去重
    df_anay_unique = data_df.drop_duplicates(keep='first')

    '''
    print(df_anay_unique)
    path = r'D:\00 量化交易\\' + this_exalter + '.xlsx'
    df_anay_unique.to_excel(path, sheet_name='1', engine='openpyxl')
    '''

    return df_anay_unique


# 龙虎榜数据透视，【上榜次数，交易金额，平均交易金额】

def lhb_fenxi(data_df):
    # 选定买入的数据部分,去重多个原因上榜。
    my_lhb_side0 = data_df.loc[data_df['side'] == '0'].loc[:,
                   ['trade_date', 'ts_code', 'exalter', 'buy']]

    # 由于多个原因重复上榜，需要去重
    my_lhb_side0_unique = my_lhb_side0.drop_duplicates(keep='first')

    print(my_lhb_side0)

    path = r'D:\00 量化交易\\' + '当前周期龙虎榜汇总' + '.xlsx'
    my_lhb_side0_unique.to_excel(path, sheet_name='4月龙虎榜打板情况统计', engine='openpyxl')

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
    lhb_df_sorted.to_excel(path2, sheet_name='4月打板数据透视', engine='openpyxl')

    return lhb_df_sorted


def monthly_lhb_analysis():
    # 选定分析周期
    my_datelist = get_my_start_end_date_list('20220401', '20220429', 'tushare')

    # 获取龙虎榜当日榜数据
    lhb_data = select_days_longhubang(my_datelist)
    # 透视上榜次数，金额，平均金额
    toushi_df = lhb_fenxi(lhb_data)
    # 筛选部分席位，减小计算量
    top_exalter_povittable = toushi_df.loc[
        (toushi_df.exalter.astype('int') < 50) & (toushi_df.exalter.astype('int') > 5)]

    # 4月上榜次数超过9次的

    dfs = []
    # len(top_exalter_povittable)
    for i in range(0, len(top_exalter_povittable)):
        print('还剩')
        print(len(top_exalter_povittable) - i)
        # 单个席位查询计算
        exalter_name = top_exalter_povittable.index[i]
        # 执行查询计算
        df_exalter_name = xiwei_ana(my_datelist, exalter_name)
        print(df_exalter_name)
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

    lhb_df_povit_as_type = lhb_df_povit.astype({'买入额': 'float'})
    lhb_df_sorted = lhb_df_povit_as_type.sort_values(by='买入额', ascending=False)

    # 导出结果
    path2 = r'D:\00 量化交易\\汇总透视.xlsx'
    lhb_df_sorted.to_excel(path2, sheet_name='1', engine='openpyxl')

    # 根据次日最大涨幅，筛选涨幅大于6%的席位。追踪此部分席位


def weekly_lhb_analysis(my_datelist):
    # 获取龙虎榜当日榜数据
    lhb_data = select_days_longhubang(my_datelist)
    # 透视上榜次数，金额，平均金额
    toushi_df = lhb_fenxi(lhb_data)
    # 筛选部分席位，减小计算量
    top_exalter_povittable = toushi_df.loc[
        (toushi_df.exalter.astype('int') < 35) & (toushi_df.exalter.astype('int') > 10)]

    dfs = []
    # len(top_exalter_povittable)
    for i in range(0, len(top_exalter_povittable)):
        print('还剩')
        print(len(top_exalter_povittable) - i)
        # 单个席位查询计算
        exalter_name = top_exalter_povittable.index[i]
        # 执行查询计算
        df_exalter_name = xiwei_ana(my_datelist, exalter_name)
        print(df_exalter_name)
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


my_datelist = get_my_start_end_date_list('20220509', '20220608', 'tushare')
weekly_lhb_analysis(my_datelist)

