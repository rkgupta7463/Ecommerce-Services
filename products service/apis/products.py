from typing import Annotated
from fastapi import APIRouter,Depends,Body
from authorization.auth_verify import user_detail_verify
from query.permissions import permission_list
from query.product import product_create
from pydantic import Field,BaseModel

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



    