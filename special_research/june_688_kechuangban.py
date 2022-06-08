# 查询今日交易数据
from my_time_func import get_my_start_end_date_list
from select_shares import select_share_by_date, select_zhangtingban_df


# 5月科创板/创业板表现研究
def kc68_one_day(querydate, market_type):
    if market_type == 'kechuang':
        market_str = '68'
    elif market_type == 'chuangye':
        market_str = '3'

    today_trade_df = select_share_by_date(querydate)

    # 截止日涨停股票list
    ztb_df = select_zhangtingban_df(querydate)

    # 判断当日是否交易
    if len(today_trade_df) == 0:
        pass
    else:

        # 科创板部分,代码以68开头
        df_68 = today_trade_df[today_trade_df.ts_code.str.startswith(market_str)]
        # print(df_68)
        # 交易额统计，tushare数据中，交易额单位是 千
        df_68_amount = df_68.amount.sum()
        # 转化成 亿
        df_68_amount_yi = '% 0.2f' % (float(df_68_amount) / 100000)
        print(querydate + '日，交易额：' + df_68_amount_yi + '亿')

        # 科创板涨停部分
        ztb_df_68 = ztb_df[ztb_df.ts_code.str.startswith(market_str)]
        if len(ztb_df_68) == 0:
            print('此版块，今日无涨停。')
        else:
            print('此版块，今日涨停个股明细:')
            print(ztb_df_68)


# 查询多日连板天梯
def kc68_date_list(startday, enddaste):
    t = get_my_start_end_date_list(startday, enddaste, 'tushare')
    print('交易额+涨停板分析')
    for i in range(len(t)):
        #  kc68_one_day(t[i], 'kechuang')
        kc68_one_day(t[i], 'chuangye')


kc68_date_list('20220601', '20220602')
