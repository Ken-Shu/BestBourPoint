import time
from io import BytesIO

from PIL import Image, ImageFilter
from starlette.responses import StreamingResponse

from BFP_Service import get_one, query_all, add
from fastapi import FastAPI
from starlette.responses import FileResponse

app = FastAPI()

@app.get('/book/{book_id}')
def get_book_by_id(book_id: int):
    return {
        'book_id': book_id
    }

@app.get('/bfp/add/{symbol}')
def add_stock_by_symbol(symbol: str):
    add(symbol)
    stock= get_one(symbol)
    return stock

@app.get('/bfp/get/{symbol}')
def get_stock_by_symbol(symbol: str):
    stock = get_one(symbol)
    return stock

@app.get('/bfp/chart/{symbol}',response_class=FileResponse)
def get_chart_by_symbol(symbol: str):
    try:
        file = open(symbol + '.png', 'rb')
    except FileNotFoundError as e:
        # 若沒有找到圖就重新新增股票
        add_stock_by_symbol(symbol)
        time.sleep(5)
        try:
            file = open(symbol + '.png', 'rb')
        except FileNotFoundError as e :
            return None
    try:
        original_image = Image.open(file)
        '''
        BLUR 模糊
        CONTOUR 輪廓
        DETAIL 細節
        EDGE_ENHANCE 邊緣增強
        EDGE_ENHANCE_MORE EDGE_ENHANCE_更多
        EMBOSS 浮雕
        FIND_EDGES 尋找邊緣
        SHARPEN 銳化
        SMOOTH 光滑的
        SMOOTH_MORE 平滑_更多
        '''
        # original_image = original_image.filter(ImageFilter.BLUR) 模糊處理

        filtered_image = BytesIO()
        original_image.save(filtered_image, "PNG")
        filtered_image.seek(0)

        return StreamingResponse(filtered_image, media_type="image/jpeg")
    except KeyError as e:
        return None
@app.get('/bfp/query/all')
def all():
    return query_all()

