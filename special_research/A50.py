from df_manage_func import add_share_msg_to_df
from select_shares import select_share_by_date

import baostock as bs
import pandas as pd

# 登陆系统
from tushare_to_baostock import baostock_to_tuhshare_sharecode

lg = bs.login()

# 获取上证50成分股
rs = bs.query_sz50_stocks()

# 打印结果集
sz50_stocks = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    sz50_stocks.append(rs.get_row_data())
result = pd.DataFrame(sz50_stocks, columns=rs.fields)
# 结果集输出到csv文件
result.to_csv("D:/sz50_stocks.csv", encoding="gbk", index=False)
# 获取baostock格式的A50成分股
A50_baostock_list = result.code.tolist()
# 将baostock格式的A50成分股，格式转化成tushare格式
A50_tushare_list=[baostock_to_tuhshare_sharecode(x) for x in A50_baostock_list ]
print(A50_tushare_list)
# 登出系统
bs.logout()


df_daily = select_share_by_date('20220620')

# 筛选出A50部分股票的交易数据
lhb_df_tracked = df_daily[df_daily.ts_code.isin(A50_tushare_list)]
print(lhb_df_tracked)
# 添加个股交易信息
lhb_df_tracked_ful_msg = add_share_msg_to_df(lhb_df_tracked)
print(lhb_df_tracked_ful_msg)

