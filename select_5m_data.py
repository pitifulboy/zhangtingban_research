# 建立mysql数据库的连接
from sqlalchemy import create_engine
import pandas as pd


def select_5m_data_by_date(tradedate):
    conn = create_engine('mysql+pymysql://root:123456@localhost:3306/qtrade', encoding='utf8')
    mysql = "SELECT  * FROM 5_minutes_data WHERE date = '" + tradedate + "'"
    df = pd.read_sql(mysql, conn)
    return df
