import data.stock as st
import strategy.base as strat
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

'''
动态策略（正向）
'''


def get_data(start_date, end_date, columns, index_symbol='000300.XSHG'):
    '''
    获取股票收盘价数据，并拼接为一个df
    :param start_date: str
    :param end_date: str
    :param columns: list
    :param index_symbol: str
    :return: dataframe，拼接后的数据表
    '''
    # 获取股票别表代码：沪深300持有个股 创业板 上证
    stocks = st.get_index_list(index_symbol)
    # 拼接收盘价数据
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks[0:10]:
        data = st.get_csv_price(code, start_date, end_date, columns)
        # 拼接多个股票的收盘价：日期 股票A股收盘价 股票B收盘价
        data.columns = [code]
        pd.concat([data_concat, data], axis=1)
    # 预览股票数据
    print(data_concat)
    return data_concat


def momentum(data_concat, shift_n=1, top_n=2):
    '''

    :param data_concat: df
    :param shift_n: int, 表示业绩统计周期（单位：月）
    :return:
    '''
    # 转换时间频率： 日 > 月
    data_concat.index = pd.to_datetime(data_concat.index)
    data_month = data_concat.resample('M').last()
    # 计算过去N个月的收益率 = 期末值 / 期初值 - 1 = (期末 - 期初) / 期初
    print(data_month.head())
    shift_return = data_month / data_month.shift(shift_n) - 1
    # 生成交易信号： 收益率排前n的 > 赢家组合 > 买入1， 排最后n个 > 输家 > 卖出-1
    buy_singal = get_top_stocks(shift_return, top_n)
    sell_singal = get_top_stocks(-1 * shift_return, top_n)
    signal = buy_singal - sell_singal
    print(signal)
    # 计算投资组合收益率
    returns = strat.calculate_portfolio_return(shift_return, signal, top_n * 2)
    # 评估策略效果： 总收益率 年华收益率 最大回撤 夏普比
    returns = strat.evaluate_strategy(returns)
    print(data_month.head())
    return returns


def get_top_stocks(data, top_n):
    # 初始化信号容器
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    # 对data的每一行进行遍历，找里面的最大值，并利用bool函数标注0或者1信号
    for index, row in data.iterrows():
        signals.loc[index] = row.isin(row.nlargest(top_n)).astype(np.int)
    return signals


if __name__ == '__main__':
    start_date = '2020-01-01'
    end_date = '2021-04-04'
    columns = ['date', 'close']
    data = get_data(start_date, end_date, columns)
    # 测试： 动量策略
    returns = momentum(data)
    # 可视化每个月的收益率
    returns.plot()
    plt.show()
