#-*- encoding:utf-8 -*-
from typing import Pattern
import pandas as pd
import pandas_datareader.data as web
import datetime
from profit import profit_compare
from tqdm import tqdm
import re
import time
import pickle
import matplotlib.pyplot as plt
# 用 yahoo finance 
# start = datetime.datetime(2020, 9, 1)
# end = datetime.datetime(2021, 6, 10)
# # 台灣股市的話要用 股票代號 加上 .TW
# df_2330 = web.DataReader('^TWII', 'yahoo', start, end)
# print(df_2330.tail(5))

# test = pd.read_csv("test.csv",encoding= 'unicode_escape')

def date_str2int(date_str):
    date_year,date_month,date_day = date_str.split("/")
    return int(date_year),int(date_month),int(date_day)

def save_data(data):
    with open('example.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_data():
    with open('example.pickle', 'rb') as handle:
        return pickle.load(handle)

checklist = pd.read_csv("example.csv",engine='python')
print (checklist)

stock_list = checklist["stock"]
stock_list = stock_list.drop_duplicates()
pattern = re.compile(".*\((.*)\)")

# set a new class
pc = profit_compare()

## get data
# for stock_id_str in tqdm(stock_list):
#     # print (stock_id_str)
#     start = datetime.datetime(2015, 11, 27)
#     # end = datetime.datetime(2015, 12, 13)
#     end = datetime.datetime.today()

    

#     result = re.match(pattern,stock_id_str)
#     stock_str = result.group(1)
#     print (stock_str)
    
#     try:
#         stock_df = web.DataReader('{}.TW'.format(stock_str), 'yahoo', start, end)
    
#     except:
#         stock_df = web.DataReader('{}.TWO'.format(stock_str), 'yahoo', start, end)
    
#     stock_df["diff"]=0
#     stock_df["cost"]=0
#     pc.stock_table_dict[stock_str]=stock_df
#     print (stock_df)

# temp save
# save_data(pc.stock_table_dict)
pc.stock_table_dict = load_data()

for data_row in tqdm(checklist.itertuples(index=True)):
    # class_type = data_row["class"]
    # stock_id_str = data_row["stock"]
    # volume = data_row["volume"]
    # price = data_row["price"]
    date_str = data_row[1]
    class_type = data_row[2]
    stock_id_str = data_row[3]
    volume = int(data_row[4])
    price = int(data_row[5])

    # if type(data_row[4])==float:
    #     volume = int(data_row[4])
    # else:
    #     volume = int(data_row[4].replace(',', ''))

    # if type(data_row[5])==float:
    #     price = int(data_row[5])
    # else:
    #     price = int(data_row[5].replace(',', ''))

    result = re.match(pattern,stock_id_str)
    stock_split_str = result.group(1)

    if class_type=="現股買進":
        class_bool = True
    elif class_type=="現股賣出":
        class_bool= False
    else:
        pass
    date_year,date_month,date_day = date_str2int(date_str)
    date = datetime.datetime(date_year, date_month, date_day)

    if stock_split_str=="2330":
        pc.if_debug=True
        pass
    else:
        pc.if_debug=False

    print (date,class_bool,stock_split_str,volume,price)
    pc.calculate_profit(stock_split_str,price,volume,class_bool,date)

for index, (key, value) in enumerate(pc.stock_table_dict.items()):


    if index == 0:
        pc.stock_table_dict[key]["total_profit"]=0
        pc.stock_table_dict[key]["total_cost"]=0

        print (pc.stock_table_dict[key])
        summary = pc.stock_table_dict[key][["total_profit","total_cost"]].copy()
        
        print (summary)
    
    print (pc.stock_table_dict[key])
    summary["total_profit"]+=pc.stock_table_dict[key]["diff"]
    summary["total_cost"]+=pc.stock_table_dict[key]["cost"]

print (summary)

start = datetime.datetime(2019, 10, 23)
summary = summary.loc[summary.index>=start]

# summary.to_csv('after_process.csv',index=True, encoding='utf-8')
summary["percent"]=summary["total_profit"].astype(float)/summary["total_cost"].astype(float)*100
summary["percent"].plot(kind="line")
# summary["total_profit"].plot(kind="line")
# summary["total_cost"].plot(kind="line")


market_table = web.DataReader('^TWII', 'yahoo', start, datetime.datetime.today())
print (market_table)
base = market_table["Close"][0]
summary["market_profit"]= (market_table["Close"]-base)/market_table["Close"]*100
summary["market_profit"].plot(kind="line")

plt.legend(["total_profit","market_profit"])
plt.ylabel("percent")
# summary["total_profit"].plot()
# plt.legend(["percent", "total_profit","total_cost"])
plt.show()
# print (stock_list)
# date_year,date_month,date_day = date_str2int(checklist["date"][0])
# start = datetime.datetime(date_year, date_month, date_day)
# date_year,date_month,date_day = date_str2int(checklist["date"][2])
# end =  datetime.datetime(date_year, date_month, date_day)
# df_2330 = web.DataReader('10632R.TW', 'GOOG', start, end)
# print (df_2330)




