import pandas as pd
from select_shares import select_shares_period
from my_time_func import date_list_gen_tushare_n


# 指定日期的，n天振幅榜
def calculate_wave(day_count, select_date):
    date_list = date_list_gen_tushare_n(day_count + 8, select_date)
    df_data = select_shares_period(date_list)

    # 指定日期有交易的股票数据
    df_data_select_date = df_data.loc[df_data['trade_date'] == select_date]
    n = len(df_data_select_date)

    mylist = []
    for x in range(n):

        sharecode_select_date = df_data_select_date.ts_code.iloc[x]
        share_data_period = df_data.loc[df_data['ts_code'] == sharecode_select_date]

        if len(share_data_period) < day_count + 1:
            mylist.append([select_date, sharecode_select_date, '0.0'])
            continue
        sum_total = 0.0

        # mysql中是倒序排列的
        for j in range(0, day_count):
            high = share_data_period.high.iloc[-day_count + j]
            low = share_data_period.low.iloc[-day_count + j]
            pre_close = share_data_period.pre_close.iloc[-day_count + j]
            wave = float("%.2f" % ((high - low) / pre_close * 100))
            # print(str(sharecode_select_date) + "第" + str(day_count -j) + "天振幅" + str(wave) + 'high' + str(high) + 'low' + str(low) + 'pre_close' + str(pre_close))
            sum_total += wave

        mylist.append([select_date, sharecode_select_date, ("%.2f" % sum_total)])

        # print(str(x + 1) + "个" + str(sharecode_select_date) + str(sum_total))

    df = pd.DataFrame(mylist, columns=['tradedate', 'sharecode', str(day_count) + '_day_wave'])
    df[str(day_count) + '_day_wave'] = df[str(day_count) + '_day_wave'].astype('float')

    return df


# 指定日期的，n天涨幅榜
def calculate_change_percent(day_count, select_date):
    date_list = date_list_gen_tushare_n(day_count + 8, select_date)
    df_data = select_shares_period(date_list)

    # 指定日期有交易的股票数据
    df_data_select_date = df_data.loc[df_data['trade_date'] == select_date]
    n = len(df_data_select_date)

    mylist = []
    for x in range(n):

        sharecode_select_date = df_data_select_date.ts_code.iloc[x]
        share_data_period = df_data.loc[df_data['ts_code'] == sharecode_select_date]

        if len(share_data_period) < day_count + 1:
            mylist.append([select_date, sharecode_select_date, '0.0'])
            continue
        sum_total = 0.0

        # mysql中是倒序排列的
        for j in range(0, day_count):
            close = share_data_period.close.iloc[-day_count + j]
            pre_close = share_data_period.pre_close.iloc[-day_count + j]
            wave = float("%.2f" % ((close - pre_close) / pre_close * 100))
            # print(str(sharecode_select_date) + "第" + str(day_count -j) + "天振幅" + str(wave) + 'high' + str(high) + 'low' + str(low) + 'pre_close' + str(pre_close))
            sum_total += wave

        mylist.append([select_date, sharecode_select_date, ("%.2f" % sum_total)])

        # print(str(x + 1) + "个" + str(sharecode_select_date) + str(sum_total))

    df = pd.DataFrame(mylist, columns=['tradedate', 'sharecode', str(day_count) + '_day_change_percent'])
    df[str(day_count) + '_day_change_percent'] = df[str(day_count) + '_day_change_percent'].astype('float')

    return df


'''
df = calculate_change_percent(3, '20220408')
print(df.sort_values(by=str(3)+'_day_change_percent', ascending=False).head(20))'''
