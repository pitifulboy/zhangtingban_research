import numpy as np

from select_shares import get_longhubang
import pandas as pd

lhb_df = get_longhubang().fillna(value='0')

# 透视
lhb_df_povit = pd.pivot_table(lhb_df, values='buy', index='exalter', columns='side', aggfunc=np.sum, fill_value=0)
# 排序,按照买入交易额降序
lhb_df_sorted = lhb_df_povit.sort_values(by='0', ascending=False).head(100)

# 席位top100 list
top100_list = lhb_df_sorted.index.tolist()

# 龙虎榜开盘卖，收益率比较
for i in range(0, 100):
    print(top100_list[i])
    df_i = lhb_df.loc[(lhb_df['exalter'] == top100_list[i]) & (lhb_df['side'] == '0')]
    print(df_i)
    print(len(df_i))
