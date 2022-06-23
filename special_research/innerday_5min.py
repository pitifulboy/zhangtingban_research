# 1，分析收盘涨幅大于5%的个股，当天前10分钟量比。根据量比筛选全部个股，判断根据10点以前量比，是否能抓住牛股
# 2，分析最大涨幅大于5%个股，第二天表现
import numpy as np
import pandas as pd

from my_time_func import get_days_before_tushare
from select_5m_data import select_5m_data_by_date
from select_shares import select_share_by_date

# 获取当日所有个股交易数据
from tushare_to_baostock import tuhshare_date_to_baostock, baostock_date_to_tuhshare, baostock_to_tuhshare_sharecode

research_date = '20220621'

daily_data = select_share_by_date(research_date)
print(daily_data)
# 筛选当日涨幅大于5%的个股
daily_data_biger5 = daily_data[daily_data['pct_chg'] > 4.99]
print(daily_data_biger5)

# 获取日期的前一日
research_date_1day_before = get_days_before_tushare(research_date, 1)
daily_data_1day_before = select_share_by_date(research_date_1day_before)

share_list = daily_data_biger5['ts_code'].tolist()
# 筛选当日涨幅大于5%的个股，的前一天交易数据
daily_data_1day_before_biger5 = daily_data_1day_before[daily_data_1day_before['ts_code'].isin(share_list)]
print(daily_data_1day_before_biger5)

# 获取当日5分钟交易数据
# 日期转换
trade_date_baostock = tuhshare_date_to_baostock(research_date)
# 将日期转换成baostock格式
df_5m_oneday = select_5m_data_by_date(trade_date_baostock)

# 调整5m交易数据格式，便于后续分析
df_5m_oneday['code'] = df_5m_oneday['code'].apply(baostock_to_tuhshare_sharecode)
df_5m_oneday['time'] = df_5m_oneday['time'].apply(lambda x: x[8:12])
# 单位转换为“千”，与tushare保持一致
df_5m_oneday['amount'] = df_5m_oneday['amount'].apply(lambda x: float(x) / 1000)

# 提取前30分钟部分的数据
timelist = ['0935', '0940', ',0945', '0950', '0955', '1000']
df_5m_oneday_first30min = df_5m_oneday[df_5m_oneday['time'].isin(timelist)]
# 透视汇总
df_5m_oneday_first30min_povit = pd.pivot_table(df_5m_oneday_first30min, index='code', values='amount',
                                               aggfunc={'amount': np.sum})

print(df_5m_oneday_first30min_povit)

# 将tushare 交易数据和 5m数据汇总
df = pd.merge(left=daily_data_1day_before_biger5, right=df_5m_oneday_first30min_povit, left_on='ts_code',
              right_on='code')
df['liangbi'] = df['amount_y'] / df['amount_x']

path = r'D:\00 量化交易\\' + '前30分钟量比研究' + '.xlsx'
df.to_excel(path, sheet_name='前30分钟量比研究', engine='openpyxl')

print(df)


# 全部股票，前30分钟量比占比
# 将tushare 交易数据和 5m数据汇总
df_ful = pd.merge(left=daily_data_1day_before, right=df_5m_oneday_first30min_povit, left_on='ts_code',
              right_on='code')

df_ful['liangbi'] = df_ful['amount_y'] / df_ful['amount_x']

path2 = r'D:\00 量化交易\\' + '大盘前30分钟量比研究' + '.xlsx'
df_ful.to_excel(path2, sheet_name='大盘前30分钟量比研究', engine='openpyxl')

