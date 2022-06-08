import pandas as pd

from df_manage_func import add_share_msg_to_df
from select_shares import select_zhangtingban_df, select_zhaban_df
import numpy as np


def query_dailytrade_by_date_and_type(queryday, querytype):
    if querytype == '涨停':
        shares_df = select_zhangtingban_df(queryday)
    elif querytype == '炸板':
        shares_df = select_zhaban_df(queryday)

    # 添加个股信息
    share_df_full = add_share_msg_to_df(shares_df)
    # 并取值,待排序
    share_df_amount = share_df_full.loc[:, ['ts_code', 'close', 'name', 'amount', 'pct_chg', 'pre_close', 'industry']]

    # 按照涨幅和交易额排序
    share_df_amount_chg = share_df_full.loc[:,
                          ['ts_code', 'close', 'name', 'amount', 'pct_chg', 'pre_close', 'industry']].astype(
        {'amount': 'float64', 'pct_chg': 'float64'})
    # 将涨跌幅按照30，20，10粗略分类后排序
    share_df_amount_chg['pct_chg'] = share_df_amount_chg['pct_chg'].round(0)

    if querytype == '涨停':
        share_df_amount_chg_ordered = share_df_amount_chg.sort_values(by=['pct_chg', 'amount'],
                                                                      ascending=False,
                                                                      ignore_index=True)

    elif querytype == '炸板':
        share_df_amount_chg_ordered = share_df_amount_chg.sort_values(by='amount', ascending=False,
                                                                      ignore_index=True)

    data_list = []
    data_list_full = []
    # 按照排序后的列表顺序导出到excel
    for k in range(0, len(share_df_amount_chg_ordered)):
        #code_name = share_df_amount_chg_ordered.iloc[k, 0][-2:] + share_df_amount_chg_ordered.iloc[k, 2][ :-2]

        code_name = share_df_amount_chg_ordered.iloc[k, 0]+ share_df_amount_chg_ordered.iloc[k, 2]
        close = '%.2f' % share_df_amount_chg_ordered.iloc[k, 1]
        pre_close = '%.2f' % share_df_amount_chg_ordered.iloc[k, 5]
        amount = '%.2f' % (share_df_amount_chg_ordered.iloc[k, 3] / 100000)
        pct_chg = '%.2f' % (float(close) / float(pre_close) * 100 - 100)
        industry = share_df_amount_chg_ordered.iloc[k, 6]
        data_list.append([k + 1, code_name, str(amount), str(close), str(pct_chg), industry])
        data_list_full.append([k + 1, code_name, str(amount), str(close), str(pct_chg), industry])

    # 抖音格式
    my_df = pd.DataFrame(data_list, columns=['序号', '名称', '交易额（亿）', '收盘', '涨跌幅（%）', '行业'])

    path = r'D:\00 量化交易\\' + queryday + querytype + '.xlsx'
    my_df.to_excel(path, sheet_name='1', engine='openpyxl')

    my_df_format = my_df.astype({'交易额（亿）': 'float'})

    # 涨停板块分析，透视
    # 透视,统计上榜次数和金额
    my_df_povit = pd.pivot_table(my_df_format, index='行业', values='交易额（亿）',
                                 aggfunc={'行业': np.count_nonzero, '交易额（亿）': np.sum})
    print(my_df_povit.keys())

    path2 = r'D:\00 量化交易\\' + queryday + querytype + '透视分析.xlsx'
    lhb_df_format = my_df_povit.astype({'交易额（亿）': 'float', '行业': 'int'})
    lhb_df_sorted = lhb_df_format.fillna(0).sort_values(by='交易额（亿）', ascending=False)
    lhb_df_sorted.to_excel(path2, sheet_name='1', engine='openpyxl')


'''
queryday = '20220509'

queryday = '20220509'

# 查询涨停
query_dailytrade_by_date_and_type(queryday, '涨停')

# 查询涨停
query_dailytrade_by_date_and_type(queryday, '涨停')'''

'''# queryday = get_today_date('tushare')
queryday = '20220509'

# 查询涨停
query_dailytrade_by_date_and_type(queryday, '涨停')

# 查询炸板df
query_dailytrade_by_date_and_type(queryday, '炸板')
'''
