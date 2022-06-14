# 查询今日交易数据
from my_time_func import get_my_start_end_date_list
from select_shares import select_share_by_date, select_zhangtingban_df


# 5月科创板/创业板表现研究
def money_flow_oneday(querydate):
    # 当日交易数据
    today_trade_df = select_share_by_date(querydate)

    # 判断当日是否交易
    if len(today_trade_df) == 0:
        pass
    else:
        print(querydate + '日交易额分布')
        # 创业板，科创板，主板，北交所

        df_amount = today_trade_df.amount.sum()
        # 转化成 亿
        df_amount_yi = '% 0.2f' % (float(df_amount) / 100000)
        print('大盘交易额：' + df_amount_yi + '亿')

        # 创业板部分,代码以3开头
        df_3 = today_trade_df[today_trade_df.ts_code.str.startswith('3')]
        df_3_amount = df_3.amount.sum()
        # 转化成 亿
        df_3_amount_yi = '% 0.2f' % (float(df_3_amount) / 100000)
        print('创业板交易额：' + df_3_amount_yi + '亿')

        # 科创板部分,代码以68开头
        df_68 = today_trade_df[today_trade_df.ts_code.str.startswith('68')]
        df_68_amount = df_68.amount.sum()
        # 转化成 亿
        df_68_amount_yi = '% 0.2f' % (float(df_68_amount) / 100000)
        print('科创板交易额：' + df_68_amount_yi + '亿')

        # 北交所 4，8开头
        df_48 = today_trade_df[today_trade_df.ts_code.str.startswith('4') | today_trade_df.ts_code.str.startswith('8')]
        df_48_amount = df_48.amount.sum()
        # 转化成 亿
        df_48_amount_yi = '% 0.2f' % (float(df_48_amount) / 100000)
        print('北交所交易额：' + df_48_amount_yi + '亿')


# 查询多日连板天梯
def kc68_date_list(startday, enddaste):
    t = get_my_start_end_date_list(startday, enddaste, 'tushare')
    print('交易额分析')
    for i in range(len(t)):
        money_flow_oneday(t[i])


kc68_date_list('20220601', '20220613')
