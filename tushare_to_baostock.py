import time


def tuhshare_to_baostock_sharecode(tushare_code):
    if tushare_code.split('.')[1] == 'SH':
        bao_stock_code = 'sh.' + tushare_code.split('.')[0]
    elif tushare_code.split('.')[1] == 'SZ':
        bao_stock_code = 'sz.' + tushare_code.split('.')[0]
    elif tushare_code.split('.')[1] == 'BJ':
        bao_stock_code = 'bj.' + tushare_code.split('.')[0]

    return bao_stock_code


def baostock_to_tuhshare_sharecode(bao_stock_code):
    if bao_stock_code.split('.')[0] == 'sh':
        tushare_code = bao_stock_code.split('.')[1] + '.SH'
    elif bao_stock_code.split('.')[0] == 'sz':
        tushare_code = bao_stock_code.split('.')[1] + '.SZ'
    elif bao_stock_code.split('.')[0] == 'bj':
        tushare_code = bao_stock_code.split('.')[1] + '.BJ'
    return tushare_code


def baostock_date_to_tuhshare(baostock_date):
    timeArray = time.strptime(baostock_date, "%Y-%m-%d")
    trade_date_tushare = time.strftime("%Y%m%d", timeArray)

    return trade_date_tushare


def tuhshare_date_to_baostock(tuhshare_date):
    timeArray = time.strptime(tuhshare_date, "%Y%m%d")
    baostock_date = time.strftime("%Y-%m-%d", timeArray)

    return baostock_date


#  20220621095000000改为 0950
def baostock_longtime_to_datetime(longtime):
    timeArray = time.strptime(longtime, "%Y%m%d")
    baostock_date = time.strftime("%Y-%m-%d", timeArray)

    return baostock_date
