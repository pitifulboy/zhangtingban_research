from A_lbtt_strategy import oneday_lbtt
from select_shares import select_zhangtingban_df, select_share_by_date, select_zhaban_df, select_dietingban_df


def qinxu_oneday(querday):
    # 今日总交易额
    total_df = select_share_by_date(querday)
    total_df_amount = '% .2f ' % (total_df.amount.sum() / 100000)

    # 涨停板
    zhangtingban_df = select_zhangtingban_df(querday)
    # 涨停个股交易额
    zhangtingban_df_amount = '% .2f ' % (zhangtingban_df.amount.sum() / 100000)
    n_zhangtingban_df = len(zhangtingban_df)

    # 连板
    lb_df = oneday_lbtt(querday)
    n_lb_df = len(lb_df)

    # 炸板
    zhaban_df = select_zhaban_df(querday)
    zhaban_df_amount = '% .2f ' % (zhaban_df.amount.sum() / 100000)
    n_zha_df = len(zhaban_df)

    # 跌停
    dieting_list = select_dietingban_df(querday)
    n_dieting = len(dieting_list)

    # print(str(date_list_format[i]) + '日，超短情绪指标')
    print('A股今日交易额：' + str(total_df_amount) + '亿')

    print('-------------------------------')
    print('今日涨停:' + str(n_zhangtingban_df) + '个')
    print('其中连板:' + str(n_lb_df) + '个')

    print('涨停个股今日交易额：' + str(zhangtingban_df_amount) + '亿')

    print('-------------------------------')
    print('炸板：' + str(n_zha_df) + '个')
    print('炸板个股今日交易额：' + str(zhaban_df_amount) + '亿')
    print('跌停：' + str(n_dieting) + '个')

    print('-------------------------------')
    print('备注：忽略部分ST个股。')


'''qinxu_oneday('20220509')'''


