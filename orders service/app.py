from fastapi import FastAPI
from apis.order import route as order_route

app=FastAPI(title="Inventory Service API")

app.include_router(order_route)

@app.get("/health-check")
def health_check():
    return {"status":True,"message":"Welcome to product service module!"}