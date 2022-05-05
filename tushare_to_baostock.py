import time

def tuhshare_to_baostock_sharecode(tushare_code):

    if tushare_code.split('.')[1] == 'SH':
        bao_stock_code = 'sh.' + tushare_code.split('.')[0]
    elif tushare_code.split('.')[1] == 'SZ':
        bao_stock_code = 'sz.' + tushare_code.split('.')[0]
    elif tushare_code.split('.')[1] == 'BJ':
        bao_stock_code = 'bj.' + tushare_code.split('.')[0]

    return bao_stock_code

def baostock_date_to_tuhshare(baostock_date):

    timeArray = time.strptime(baostock_date, "%Y-%m-%d")
    trade_date_tushare = time.strftime("%Y%m%d", timeArray)

    return trade_date_tushare


def tuhshare_date_to_baostock(tuhshare_date):

    timeArray = time.strptime(tuhshare_date, "%Y%m%d")
    baostock_date = time.strftime("%Y-%m-%d", timeArray)

    return baostock_date