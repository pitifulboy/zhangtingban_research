from select_shares import select_msg_by_shareslist
import pandas as pd


def add_share_msg_to_df(trade_df):
    ts_code_list = trade_df['ts_code'].to_list()
    df_msg = select_msg_by_shareslist(ts_code_list)
    x = pd.merge(left=trade_df, right=df_msg, on='ts_code')

    return x

