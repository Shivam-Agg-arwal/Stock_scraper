from fastapi import FastAPI
from scraper import scrape_stock_data

app = FastAPI()

@app.get("/{symbol}")
def get_stock_data(symbol: str):
    result = scrape_stock_data(symbol)
    return result
