import pandas as pd

from select_shares import select_zhangtingban_df

df = select_zhangtingban_df('20220428')

print(df['ts_code'].tolist())
