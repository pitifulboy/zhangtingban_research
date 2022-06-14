from df_manage_func import add_share_msg_to_df
from select_shares import select_one_day_longhubang

# 指定查询日期
querydate = '20220609'

# 跟踪席位名单
track_list = ['开源证券股份有限公司上海中山南路证券营业部', '开源证券股份有限公司西安长安路证券营业部', '华泰证券股份有限公司成都蜀金路证券营业部', '国联证券股份有限公司北京分公司',
              '东亚前海证券有限责任公司北京分公司', '东莞证券股份有限公司北京分公司', '东方证券股份有限公司深圳海德三道证券营业部', '财通证券股份有限公司杭州上塘路证券营业部',
              '华鑫证券有限责任公司上海银翔路证券营业部', '中国中金财富证券有限公司无锡人民中路证券营业部', '华鑫证券有限责任公司深圳益田路证券营业部', '东莞证券股份有限公司浙江分公司',
              '东兴证券股份有限公司晋江和平路证券营业部', '长城国瑞证券有限公司晋江东华街证券营业部', '中国银河证券股份有限公司绍兴证券营业部', '兴业证券股份有限公司上海金陵东路证券营业部',
              '东亚前海证券有限责任公司江苏分公司', '华鑫证券有限责任公司成都交子大道证券营业部', '国盛证券有限责任公司宁波桑田路证券营业部', '安信证券股份有限公司西安曲江池南路证券营业部',
              '东方财富证券股份有限公司上海东方路证券营业部', '国金证券股份有限公司厦门湖滨南路证券营业部', '中信证券股份有限公司上海溧阳路证券营业部'
              ]

# 获取龙虎榜数据
lhb_df = select_one_day_longhubang(querydate)

# 根据席位筛选数据
lhb_df_tracked = lhb_df[lhb_df.exalter.isin(track_list)]
lhb_df_tracked_ful_msg=add_share_msg_to_df(lhb_df_tracked)


# 导出结果
path = r'D:\00 量化交易\\跟踪席位' + querydate + '日龙虎榜.xlsx'
lhb_df_tracked_ful_msg.to_excel(path, sheet_name='1', engine='openpyxl')
