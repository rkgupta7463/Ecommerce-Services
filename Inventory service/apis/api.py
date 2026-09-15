from fastapi import APIRouter

route=APIRouter(prefix="/api/order",tags=["Orders"])

@route.post('/create')
def prod_order():
    return {"status":True,"message":"Welcome message from order servic!"}