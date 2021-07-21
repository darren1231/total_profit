#-*- encoding:utf-8 -*-
from typing import Pattern
import pandas as pd
from pandas.io.parsers import read_csv
import pandas_datareader.data as web
import datetime
from profit import profit_compare
from tqdm import tqdm
import re
import time
import pickle
import matplotlib.pyplot as plt
from pyxirr import xirr
import yfinance as yf
# yf.pdr_override()

class User(object):
    def __init__(self):
        self.Buy_symbol = "現股買進"
        self.Sell_symbol = "現股賣出"
        self.checklist=self.read_action_csv(True)

    def read_action_csv(self,debug=False):

        file_path="example.csv"
        checklist = pd.read_csv(file_path,engine='python')
        if debug:
            print(checklist)

        return checklist
    
    def add_cash_flow(self):

        checklist = self.checklist
        checklist["cash_flow"]=checklist["volume"]*checklist["price"]*\
        checklist["class"].map({self.Buy_symbol:-1, self.Sell_symbol:1})
        self.checklist = checklist

        

    def get_stock_list(self,debug=False):

        checklist = self.checklist
        stock_list = checklist["stock"]
        stock_list = stock_list.drop_duplicates()

        process=[]
        pattern = re.compile(".*\((.*)\)")
        for stock_id_str in stock_list:

            result = re.match(pattern,stock_id_str)
            stock_str = result.group(1)
            process.append(stock_str)
            
        if debug:
            print(stock_list)

        return process
    
    
    def get_stock_history(self,start,end,stock_str):
        """
        Args:
            start: start date
            end: end date
            stock_str: the id of the stock
        
        Return:
            stock_df: pandas data


        """
        try:
            stock_df = web.DataReader('{}.TW'.format(stock_str), 'yahoo', start, end)
        
        except:
            stock_df = web.DataReader('{}.TWO'.format(stock_str), 'yahoo', start, end)
        
        stock_df["diff"]=0
        stock_df["cost"]=0
        stock_df["volume"]=0

        return stock_df

    def save_data(self,data,file_name):
        with open(file_name, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_data(self,file_name):
        with open(file_name, 'rb') as handle:
            return pickle.load(handle)

    def date_str2int(self,date_str):
        date_year,date_month,date_day = date_str.split("/")
        return int(date_year),int(date_month),int(date_day)
    
    def calculate_profit(self):
        pattern = re.compile(".*\((.*)\)")

        for data_row in tqdm(self.checklist.itertuples(index=True)):
            
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

            if class_type==self.Buy_symbol:
                class_bool = True
            elif class_type==self.Sell_symbol:
                class_bool= False
            else:
                pass
            date_year,date_month,date_day = self.date_str2int(date_str)
            date = datetime.datetime(date_year, date_month, date_day)

            # if stock_split_str=="2330":
            #     pc.if_debug=True
            #     pass
            # else:
            #     pc.if_debug=False

            print (date,class_bool,stock_split_str,volume,price)
            pc.calculate_profit(stock_split_str,price,volume,class_bool,date)

    def summary(self,stock_table_dict):
        for index, (key, value) in enumerate(stock_table_dict.items()):


            if index == 0:
                stock_table_dict[key]["total_profit"]=0
                stock_table_dict[key]["total_cost"]=0
                stock_table_dict[key]["sell_all"]=0

                print (stock_table_dict[key])
                summary = stock_table_dict[key][["total_profit","total_cost","sell_all"]].copy()
                
                print (summary)
            
            print (pc.stock_table_dict[key])
            summary["total_profit"]+=stock_table_dict[key]["diff"]
            summary["total_cost"]+=stock_table_dict[key]["cost"]
            summary["sell_all"]+=stock_table_dict[key]["volume"]*stock_table_dict[key]["Close"]
        return summary
    
    def compare_market(self,summary):
        
        checklist=self.checklist
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
        return summary,market_table
    
    def plot_summary(self,summary,market_table):
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

if __name__=="__main__":
    # set a new class
    user = User()    
    pc = profit_compare()
    stock_id_list = user.get_stock_list(debug=True)


    ## Step1:Get history of stock data
    ###############################################
    # start = datetime.datetime(2015, 11, 27)
    # # end = datetime.datetime(2015, 12, 13)
    # end = datetime.datetime.today()
    # for stock_id in tqdm(stock_id_list):
    #     stock_df=user.get_stock_history(start,end,stock_id)
    #     pc.stock_table_dict[stock_id]=stock_df
    # user.save_data(pc.stock_table_dict,"20210720_stock_data.pickle")
    pc.stock_table_dict = user.load_data('20210720_stock_data.pickle')
    ###############################################
    # Step2: calculate profit
    # pc.if_debug = True
    user.add_cash_flow()
    user.calculate_profit()

    summary=user.summary(pc.stock_table_dict)
    start = datetime.datetime(2019, 10, 23)
    summary = summary.loc[summary.index>=start]
    print (summary)
    # market_table = web.DataReader('^TWII', 'yahoo', start, datetime.datetime.today())
    #################################################
    #Step3: Compare market
    summary,market_table=user.compare_market(summary)
    user.plot_summary(summary,market_table)
    # print (summary)

    
