from my_time_func import get_today_date
from update_daily_data import update_tradedata_from_toshare
from update_share_msg import update_share_name_from_tushare

# 今天
today_str = get_today_date('tushare')

# 更新股票列表，防止新股无法匹配名称
update_share_name_from_tushare()
# 更新股票交易数据
update_tradedata_from_toshare(today_str)
