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
from pyxirr import xirr
# from pandas_datareader import data

# 用 yahoo finance 
# start = datetime.datetime(2020, 9, 1)
# end = datetime.datetime(2021, 6, 10)
# 台灣股市的話要用 股票代號 加上 .TW
# df_2330 = web.DataReader('1101.TW', 'yahoo-actions')
# df_2330 = web.DataReader('^TWII', 'yahoo', start, end)
# print(df_2330)

# test = pd.read_csv("test.csv",encoding= 'unicode_escape')

def date_str2int(date_str):
    date_year,date_month,date_day = date_str.split("/")
    return int(date_year),int(date_month),int(date_day)

def save_data(data):
    with open('example_add_volume.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_data():
    with open('example_add_volume.pickle', 'rb') as handle:
        return pickle.load(handle)

# Buy symbol
#######################################
Buy_symbol = "現股買進"
Sell_symbol = "現股賣出"
#######################################

checklist = pd.read_csv("example.csv",engine='python')
print (checklist)
checklist["cash_flow"]=checklist["volume"]*checklist["price"]*\
    checklist["class"].map({Buy_symbol:-1, Sell_symbol:1})
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
#     stock_df["volume"]=0
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
    cashflow = int(data_row[6])

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

    if class_type==Buy_symbol:
        class_bool = True
    elif class_type==Sell_symbol:
        class_bool= False
    else:
        pass
    date_year,date_month,date_day = date_str2int(date_str)
    date = datetime.datetime(date_year, date_month, date_day)

    # if stock_split_str=="2330":
    #     pc.if_debug=True
    #     pass
    # else:
    #     pc.if_debug=False

    print (date,class_bool,stock_split_str,volume,price)
    pc.calculate_profit(stock_split_str,price,volume,class_bool,date)

for index, (key, value) in enumerate(pc.stock_table_dict.items()):


    if index == 0:
        pc.stock_table_dict[key]["total_profit"]=0
        pc.stock_table_dict[key]["total_cost"]=0
        pc.stock_table_dict[key]["sell_all"]=0

        print (pc.stock_table_dict[key])
        summary = pc.stock_table_dict[key][["total_profit","total_cost","sell_all"]].copy()
        
        print (summary)
    
    print (pc.stock_table_dict[key])
    summary["total_profit"]+=pc.stock_table_dict[key]["diff"]
    summary["total_cost"]+=pc.stock_table_dict[key]["cost"]
    summary["sell_all"]+=pc.stock_table_dict[key]["volume"]*pc.stock_table_dict[key]["Close"]

# print (summary)
start = datetime.datetime(2019, 10, 23)
summary = summary.loc[summary.index>=start]
print (summary)

## add xirr list
print (checklist)
checklist['date'] = pd.to_datetime(checklist['date'], format='%Y/%m/%d')
# checklist = checklist.loc[checklist.date>=start]
print (checklist)
market_table = web.DataReader('^TWII', 'yahoo', start, datetime.datetime.today())

for data_row in tqdm(summary.itertuples(index=True)):
    date = data_row.Index

    ## total profit
    less_then_date = checklist.loc[checklist['date']<date]
    equal_date = checklist.loc[checklist['date']==date]

    
    

    # print (less_then_date)
    # print (equal_date)
    num_row = less_then_date.shape[0]
    total_cash_flow = less_then_date[["date","cash_flow"]]

   
    #if date exist in checklist
    if equal_date.shape[0]!=0:      
        
        total_cash_flow.loc[-1]=[date,summary.loc[date,"sell_all"].copy()+equal_date["cash_flow"].sum().copy()]
    #date not in checklist
    else:
        total_cash_flow.loc[-1]=[date,summary.loc[date,"sell_all"].copy()]
    # print (total_cash_flow)
    # new_add_date = summary.loc[date,"sell_all"].copy()
    # print (new_add_date)
    if num_row==0:
        summary.loc[date,"apy"]=0
        continue
    else:
        # print (xirr(total_cash_flow))
        # if xirr(total_cash_flow)>30.0:
        #     pass
        #     summary.loc[date,"apy"]=0
        #     print (total_cash_flow)
        # else:
        summary.loc[date,"apy"]=xirr(total_cash_flow)
        
        ## market profit
        market_equal_date = market_table.loc[market_table.index==date]
        dates = [market_table.index[0]]
        values = [market_table.iloc[0]["Close"]*-1]
        market_cash_flow = pd.DataFrame(zip(dates, values))
        # print (market_cash_flow)

        market_cash_flow.loc[-1]=[date,market_table.loc[date,"Close"].copy()]        
        # print (market_cash_flow)
        summary.loc[date,"market_apy"]=xirr(market_cash_flow)*100
        
        # print (summary)
    

    


start = datetime.datetime(2020, 1, 1)
summary = summary.loc[summary.index>=start]


summary["apy"]=summary["apy"]*100
summary['apy'] = summary['apy'].fillna(0)
print (summary)
# summary.to_csv('after_process.csv',index=True, encoding='utf-8')
summary["percent"]=summary["total_profit"].astype(float)/summary["total_cost"].astype(float)*100

summary["percent"].plot(kind="line")
summary["apy"].plot(kind="line")

# summary["total_profit"].plot(kind="line")
# summary["total_cost"].plot(kind="line")



print (market_table)
base = market_table["Close"][0]
summary["market_profit"]= (market_table["Close"]-base)/market_table["Close"]*100
summary["market_profit"].plot(kind="line")
summary["market_apy"].plot(kind="line")

plt.legend(["total_profit","apy","market_profit","market_apy"])
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




