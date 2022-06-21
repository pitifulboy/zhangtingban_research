from df_manage_func import add_share_msg_to_df
from select_shares import select_share_by_date
import baostock as bs
import pandas as pd
from tushare_to_baostock import baostock_to_tuhshare_sharecode
# 登陆系统
lg = bs.login()
# 获取中证500成分股
rs = bs.query_zz500_stocks()

# 打印结果集
zz500_stocks = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    zz500_stocks.append(rs.get_row_data())
result = pd.DataFrame(zz500_stocks, columns=rs.fields)


# 获取baostock格式的沪深300成分股
zz500_baostock_list = result.code.tolist()
# 将baostock格式的A50成分股，格式转化成tushare格式
zz500_tushare_list = [baostock_to_tuhshare_sharecode(x) for x in zz500_baostock_list]
print(zz500_tushare_list)
# 登出系统
bs.logout()

df_daily = select_share_by_date('20220620')

# 筛选出A50部分股票的交易数据
lhb_df_tracked = df_daily[df_daily.ts_code.isin(zz500_tushare_list)]
print(lhb_df_tracked)
# 添加个股交易信息
lhb_df_tracked_ful_msg = add_share_msg_to_df(lhb_df_tracked)
print(lhb_df_tracked_ful_msg)
