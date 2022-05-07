import numpy as np

from my_time_func import get_my_startdate_list, get_my_start_end_date_list, get_days_before_tushare
from df_manage_func import add_share_msg_to_df
from select_shares import get_longhubang, select_days_longhubang, select_one_share_by_startdate
import pandas as pd


def get_top_exalter(n):
    # 获取全部龙虎榜数据
    lhb_df = get_longhubang().fillna(value='0')
    # 透视
    lhb_df_povit = pd.pivot_table(lhb_df, values='buy', index='exalter', columns='side', aggfunc=np.sum, fill_value=0)
    # 排序,按照买入交易额降序
    lhb_df_sorted = lhb_df_povit.sort_values(by='0', ascending=False).head(n)
    top_list = lhb_df_sorted.index.tolist()
    return top_list


# 根据席位查询历史龙虎榜
def query_longhubang_by_exalter(exalter):
    # 获取全部龙虎榜数据
    lhb_df = get_longhubang().fillna(value='0')
    # 根据席位 查询买入上榜记录
    df_i = lhb_df.loc[(lhb_df['exalter'] == exalter) & (lhb_df['side'] == '0')]
    # 按照日期倒序排列
    df_i_sorted = df_i.sort_values(by='trade_date', ascending=False, ignore_index=True)

    # 添加个股信息
    share_df_full = add_share_msg_to_df(df_i_sorted)
    share_df_full_partvalues = share_df_full.loc[:, ['trade_date', 'ts_code', 'name', 'buy', 'exalter']]

    return share_df_full_partvalues


# 获取指定时间段的全部龙虎榜数据
my_datelist = get_my_start_end_date_list('20220401', '20220429', 'tushare')
my_longhubang_datelist = select_days_longhubang(my_datelist)
# print(my_longhubang_datelist)

# 选定席位
this_exalter = '财通证券股份有限公司杭州上塘路证券营业部'

# 获取该席位龙虎榜买入记录
lhb_this_exalter = my_longhubang_datelist.loc[
    (my_longhubang_datelist['exalter'] == this_exalter) & (my_longhubang_datelist['side'] == '0')]

# print(lhb_this_exalter)

fina_data_list = []
for i in range(0, len(lhb_this_exalter)):
    # 上榜日
    bang_date = lhb_this_exalter.iloc[i, 0]
    # 上榜后表现数据
    share_after_lhb = select_one_share_by_startdate(lhb_this_exalter.iloc[i, 1], lhb_this_exalter.iloc[i, 0])

    # 分析上榜后n日数据
    num_day = 3
    #  添加股票信息,保留3个交易日数据
    share_after_lhb_ful_msg = add_share_msg_to_df(share_after_lhb).head(num_day)

    # 保留待分析信息
    share_after_lhb_part = share_after_lhb_ful_msg.loc[:,
                           ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'name']]
    # print(share_after_lhb_part)

    anay_list = []
    # 计算上榜后2日，开盘涨幅，最大涨幅，最大跌幅，收盘涨幅，
    for j in range(0, num_day):
        # 开盘涨幅
        kp_zf = '%.2f' % (float(share_after_lhb_part.loc[j, 'open']) / float(
            share_after_lhb_part.loc[j, 'pre_close']) * 100 - 100)

        # 最大涨幅
        zd_zf = '%.2f' % (float(share_after_lhb_part.loc[j, 'high']) / float(
            share_after_lhb_part.loc[j, 'pre_close']) * 100 - 100)

        # 最小涨幅
        zx_zf = '%.2f' % (float(share_after_lhb_part.loc[j, 'low']) / float(
            share_after_lhb_part.loc[j, 'pre_close']) * 100 - 100)

        # 收盘涨幅
        sp_zf = '%.2f' % (float(share_after_lhb_part.loc[j, 'close']) / float(
            share_after_lhb_part.loc[j, 'pre_close']) * 100 - 100)

        anay_list.append([kp_zf, zd_zf, zx_zf, sp_zf])

    # 将信息和数据汇总
    ts_code = share_after_lhb_part.iloc[0, 0]
    # 修正龙虎榜日期，往前调整1天
    trade_date = share_after_lhb_part.iloc[0, 1]
    read_trade_date = get_days_before_tushare(trade_date, 1)

    name = share_after_lhb_part.iloc[0, 7]
    msg_df = [[read_trade_date, ts_code, name]]
    # 拼接个股信息和数据
    ful_df = msg_df + anay_list

    fina_data_list.append([x for list_elements in ful_df for x in list_elements])

# 将数据转换为df格式
data_df = pd.DataFrame(fina_data_list,
                       columns=['上榜日', '代码', '名称', '上榜日涨幅', '0日最大涨幅', '0日最小涨幅', '0日收盘涨幅', '次日开盘涨幅', '次日最大涨幅', '次日最小涨幅',
                                '次日收盘涨幅', '2日开盘涨幅', '2日最大涨幅', '2日最小涨幅', '2日收盘涨幅'])

data_df['代码名称'] = data_df['代码'] + data_df['名称']
data_df['代码名称'] = data_df['代码名称'].str[3:12]

df_anay = data_df.loc[:, ['上榜日', '代码名称', '上榜日涨幅', '次日开盘涨幅', '次日最大涨幅', '次日最小涨幅', '次日收盘涨幅']]
# 由于多个原因重复上榜，需要去重
df_anay_unique=df_anay.drop_duplicates(keep='first')

print(df_anay_unique)

path = r'D:\00 量化交易\\' + this_exalter + '.xlsx'
df_anay_unique.to_excel(path, sheet_name='1', engine='openpyxl')
