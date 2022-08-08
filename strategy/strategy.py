'''
用来创建交易策略，生成交易信号
'''

import data.stock as st
import numpy as np


def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where(data['weekday'] == 3, 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where(data['weekday'] == 0, -1, 0)

    # 模拟重复买入：周五在此买入
    data['buy_signal'] = np.where((data['weekday'] == 3) | (data['weekday'] == 4), 1, 0)
    return data


if __name__ == '__main__':
    data = week_period_strategy('000001.XSHE', 'daily', '2020-01-01', '2020-02-28')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal']])
