from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
from my_time_func import get_my_enddate_list
from select_shares import select_share_by_date, select_zhangtingban_df_bydf, select_zhaban_df_bydf


# 计算单日交易量相关数据
def qinxu_jiaoyie_oneday(querday):
    # 今日总交易额
    total_df = select_share_by_date(querday)
    total_df_amount = '% .0f ' % (total_df.amount.sum() / 100000)

    # 涨停板
    zhangtingban_df = select_zhangtingban_df_bydf(total_df)
    # 涨停个股交易额
    zhangtingban_df_amount = '% .0f ' % (zhangtingban_df.amount.sum() / 100000)
    n_zhangtingban_df = len(zhangtingban_df)

    # 炸板
    zhaban_df = select_zhaban_df_bydf(total_df)
    zhaban_df_amount = '% .0f ' % (zhaban_df.amount.sum() / 100000)
    n_zha_df = len(zhaban_df)
    # 日期，大盘交易额，涨停交易额，涨停数，炸板交易额，炸板数
    datalist = [querday, total_df_amount, zhangtingban_df_amount, n_zhangtingban_df, zhaban_df_amount,
                n_zha_df]
    return datalist


# 计算多日交易量相关数据
def days_jiaoyie_data(endday, day_num):
    datelist = get_my_enddate_list(endday, 80, 'tushare')

    data_all = []
    # 倒序查询15个交易日的数据，用于绘图
    for i in range(0, len(datelist)):
        # 倒序计算
        x = qinxu_jiaoyie_oneday(datelist[-i - 1])
        # 只计算15个交易额
        if len(data_all) < day_num:
            # 非交易日数据为空，跳过非交易额
            if x[1] != ' 0 ':
                data_all.append(x)
        else:
            break
    # 倒序排列，调整成日期正序
    data_all = data_all[::-1]
    return data_all


# 绘制交易额组合图。大盘交易额+涨停交易额+炸板交易额
def draw_pic_amounts_data(list_15):
    # 获取pyecharts所需数据
    date_list = [x[0] for x in list_15]
    zhangting_amount_list = [x[2] for x in list_15]
    zhaban_amount_list = [x[4] for x in list_15]
    # 大盘交易额
    dapan_amount_list = [x[1] for x in list_15]

    mybar = (
        Bar()
            .add_xaxis(date_list)
            .add_yaxis("涨停交易额", zhangting_amount_list, stack="stack1",
                       itemstyle_opts=opts.ItemStyleOpts(color="#ff0000"))
            .add_yaxis("炸板交易额", zhaban_amount_list, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color="#00ff00"))
            .extend_axis(yaxis=opts.AxisOpts(is_show=False))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=16, font_weight='lighter',
                                      color='#000000'))
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90, font_size=16)),
            yaxis_opts=opts.AxisOpts(is_show=False),
            title_opts=opts.TitleOpts(
                title=date_list[-1] + "日资金趋势", pos_top='5%',
                title_textstyle_opts=opts.TextStyleOpts(font_size=36),
                pos_left='center', ),
        )
    )

    myLine = (
        Line()
            .add_xaxis(date_list)
            .add_yaxis(
            "大盘交易额",
            dapan_amount_list,
            yaxis_index=1,
        )
            .set_series_opts(
            linestyle_opts=opts.LineStyleOpts(width=4),
            label_opts=opts.LabelOpts(position='inside', font_size=24, font_weight='lighter', color='#000000'))
    )
    overlap_bar_line = mybar.overlap(myLine)

    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(overlap_bar_line, grid_opts=opts.GridOpts(pos_bottom='10%', pos_top='10%'), is_control_axis_index=True)
    mygrid.render("jiaoyie.html")

    make_snapshot(snapshot, "jiaoyie.html", date_list[-1] + "交易资金.png", pixel_ratio=2)


def draw_pic_zhangtingzhaban_num_data(list_15):
    # 获取pyecharts所需数据
    date_list = [x[0] for x in list_15]
    zhangting_amount_list = [x[3] for x in list_15]
    zhaban_amount_list = [x[5] for x in list_15]

    mybar = (
        Bar()
            .add_xaxis(date_list)
            .add_yaxis("涨停个数", zhangting_amount_list, stack="stack1",
                       itemstyle_opts=opts.ItemStyleOpts(color="#ff0000"), )
            .add_yaxis("炸板个数", zhaban_amount_list, stack="stack1", itemstyle_opts=opts.ItemStyleOpts(color="#00ff00"))
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=16, rotate=-90, font_weight='lighter',
                                      color='#000000'))
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90, font_size=16)),
            yaxis_opts=opts.AxisOpts(is_show=False),
            title_opts=opts.TitleOpts(title="涨停炸板个数", pos_top='5%',
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=36),
                                      pos_left='center', ),
        )
    )
    mygrid = Grid(opts.InitOpts(bg_color='white', width="1600px", height="900px"))
    mygrid.add(mybar, grid_opts=opts.GridOpts(pos_bottom='10%', pos_top='10%'))
    mygrid.render("zhangdingzhaban_num.html")

    make_snapshot(snapshot, "zhangdingzhaban_num.html", date_list[-1] + "涨停炸板个数.png", pixel_ratio=2)


def calulate_jiaoyie(date):
    list_my = days_jiaoyie_data(date, 15)
    draw_pic_amounts_data(list_my)
    #draw_pic_zhangtingzhaban_num_data(list_my)

