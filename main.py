from A_dapan_zhangdie_fudufenbu import draw_zhangdie_fenbu_bar
from A_lbtt_strategy import oneday_lbtt
from A_n_days_dapan import n_days_dapan
from A_qinxu_zhibiao import qinxu_oneday
from A_zhangting_jiaoyie import query_dailytrade_by_date_and_type
from A_zhangting_zhaban_data import calulate_jiaoyie
from my_time_func import get_today_date, get_days_after_tushare, get_my_start_end_date_list
from select_shares import get_dailytrade_maxdate, select_share_by_date
from update_daily_data import update_tradedata_from_toshare, update_tradedata_from_toshare_by_datelist
from update_share_msg import update_share_name_from_tushare

# 获取最新日期
today_date = get_today_date('tushare')
#today_date = '20220512'

# 更新股票名称等股票信息表。
update_share_name_from_tushare()

# 自动更细交易数据
# 更新tushare日常交易数据
# 获取mysql中存储的最新日期
maxdate = get_dailytrade_maxdate()
# 起始日期是mysql日期的后一天
update_start = get_days_after_tushare(maxdate, 1)

# 判断mysql中是否已经更新最新数据，如果不是最新数据
if maxdate != today_date:
    # 生成需要更新的datelist
    date_list = get_my_start_end_date_list(update_start, today_date, 'tushare')
    # 更新日常交易数据
    update_tradedata_from_toshare_by_datelist(date_list)
else:
    # 查询单日连板天梯
    print('计算连板天梯')
    oneday_lbtt(today_date)
    print('计算当日涨跌分布')
    draw_zhangdie_fenbu_bar(today_date)
    print('计算多日涨跌分布')
    n_days_dapan(today_date)
    # 查询涨停
    print('导出涨跌停excel')
    query_dailytrade_by_date_and_type(today_date, '涨停')
    # 查询炸板df
    query_dailytrade_by_date_and_type(today_date, '炸板')
    # 计算大盘交易额，涨停炸板交易额
    print('计算大盘交易额，涨停炸板交易额')
    calulate_jiaoyie(today_date)
    qinxu_oneday(today_date)
