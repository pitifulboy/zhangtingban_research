import pandas as pd
from pyecharts.charts import Bar, Grid
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

from df_manage_func import add_share_msg_to_df
from select_shares import select_share_by_date


# 分析时间段内，个股涨跌分布情况
def period_zhangdie_fenbu(stratdate, enddate):
    # 读取开始日期的交易数据

    stratdate_trade_df = select_share_by_date(stratdate)
    print(stratdate + "日交易数据")
    print(stratdate_trade_df)

    # 读取结束日期的交易数据

    enddate_trade_df = select_share_by_date(enddate)
    print(enddate + "日交易数据")
    print(enddate_trade_df)

    # 取两个交易日的有交易股票的交集
    df_merged = pd.merge(left=stratdate_trade_df, right=enddate_trade_df, how="inner", on='ts_code')

    # 累计涨跌幅(忽略分红导致的股价下降）
    df_merged['total_pct_chg'] = ((df_merged['close_y'] - df_merged['close_x']) / df_merged['close_y']) * 100
    print("个股累计涨幅")
    print(df_merged.loc[:, ["ts_code", "total_pct_chg"]])

    # 添加个股信息
    df_full = add_share_msg_to_df(df_merged)
    path_00=r'D:\00 量化交易\\区间板块涨跌分析.xlsx'
    df_full.to_excel(path_00, sheet_name='1', engine='openpyxl')

    # 大盘涨跌分布
    zhangdie_list = []

    # 跌幅大于 -10%
    y = len(df_merged.loc[df_merged['total_pct_chg'] <= -20.0])
    zhangdie_list.append(['<-20%', y])

    for i in range(-10, 20):
        num = len(df_merged.loc[df_merged['total_pct_chg'] > i * 2 + 0.0]) - len(
            df_merged.loc[df_merged['total_pct_chg'] > i * 2 + 2.0])

        zhagndiefu_str = str(i * 2) + '%< x<' + str(i * 2 + 2) + '%'
        zhangdie_list.append([zhagndiefu_str, num])

    # 涨幅大于10%
    x = len(df_merged.loc[df_merged['total_pct_chg'] > 40.0])
    zhangdie_list.append(['>40%', x])

    return zhangdie_list


def period_draw_zhangdie_fenbu_bar(startdate, enddate):
    data_list = period_zhangdie_fenbu(startdate, enddate)
    # 将数据转换为pyecharts需要的格式
    x = [a[0] for a in data_list]

    y = []

    for i in range(0, len(data_list)):
        if i < 11:
            y.append(
                opts.BarItem(
                    name='',
                    value=data_list[i][1],
                    itemstyle_opts=opts.ItemStyleOpts(color="#00ff00"),
                )
            )
        else:
            y.append(
                opts.BarItem(
                    name='',
                    value=data_list[i][1],
                    itemstyle_opts=opts.ItemStyleOpts(color="#ff0000"),
                )
            )

    mybar = (
        Bar()
        .add_xaxis(x)
        .add_yaxis("", y_axis=y)
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, font_size=12, font_weight='lighter', color="#000000"),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(interval=0, rotate=-90, font_size=12), ),
            title_opts=opts.TitleOpts(title=stratdate + "日-" + enddate + "日期间，个股累计涨跌分布", pos_top='5%',
                                      pos_left='center', title_textstyle_opts=opts.TextStyleOpts(font_size=18), ),
            yaxis_opts=opts.AxisOpts(is_show=False, ),
        )

    )

    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_bottom='15%'))
    mygrid.render("qujian_shares.html")

    make_snapshot(snapshot, "qujian_shares.html", stratdate + "日-" + enddate + "日涨跌分布.png", pixel_ratio=2)

    return mygrid


stratdate = '20220425'
enddate = '20221111'
period_draw_zhangdie_fenbu_bar(stratdate, enddate)
