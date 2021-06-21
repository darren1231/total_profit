# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 16:41:39 2018
@author: darren
"""


import pandas as pd
import requests
import re

def fetch_table(url):
    """
    fetch table from the Internet
    Args:
        url: website url
    Return:
        pd_table : pandas table
    """
    
    
    # pretend to be the chrome brower to solve the forbidden problem
    header = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    html_text = requests.get(url, headers=header)
    
    # to solve garbled text
    html_text.encoding =  html_text.apparent_encoding
    pd_table = pd.read_html(html_text.text)[0]
    
    return pd_table

def store_csv():
    """
    Store the information to csv file
    """
    url_stock = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    url_otc = "http://isin.twse.com.tw/isin/C_public.jsp?strMode=4"
    stock_table = fetch_table(url_stock)
    stock_table.to_csv("stock_name.csv",index=None,encoding="utf_8_sig")
    otc_table = fetch_table(url_otc)
    otc_table.to_csv("otc_name.csv",index=None,encoding="utf_8_sig")

def extract_code(index_range,csv_string):
    """
    extract code from pandas data frame
    Args:
        index_range: a list which length is 2, containing start and end index
        csv_string : the name to the csv file
        
    Return:
        code_list: a list contain stock code
    """
    code_list = []
    table = pd.read_csv(csv_string)
    
    start = index_range[0]
    end  = index_range[1]
    
    for i in range(start,end):
        string = table.iloc[i][0]        
        pattern = "\d*"
        code = re.compile(pattern).findall(string)[0]
        code_list.append(code)
        
    return code_list

# store_csv()
# oct_code_list = extract_code([4452,5210],"otc_name.csv")
# print ("The length of oct:",len(oct_code_list))
# print(oct_code_list)
#
stock_code_list = extract_code([2,918],"stock_name.csv")
print ("The length of stock:",len(stock_code_list))
print (stock_code_list)