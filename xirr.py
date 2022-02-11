
import datetime

from datetime import date
from pyxirr import xirr
import pandas as pd
dates = [date(2020, 1, 1), date(2020, 3, 1), date(2020, 10, 30), date(2021, 2, 15)]
values = [-10_000, -5750, -4250, -3250]
print (xirr(dates, values))
pd_data = pd.DataFrame(zip(dates, values))
print (pd_data)
print (xirr(pd_data))
# 函數
def xirr(cashflows):
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


# 測試
data = [(datetime.date(2006, 1, 24), -39967), (datetime.date(2008, 2, 6), -19866), (datetime.date(2010, 10, 18), 245706), (datetime.date(2013, 9, 14), 52142)]
print (xirr(data))