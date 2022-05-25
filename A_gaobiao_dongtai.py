#  1-n日 涨幅计算top50
from df_manage_func import add_share_msg_to_df
from my_time_func import get_my_enddate_list, get_today_date
from select_shares import select_shares_period
import pandas as pd


def caculate_ndays_zhangfu(n_days):
    # 不考虑45个自然日之前，没交易的个股。

    today_date = get_today_date('tushare')
    # 生成日期list
    date_period = get_my_enddate_list(today_date, n_days, 'tushare')
    # 获日期段内，取交易数据
    df_date_period = select_shares_period(date_period)

    # 获取指定日期段中，最早的交易日期
    min_date = df_date_period.trade_date.min()
    # 以最早日期有交易个股为基准，进行计算。不考虑日期段上市的新股
    df_min_date = df_date_period.loc[df_date_period['trade_date'] == min_date]
    # 周期起始日，有交易个股list
    ts_code_list_min_date = df_min_date.ts_code.tolist()

    # 先确定最大值，和最小值。分别求：最大值左侧最小值，并计算涨幅；最小值右侧最大值，并计算涨幅。比较2个涨幅，确定最大涨幅。
    # len(ts_code_list_min_date)
    data_list = []
    for i in range(0, len(ts_code_list_min_date)):
        # 根据个股代码遍历，获取个股代码
        df_cacul_ts_code = df_date_period.loc[df_date_period['ts_code'] == ts_code_list_min_date[i]]

        # 获取最小，最大index名称，方便切片
        lowest = df_cacul_ts_code.low.min()
        # 最后一个交易额收盘价
        x = df_cacul_ts_code.iloc[-1, 5]

        # 涨幅
        pct_chg = '%0.2f' % (x / lowest * 100 - 100)
        print([ts_code_list_min_date[i], pct_chg])
        data_list.append([ts_code_list_min_date[i], pct_chg])

    mycolumns = ['ts_code', 'max_zhangfu']
    df_result = pd.DataFrame(data=data_list, columns=mycolumns).astype({'max_zhangfu': 'float'})
    df_result_sorted = df_result.sort_values(by='max_zhangfu', ascending=False)
    # 添加个股信息
    df_full_msg = add_share_msg_to_df(df_result_sorted)

    # 最新一日交易数据
    # 获取指定日期段中，最早的交易日期
    max_date = df_date_period.trade_date.max()
    # 以最早日期有交易个股为基准，进行计算。不考虑日期段上市的新股
    df_max_date = df_date_period.loc[df_date_period['trade_date'] == max_date]

    df_add_new_tradedata = pd.merge(left=df_full_msg, right=df_max_date, on='ts_code')
    df_result_final = df_add_new_tradedata.loc[:, [ 'name', 'industry', 'max_zhangfu', 'pct_chg']]
    df_result_final.columns = [ '名称', '板块', str(n_days) + '日涨幅', '今日涨幅']
    print(df_result_final.keys())
    # 调整数据格式
    # df_result_final['代码'] = df_result_final['代码'].map(lambda x: x[-6:-3])
    df_result_final['名称'] = df_result_final['名称'].map(lambda x: x[:-2])
    df_result_final['今日涨幅'] = df_result_final['今日涨幅'].map(lambda x: '%0.2f' % x)
    df_result_final[str(n_days) + '日涨幅'] = df_result_final[str(n_days) + '日涨幅'].map(lambda x: '%0.2f' % x)

    path = r'D:\00 量化交易\\' + str(n_days) + '日高标动态.xlsx'
    df_result_final.to_excel(path, sheet_name='1', engine='openpyxl')

    print(df_result_final.head(100))
    return df_result_final


def caculate_gaobiao_7_14():
    caculate_ndays_zhangfu(14)
    caculate_ndays_zhangfu(7)
