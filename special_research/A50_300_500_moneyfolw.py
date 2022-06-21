# 当日交易数据
import numpy as np
import pandas as pd
from df_manage_func import add_share_msg_to_df
from my_time_func import get_my_start_end_date_list
from select_shares import select_share_by_date, select_A50, select_hs300, select_zz500, select_shares_period


# 交易市场资金变化
def a50_300_500_money_flow(datelist):
    # 获取A50个股
    a50 = select_A50()
    # 获取沪深300个股
    hs300 = select_hs300()
    # 获取中证500个股
    zz500 = select_zz500()
    # 获取交易数据
    today_trade_df = select_shares_period(datelist)

    # 获取A50个股交易数据
    a50_today_trade_df_ful_msg = pd.merge(left=a50, right=today_trade_df, left_on='code', right_on='ts_code')
    # 市场透视
    a50_my_df_povit = pd.pivot_table(a50_today_trade_df_ful_msg, columns='trade_date', values='amount',
                                     aggfunc=np.sum, margins=False)
    print(a50_my_df_povit)

    # 获取沪深300个股交易数据
    hs300_today_trade_df_ful_msg = pd.merge(left=hs300, right=today_trade_df, left_on='code', right_on='ts_code')
    # 市场透视
    hs300_my_df_povit = pd.pivot_table(hs300_today_trade_df_ful_msg, columns='trade_date', values='amount',
                                     aggfunc=np.sum, margins=False)
    print(hs300_my_df_povit)

    # 获取中证500个股交易数据
    zz500_today_trade_df_ful_msg = pd.merge(left=zz500, right=today_trade_df, left_on='code', right_on='ts_code')
    # 市场透视
    zz500_my_df_povit = pd.pivot_table(zz500_today_trade_df_ful_msg, columns='trade_date', values='amount',
                                       aggfunc=np.sum, margins=False)
    print(zz500_my_df_povit)


mydatelist = get_my_start_end_date_list('20220608', '20220621', 'tushare')

a50_300_500_money_flow(mydatelist)
