import data.stock as st
import strategy.ma_strategy as ma
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

'''
寻找最优参数（以MA双均线策略为例）
'''
# stocks = ["000001.XSHE"]
data = st.get_csv_price('000001.XSHE', '2016-01-01', '2021-01-01')
# 参数1：股票池

# 参数2：周期参数
params = [5, 10, 20, 60, 120, 150]
# 存放收益和参数
res = []

# 匹配并计算不同的周期参数对：5-10，5-20 ...... 120-250
for short in params:
    for long in params:
        if long > short:
            data_res = ma.ma_strategy(data, short, long)
            # 获取周期参数，及其对应累计收益率
            cum_profit = data_res['cum_profit'].iloc[-1]
            res.append([short, long, cum_profit])
# 将结果列表转换为dataframe， 并找到最优参数
print(res)
res = pd.DataFrame(res, columns=['short_win', 'long_win', 'cum_profit'])
res.sort_values(by='cum_profit', ascending=False)  # 按收益倒序排列
print(res)
