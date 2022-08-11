import pandas as pd

import data.stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt

# 容器： 存放夏普
sharpes = []
# 获取三只股票的数据: 比亚迪 宁德时代 隆基
codes = ['002584.XSHE', '300750.XSHE', '601012.XSHG']
for code in codes:
    data = st.get_single_price(code, 'daily', '2018-10-01', '2021-01-01')
    print(data.head())
    # 计算每只股票的夏普比率
    sharpe, sharpe_year = stb.calculte_sharpe(data)
    sharpes.append([code, sharpe_year])  #存放夏普
    print(sharpes)

# 可视化3只股票并比较
sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code')
print(sharpes)

sharpes.plot.bar(title="Compare Annual Sharpe Ratio")
plt.xticks(rotation=20)
plt.show()



