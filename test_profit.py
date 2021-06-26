from profit import profit_compare
import datetime
import pickle

def load_data():
    with open('test.pickle', 'rb') as handle:
        return pickle.load(handle)

def test_stock_code():
    pc = profit_compare()
    pc.add_stock_code(2330,50)
    pc.add_stock_code(2330,100)
    pc.add_stock_code(2317,100)
    pc.show_stock_code_dict()
    pc.del_stock_code(2317,100)
    pc.show_stock_code_dict()

def test_calculate_profit():
    pc = profit_compare()
    stock_code = "2330"
    pc.stock_table_dict[stock_code]=load_data()
    pc.stock_table_dict[stock_code]["diff"]=0
    pc.stock_table_dict[stock_code]["cost"]=0
    pc.stock_table_dict[stock_code]["volume"]=0
    pc.if_debug = True
    date = datetime.datetime(2015, 11, 30)
    pc.calculate_profit(stock_code,140,50,True,date)
    date = datetime.datetime(2015, 12, 1)
    pc.calculate_profit(stock_code,140,50,True,date)

    date = datetime.datetime(2015, 12, 4)
    pc.calculate_profit(stock_code,140.5,50,False,date)
    date = datetime.datetime(2015, 12, 8)
    pc.calculate_profit(stock_code,142.5,50,False,date)

    date = datetime.datetime(2015, 12, 14)
    pc.calculate_profit(stock_code,139.5,50,True,date)

test_calculate_profit()