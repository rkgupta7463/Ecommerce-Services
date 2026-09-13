from typing import Annotated
from fastapi import APIRouter,Depends,Body
from authorization.auth_verify import user_detail_verify
from query.permissions import permission_list
from query.category import *
from pydantic import Field,BaseModel

# Create an APIRouter for product-related routes
router = APIRouter(
    prefix="/api/category",
    tags=["Category"]
)

class CategoryCreateSchema(BaseModel):
    name:str
    description:str
    parent_cat_id:int=None
    is_active:bool 

@router.post('/create')
async def create_product(payload:CategoryCreateSchema,user: dict = Depends(user_detail_verify)):
    try: 
        data=payload.dict()

        user_permissions=permission_list(user_id=user['user_id'],role_id=user['role_id'])
        if 'category.create' in user_permissions:
            data['user_id']=user['user_id']
            result=category_create(data=data)
            return {"status":True,"message":"Fetched user data!","data":result}
        else:
            return {"status":False,"message":"user doesn't have permission to perform this action!","data":[]}

    except Exception as e:
        print("e:- ",e)
        return {"status":True,"message":f"exception:- {e}","data":[]}



@router.get('/get')
async def get_specific_category(cat_id:int):
    try:
        data=category_by_id(cat_id=cat_id)
        return {"status":True,"message":"filtered categories","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}



@router.get('/filter')
async def category_filter(query:str):
    try:
        data=category_by_filter(query=query)
        return {"status":True,"message":"filtered categories","data":data}
    except Exception as e:
        return {"status":False,"message":f"exception:- {e}"}

    

    