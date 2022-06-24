from select_shares import select_one_share_by_longhubang_xiwei

xiwei = '中国银河证券股份有限公司大连金马路证券营业部'
df = select_one_share_by_longhubang_xiwei(xiwei)
print(df)

# 导出结果
path = r'D:\00 量化交易\\中国银河证券股份有限公司大连金马路证券营业部.xlsx'
df.to_excel(path, sheet_name='1', engine='openpyxl')
