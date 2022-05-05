import pandas as pd

enddate = '20220422'
today_1 = pd.to_datetime(enddate, format='%Y%m%d')
print(today_1)
