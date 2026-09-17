from typing import Annotated
from fastapi import APIRouter,Depends,Body
from authorization.auth_verify import user_detail_verify
from query.permissions import permission_list
from query.product import *
from pydantic import Field,BaseModel
from RateLimit import RateLimiter

# Create an APIRouter for product-related routes
router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)

class ProductCreateSchema(BaseModel):
    name:str
    cat_id:int
    description:str
    sku:str
    price:int
    discount_price:int
    brand:str
    is_active:bool 

@router.post('/create')
async def create_product(payload:ProductCreateSchema,user: dict = Depends(user_detail_verify)):
    try: 
        data=payload.dict()

        user_permissions=permission_list(user_id=user['user_id'],role_id=user['role_id'])
        if 'product.create' in user_permissions:
            data['user_id']=user['user_id']
            result=product_create(data=data)
            return {"status":True,"message":"Fetched user data!","data":result}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}

    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}




@router.get('/get')
async def get_specific_product(prod_id:int):
    try:
            data=product_by_id(prod_id=prod_id)
            return {"status":True,"message":"filtered product","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}



@router.get('/filter')
async def product_filter(query:str,data:None= Depends(RateLimiter(times=5,seconds=60))):
    try:
        data=producty_by_filter(query=query)
        return {"status":True,"message":"filtered products","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}

    

        