from fastapi import FastAPI
from apis.products import router as product_route
from apis.category import router as category_route

app=FastAPI(title="Product Service API")

app.include_router(product_route)
app.include_router(category_route)

@app.get("/health-check")
def health_check():
    return {"status":True,"message":"Welcome to product service module!"}