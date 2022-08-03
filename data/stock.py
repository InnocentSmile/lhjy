from jqdatasdk import *
import pandas as pd
import datetime

auth('15717929717', 'Pzl123456')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码
# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10000)
# 上海证券交易所	.XSHG	600519.XSHG	贵州茅台
# 深圳证券交易所	.XSHE	000001.XSHE	平安银行


def get_stock_list():
    '''
    获取所有A股股票列表
    :return: stock_list
    '''
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list


def get_single_stock_price(code, time_freq, start_date, end_date):
    '''
    获取单个股票行情数据
    :param code:
    :param timeperiod:
    :param startdate:
    :param endate:
    :return: data
    '''
    data = get_price(code, end_date=end_date, start_date=start_date, frequency=time_freq, panel=False)
    return data


def export_stock_price(data, filename):
    '''
    导出股票行情数据
    :param data:
    :param filename:
    :return:
    '''
    file_root = '/home/damon/PycharmProjects/lhjy/price' + filename + '.csv'
    data.to_csv(file_root)
    print('已成功存储至: ', file_root)


def transfer_price_freq(data, time_freq):
    '''
    将数据转换为指定周期 开盘价（当周第一天） 收盘价（当周最后一天）
    resample函数
    转换周期： 日K转换为周K
    获取周K（当周的）：开盘价（当周第一天） 收盘价（当周最后一天）
    :return:
    '''
    # 原因：虽然已经指定date列为index，把这个index却是字符串来的，要把字符串的index转为时间类型的，才能resample
    # df = data.set_index(pd.DatetimeIndex(pd.to_datetime(data.time)))
    # df['weekday'] = df.index.weekday
    # print(df)
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    return df_trans
#将所有股票列表转换成数组

# df = get_price(["600519.XSHG", "000001.XSHE"], end_date='2022-07-20 14:00:00', count=10, frequency='daily',
#                fields=['open', 'close', 'high', 'low', 'volume', 'money'])
# print(df)


# resample函数
# 转换周期： 日K转换为周K
# 获取周K（当周的）：开盘价（当周第一天） 收盘价（当周最后一天）

# print(df_week)
# # 汇总统计： 统计一下月成交量成交额（sum）
# df_week['volume(sum)'] = df['volume'].resample("W").sum()
# df_week['money(sum)'] = df['money'].resample("W").sum()
# print(df_week)

'''获取股票财务指标'''
# df = get_fundamentals(query(indicator), statDate='2020')

# df.to_csv('/home/damon/PycharmProjects/lhjy/data/finance/finance2020.csv')
# 基于盈利指标选股： eps,operating_profit,roe,inc_net_profit_year_on_year
# df = df[(df['eps'] > 0) & (df['operating_profit'] > 1012173617) &
#         (df['roe'] > 11) & (df['inc_net_profit_year_on_year'] > 10)]

# print(df)

'''获取股票估值指标'''
df_valuation = get_fundamentals(query(valuation), statDate=datetime.datetime.today())
print(df_valuation.head())
