from fastapi import FastAPI
from apis.api import router as inventory_router

app=FastAPI(title="Inventory Managment Service API")
app.include_router(router=inventory_router)

@app.get('/health-check')
def inventory_heath_check():
    return {"status":True,"message":"Welcome message from Inventory servic!"}

    