# 板块信息获取
# 指定日期（日期区间）
# 1、获取交易数据+个股信息数据。
# 2，数据分析整理（当日：板块个股数，板块交易额，板块平均涨幅，涨幅离散度，当日涨幅top5）
#                多日：板块持续性。高标情况。


# 开盘涨幅top6的板块，研究当日开盘涨幅超过2%的个股走势，是否冲击涨停，低位股的后续上涨概率。

# 研究当日开盘涨幅超过2%的个股走势，是否冲击涨停，低位股的后续上涨概率。研究对应的板块


# 板块趋势 + 各股趋势离散度。周期2-5日
from df_manage_func import add_share_msg_to_df
from my_time_func import get_my_start_end_date_list
from select_shares import select_shares_period
import pandas as pd
import numpy as np

# 设定周期
startday = '20220601'
enddate = '20220620'
datelist = get_my_start_end_date_list(startday, enddate, 'tushare')

# 获取周期内交易数据
df_period = select_shares_period(datelist)

# 添加个股信息
share_df_full = add_share_msg_to_df(df_period)

# 基础数据存档
path = r'D:\00 量化交易\\'+startday+'-'+enddate+'个股数据.xlsx'
share_df_full.to_excel(path, sheet_name='1', engine='openpyxl')

# 获取开盘涨幅top6的行业板块

# 透视,按照：行业+日期，交易量，股票数，开盘平均涨幅。
my_df_povit = pd.pivot_table(share_df_full, values=[ 'pct_chg', 'amount'], index='industry',
                             columns='trade_date',
                             aggfunc={'pct_chg': np.mean, 'amount': np.sum})

# 按照选定周期中，第一天的交易降序排列
lhb_df_sorted = my_df_povit.sort_values(by=('amount', startday), ascending=False)

path2 = r'D:\00 量化交易\\'+startday+'-'+enddate+'板块趋势透视分析.xlsx'
lhb_df_sorted.to_excel(path2, sheet_name='1', engine='openpyxl')
