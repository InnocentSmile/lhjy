'''
用来创建交易策略，生成交易信号
'''

import data.stock as st
import strategy.base as strat
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

'''
双均线策略
'''


def ma_strategy(data, short_window=5, long_window=20):
    '''

    :param data: datadrame, 投资标的行情数据（必须包含收盘价）
    :param short_window: 短期n日移动平均线，默认5
    :param long_window: 长期n日移动平均线，默认20
    :return:
    '''
    data = pd.DataFrame(data)
    # 计算技术指标： ma短期 ma长期
    data['short_ma'] = data['close'].rolling(window=short_window).min()
    data['long_ma'] = data['close'].rolling(window=long_window).min()
    # 生成信号： 金叉买入 死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], 1, 0)

    # 过滤信号 strat.compose_singal
    data = strat.compose_singal(data)

    # 数据预览
    # print(data[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal', 'signal']])

    # 删除多余的columns
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)
    return data


if __name__ == '__main__':
    code = '000001.XSHE'
    data = st.get_single_price(code=code,
                               time_freq="daily",
                               start_date="2020-01-01",
                               end_date="2021-01-01")
    df = ma_strategy(data)
    print(df[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal', 'signal']])
