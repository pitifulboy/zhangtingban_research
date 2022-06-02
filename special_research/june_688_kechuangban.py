# 查询今日交易数据
from my_time_func import get_my_start_end_date_list
from select_shares import select_share_by_date, select_zhangtingban_df


# 5月科创板表现研究
def kc68_one_day(querydate):
    today_trade_df = select_share_by_date(querydate)

    # 截止日涨停股票list
    ztb_df = select_zhangtingban_df(querydate)

    # 判断当日是否交易
    if len(today_trade_df) == 0:
        pass
    else:

        # 科创板部分,代码以68开头
        df_68 = today_trade_df[today_trade_df.ts_code.str.startswith('30')]
        # print(df_68)
        # 交易额统计，tushare数据中，交易额单位是 千
        df_68_amount = df_68.amount.sum()
        # 转化成 亿
        df_68_amount_yi = '% 0.2f' % (float(df_68_amount) / 100000)
        print(querydate)
        print(df_68_amount_yi)

        # 科创板涨停部分
        ztb_df_68 = ztb_df[ztb_df.ts_code.str.startswith('30')]

        print(ztb_df_68)


# 查询多日连板天梯
def kc68_date_list(startday, enddaste):
    t = get_my_start_end_date_list(startday, enddaste, 'tushare')
    for i in range(len(t)):
        kc68_one_day(t[i])


kc68_date_list('20220501', '20220601')
