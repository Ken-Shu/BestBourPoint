import sqlite3

def create_table():
    sql = '''
        create table if not exists bfp(
            id integer not null primary key autoincrement,
            symbol text not null,
            best_buy_1 integer,
            best_buy_2 integer,
            best_buy_3 integer,
            best_buy_4 integer,
            best_sell_1 integer,
            best_sell_2 integer,
            best_sell_3 integer,
            best_sell_4 integer,
            transaction_time text,
            price text,
            create_time timestamp default current_timestamp
        )
    '''
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def find_all():
    sql = 'select * from bfp'
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()
    return cursor.execute(sql).fetchall()


def find_one(symbol):
    sql = 'select * from bfp where symbol = ?'
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()
    return cursor.execute(sql, [symbol]).fetchone()



def append_record(symbol, best_buy_1, best_buy_2, best_buy_3, best_buy_4,best_sell_1, best_sell_2, best_sell_3, best_sell_4, transaction_time, price):
    sql = 'insert into bfp(symbol, best_buy_1, best_buy_2, best_buy_3, best_buy_4,best_sell_1, best_sell_2, best_sell_3, best_sell_4, transaction_time, price) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()
    params = [symbol, best_buy_1, best_buy_2, best_buy_3, best_buy_4,best_sell_1, best_sell_2, best_sell_3, best_sell_4, transaction_time, price]
    cursor = cursor.execute(sql, params)
    print('新增筆數:', cursor.rowcount)
    conn.commit()
    conn.close()

def delete_record(symbol):
    sql = 'delete from bfp where symbol = ?'
    conn = sqlite3.connect("stock.db")
    cursor = conn.cursor()
    cursor = cursor.execute(sql, [symbol])
    print('刪除筆數:', cursor.rowcount)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # create_table()
    stocks = find_all()
    print(len(stocks), stocks)
    stock = find_one('2330')
    print(stock)

    prices = stock[11]
    prices = prices.strip('[').strip(']')
    prices = prices.split(', ')
    print(len(prices), prices)

    dates = stock[10]
    dates = dates.strip('[').strip(']').replace('datetime.datetime', '')
    dates = dates.split('), (')
    dates = [item.strip('(') for item in dates]
    print(len(dates), dates)