# 读取区间交易数据
# 生成日期dataframe
import pandas as pd

from classify_shares_market import get_zhangdie_limit
from df_manage_func import add_share_msg_to_df
from select_shares import select_shares_period

startdate = '20220101'
enddate = '20220726'

daylist = pd.date_range(start=startdate, end=enddate)
daylist_new = [x.strftime('%Y%m%d') for x in daylist]
df_period = select_shares_period(daylist_new)

# 获取个股涨跌幅
df_period['limit_zhagndie'] = df_period['ts_code'].apply(get_zhangdie_limit)
# 获取涨停价,并调整格式
df_period['zhangtingjia'] = (
    (df_period['pre_close'] * (1 + df_period['limit_zhagndie'])).apply(lambda x: '%0.2f' % x)).astype('float')
# 判断收盘价是否与涨停价相等
df_period['是否涨停'] = df_period['zhangtingjia'] - df_period['close']
df_zt = df_period[df_period['是否涨停'] == 0.00]
df_zt.loc[:, '连板数'] = 1

# 默认每天都有涨停板，获取交易日历。升序排列
trade_date_list = sorted(list(set(df_period.trade_date.tolist())))
for i in range(1, len(trade_date_list)):

    # 当日涨停df
    thisday = trade_date_list[i]
    print(thisday)
    df_zt_thisday = df_zt[df_zt.trade_date == thisday]

    # 如果昨日涨停，连板数等于昨日连板数+1
    lastday = trade_date_list[i - 1]
    # 昨日涨停数据
    df_zt_lastday = df_zt[df_zt.trade_date == lastday]
    # 昨日涨停个股list
    df_zt_lastday_list = df_zt_lastday.ts_code.tolist()

    # 选取连板
    df_zt_lianban = df_zt_thisday[df_zt_thisday.ts_code.isin(df_zt_lastday_list)]
    lianban_list = df_zt_lianban.ts_code.tolist()
    print(lianban_list)

    # 连板数 = 昨日连板数+1
    for j in range(0, len(lianban_list)):
        share_tscode = lianban_list[j]
        print(share_tscode)
        # 前一日连板
        df_lastday_lb = df_zt_lastday[df_zt_lastday['ts_code'] == share_tscode].copy()
        lastday_lb_num = df_lastday_lb.iloc[0, 14]

        df_zt['连板数'].loc[(df_zt['ts_code'] == share_tscode) & (df_zt['trade_date'] == thisday)] = lastday_lb_num + 1
        print(df_zt['连板数'].loc[(df_zt['ts_code'] == share_tscode) & (df_zt['trade_date'] == thisday)])

path = r'D:\00 量化交易\\2022年7月28日接力连板分析.xlsx'
resultdf=add_share_msg_to_df(df_zt)
resultdf.to_excel(path, sheet_name='1', engine='openpyxl')
