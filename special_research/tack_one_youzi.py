from df_manage_func import add_share_msg_to_df
from select_shares import select_one_share_by_longhubang_xiwei

xiwei = '中国银河证券股份有限公司大连金马路证券营业部'
df = select_one_share_by_longhubang_xiwei(xiwei)
df_1=add_share_msg_to_df(df)
print(df_1)

# 导出结果
path = r'D:\00 量化交易\\中国银河证券股份有限公司大连金马路证券营业部.xlsx'
df_1.to_excel(path, sheet_name='1', engine='openpyxl')
