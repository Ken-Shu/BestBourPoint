import twstock
from BFP_Dao import find_all, find_one, append_record, delete_record
import matplotlib.pyplot as plt
def parse_stock(stock):
    stock = list(stock)
    # print(len(stock), type(stock), stock)
    prices = stock[11]
    prices = prices.strip('[').strip(']')
    prices = prices.split(', ')
    stock[11] = prices

    dates = stock[10]
    dates = dates.strip('[').strip(']').replace('datetime.datetime', '')
    dates = dates.split('), (')
    dates = [item.strip('(') for item in dates]
    stock[10] = dates
    return tuple(stock)

def stock_orm(data):
    stock = {}
    stock.setdefault('id', data[0])
    stock.setdefault('symbol', data[1])
    stock.setdefault('best_buy_1', data[2])
    stock.setdefault('best_buy_2', data[3])
    stock.setdefault('best_buy_3', data[4])
    stock.setdefault('best_buy_4', data[5])
    stock.setdefault('best_sell_1', data[6])
    stock.setdefault('best_sell_2', data[7])
    stock.setdefault('best_sell_3', data[8])
    stock.setdefault('best_sell_4', data[9])
    stock.setdefault('transaction_time', data[10])
    stock.setdefault('prices', data[11])
    stock.setdefault('create_time', data[12])
    return stock

def query_all():
    stocks = find_all()
    stocks = [stock_orm(parse_stock(stock)) for stock in stocks]
    return stocks


def get_one(symbol):
    stock = find_one(symbol)
    try:
        stock = stock_orm(parse_stock(stock))
    except Exception as e:
        stock = {
            "message": "無此代號"
        }
    return stock

def add(symbol):
    stock = twstock.Stock(symbol)  # 取得標的物件
    bfp = twstock.BestFourPoint(stock)
    # 刪除紀錄
    delete_record(symbol)
    # 加入資料表
    append_record(symbol, bfp.best_buy_1(), bfp.best_buy_2(), bfp.best_buy_3(), bfp.best_buy_4(), bfp.best_sell_1(),
                  bfp.best_sell_2(), bfp.best_sell_3(), bfp.best_sell_4(),
                  str(stock.date), str(stock.price))
    # 產生 chart
    # 繪圖
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title(symbol + "走勢圖")
    plt.ylabel("價格")
    plt.xlabel("時間")
    plt.plot(stock.date, stock.price, 'b-', linewidth=1, label='價格')
    plt.legend()  # 加入圖例
    plt.grid(True)  # 格線
    plt.savefig(symbol + '.png')


if __name__ == '__main__':
    print(query_all())
    print(get_one('2330'))
    add('2330')