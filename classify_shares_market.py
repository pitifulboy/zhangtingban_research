# 暂不考虑st股票
# 沪市主板 6开头  10%涨跌幅
# 深市主板 0开头  10%涨跌幅
# 北交所 4，8开头  30%涨跌幅
# 创业板 3开头   20%涨跌幅
# 科创板 68开头  20%涨跌幅

def get_zhangdie_limit(ts_code):
    limit = 0
    if ts_code[0:1] == '0':
        limit = 0.1
    elif ts_code[0:1] == '3':
        limit = 0.2
    elif ts_code[0:1] == '4':
        limit = 0.3
    elif ts_code[0:1] == '8':
        limit = 0.3
    elif ts_code[0:2] == '68':
        limit = 0.2
    elif ts_code[0:1] == '6':
        limit = 0.1
    return limit
