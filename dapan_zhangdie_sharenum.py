import pandas as pd
from select_shares import select_shares_period


def get_dapan_zhangdie_num(startdate, enddate):
    # 生成日期dataframe
    daylist = pd.date_range(start=startdate, end=enddate)
    daylist_new = [x.strftime('%Y%m%d') for x in daylist]
    df_period = select_shares_period(daylist_new)

    data_list = []
    for day in range(0, len(daylist_new)):
        thisday = daylist_new[day]
        df = df_period.loc[df_period.trade_date == thisday]

        l = len(df)
        up_num = 0
        down_num = 0

        if len(df) > 0:

            for i in range(l):
                pre_close = df.iloc[i].pre_close
                close = df.iloc[i].close
                if close >= pre_close:
                    up_num = up_num + 1
                else:
                    down_num = down_num + 1

            data_list.append([thisday, up_num, down_num])
    return data_list
