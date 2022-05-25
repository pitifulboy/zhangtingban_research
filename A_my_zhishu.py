import pandas as pd
from my_time_func import get_my_enddate_list
from select_shares import select_share_by_date
from pyecharts import options as opts
from pyecharts.charts import Kline


# 计算单日大盘平均涨跌幅
def one_day_zhishu(querday):
    # 单盘全部股票指数计算
    df_daily = select_share_by_date(querday)

    # 遍历 最大涨幅，最小涨幅，收盘涨幅
    datalist = []

    if len(df_daily) == 0:
        pass
    else:
        for i in range(0, len(df_daily)):
            # 昨日收盘价
            pre_close = df_daily['pre_close'][i]
            # 今日开盘
            open = df_daily['open'][i]
            # 最高价
            high = df_daily['high'][i]
            # 最低价
            low = df_daily['low'][i]
            # 收盘价
            close = df_daily['close'][i]

            # 开盘涨幅
            open_pct_chg = open / pre_close * 100 - 100
            # 最大涨幅
            max_pct_chg = high / pre_close * 100 - 100
            # 最小涨幅
            min_pct_chg = low / pre_close * 100 - 100
            # 收盘涨幅
            close_pct_chg = close / pre_close * 100 - 100

            datalist.append([querday, open_pct_chg, close_pct_chg, min_pct_chg, max_pct_chg])

    this_columns = ['querday', 'open_pct_chg', 'close_pct_chg', 'min_pct_chg', 'max_pct_chg']
    df = pd.DataFrame(datalist, columns=this_columns)
    result = [querday, df['open_pct_chg'].mean(), df['close_pct_chg'].mean(), df['min_pct_chg'].mean(),
              df['max_pct_chg'].mean()]

    return result


# 计算多日大盘平均涨跌幅
def days_dapan_mean(date_list):
    days_data = []
    for i in range(len(date_list)):
        one_day_data = one_day_zhishu(date_list[i])

        if len(one_day_data):
            print(one_day_data)
            days_data.append(one_day_data)

    this_columns2 = ['querday', 'open_pct_chg', 'close_pct_chg', 'min_pct_chg', 'max_pct_chg']
    # 删除空行
    all_df = pd.DataFrame(days_data, columns=this_columns2).dropna()
    print(all_df)

    # 对开盘价进行累计

    for i in range(1, len(all_df)):
        all_df.iloc[i, 1] = all_df.iloc[i, 1] + all_df.iloc[i - 1, 2]
    print(all_df)

    return all_df


datelist = get_my_enddate_list('20220524', 150, 'tushare')
pic_data = days_dapan_mean(datelist)

kline_data_x = pic_data.loc[:, 'querday'].values.tolist()
kline_data_y = pic_data.loc[:, ['open_pct_chg', 'close_pct_chg', 'min_pct_chg', 'max_pct_chg']].values.tolist()

c = (
    Kline()
        .add_xaxis(kline_data_x)
        .add_yaxis("kline", kline_data_y)
        .set_global_opts(
        yaxis_opts=opts.AxisOpts(is_scale=True),
        xaxis_opts=opts.AxisOpts(is_scale=True),
        title_opts=opts.TitleOpts(title="Kline-基本示例"),
    )
        .render("kline_base.html")
)
