import data.stock as st
import strategy.ma_strategy as mastrat
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


def ttest(data_return):
    '''
    对策略收益进行t检验
    :param strat_return: dataframe， 单次收益率
    :return: float，t值和p值
    '''
    # 调用假设检验ttest函数：scipy
    # 获取t p
    t, p = stats.ttest_1samp(data_return, 0, nan_policy='omit')

    # 判断是否与理论均值有显著差异: α=0.05
    p_value = p / 2
    print(f"t_value={t},p_value={p_value}")
    print("是否可以拒绝H0：收益均值 = 0：", p_value < 0.05)
    return t, p_value


if __name__ == '__main__':
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    for code in stocks:
        print(code)
        # 存款累计收益率
        df = st.get_single_price(code=code,
                                 time_freq="daily",
                                 start_date="2016-12-01",
                                 end_date="2021-01-01")
        df = mastrat.ma_strategy(df)  # 调用双均线策略
        # 策略的单次收益率
        returns = df['profit_pct']
        # print(returns)

        # 绘制一下分布图用于观察
        # plt.hist(returns, bins=30)
        # plt.show()

        # 对多个股票进行计算 测试
        ttest(returns)
