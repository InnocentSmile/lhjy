import data.stock as st

'''获取价格，并且计算涨跌幅'''

# 获取平安银行的行情数据（日K）
data = st.get_single_price('000001.XSHE', 'daily', '2020-01-01', '2020-02-1')
print(data)
# 计算涨跌幅，验证准确性
data = st.calculate_change_pct(data)
print(data)

# 获取周K
data = st.transfer_price_freq(data, 'w')
# 计算涨跌幅，验证准确性
data = st.calculate_change_pct(data)
print(data)
