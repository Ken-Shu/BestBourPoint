import uvicorn
import time
from io import BytesIO

from PIL import ImageFilter, Image
from starlette.responses import StreamingResponse

from BFP_Service import get_one, query_all, add
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/book/{book_id}')
def get_book_by_id(book_id: int):
    return {
        'book_id': book_id
    }

@app.get('/bfp/add/{symbol}')
def add_stock_by_symbol(symbol: str):
    add(symbol)
    stock = get_one(symbol)
    return stock

@app.get('/bfp/get/{symbol}')
def get_stock_by_symbol(symbol: str):
    stock = get_one(symbol)
    return stock

@app.get('/bfp/chart/{symbol}', response_class=FileResponse)
def get_chart_by_symbol(symbol: str):
    try:
        file = open(symbol + '.png', 'rb')
    except FileNotFoundError as e:
        # 若沒有找到圖就重新新增股票
        add_stock_by_symbol(symbol)
        time.sleep(5)
        try:
            file = open(symbol + '.png', 'rb')
        except FileNotFoundError as e:
            return None

    try:
        original_image = Image.open(file)
        #original_image = original_image.filter(ImageFilter.BLUR)  # 模糊處理
        original_image = original_image.filter(ImageFilter.UnsharpMask)  # 銳利處理

        filtered_image = BytesIO()
        original_image.save(filtered_image, "PNG")
        filtered_image.seek(0)

        return StreamingResponse(filtered_image, media_type="image/png")
    except KeyError as e:
        return None

@app.get('/bfp/query/all')
def qyery_stocks():
    return query_all()


if __name__ == '__main__':
    # uvicorn.run('api:app')
    uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="info")

