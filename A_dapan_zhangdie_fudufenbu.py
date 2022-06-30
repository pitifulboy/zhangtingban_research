import pandas as pd
from pyecharts.charts import Bar, Grid
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
from select_shares import select_share_by_date


def oneday_zhangdie_fenbu(querydate):
    # 查询今日交易数据
    today_trade_df = select_share_by_date(querydate)

    # 大盘涨跌分布
    zhangdie_list = []

    # 跌幅大于 -10%
    y = len(today_trade_df.loc[today_trade_df['pct_chg'] <= -10.0])
    zhangdie_list.append(['<-10%', y])

    for i in range(-10, 10):
        num = len(today_trade_df.loc[today_trade_df['pct_chg'] > i + 0.0]) - len(
            today_trade_df.loc[today_trade_df['pct_chg'] > i + 1.0])

        zhagndiefu_str = str(i) + '%< x<' + str(i + 1) + '%'
        zhangdie_list.append([zhagndiefu_str, num])

    # 涨幅大于10%
    x = len(today_trade_df.loc[today_trade_df['pct_chg'] > 10.0])
    zhangdie_list.append(['>10%', x])

    return zhangdie_list


def draw_zhangdie_fenbu_bar(querydate):
    data_list = oneday_zhangdie_fenbu(querydate)
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
            title_opts=opts.TitleOpts(title=querydate[4:] + "个股涨跌分布", pos_top='5%',
                                      pos_left='center', title_textstyle_opts=opts.TextStyleOpts(font_size=12), ),
            yaxis_opts=opts.AxisOpts(is_show=False, ),
        )

    )

    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_bottom='15%'))
    mygrid.render(querydate + "_shares.html")

    make_snapshot(snapshot, querydate + "_shares.html", querydate + "_shares.png", pixel_ratio=2)

    return mygrid


# 今天
#querydate = get_today_date('tushare')

# 生成指定日期涨跌分布
#querydate = '20220509'

#draw_zhangdie_fenbu_bar(querydate)
