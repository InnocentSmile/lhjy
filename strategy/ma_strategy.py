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
    print(f"========当前周期参数： {short_window}， {long_window}")
    data = pd.DataFrame(data)
    # 计算技术指标： ma短期 ma长期
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    # 生成信号： 金叉买入 死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)

    # 过滤信号 strat.compose_singal
    data = strat.compose_singal(data)

    # 计算单次收益
    data = strat.calculate_pro_pct(data)
    # 计算累计收益
    data = strat.calculate_cum_prof(data)

    # 删除多余的columns
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)
    # 数据预览
    print(data[['close', 'short_ma', 'long_ma', 'signal', 'cum_profit']])
    return data


if __name__ == '__main__':
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    # 存款累计收益率
    cum_profits = pd.DataFrame()
    for code in stocks:
        df = st.get_single_price(code=code,
                                   time_freq="daily",
                                   start_date="2016-01-01",
                                   end_date="2021-01-01")
        df = ma_strategy(df)  # 调用双均线策略
        cum_profits[code] = df['cum_profit'].reset_index(drop=True)  # 存储累计收益率

        # 折线图
        df['cum_profit'].plot(label=code)
        # 筛选有信号点
        # df = df[df['signal'] != 0]
        # 预览数据
        print(f"开仓次数{int(len(df))}")
        # print(df[['close', 'short_ma', 'long_ma', 'signal']])
        # print(df[['close', 'signal', 'profit_pct', 'cum_profit']])
    print(cum_profits)
    cum_profits.plot()
    plt.title('Comparison of Ma Strategy Profits')
    plt.show()
