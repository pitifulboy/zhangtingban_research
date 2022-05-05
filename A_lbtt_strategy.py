import pandas as pd
from pyecharts.charts import Bar, Grid
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
from operator import itemgetter
from df_manage_func import add_share_msg_to_df
from my_time_func import get_today_date, get_my_start_end_date_list
from select_shares import select_data_by_shareslist_lastdate, select_zhangtingban_df


# 查询单日连板天梯并作图
def oneday_lbtt(querydate):
    # 截止日涨停股票list
    ztb_df = select_zhangtingban_df(querydate)

    # 查询一系列股票dataframe
    shares_df = select_data_by_shareslist_lastdate(ztb_df.ts_code.to_list(), querydate)

    lbtt = []
    for i in range(0, len(ztb_df)):
        df_this_share = shares_df.loc[shares_df.ts_code == ztb_df.ts_code.iloc[i]]
        # 添加个股信息
        share_df_full = add_share_msg_to_df(df_this_share)

        # 连板天数
        n = 0
        # 个股交易数据天数
        l = len(df_this_share)

        # 计算个股连板天数
        for j in range(0, l):
            close = '%.2f' % (df_this_share["close"].iloc[-1 - j])
            pre_close = df_this_share["pre_close"].iloc[-1 - j]
            # 涨停价
            up_limit = '%.2f' % (pre_close * 1.1)
            if close == up_limit:
                n = n + 1
            else:
                break

        if n > 1:
            #  【代码+名称，日期，连板天数】
            lbtt.append([share_df_full.ts_code.iloc[0] + share_df_full.name.iloc[0], querydate, n])

    lbtt_ordered = sorted(lbtt, key=itemgetter(2), reverse=False)

    name = [x[0][7:11] for x in lbtt_ordered]
    num = [x[2] for x in lbtt_ordered]

    # 作图
    mybar = (
        Bar()
            .add_xaxis(name)
            .add_yaxis("连板数", num)
            .reversal_axis()
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, font_size=18, color="#000000", position='right'),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=querydate[4:] + "连板天梯", pos_top='5%',
                                      pos_left='center', title_textstyle_opts=opts.TextStyleOpts(font_size=36), ),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=18)),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )

    mygrid = Grid(opts.InitOpts(bg_color='white', width="800px", height="1200px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_left='30%', pos_top='10%'))
    mygrid.render(querydate + "lbtt.html")

    make_snapshot(snapshot, querydate + "lbtt.html", querydate + "_lbtt.png", pixel_ratio=2)

    return lbtt_ordered


def today_lbtt():
    querydate = get_today_date('tushare')
    # 生成今日涨跌分布
    oneday_lbtt(querydate)


def date_list_lbtt(startday, enddaste):
    t = get_my_start_end_date_list(startday, enddaste, 'tushare')
    for i in range(len(t)):
        oneday_lbtt(t[i])


# 查询单日连板天梯
oneday_lbtt('20220429')

# 查询今日连板天梯
# today_lbtt()

# 查询多日连板天梯
#date_list_lbtt('20220401','20220429')
