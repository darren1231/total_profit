import pandas_datareader.data as web
import pickle

class profit_compare(object):

    def __init__(self):
        self.stock_code_dict={}
        self.stock_table_dict={}
        self.net_profit = 0
        self.cost = 0
        self.handling_fee = 0.001425
        self.tax_fee = 0.003
        self.unrealized_profit=0
        self.realized_profit=0
        self.if_debug=False

    def add_stock_code(self, stock_code,volume):
        """
        return:
            if_add:
        """

        if stock_code in self.stock_code_dict.keys():
            self.stock_code_dict[stock_code]+=volume
            return True
        else:
            self.stock_code_dict[stock_code]=volume
            return False

    def del_stock_code(self, stock_code,volume):
        """

        return:
            if_empty:
        """

        if stock_code in self.stock_code_dict.keys():
            self.stock_code_dict[stock_code]-=volume

            # if volume is empty
            if self.stock_code_dict[stock_code]<=0:
                del self.stock_code_dict[stock_code]
                return True
            else: #self.stock_code_dict[stock_code]>0:
                return False
            # else:
            #     raise ValueError("error {} {}".format(self.stock_code_dict[stock_code],stock_code)) 
        else:
            raise ValueError("error {} {}".format(self.stock_code_dict[stock_code],stock_code)) 

    def show_stock_code_dict(self):

        for key,value in self.stock_code_dict.items():
            print (key,value)
    def show_stock_table_dict(self):
        for key,value in self.stock_table_dict.items():
            print (key,value)

    def save_data(self,data):
        with open('test.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load_data(self):
        with open('test.pickle', 'rb') as handle:
            return pickle.load(handle)

    def debug_for_table(self,table):

        if self.if_debug==True:
            print (table)


    def calculate_profit(self,stock_code,price,volume,if_b,date):
        """
        stock_code: the id to the stock
        price: the price for buy or sell
        volume: the volume of the stock
        if_b: whether buy or sell (boolean)
        date: ex:datetime.datetime(2015, 11, 30)
        """
        ochw_table = self.stock_table_dict[stock_code]

        
        ## buy stock
        if if_b:
            if_add_before = self.add_stock_code(stock_code,volume)

            ochw_table["diff_temp"]=(ochw_table["Close"]-price)*volume
            ochw_table["cost_temp"]=price*volume
            ochw_table["volume_temp"]=volume

            self.debug_for_table(ochw_table)
            ochw_table.loc[ochw_table.index<date,"diff_temp"]=0
            ochw_table.loc[ochw_table.index<date,"cost_temp"]=0
            ochw_table.loc[ochw_table.index<date,"volume_temp"]=0
            self.debug_for_table(ochw_table)
            ochw_table["diff"]+= ochw_table["diff_temp"]
            ochw_table["cost"]+= ochw_table["cost_temp"]
            ochw_table["volume"]+= ochw_table["volume_temp"]
            self.debug_for_table(ochw_table)
            ochw_table=ochw_table.drop(columns=["diff_temp"])
            ochw_table=ochw_table.drop(columns=["cost_temp"])
            ochw_table=ochw_table.drop(columns=["volume_temp"])
            self.debug_for_table(ochw_table)

        
        ## sell stock
        else:
            if_empty = self.del_stock_code(stock_code,volume)
            
            
            ochw_table["diff_temp"]=(ochw_table["Close"]-price)*volume*-1
            ochw_table["cost_temp"]=price*volume
            ochw_table["volume_temp"]=volume

            
            self.debug_for_table (ochw_table)
            ochw_table.loc[ochw_table.index<date,"diff_temp"]=0
            ochw_table.loc[ochw_table.index<date,"cost_temp"]=0
            ochw_table.loc[ochw_table.index<date,"volume_temp"]=0
            self.debug_for_table (ochw_table)

            

            ochw_table["diff"]+= ochw_table["diff_temp"]
            ochw_table["cost"]-= ochw_table["cost_temp"]
            ochw_table["volume"]-= ochw_table["volume_temp"]
            ochw_table=ochw_table.drop(columns=["diff_temp"])
            ochw_table=ochw_table.drop(columns=["cost_temp"])
            ochw_table=ochw_table.drop(columns=["volume_temp"])

            if  if_empty:
                ochw_table.loc[ochw_table.index>=date,"realized_profit_temp"]=ochw_table.loc[ochw_table.index>=date,"cost"]*-1
                ochw_table.loc[ochw_table.index<date,"realized_profit_temp"]=0
                ochw_table["realized_profit"]+= ochw_table["realized_profit_temp"]
                ochw_table=ochw_table.drop(columns=["realized_profit_temp"])

                ochw_table.loc[ochw_table.index>=date,"cost"]=0
                ochw_table.loc[ochw_table.index>=date,"volume"]=0
            

            self.debug_for_table (ochw_table)
        ## update
        self.stock_table_dict[stock_code]=ochw_table
    
    def xirr(self,cashflows):
        years = [(ta[0] - cashflows[0][0]).days / 365. for ta in cashflows]
        residual = 1.0
        step = 0.05
        guess = 0.05
        epsilon = 0.0001
        limit = 10000
        while abs(residual) > epsilon and limit > 0:
            limit -= 1
            residual = 0.0
            for i, trans in enumerate(cashflows):
                residual += trans[1] / pow(guess, years[i])
            if abs(residual) > epsilon:
                if residual > 0:
                    guess += step
                else:
                    guess -= step
                    step /= 2.0
        return guess - 1