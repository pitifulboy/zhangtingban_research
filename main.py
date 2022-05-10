from my_time_func import get_today_date, get_days_after_tushare, get_my_start_end_date_list
from select_shares import get_dailytrade_maxdate
from update_daily_data import update_tradedata_from_toshare, update_tradedata_from_toshare_by_datelist
from update_share_msg import update_share_name_from_tushare

# 更新股票名称等股票信息表。
update_share_name_from_tushare()

# 更新tushare日常交易数据
# 获取mysql中存储的最新日期
maxdate = get_dailytrade_maxdate()
# 获取最新日期
today_date = get_today_date('tushare')
# 起始日期是mysql日期的后一天
update_start = get_days_after_tushare(maxdate, 1)
# 生成需要更新的datelist
date_list = get_my_start_end_date_list(update_start, today_date, 'tushare')
# 更新日常交易数据
update_tradedata_from_toshare_by_datelist(date_list)
