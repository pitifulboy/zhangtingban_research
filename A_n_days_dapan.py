import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot

from dapan_zhangdie_sharenum import get_dapan_zhangdie_num


def n_days_dapan(enddate):
    # 今天
    end_date = pd.to_datetime(enddate, format='%Y%m%d')

    # 70天前
    today_70 = (end_date - pd.to_timedelta(70, "d"))

    # 设置70天跨度，以便删选出30个交易日
    list = get_dapan_zhangdie_num(today_70.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'))
    list_15 = list[-15::]

    print(list_15)

    # 获取pyecharts所需数据
    date_list = [x[0] for x in list_15]
    up_list = [x[1] for x in list_15]
    downlist = [-x[2] for x in list_15]

    mybar = (
        Bar()
            .add_xaxis(date_list)
            .add_yaxis("上涨（含收平）", up_list, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color="#ff0000"), )
            .add_yaxis("下跌", downlist, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color="#00ff00"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=16, rotate=-90, font_weight='lighter',
                                      color='#000000'))
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90, font_size=16)),
            yaxis_opts=opts.AxisOpts(is_show=False),
            title_opts=opts.TitleOpts(title=enddate[4:] + "前15个交易日个股涨跌数", pos_top='5%', title_textstyle_opts=opts.TextStyleOpts(font_size=36),
                                      pos_left='center', ),
        )
    )
    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_bottom='10%', pos_top='10%'))
    mygrid.render("gen_15days_dapan.html")

    make_snapshot(snapshot, "gen_15days_dapan.html", querydate+"15日大盘涨跌分布.png", pixel_ratio=2)


# querydate = pd.Timestamp.now()
querydate = '20220509'
n_days_dapan(querydate)
