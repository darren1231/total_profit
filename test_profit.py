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

    ##
    # diff: the profit for each day(unrealized+realized)
    # cost:  the cost for each day
    # volume: the volume remain for each day
    #
    # ochw_table["diff_temp"]=(ochw_table["Close"]-price)*volume
    # ochw_table["cost_temp"]=price*volume
    # ochw_table["volume_temp"]=volume

    # summary["total_profit"]+=stock_table_dict[key]["diff"]
    # summary["total_cost"]+=stock_table_dict[key]["cost"]
    # summary["sell_all"]+=stock_table_dict[key]["volume"]*stock_table_dict[key]["Close"]
    ##
    pc.stock_table_dict[stock_code]["diff"]=0
    pc.stock_table_dict[stock_code]["cost"]=0
    pc.stock_table_dict[stock_code]["volume"]=0
    pc.stock_table_dict[stock_code]["realized_profit"]=0
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

def test_xirr():
    pc = profit_compare()
    data = [(datetime.date(2006, 1, 24), -39967), (datetime.date(2008, 2, 6), -19866), (datetime.date(2010, 10, 18), 245706), (datetime.date(2013, 9, 14), 52142)]
    data = [ (datetime.date(2013, 9, 14), -52142)]
    print (pc.xirr(data))

test_calculate_profit()
# test_xirr()