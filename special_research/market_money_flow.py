from df_manage_func import add_share_msg_to_df
from my_time_func import get_my_start_end_date_list
from select_shares import select_shares_period
import pandas as pd
import numpy as np


# 交易市场资金变化
def days_money_flow(datelist):
    # 交易数据
    today_trade_df = select_shares_period(datelist)
    # 添加个股信息
    today_trade_df_ful_msg = add_share_msg_to_df(today_trade_df)
    # 市场透视
    my_df_povit = pd.pivot_table(today_trade_df_ful_msg, index='market', columns='trade_date', values='amount',
                                 aggfunc=np.sum, margins=False)
    print(my_df_povit)

    my_df_povit_industry = pd.pivot_table(today_trade_df_ful_msg, index='industry', columns='trade_date',
                                          values='amount',
                                          aggfunc=np.sum, margins=False)
    print(my_df_povit_industry.sort_values(by='industry', ascending=False))

    return my_df_povit


mydatelist = get_my_start_end_date_list('20220608', '20220621', 'tushare')

days_money_flow(mydatelist)
