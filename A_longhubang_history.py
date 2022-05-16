import numpy as np

from my_time_func import get_my_startdate_list, get_my_start_end_date_list, get_days_before_tushare
from df_manage_func import add_share_msg_to_df
from select_shares import select_days_longhubang, select_one_share_by_startdate, \
    select_one_day_longhubang, select_one_share_by_longhubang_xiwei
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
            amount = lhb_this_exalter.iloc[i, 3]

            msg_df = [[trade_date, ts_code, name, amount]]
            # 拼接个股信息和数据
            ful_df = msg_df + anay_list
            print(ful_df)
            fina_data_list.append([x for list_elements in ful_df for x in list_elements])

    # 将数据转换为df格式
    data_df = pd.DataFrame(fina_data_list,
                           columns=['上榜日', '代码', '名称', '买入额', '当日开盘涨幅', '当日最大涨幅', '当日最小涨幅', '当日收盘涨幅', '次日开盘涨幅',
                                    '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅'])

    data_df['代码名称'] = data_df['代码'] + data_df['名称']
    data_df['代码名称'] = data_df['代码名称'].str[3:11]

    df_anay = data_df.loc[:, ['上榜日', '代码名称', '买入额', '当日收盘涨幅', '次日开盘涨幅', '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅']]

    # 由于多个原因重复上榜，需要去重
    df_anay_unique = df_anay.drop_duplicates(keep='first')

    '''ava_name = '平均值'
    ava_amount = df_anay_unique['买入额'].mean()
    print(ava_amount)
    ava_1day_kp = df_anay_unique['次日开盘涨幅'].mean()
    print(ava_1day_kp)
    ava_1day_zd = df_anay_unique['次日最大涨幅'].mean()
    print(ava_1day_zd)
    ava_1day_zx = df_anay_unique['次日最小涨幅'].mean()
    print(ava_1day_zx)
    ava_1day_sp = df_anay_unique['次日收盘涨幅'].mean()
    print(ava_1day_sp)

    ava_data_list = ['', ava_name, ava_amount, '', ava_1day_kp, ava_1day_zd, ava_1day_zx, ava_1day_sp]
    ava_df = pd.DataFrame(ava_data_list,
                          columns=['上榜日', '代码名称', '买入额', '当日收盘涨幅', '次日开盘涨幅', '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅'])
    df_anay_fina = pd.concat([df_anay_unique, ava_df], axis=1)

    print(df_anay_fina)'''

    # print(df_anay_unique)

    path = r'D:\00 量化交易\\' + this_exalter + '.xlsx'
    df_anay_unique.to_excel(path, sheet_name='1', engine='openpyxl')
