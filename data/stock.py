from jqdatasdk import *
import pandas as pd

auth('15717929717', 'Pzl123456')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码
# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100)
# 上海证券交易所	.XSHG	600519.XSHG	贵州茅台
# 深圳证券交易所	.XSHE	000001.XSHE	平安银行



#将所有股票列表转换成数组
# stocks = list(get_all_securities(['stock']).index)
# print(stocks)
# df = get_price(["600519.XSHG", "000001.XSHE"], end_date='2022-07-20 14:00:00', count=10, frequency='daily',
#                fields=['open', 'close', 'high', 'low', 'volume', 'money'])
# print(df)


# resample函数
# 转换周期： 日K转换为周K
# 获取周K（当周的）：开盘价（当周第一天） 收盘价（当周最后一天）
# df = get_price(["000001.XSHG"], end_date='2020-12-31', start_date='2020-01-01', frequency='daily', panel=False)
# # 原因：虽然已经指定date列为index，把这个index却是字符串来的，要把字符串的index转为时间类型的，才能resample
# df = df.set_index(pd.DatetimeIndex(pd.to_datetime(df.time)))
# df['weekday'] = df.index.weekday
# print(df)
# df_week = pd.DataFrame()
# df_week['open'] = df['open'].resample('W').first()
# df_week['close'] = df['close'].resample('W').last()
# df_week['high'] = df['high'].resample('W').max()
# df_week['low'] = df['low'].resample('W').min()
# print(df_week)
# # 汇总统计： 统计一下月成交量成交额（sum）
# df_week['volume(sum)'] = df['volume'].resample("W").sum()
# df_week['money(sum)'] = df['money'].resample("W").sum()
# print(df_week)

'''获取股票财务指标'''
df = get_fundamentals(query(indicator), statDate='2020')

# df.to_csv('/home/damon/PycharmProjects/lhjy/data/finance/finance2020.csv')
# 基于盈利指标选股： eps,operating_profit,roe,inc_net_profit_year_on_year
df = df[df['eps'] > 0]

