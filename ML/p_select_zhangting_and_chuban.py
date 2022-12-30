# 选定分析周期
from my_time_func import get_my_start_end_date_list
from select_shares import select_shares_period


# 设定起始，结束日期。
date_period = get_my_start_end_date_list('20221101', '20221111', 'tushare')

# 获日期段内，取交易数据
df_date_period = select_shares_period(date_period)

print(df_date_period)
