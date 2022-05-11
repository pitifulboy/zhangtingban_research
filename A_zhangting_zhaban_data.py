from A_lbtt_strategy import oneday_lbtt
from my_time_func import get_my_enddate_list
from select_shares import select_share_by_date, select_zhangtingban_df, select_zhaban_df, select_dietingban_df


def qinxu_jiaoyie_oneday(querday):
    # 今日总交易额
    total_df = select_share_by_date(querday)
    total_df_amount = '% .2f ' % (total_df.amount.sum() / 100000)

    # 涨停板
    zhangtingban_df = select_zhangtingban_df(querday)
    # 涨停个股交易额
    zhangtingban_df_amount = '% .2f ' % (zhangtingban_df.amount.sum() / 100000)
    n_zhangtingban_df = len(zhangtingban_df)

    # 炸板
    zhaban_df = select_zhaban_df(querday)
    zhaban_df_amount = '% .2f ' % (zhaban_df.amount.sum() / 100000)
    n_zha_df = len(zhaban_df)
    # 日期，大盘交易额，涨停交易额，涨停数，炸板交易额，炸板数
    datalist = [querday, total_df_amount, zhangtingban_df_amount, n_zhangtingban_df, zhaban_df_amount,
                n_zha_df]
    return datalist


datelist = get_my_enddate_list('20220510', 26, 'tushare')

data_all = []
for i in range(0, len(datelist)):
    x = qinxu_jiaoyie_oneday(datelist[i])
    if x[1] != '0.00':
        data_all.append(x)
        print(x)
print(data_all)
