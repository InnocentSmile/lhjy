from jqdatasdk import *
import pandas as pd
import datetime

auth('15717929717', 'Pzl123456')  # 账号是申请时所填写的手机号；密码为聚宽官网登录密码
# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10000)

data_root = '/home/damon/PycharmProjects/lhjy/data/'

def get_stock_list():
    '''
    获取所有A股股票列表  上海证券交易所	.XSHG	600519.XSHG	贵州茅台
                      深圳证券交易所	.XSHE	000001.XSHE	平安银行
    :return: stock_list
    '''
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list


def get_single_price(code, time_freq, start_date, end_date):
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


def export_data(data, filename, type):
    '''
    导出股票相关数据
    :param data:
    :param filename:
    :type data: 股票数据类型 可以是： price，finance
    :return:
    '''
    file_root = data_root + type + "/" + filename + '.csv'
    data.index.names = ['date']
    data.to_csv(file_root) # 判断一下file是否存在 > 存在：追加 / 不存在：保存
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


def get_single_finance(code, date, statDate):
    '''
    获取单个股票财务指标
    :return:
    '''
    data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=statDate)
    return data


def get_single_valuation(code, date, statDate):
    '''
    获取单个股票估值指标
    :param code:
    :param date:
    :param statDate:
    :return:
    '''
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statDate)
    return data


def get_csv_data(code, type):
    '''

    :param code:
    :return:
    '''
    file_root = data_root + type + "/" + code + '.csv'
    return pd.read_csv(file_root)


def calculate_change_pct(data):
    '''
    涨跌幅 = (当期收盘价 - 前期收盘价) / 前期收盘价
    :param data: dataframe，带有收盘价
    :return: dataframe，带有涨跌幅
    '''
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data
