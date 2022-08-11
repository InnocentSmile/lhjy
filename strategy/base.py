'''
用来创建交易策略，生成交易信号
'''

import data.stock as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd


def compose_singal(data):
    '''
    整合信号
    :param data:
    :return:
    '''
    # 模拟重复买入：周二在此买入
    # data['sell_signal'] = np.where((data['weekday'] == 0) | (data['weekday'] == 1), -1, 0)
    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0,
                                   data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']

    return data


def calculate_pro_pct(data):
    '''
    计算收益率
    :param data:
    :return:
    '''
    # 计算单次收益率： 开仓 平仓（开仓的全部股数）
    data = data[data['signal'] != 0]
    # data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close']
    data['profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]
    return data


def calculate_pro_pct2(data):
    '''
    计算收益率
    :param data:
    :return:
    '''
    # 计算单次收益率： 开仓 平仓（开仓的全部股数）
    # 筛选信号不为0的，并且计算涨跌幅
    data.loc[data['signal'] != 0, 'profit_pct'] = data['close'].pct_change()
    # data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close']
    # data['profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]
    return data


def calculate_cum_prof(data):
    '''
    计算累计收益率
    :param data:
    :return:
    '''
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def caculate_max_drawdown(data):
    '''
    计算最大回撤比
    :param data:
    :return:
    '''
    # 选取时间周期
    window = 252
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window, min_periods=1).max()
    # 计算当天的回撤比 (谷值 - 疯值) / 峰值 = 谷值 / 峰值  - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).max()
    return data


def calculte_sharpe(data):
    '''
    计算夏普比率，返回的是年华的夏普比率
    :param data:
    :return:
    '''
    # 公式： sharpe = (回报率的均值 - 无风险利率) / 回报率的标准差
    # 因子项
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year


def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where(data['weekday'] == 3, 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where(data['weekday'] == 0, -1, 0)

    data = compose_singal(data)  # 整合信号
    data = calculate_pro_pct2(data)  # 计算收益率
    data = calculate_cum_prof(data)  # 计算累计收益率
    # data = caculate_max_drawdown(data)  # 最大回撤
    return data

