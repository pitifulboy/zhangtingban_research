import pandas as pd

from df_manage_func import add_share_msg_to_df
from my_time_func import get_my_start_end_date_list, get_today_date
from select_shares import select_zhangtingban_df, select_zhaban_df


def query_dailytrade_by_date_and_type(queryday, type):
    if type == '涨停':
        shares_df = select_zhangtingban_df(queryday)
    elif type == '炸板':
        shares_df = select_zhaban_df(queryday)

    # 添加个股信息
    share_df_full = add_share_msg_to_df(shares_df)
    # 按照交易额排序，并取值
    share_df_amount = share_df_full.sort_values(by='amount', ascending=False, ignore_index=True).loc[:,
                      ['ts_code', 'close', 'name', 'amount']]

    # print('序号      ' + '    交易额    ' + '  收盘价 ')
    data_list = []
    for k in range(0, len(share_df_amount)):
        code_name = share_df_amount.iloc[k, 0] + share_df_amount.iloc[k, 2]
        close = '%.2f' % share_df_amount.iloc[k, 1]
        amount = '%.2f' % (share_df_amount.iloc[k, 3] / 100000)
        data_list.append([k + 1, code_name[7:11], str(amount) + '亿', str(close)])

        # print(str(k + 1) + '   ' + code_name[7:11] + '  ' + str(amount) + '亿' + '   ' + str(close))

    # 抖音格式
    my_df = pd.DataFrame(data_list, columns=['序号', '名称', '交易额', '收盘'])
    print(my_df)

    path = r'D:\00 量化交易\\' + queryday + type + '.xlsx'
    my_df.to_excel(path, sheet_name='1', engine='openpyxl')


# queryday = get_today_date('tushare')
queryday = '20220429'

# 查询涨停
query_dailytrade_by_date_and_type(queryday, '涨停')

# 查询炸板df
query_dailytrade_by_date_and_type(queryday, '炸板')
