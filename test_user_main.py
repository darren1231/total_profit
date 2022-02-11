from user_main import User
import datetime

user = User()

def test_get_stock_history():
    start = datetime.datetime(2015, 11, 27)
    end = datetime.datetime(2015, 12, 13)
    user.get_stock_history(start,end,"2330")

test_get_stock_history()