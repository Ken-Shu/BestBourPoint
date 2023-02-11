import twstock
import matplotlib.pyplot as plt
from BFP_Dao import append_record
'''
認識 BestFourPoint
透過四大買賣點來判斷是否要買賣股票。四個買賣點分別為：
+------------------+-------------------+
| 四大買點           | 四大賣點           |
+------------------+-------------------+
| 量大收紅           | 量大收黑           |
+------------------+-------------------+
| 量縮價不跌         | 量縮價跌           |
+------------------+-------------------+
| 三日均價由下往上    | 三日均價由上往下    |
+------------------+-------------------+
| 三日均價大於六日均價 | 三日均價小於六日均價 |
+------------------+-------------------+
'''

if __name__ == '__main__':
    symbol = input('請輸入股票代號(例如:2330)')
    # symbol = '2327'
    print('分析標的', symbol)
    stock = twstock.Stock(symbol)  # 取的標的物件
    print(stock.data)
    print(stock.price)
    bfp = twstock.BestFourPoint(stock)
    buy = bfp.best_four_point_to_buy()
    sell = bfp.best_four_point_to_sell()
    summary = bfp.best_four_point()
    print("buy : ", buy)  # False 表示無分析資料
    print(bfp.best_buy_1(), bfp.best_buy_2(), bfp.best_buy_3(), bfp.best_buy_4())
    print("sell : ", sell)  # False 表示無分析資料
    print(bfp.best_sell_1(), bfp.best_sell_2(), bfp.best_sell_3(), bfp.best_sell_4())
    print("summary : ", summary)  # True 建議買進 False 建議賣出

    # 加入資料表
    append_record(symbol, bfp.best_buy_1(), bfp.best_buy_2(), bfp.best_buy_3(), bfp.best_buy_4(), bfp.best_sell_1(), bfp.best_sell_2(), bfp.best_sell_3(), bfp.best_sell_4(), str(stock.date), str(stock.price))
    print('寫入成功')
    '''
    for data in stock.raw_data:
        print(data['date'], data['title'])
        for item in data['fields']:
            print(item)
            '''
    # 繪圖
    plt.title(symbol)
    plt.plot(stock.data, stock.price, 'b-', linewidth=1)
    plt.grid(True)  # 格線
    plt.savefig(symbol + '.png')
    plt.show()
