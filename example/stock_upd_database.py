import data.stock as st

# 初始化code
code = "000002.XSHE"
# 调用一直股票的行情数据
# data = st.get_single_price(code=code,
#                            time_freq="daily",
#                            start_date="2021-01-01",
#                            end_date="2021-02-01")
# # 存入csv
# st.export_data(data=data, filename=code, type="price")


# 从csv中获取数据
# data = st.get_csv_data(code, 'price')
# print(data)

# 实时更新数据： 假设每天更新日K数据 ---> 存在csv文件里面 ---> data.to_csv(append)


# 1.获取所有股票代码
# stock_list = st.get_stock_list()
# 2.存储到csv文件中
# for code in stock_list:
#     df = st.get_single_price(code, 'daily')
#     st.export_data(df, filename=code, type="price")
# 3.每日更新数据
st.init_db()
# for code in stock_list:
#     st.update_daily_price(code, 'price')
